# produces the 128 bit encrypted message
from Crypto.Hash import SHA

from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA



class ElectronicSignature:
    # создает открытый и закрытые ключи (RSA)
    def get_keys(self):
        private_key = RSA.generate(2048)
        private_key_str = private_key.exportKey('PEM')
        public_key = private_key.publickey()
        public_key_str = public_key.exportKey('PEM')
        return public_key_str, private_key_str

    # генерирует хэш (MD5) и подписывает данные (RSA)
    def sign_data(self, bytes_array, private_key):
        key = RSA.importKey(private_key)
        hash = self._make_hash(bytes_array)

        signature_obj = PKCS1_v1_5.new(key)
        return signature_obj.sign(hash)

    # генерирует хэш (MD5) и проверяет данные (RSA)
    def check_data(self, bytes_array, public_key, signature):
        key = RSA.importKey(public_key)
        hash = self._make_hash(bytes_array)
        verifier = PKCS1_v1_5.new(key)
        return verifier.verify(hash, signature)

    def _make_hash(self, bytes_array):
        return SHA.new(bytes_array)
