from typing import Callable, ClassVar, Generator

type PaddingOracle = Callable[[bytes], bool]


class PartialBlock:
    def __init__(self, block_length: int) -> None:
        self.block_length = block_length
        self._known_bytes = bytearray(block_length)
        self.num_bytes_known = 0

    @property
    def num_bytes_unknown(self):
        return self.block_length - self.num_bytes_known

    @property
    def known_bytes(self) -> bytes:
        return bytes(self._known_bytes)

    def is_complete(self) -> bool:
        return self.num_bytes_known == self.block_length

    def update(self, new_known_bytes: bytes) -> None:
        assert len(new_known_bytes) <= self.num_bytes_unknown
        old_first_known_byte_index = self.num_bytes_unknown
        new_first_known_byte_index = old_first_known_byte_index - len(new_known_bytes)
        self._known_bytes[new_first_known_byte_index:old_first_known_byte_index] = new_known_bytes
        self.num_bytes_known += len(new_known_bytes)


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
        partial_decryption = PartialBlock(self.block_length)
        while not partial_decryption.is_complete():
            self.step_crack_plaintext_block(
                plaintext_block_index,
                partial_decryption,
            )
            print(partial_decryption.known_bytes)

        preceding_block = self._block_at(plaintext_block_index)
        plaintext = bytearray(partial_decryption.known_bytes)
        for byte_index in range(self.block_length):
            plaintext[byte_index] ^= preceding_block[byte_index]
        return plaintext

    def step_crack_plaintext_block(
        self,
        plaintext_block_index: int,
        partial_decryption: PartialBlock,
    ) -> None:
        assert partial_decryption.block_length == self.block_length
        assert not partial_decryption.is_complete()

        first_known_byte_index = partial_decryption.num_bytes_unknown
        last_unknown_byte_index = first_known_byte_index - 1

        preceding_block = bytearray(self._block_at(plaintext_block_index))
        other_preceding_block = bytearray(self._block_at(plaintext_block_index))
        ciphertext_block = self._ciphertext_block_at(plaintext_block_index)

        # spoof padding for known bytes
        target_padding = partial_decryption.num_bytes_known + 1
        for byte_index in range(first_known_byte_index, self.block_length):
            preceding_block[byte_index] = partial_decryption.known_bytes[byte_index] ^ target_padding
            other_preceding_block[byte_index] = partial_decryption.known_bytes[byte_index] ^ (target_padding - 1)

        # assert target_padding == 1 or self.oracle(other_preceding_block + ciphertext_block)

        # find a mutation which turns the last unknown byte into valid padding
        for try_byte_value in range(256):
            c1_prime = bytearray(preceding_block)
            c1_prime[last_unknown_byte_index] = try_byte_value
            if not self.oracle(c1_prime + ciphertext_block):
                continue
            if last_unknown_byte_index == 0:
                break

            c1_prime_prime = bytearray(c1_prime)
            c1_prime_prime[last_unknown_byte_index - 1] ^= 1
            assert c1_prime_prime != c1_prime
            if self.oracle(c1_prime_prime + ciphertext_block):
                break
        else:
            raise Exception("no value found")

        partial_decryption.update((c1_prime[last_unknown_byte_index] ^ target_padding).to_bytes(length=1))
