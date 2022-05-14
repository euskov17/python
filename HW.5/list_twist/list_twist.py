from collections import UserList
import typing as tp

# https://github.com/python/mypy/issues/5264#issuecomment-399407428
from setuptools.command.alias import alias

if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    data: list = []
    reversed: list = []
    first = 0
    last = 0
    size = 0

    def __init__(self, lst=None):
        if lst is None:
            self.data = []
            self.reversed = []
            self.size = 0
        else:
            self.data = lst
            self.reversed = list(reversed(lst))
            self.first = self.data[0]
            self.last = self.data[len(self.data) - 1]
            self.size = len(self.data)
    #
    #
    # def reversed(self):
    #     self.data = list(reversed(self.data))
    #
    # def last(self):
    #     self.data = self.data[len(self.data) - 1]
    #
    # @staticmethod
    # def first(self):
    #     yield self.data[0]
    #
    # def size(self) -> int:
    #     return len(self.data)

    F = first
    L = last
    S = size
    R = reversed



extended_list = ListTwist()

assert extended_list.data == []

print( extended_list.reversed) #== []
print(extended_list.R ) #== []

print(len(extended_list)) # == 0
print( extended_list.size) # == 0
print(extended_list.S)