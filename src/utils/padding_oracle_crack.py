import asyncio
from contextlib import AsyncExitStack
from typing import Awaitable, Callable, ClassVar, Generator

from utils import asyncio_extras
from utils.code_highlight import code_highlight
from utils.reprint import PrinterABC, Printer, NoOpPrinter

type PaddingOracle = Callable[[bytes, bytes], Awaitable[bool]]


class InsignificantResultException(Exception):
    pass


def is_significant(future: asyncio.Future) -> bool:
    if future.cancelled(): return False
    if isinstance(future.exception(), InsignificantResultException): return False
    return True


class PartiallyCrackedBlock:
    def __init__(self,
        block_length: int,
        preceding_ciphertext_block: bytes,
        ciphertext_block: bytes,
    ) -> None:
        assert len(preceding_ciphertext_block) == block_length
        assert len(ciphertext_block) == block_length

        self.block_length = block_length
        self.preceding_ciphertext = preceding_ciphertext_block
        self.ciphertext = ciphertext_block
        self._known_decryption = bytearray(block_length)
        self._known_plaintext = bytearray(block_length)
        self.num_bytes_known = 0

    @property
    def num_bytes_unknown(self):
        return self.block_length - self.num_bytes_known

    @property
    def known_decryption(self) -> bytes:
        return bytes(self._known_decryption)

    @property
    def known_plaintext(self) -> bytes:
        return bytes(self._known_plaintext)

    def is_complete(self) -> bool:
        return self.num_bytes_known == self.block_length

    def update(self, new_known_byte_decryption: int) -> None:
        assert 0 <= new_known_byte_decryption < 256

        first_known_byte_index = self.num_bytes_unknown
        last_unknown_byte_index = first_known_byte_index - 1
        self._known_decryption[last_unknown_byte_index] = new_known_byte_decryption
        mask_byte = self.preceding_ciphertext[last_unknown_byte_index]
        self._known_plaintext[last_unknown_byte_index] = new_known_byte_decryption ^ mask_byte
        self.num_bytes_known += 1

    async def step_crack(self, oracle: PaddingOracle) -> None:
        assert not self.is_complete()

        first_known_byte_index = self.num_bytes_unknown
        last_unknown_byte_index = first_known_byte_index - 1

        preceding_block = bytearray(self.preceding_ciphertext)
        ciphertext_block = self.ciphertext

        # spoof padding for known bytes
        target_padding = self.num_bytes_known + 1
        for byte_index in range(first_known_byte_index, self.block_length):
            preceding_block[byte_index] = self.known_decryption[byte_index] ^ target_padding

        # find a mutation which turns the last unknown byte into valid padding
        async def try_byte_value(value: int) -> int:
            c1_prime = bytearray(preceding_block)
            c1_prime[last_unknown_byte_index] = value
            if not await oracle(c1_prime, ciphertext_block):
                raise InsignificantResultException
            if last_unknown_byte_index == 0:
                return value

            c1_prime[last_unknown_byte_index - 1] ^= 1
            if not await oracle(c1_prime, ciphertext_block):
                raise InsignificantResultException
            return value

        successful_byte_value = await asyncio_extras.race_predicate(
            is_significant,
            (try_byte_value(value) for value in range(256))
        )

        self.update(successful_byte_value ^ target_padding)

    def _render_byte_hex(self, byte_index: int) -> str:
        if byte_index < self.num_bytes_unknown:
            return "??"
        return self._known_plaintext[byte_index].to_bytes(length=1).hex()

    def _render_byte_ascii(self, byte_index: int) -> str:
        if byte_index < self.num_bytes_unknown:
            return "?"
        byte_value = self._known_plaintext[byte_index]
        if byte_value < 32 or 128 <= byte_value:
            return u"\u21af"
        byte_char = chr(byte_value)
        if byte_char == "\n":
            return u"\u240A"
        if byte_char == "\r":
            return u"\u240D"
        if byte_char == "\t":
            return u"\u21e5"
        return byte_char

    def render_progress(self) -> str:
        hex_progress = " ".join(self._render_byte_hex(byte_index) for byte_index in range(self.block_length))
        ascii_progress = "".join(self._render_byte_ascii(byte_index) for byte_index in range(self.block_length))

        return code_highlight(f"bytes.fromhex({hex_progress!r}) ({ascii_progress!r})")


class PaddingOracleCracker:
    """
    assume 128-bit blocks.

    -- modify penultimate block s.t. decryption of final byte is a padding byte --
    for 'mod' values 0 through 256,
    set the last byte of C_0 = IV to 'mod' to construct C_0'
    try to decrypt C' = (C_0', C_1)
    If the padding is correct, the last byte of D(C_1) ^ C_0' is a padding byte (0x01...0x10)

    -- determine which padding byte is exhibited --
    tamper with the penultimate unknown byte of C' to construct C_0''
    try to decrypt C'' = (C_0'', C_1)
    If the padding is no longer correct, continue through the 'mod' for-loop
    Otherwise, the padding remains correct despite tampering.
    This means the penultimate unknown byte of D(C_1) ^ C_0' is the final non-padding byte
    In any other case, tampering would have invalidated the padding
    therefore, the final unknown byte is 0x01
    """

    block_length: ClassVar[int] = 16
    """Block length (in bytes) of the cipher being attacked"""

    def __init__(self, iv: bytes, ciphertext: bytes, oracle: PaddingOracle, *, render_progress: bool = True) -> None:
        assert len(iv) == self.block_length
        number_of_ciphertext_blocks, ciphertext_overflow_length = divmod(len(ciphertext), self.block_length)
        assert ciphertext_overflow_length == 0

        self.iv = iv
        self.ciphertext = ciphertext
        self._number_of_ciphertext_blocks = number_of_ciphertext_blocks

        self.oracle = oracle

        self.printer_factory = Printer if render_progress else NoOpPrinter

    def _block_at(self, index: int) -> bytes:
        if index == 0:
            return self.iv
        return self._ciphertext_block_at(index - 1)

    def _ciphertext_block_at(self, index: int) -> bytes:
        from_index = index * self.block_length
        to_index = from_index + self.block_length
        return self.ciphertext[from_index:to_index]

    def _ciphertext_blocks(self) -> Generator[bytes]:
        for index in range(self._number_of_ciphertext_blocks):
            yield self._ciphertext_block_at(index)

    async def crack_plaintext(self) -> bytearray:
        plaintext = bytearray()

        futures: list[asyncio.Future[bytes]] = []
        async with AsyncExitStack() as stack:
            printer = self.printer_factory(line_count=self._number_of_ciphertext_blocks)
            stack.enter_context(printer)
            task_group = asyncio.TaskGroup()
            await stack.enter_async_context(task_group)

            for index in range(self._number_of_ciphertext_blocks):
                future = task_group.create_task(self.crack_plaintext_block(index, printer))
                futures.append(future)

        for future in futures:
            block = future.result()
            plaintext.extend(block)

        padding_length = plaintext[-1]
        return plaintext[:-padding_length]

    async def crack_plaintext_block(self, plaintext_block_index: int, printer: PrinterABC) -> bytes:
        partial_decryption = PartiallyCrackedBlock(
            self.block_length,
            self._block_at(plaintext_block_index),
            self._ciphertext_block_at(plaintext_block_index),
        )
        def render_progress():
            printer(
                f"block {plaintext_block_index}: {partial_decryption.render_progress()}",
                line_index=plaintext_block_index,
            )

        render_progress()
        while not partial_decryption.is_complete():
            await partial_decryption.step_crack(self.oracle)
            render_progress()

        return partial_decryption.known_plaintext
