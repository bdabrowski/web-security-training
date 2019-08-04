import unittest

from .crypto_message import encrypt, decrypt


class TestCryptoFunctions(unittest.TestCase):

    def test_encode(self):
        encoded = encrypt('Lorem Ipsum', '12345678')
        self.assertNotEqual(encoded, 'Loerm Ipsum')

    def test_decode(self):
        encoded = encrypt('Lorem Ipsum', '12345678')
        self.assertEqual(decrypt(encoded, '12345678'), 'Lorem Ipsum')

    def test_invalid_decode(self):
        encoded = encrypt('Lorem Ipsum', '12345678')
        self.assertRaises(ValueError, decrypt, encoded, 'wrongpassword')
