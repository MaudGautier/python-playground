"""
This experiment aimed at understanding how the `frozen` parameter of Pydantic Config works:
- Frozen aims at making fields IMMUTABLE
- Frozen also makes objects HASHABLE when possible (cf PR below)

Note: the `frozen` parameter was introduced in this PR: https://github.com/pydantic/pydantic/pull/1881
Based on this feature request: https://github.com/pydantic/pydantic/issues/1303
In particular, the hash function is generated with:
```
def generate_hash_function(frozen: bool) -> Optional[Callable[[Any], int]]:
    def hash_function(self_: Any) -> int:
        return hash(self_.__class__) + hash(tuple(self_.__dict__.values()))

    return hash_function if frozen else None
```
This explains why it does create the hash when some fields are non-hashable.
"""

from typing import List

from pydantic import BaseModel

from utils import AssertError


# ---------------------------------------------------------------- #
# Frozen: redefines the __hash__ function ==> hashable + immutable #
# ---------------------------------------------------------------- #
class FrozenModel(BaseModel):
    x: int
    y: str

    class Config:
        frozen = True


frozen_1 = FrozenModel(x=1, y='b')
frozen_2 = FrozenModel(x=1, y='b')
frozen_list = [frozen_1, frozen_2]


def test_frozen_hashes_object():
    """ With frozen=True, it is hashable (and thus, can be put in a set without any error)
    """
    set(frozen_list)


def test_frozen_crashes_when_mutating_instance():
    """ But with frozen=True, it is immutable (and thus, CANNOT be modified)
    """
    try:
        frozen_1.y = 'a'  # TypeError: "FrozenModel" is immutable and does not support item assignment
        frozen_1.x = 2  # TypeError: "FrozenModel" is immutable and does not support item assignment
    except TypeError:
        pass
    else:
        raise AssertError("expected an exception")


# ------------------------------------------- #
# Not Frozen ==> NOT hashable + NOT immutable #
# ------------------------------------------- #
class NotFrozenModel(BaseModel):
    x: int
    y: str

    class Config:
        frozen = False


not_frozen_1 = NotFrozenModel(x=1, y='b')
not_frozen_2 = NotFrozenModel(x=1, y='b')
not_frozen_list = [not_frozen_1, not_frozen_2]


def test_not_frozen_crashes_on_hashing():
    """ With frozen=False, it is NOT hashable (and thus, CANNOT be put in a set)
    """
    try:
        set(not_frozen_list)  # TypeError: unhashable type: 'NotFrozenModel'
    except TypeError:
        pass
    else:
        raise AssertError("expected an exception")


def test_not_frozen_allows_mutating_instance():
    """ But with frozen=False, it is mutable (and thus, can be modified)
    """
    not_frozen_1.y = 'a'
    not_frozen_1.x = 2


# ------------------------------------------------------------ #
# Frozen with NON-hashable fields ==> NOT hashable + immutable #
# ------------------------------------------------------------ #
class FrozenWithNonHashableFieldsModel(BaseModel):
    x: int
    y: List[int]

    class Config:
        frozen = True


frozen_with_non_hashable_fields_1 = FrozenWithNonHashableFieldsModel(x=1, y=[1, 2, 3])
frozen_with_non_hashable_fields_2 = FrozenWithNonHashableFieldsModel(x=1, y=[1, 2, 3])
frozen_with_non_hashable_fields_list = [frozen_with_non_hashable_fields_1, frozen_with_non_hashable_fields_2]

def test_frozen_with_non_hashable_fields_crashes_on_hashing():
    """ With frozen=True on NON-hashable fields, it is NOT hashable (and thus, CANNOT be put in a set)
    """
    try:
        set(frozen_with_non_hashable_fields_list)  # TypeError: unhashable type: 'list'
    except TypeError:
        pass
    else:
        raise AssertError("expected an exception")


def test_frozen_with_non_hashable_fields_crashes_when_mutating_instance():
    """ With frozen=True (no matter if fields are hashable or not), it is immutable (and thus, CANNOT be modified)
    """
    try:
        frozen_with_non_hashable_fields_1.y = [1, 2, 3, 4]  # TypeError: "FrozenWithUnhashableFieldsModel" is immutable and does not support item assignment
        frozen_with_non_hashable_fields_1.x = 2  # TypeError: "FrozenWithUnhashableFieldsModel" is immutable and does not support item assignment
    except TypeError:
        pass
    else:
        raise AssertError("expected an exception")


if __name__ == '__main__':
    test_frozen_hashes_object()
    test_frozen_crashes_when_mutating_instance()
    test_not_frozen_crashes_on_hashing()
    test_not_frozen_allows_mutating_instance()
    test_frozen_with_non_hashable_fields_crashes_on_hashing()
    test_frozen_with_non_hashable_fields_crashes_when_mutating_instance()
