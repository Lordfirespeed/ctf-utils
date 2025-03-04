from typing import Callable, ClassVar, Generator

type PaddingOracle = Callable[[bytes], bool]


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

    def step_crack(self, oracle: PaddingOracle) -> None:
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
        for try_byte_value in range(256):
            c1_prime = bytearray(preceding_block)
            c1_prime[last_unknown_byte_index] = try_byte_value
            if not oracle(c1_prime + ciphertext_block):
                continue
            if last_unknown_byte_index == 0:
                break

            c1_prime_prime = bytearray(c1_prime)
            c1_prime_prime[last_unknown_byte_index - 1] ^= 1
            assert c1_prime_prime != c1_prime
            if oracle(c1_prime_prime + ciphertext_block):
                break
        else:
            raise Exception("no value found")

        self.update(c1_prime[last_unknown_byte_index] ^ target_padding)

    def _render_byte_hex(self, byte_index: int) -> str:
        if byte_index < self.num_bytes_unknown:
            return "__"
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
        return f"{hex_progress} ({ascii_progress})"


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

    def __init__(self, iv: bytes, ciphertext: bytes, oracle: PaddingOracle) -> None:
        assert len(iv) == self.block_length
        number_of_ciphertext_blocks, ciphertext_overflow_length = divmod(len(ciphertext), self.block_length)
        assert ciphertext_overflow_length == 0

        self.iv = iv
        self.ciphertext = ciphertext
        self._number_of_ciphertext_blocks = number_of_ciphertext_blocks

        self.oracle = oracle

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

    def crack_plaintext(self) -> bytearray:
        plaintext = bytearray()
        for index in range(self._number_of_ciphertext_blocks):
            block = self.crack_plaintext_block(index)
            plaintext.extend(block)
        return plaintext

    def crack_plaintext_block(self, plaintext_block_index: int) -> bytes:
        partial_decryption = PartiallyCrackedBlock(
            self.block_length,
            self._block_at(plaintext_block_index),
            self._ciphertext_block_at(plaintext_block_index),
        )
        while not partial_decryption.is_complete():
            partial_decryption.step_crack(self.oracle)
            print(partial_decryption.render_progress())

        return partial_decryption.known_plaintext
