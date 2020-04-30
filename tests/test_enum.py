from unittest import TestCase
import json
import attr

from marshenum import RegisteredEnum, attr_with_schema


def enum_to_schema(enum_cls):
    @attr_with_schema(register_as_scheme=True, strict=True)
    @attr.s(auto_attribs=True)
    class MyEnum:
        enum: enum_cls

    return MyEnum.schema


def enum_to_field(enum_cls):
    return enum_to_schema(enum_cls)._declared_fields['enum']


class MyIntEnum(int, RegisteredEnum):
    a = 1
    b = 2
    c = 3


class MyStrEnum(RegisteredEnum):
    a = "A"
    b = "B"
    c = "C"


class MyTupleEnum(tuple, RegisteredEnum):
    a = (1, "a")
    b = (2, "b")
    c = (3, "c")


class MyByKeyIntEnum(int, RegisteredEnum):
    __by_value__ = False
    a = 1
    b = 2
    c = 3


class MyLoadByKeyIntEnum(int, RegisteredEnum):
    __load_by_value__ = False
    a = 1
    b = 2
    c = 3


class MyDumpByKeyIntEnum(int, RegisteredEnum):
    __dump_by_value__ = False
    a = 1
    b = 2
    c = 3


class EnumTest(TestCase):
    def test_enum_metadata(self):
        self.assertListEqual(
            enum_to_field(MyIntEnum).metadata.get('enum', []),
            [1, 2, 3])
        self.assertListEqual(
            enum_to_field(MyStrEnum).metadata.get('enum', []),
            ["A", "B", "C"])
        self.assertListEqual(
            enum_to_field(MyTupleEnum).metadata.get('enum', []),
            [(1, "a"), (2, "b"), (3, "c")])
        self.assertListEqual(
            enum_to_field(MyByKeyIntEnum).metadata.get('enum', []),
            ["a", "b", "c"])
        self.assertListEqual(
            enum_to_field(MyLoadByKeyIntEnum).metadata.get('enum', []),
            ["a", "b", "c"])
        self.assertListEqual(
            enum_to_field(MyDumpByKeyIntEnum).metadata.get('enum', []),
            [1, 2, 3])


class SchemaTest(TestCase):
    def test_loads(self):
        self.assertEqual(
            enum_to_schema(MyIntEnum)().loads('{"enum": 1}').enum,
            MyIntEnum.a)
        self.assertEqual(
            enum_to_schema(MyStrEnum)().loads('{"enum": "A"}').enum,
            MyStrEnum.a)
        self.assertEqual(
            enum_to_schema(MyTupleEnum)().loads('{"enum": [1, "a"]}').enum,
            MyTupleEnum.a)
        self.assertEqual(
            enum_to_schema(MyByKeyIntEnum)().loads('{"enum": "a"}').enum,
            MyByKeyIntEnum.a)
        self.assertEqual(
            enum_to_schema(MyLoadByKeyIntEnum)().loads('{"enum": "a"}').enum,
            MyLoadByKeyIntEnum.a)
        self.assertEqual(
            enum_to_schema(MyDumpByKeyIntEnum)().loads('{"enum": 1}').enum,
            MyDumpByKeyIntEnum.a)

    def test_dumps(self):
        self.assertEqual(
            enum_to_schema(MyIntEnum)().dumps({"enum": MyIntEnum.a}),
            json.dumps({"enum": 1}))
        self.assertEqual(
            enum_to_schema(MyStrEnum)().dumps({"enum": MyStrEnum.a}),
            json.dumps({"enum": "A"}))
        self.assertEqual(
            enum_to_schema(MyTupleEnum)().dumps({"enum": MyTupleEnum.a}),
            json.dumps({"enum": (1, "a")}))
        self.assertEqual(
            enum_to_schema(MyByKeyIntEnum)().dumps({"enum": MyByKeyIntEnum.a}),
            json.dumps({"enum": "a"}))
        self.assertEqual(
            enum_to_schema(MyLoadByKeyIntEnum)().dumps(
                {"enum": MyLoadByKeyIntEnum.a}),
            json.dumps({"enum": 1}))
        self.assertEqual(
            enum_to_schema(MyDumpByKeyIntEnum)().dumps(
                {"enum": MyDumpByKeyIntEnum.a}),
            json.dumps({"enum": "a"}))


