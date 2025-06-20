from typing import TypeAlias, Any

State: TypeAlias = Any
NodeLocation: TypeAlias = tuple[str, int]
Position: TypeAlias = tuple[int | float, int | float]

class RenpyTestException(RuntimeError):pass
class RenpyTestAssertionError(AssertionError):pass
class RenpyTestTimeoutError(TimeoutError):pass
