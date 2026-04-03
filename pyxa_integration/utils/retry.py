from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retries(func: Callable[[], T], retries: int = 2, base_delay_s: float = 0.3) -> T:
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            return func()
        except Exception as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(base_delay_s * (2**attempt))

    if last_error is None:
        raise RuntimeError("Retry loop failed without capturing an exception")
    raise last_error
