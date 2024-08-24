"""
This experiment (done by Laurent) aimed at revealing the behavior of extra in Pydantic:
- Extra.allow: extra fields are kept (and no error raised)
- Extra.ignore: extra fields are ignored and removed (and no error raised)
- Extra.forbid: extra fields raise an error
"""
from pydantic import BaseModel, Extra, ValidationError

from utils import AssertError


class MySchema(BaseModel):
    a: str


class MySchemaAllow(MySchema):
    class Config:
        extra = Extra.allow


class MySchemaIgnore(MySchema):
    class Config:
        extra = Extra.ignore


class MySchemaForbid(MySchema):
    class Config:
        extra = Extra.forbid


data = dict(a="first field", b="ignore me or don't")


def test_allow_serializes_unknown_attributes():
    s = MySchemaAllow(**data)
    assert s.dict() == {
        "a": "first field",
        "b": "ignore me or don't",
    }


def test_ignore_drops_unknown_attributes():
    s = MySchemaIgnore(**data)
    assert s.dict() == {
        "a": "first field",
    }


def test_forbid_crashes_on_unknown_attributes():
    try:
        s = MySchemaForbid(**data)
    except ValidationError:
        pass
    else:
        raise AssertError("expected an exception")


if __name__ == '__main__':
    test_allow_serializes_unknown_attributes()
    test_ignore_drops_unknown_attributes()
    test_forbid_crashes_on_unknown_attributes()
