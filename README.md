This library helps to create marshmallow schemas easier.


## Run flask locally

```
export FLASK_APP=demo_app.flask_app
flask run
```

## Testing

Run the following:
```
python -m pytest tests
```

## Usage

### Enums

Derive from RegisteredEnum class to have serializable enum. Set `__load_by_value__` and `__dump_by_value__` to correspondingly load and dump enumerations by their keys or values. Set `__by_value__` for both of them. Default values are `True`.

```
Class Letter(RegisteredEnum):
    __load_by_value__ = False

    a = 'First letter'
    b = 'Second letter'
    ...
```

If request and response schemas have Enum in their fields, you can request a letter and see the value of it, e.g. requesting `a` you will get `First letter`.

Register EnumField to api with
```
api.register_field(EnumField, 'string', None)
```

### Derive

To derive from an `attrs` class use `derive` decorator. Here is an example:
```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Base:
    obj: dict
    integer: int = 0


@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
@derive(AllowNoneDict, exclude={"obj"})
class Derived:
    string: str
```

Note, that `@derive` should be called first. `derive` get an additional `exclude` argument, which excludes already existing attributes from base class(it doesn't exclude from current class).
The `Derived` class above is equivalent to the following:
```
@attr_with_schema(register_as_scheme=True, strict=True)
@attr.s(auto_attribs=True)
class Derived:
    string: str
    integer: int = 0
```

### Sqlalchemy models
To add a marshmallow schema to sqlalchemy model use `model_with_schema` decorator:

```
@model_with_schema
class Table(db.Model):
    __tablename__ = 'table'
    column = Column(String, primary_key=True)
    letter = Column(Letter)
    dictionary = Column(JSON)
    array: List[str] = Column(JSON)
```

The created marshmallow schema is stored on `Table.schema`. Here, `array` will be loaded as `list` and `dictionary` will be loaded as `dict`.
