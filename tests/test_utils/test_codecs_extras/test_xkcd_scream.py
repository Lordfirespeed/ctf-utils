import unittest

from extras.codecs_extras.xkcd_scream import screamify, unscreamify


class XKCDScreamTests(unittest.TestCase):
    def test_letter_d(self) -> None:
        """
        Some 'scream' implementations consider the encryption of `D` to be `A\u0331`, others
        consider it to be `A\u0332`.
        `unscreamify` should successfully decrypt either.
        """
        first_d = unscreamify("A\u0331a\u0331")
        second_d = unscreamify("A\u0332a\u0332")
        self.assertEqual(first_d, second_d)

    def test_flag_style_vector(self) -> None:
        ciphertext = u"a̮ăaa̋{â_A̮âA̧a̤A̦a̽A̦ȃȁA̮ȃȁA̮a̦A̰AÄå_19ăȁa̦Äa̯_âȺáA̯äāâÂa̽A̽Ȃ-ⱥã}"
        plaintext = unscreamify(ciphertext)
        self.assertEqual(plaintext, "flag{n_FnCqYxYrwFrwFyHAUo_19lwyUp_nZePutnNxXR-zs}")
        round_trip_ciphertext = screamify(plaintext)
        self.assertEqual(round_trip_ciphertext, ciphertext)
        round_trip_plaintext = unscreamify(round_trip_ciphertext)
        self.assertEqual(round_trip_plaintext, plaintext)


if __name__ == "__main__":
    unittest.main()
