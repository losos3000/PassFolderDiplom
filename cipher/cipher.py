from gostcrypto import gostcipher, gosthash
from pydantic import BaseModel

from server.configuration.config import settings

key = bytearray([
    0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10, 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
])


class Cipher:

    def __init__(self, seed: list[str]) -> None:
        # self.id = gosthash.new(
        #     'streebog256',
        #     data=('.'.join(seed)).encode()).hexdigest()

        self.__cipher_obj = gostcipher.new(
            'kuznechik',
            # gosthash.new(
            #     'streebog256',
            #     data='.'.join(seed).encode()).digest()
            seed
            ,gostcipher.MODE_ECB,
            pad_mode=gostcipher.PAD_MODE_1)

    def encrypt(self, value: str) -> str:
        return self.__cipher_obj.encrypt(value.encode('utf-16')).hex()

    def decrypt(self, value: str) -> str:
        return self.__cipher_obj.decrypt(bytearray.fromhex(value)).decode('utf-16').rstrip('\x00')


cipher_manager = Cipher(key)

