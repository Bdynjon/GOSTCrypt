import numpy as np
import operations as op
import itertools


class GOSTCrypt:
    __slots__ = {
        '__key',
        '__key_table',
    }

    def __init__(self, key=None, key_table=None):
        self.key = key
        self.key_table = key_table

    def simple_replace_encr(self, text):
        text = op.text_to_bits(text)
        if len(text) % 64 != 0: raise ValueError('Размер текста должен быть кратен 64 бит')
        text = [int(text[part_num * 64: part_num * 64 + 64], 2) for part_num in range(len(text)//64)]

        result = ''
        for block in text:
            result += (bin(self.__encrypt_block(block))[2:]).zfill(64)

        return op.btext_from_bits(result)

    def simple_replace_decr(self, text):
        text = op.btext_to_bits(text)
        if len(text) % 64 != 0: raise ValueError('Размер шифр-текста должен быть кратен 64 бит')
        text = [int(text[part_num * 64: part_num * 64 + 64], 2) for part_num in range(len(text) // 64)]

        result = ''
        for block in text:
            result += (bin(self.__decrypt_block(block))[2:]).zfill(64)

        return op.text_from_bits(result)

    def __encrypt_block(self, block):
        left, right = block >> 32, block & 0xFFFFFFFF

        for i in range(24):
            left, right = self.__main_operation(left, right, self.key[i % 8])

        for i in range(7, -1, -1):
            left, right = self.__main_operation(left, right, self.key[i])

        return (right << 32) | left

    def __decrypt_block(self, block):
        left, right = block >> 32, block & 0xFFFFFFFF

        for i in range(8):
            left, right = self.__main_operation(left, right, self.key[i])

        for i in range(23, -1, -1):
            left, right = self.__main_operation(left, right, self.key[i % 8])

        return (right << 32) | left

    def __main_operation(self, left, right, key):
        temp = right ^ key
        res = 0

        for i in range(8):
            res |= self.key_table[i][(temp >> i*4) & 0b1111] << i*4
        res = ((res >> (32-11)) | (res << 32)) & 0xFFFFFFFF
        left ^= res

        return right, left

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if type(key) == str:
            key = op.text_to_bits(key)
            if len(key) != 256: raise ValueError('Ключ должен быть строкой в 32 бита')
            self.__key = [int(key[part_num*32: part_num*32 + 32], 2) for part_num in range(8)]
        else:
            self.__key = None

    @property
    def key_table(self):
        return self.__key_table

    @key_table.setter
    def key_table(self, key_table):
        if key_table:
            key_table = np.array(key_table, dtype=np.uint8)
            if key_table.shape != (8, 16) or\
                    len(key_table[key_table > 15]) != 0 or\
                    not op.has_unique_rows(key_table):
                raise ValueError("Таблица замен должна быть массивом чисел от 0 до 15 размера 8 на 16")
            self.__key_table = key_table
        else:
            self.__key_table = None


def main():
    gost = GOSTCrypt()
    key = 'qwer17lkybz5f9up3m4h08nkudjhhtgf'
    key_table = [np.random.permutation(row) for row in itertools.repeat(range(16), 8)]
    gost.key = key
    gost.key_table = key_table

    text = '1234567891230458'

    cipher_text = gost.simple_replace_encr(text)
    print(cipher_text)
    print(gost.simple_replace_decr(cipher_text))


if __name__ == "__main__":
    main()
