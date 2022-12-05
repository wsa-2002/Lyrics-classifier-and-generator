import typing
import enum

T = typing.TypeVar("T")


class RoleType(enum.Enum):
    role1 = 'ROLE1'
    role2 = 'ROLE2'

    def __gt__(self: T, other: T):
        items = tuple(self.__class__)
        return items.index(self).__gt__(items.index(other))

    def __lt__(self: T, other: T):
        return self != other and not self.__gt__(other)

    def __ge__(self: T, other: T):
        return self == other or self.__gt__(other)

    def __le__(self: T, other: T):
        return self == other or not self.__gt__(other)
