import enum
from typing import TypeAlias, Any

NodeState: TypeAlias = Any
NodeLocation: TypeAlias = tuple[str, int]
Position: TypeAlias = tuple[int | float, int | float]


class RenpyTestException(RuntimeError):
    pass


class RenpyTestAssertionError(AssertionError):
    pass


class RenpyTestTimeoutError(TimeoutError):
    pass


class HookType(enum.Enum):
    AFTER = "after"
    AFTER_EACH_CASE = "after_each_case"
    AFTER_EACH_SUITE = "after_each_suite"
    BEFORE = "before"
    BEFORE_EACH_CASE = "before_each_case"
    BEFORE_EACH_SUITE = "before_each_suite"
