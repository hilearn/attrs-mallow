from enum import Enum, EnumMeta

from marshmallow import validate, ValidationError
from marshmallow.fields import Field
from marshmallow_annotations import registry


class EnumField(Field):
    default_error_messages = {
        'invalid_value': 'Invalid enum value for {cls}: {inpt}'
    }

    def __init__(self, cls, *args, **kwargs):
        self._enum_cls = cls
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj):
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self._enum_cls._value2member_map_[value]
        except KeyError:
            pass
        except TypeError:
            for k, v in self._enum_cls._value2member_map_.items():
                if v == value:
                    return type(self)[k]
        self.fail('invalid_value', inpt=value)

    def fail(self, key, **kwargs):
        if key in self.default_error_messages:
            msg = self.default_error_messages[key].format(
                inpt=kwargs['inpt'],
                cls=self._enum_cls.__name__)
            raise ValidationError(msg)
        super().fail(key, **kwargs)


class RegisteredEnumMeta(EnumMeta):
    def __new__(cls, name, bases, cls_dict):
        if (not any(base_type in base_cls.mro()
                    for base_cls in bases
                    for base_type in [int, float, str, tuple])
                and name != 'RegisteredEnum'):
            bases = (str, *bases)
        return super().__new__(cls, name, bases, cls_dict)


class RegisteredEnum(Enum, metaclass=RegisteredEnumMeta):
    def __init_subclass__(cls):
        def _enum_field_converter(converter, subtypes, opts):
            keys = cls._value2member_map_.keys()
            return EnumField(cls,
                             validate=validate.OneOf(keys))

        registry.register(cls, _enum_field_converter)
