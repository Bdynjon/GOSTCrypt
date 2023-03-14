import numpy


class GOSTCrypt:
    __slots__ = {
        '__key',
        '__key_table',
    }

    def __init__(self, key, key_table):
        self.key = key
        self.key_table = key_table

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key: str):

        self.__key = key

    @property
    def key_table(self):
        return self.__key_table

    @key_table.setter
    def key_table(self, key_table):
        self.__key_table = key_table
