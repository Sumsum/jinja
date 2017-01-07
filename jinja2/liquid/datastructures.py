from collections import UserList


class List(UserList):
    """
    list with some exta (ruby) properties
    """
    def __init__(self, data=None):
        self.data = list(data or [])

    def __str__(self):
        return ''.join([str(v) for v in self.data])

    @property
    def size(self):
        return self.__len__()

    @property
    def first(self):
        try:
            return self.data[0]
        except IndexError:
            return None

    @property
    def last(self):
        try:
            return self.data[-1]
        except IndexError:
            return None
