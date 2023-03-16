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
        if len(text) % 64 != 0: raise ValueError(f'Размер текста должен быть кратен 64 бит ({len(text)})')
        text = [np.uint64(int(text[part_num * 64: part_num * 64 + 64], 2)) for part_num in range(len(text)//64)]

        result = ''
        for block in text:
            result += (bin(self.__encrypt_block(block))[2:]).zfill(64)
        return op.btext_from_bits(result)

    def simple_replace_decr(self, text):
        text = op.btext_to_bits(text)
        if len(text) % 64 != 0: raise ValueError(f'Размер шифр-текста должен быть кратен 64 бит ({len(text)})')
        text = [np.uint64(int(text[part_num * 64: part_num * 64 + 64], 2)) for part_num in range(len(text)//64)]

        result = ''
        for block in text:
            result += (bin(self.__decrypt_block(block))[2:]).zfill(64)

        return op.text_from_bits(result)

    def __encrypt_block(self, block):
        left, right = np.uint32(np.right_shift(block, np.uint8(32))), np.uint32(np.bitwise_and(block, np.uint32(0xFFFFFFFF)))

        for i in range(24):
            left, right = self.__main_operation(left, right, self.key[i % 8])

        for i in range(7, -1, -1):
            left, right = self.__main_operation(left, right, self.key[i])

        return np.left_shift(right, np.uint64(32)) | left

    def __decrypt_block(self, block):
        left, right = np.uint32(np.right_shift(block, np.uint8(32))), np.uint32(np.bitwise_and(block, np.uint32(0xFFFFFFFF)))

        for i in range(8):
            left, right = self.__main_operation(left, right, self.key[i])

        for i in range(23, -1, -1):
            left, right = self.__main_operation(left, right, self.key[i % 8])

        return np.left_shift(right, np.uint64(32)) | left

    def __main_operation(self, left, right, key):
        temp = np.bitwise_xor(right, key)
        res = np.uint32(0)

        for i in range(8):
            l = self.key_table[i][(temp >> i*4) & 0b1111]
            res |= np.left_shift(l, np.uint32(i*4))
        res = np.uint32(((res >> (32-11)) | np.uint32(res << np.uint32(11))) & np.uint32(0xFFFFFFFF))
        left ^= res

        return right, left

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if type(key) == str:
            key = op.text_to_bits(key)
            if len(key) != 256: raise ValueError('Ключ должен быть строкой в 256 бит')
            self.__key = [np.uint32(int(key[part_num*32: part_num*32 + 32], 2)) for part_num in range(8)]
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
                    len(key_table[key_table > 15]) != 0:
                    #not op.has_unique_rows(key_table):
                raise ValueError("Таблица замен должна быть массивом чисел от 0 до 15 размера 8 на 16")
            self.__key_table = key_table
        else:
            self.__key_table = None


def main():
    # Создание экземпляра класса GOSTCrypt
    gost = GOSTCrypt()

    # Определение ключевой информации
    key = 'qwer17lkybz5f9up3m4h08nkudjhhtgf'
    key_table = [np.random.permutation(row) for row in itertools.repeat(range(16), 8)]

    # Установка ключевой информации
    gost.key = key
    gost.key_table = key_table

    # text = 'Test message cry'
    # Задание текста для шифрования
    text = 'Тестовое сообщение!кр'
    print('Исходный текст : ', text)

    # Шифрование текста и вывод в консоль
    encrypted_text = gost.simple_replace_encr(text)
    print('Зашифрованный текст : ', encrypted_text)

    path = "D://cipher_text.txt"
    op.save_text(encrypted_text, path)
    encrypted_text = op.load_text(path)

    # Расшифрование текста и вывод в консоль
    decrypted_text = gost.simple_replace_decr(encrypted_text)
    print('Расшифрованный текст : ', decrypted_text)


if __name__ == "__main__":
    main()
