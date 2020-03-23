from marshmallow_annotations.ext.attrs import AttrsSchema


def attr_with_schema(**kwargs):
    def decorator(cls):
        class Schema(AttrsSchema):
            class Meta:
                locals().update(kwargs)
                target = cls
        cls.schema = Schema
        Schema.__name__ = cls.__name__ + "Schema"
        def attr_iter(self):
            return iter(self.__dict__.items())
        cls.__iter__ = attr_iter
        return cls
    return decorator
