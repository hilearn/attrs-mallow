import attr

import marshmallow as ma

from marshmallow_helpers import attr_with_schema
from marshmallow_helpers import RegisteredEnum as Enum
from marshmallow_helpers import derive


class IntExampleEnum(int, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3


class StrExampleEnum(str, Enum):
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'


class KeyEnum(str, Enum):
    __load_by_value__ = False

    a = "first letter"
    b = "second letter"


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class EnumQuery:
    int_enum: IntExampleEnum
    str_enum: StrExampleEnum

    class SchemaMeta:
        class Fields:
            int_enum = {"allow_none": True}


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class EnumResponse:
    int_enum: IntExampleEnum
    str_enum: StrExampleEnum


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class AllowNoneDict:
    obj: dict
    integer: int = 0
    prime: bool = False

    class SchemaMeta:
        class Fields:
            obj = {"allow_none": True}
            integer = {"allow_none": True,
                       "validate": ma.validate.Range(min=0, max=100)}

    class Schema:
        @ma.validates_schema
        def prime_integer(self, data, **kwargs):
            if data["prime"] and (data['integer'] is None
                                  or not self.is_prime(data['integer'])):
                raise ma.ValidationError("integer was supposed to be prime")

        @staticmethod
        def is_prime(num):
            for i in range(2, num - 1):
                if num % i == 0:
                    return False
            return True


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
@derive(AllowNoneDict, exclude=["obj"])
class Derived:
    string: str = "asdf"


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class ByKey:
    key: KeyEnum
