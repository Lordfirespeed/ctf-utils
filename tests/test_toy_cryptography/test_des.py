import unittest

from toy_cryptography.feistel_cipher.scheme import FeistelText, encryption_round
from toy_cryptography.des.key_schedule import des_key_schedule
from toy_cryptography.des.feistel_function import des_feistel_function


class DESKeyScheduleTests(unittest.TestCase):
    """
    https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
    """

    sample_round_keys = (
        0b000110_110000_001011_101111_111111_000111_000001_110010,
        0b011110_011010_111011_011001_110110_111100_100111_100101,
        0b010101_011111_110010_001010_010000_101100_111110_011001,
        0b011100_101010_110111_010110_110110_110011_010100_011101,
        0b011111_001110_110000_000111_111010_110101_001110_101000,
        0b011000_111010_010100_111110_010100_000111_101100_101111,
        0b111011_001000_010010_110111_111101_100001_100010_111100,
        0b111101_111000_101000_111010_110000_010011_101111_111011,
        0b111000_001101_101111_101011_111011_011110_011110_000001,
        0b101100_011111_001101_000111_101110_100100_011001_001111,
        0b001000_010101_111111_010011_110111_101101_001110_000110,
        0b011101_010111_000111_110101_100101_000110_011111_101001,
        0b100101_111100_010111_010001_111110_101011_101001_000001,
        0b010111_110100_001110_110111_111100_101110_011100_111010,
        0b101111_111001_000110_001101_001111_010011_111100_001010,
        0b110010_110011_110110_001011_000011_100001_011111_110101,
    )

    def test_round_keys(self):
        main_key = 0b00010011_00110100_01010111_01111001_10011011_10111100_11011111_11110001
        key_schedule = des_key_schedule(main_key)
        for expected_round_key, round_key in zip(self.sample_round_keys, key_schedule):
            self.assertEqual(expected_round_key, round_key)

class DESFeistelFunctionTests(unittest.TestCase):
    """
    NIST Special Publication 500-20
    https://csrc.nist.gov/pubs/sp/500/20/upd1/final
    """

    sample_input = (
        FeistelText(left=0x00000000, right=0x00000000, half_length=32)
    )

    sample_round_outputs = (
        FeistelText(left=0x00000000, right=0x47092B5B, half_length=32),
        FeistelText(left=0x47092B5B, right=0x53F372AF, half_length=32),
        FeistelText(left=0x53F372AF, right=0x9F1D158B, half_length=32),
        FeistelText(left=0x9F1D158B, right=0x8109CBEE, half_length=32),
        FeistelText(left=0x8109CBEE, right=0x60448698, half_length=32),
        FeistelText(left=0x60448698, right=0x29EBB1A4, half_length=32),
        FeistelText(left=0x29EBB1A4, right=0x620CC3A3, half_length=32),
        FeistelText(left=0x620CC3A3, right=0xDEEB3D8A, half_length=32),
        FeistelText(left=0xDEEB3D8A, right=0xA1A0354D, half_length=32),
        FeistelText(left=0xA1A0354D, right=0x9F0303DC, half_length=32),
        FeistelText(left=0x9F0303DC, right=0xFD898EE8, half_length=32),
        FeistelText(left=0xFD898EE8, right=0x2D1AE1DD, half_length=32),
        FeistelText(left=0x2D1AE1DD, right=0xCBC829FA, half_length=32),
        FeistelText(left=0xCBC829FA, right=0xB367DEC9, half_length=32),
        FeistelText(left=0xB367DEC9, right=0x3F6C3EFD, half_length=32),
        FeistelText(left=0x3F6C3EFD, right=0x5A1E5228, half_length=32),
    )

    def test_round_outputs(self):
        key = 0x10316E028C8F3B4A
        key_schedule = des_key_schedule(key)
        text = self.sample_input
        for round_index in range(16):
            round_key = next(key_schedule)
            text = encryption_round(text, round_key, des_feistel_function)
            expected_text = self.sample_round_outputs[round_index]
            self.assertEqual(expected_text, text, msg=f"failure after round {round_index+1}")
