import numpy as np
import operations as op
import itertools
import functools


class GOSTCrypt:
    __slots__ = {
        '__key',
        '__key_table',
    }

    def __init__(self, key=None, key_table=None):
        self.key = key
        self.key_table = key_table

    def encrypt(self, text: str):
        pass

    def __main_operation(self):
        pass

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if type(key) == str:
            key = op.text_to_bits(key)
            if len(key) != 32: raise ValueError('Ключ должен быть строкой в 32 бита')
            self.__key = key
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
    key = 'qwer'
    key_table = [np.random.permutation(row) for row in itertools.repeat(range(16), 8)]
    print(key_table)
    gost.key = key
    gost.key_table = key_table
    print(gost.key_table)



if __name__ == "__main__":
    main()
