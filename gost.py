import numpy as np
import operations as op


class GOSTCrypt:
    __slots__ = {
        '__key',
        '__key_table',
    }

    def __init__(self, key=None, key_table=None):
        self.key = key
        self.key_table = key_table

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):
        if type(key) == str:
            key = op.text_to_bits(key)
            if len(key) != 64: raise ValueError('Ключ должен быть строкой в 64 бита')
            self.__key = key
        else:
            self.__key = None

    @property
    def key_table(self):
        return self.__key_table

    @key_table.setter
    def key_table(self, key_table):
        self.__key_table = key_table


def main():
    gost = GOSTCrypt()
    key = 'qwertyui'
    gost.key = key


if __name__ == "__main__":
    main()
