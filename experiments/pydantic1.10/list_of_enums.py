"""
This experiment aimed at understanding whether pydantic allows None values in an `enum.StrEnum`.
Answer: no.
"""

import enum

import pydantic
from pydantic import BaseModel

from utils import AssertError


class Choice(enum.StrEnum):
    CHOICE_1 = "CHOICE_1"
    CHOICE_2 = "CHOICE_2"
    CHOICE_3 = "CHOICE_3"


class MultipleChoices(BaseModel):
    choices: list[Choice]


def test_list_without_none_works():
    t = MultipleChoices(choices=["CHOICE_1", "CHOICE_2"])  # ok


def test_list_with_none_crashes():
    try:
        t = MultipleChoices(choices=["CHOICE_1", None])  # validation error: none is not an allowed value (type=type_error.none.not_allowed)
    except pydantic.ValidationError:
        pass
    else:
        raise AssertError("expected an exception")


if __name__ == '__main__':
    test_list_without_none_works()
    test_list_with_none_crashes()
