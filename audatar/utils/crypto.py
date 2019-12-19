from cryptography.fernet import Fernet


class Crypto:
    def __init__(self, key=None):
        if key is None:
            self._fernet_key = self._generate_fernet_key()
        else:
            self._fernet_key = key

    def _generate_fernet_key(self):
        """generate fernet key (this is your "secret")

        :return: secret key (save this in vault)
        """
        key = Fernet.generate_key()
        return key.decode()

    def _get_cipher_suite(self):
        """get cipher suite.

        :return: cipher_suite.
        """
        cipher_suite = Fernet(self._fernet_key)
        return cipher_suite

    def get_fernet_key(self):
        return self._fernet_key

    def encode_text(self, text):
        """encode the text.

        :param text: connection string to be encoded.
        :return: encoded text
        """
        encoded_text = self._get_cipher_suite().encrypt(text.encode())
        return encoded_text.decode()

    def decode_text(self, encoded_text):
        """decode the text.

        :param encoded_text: text encoded using same secret.
        :return: decoded text
        """
        decoded_text = self._get_cipher_suite().decrypt(encoded_text.encode())
        return decoded_text.decode()


def generate_encrypted_connection_string(c, text):
    print('Given Text: ', text)
    e_text = c.encode_text(text)
    print('Encoded Text: ', e_text)


def generate_decrypted_connection_string(c, e_text):
    print('Given Text: ', e_text)
    d_text = c.decode_text(e_text)
    print('Decoded Text: ', d_text)


if __name__ == '__main__':
    secret_key = ''
    c = Crypto(secret_key)
