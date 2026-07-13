from __future__ import annotations

import json
from timeit import timeit

import smonitor

from depdigest import dep_digest


def main(number: int = 300_000) -> None:
    def plain(value: int) -> int:
        return value + 1

    decorated = dep_digest("json")(plain)

    @dep_digest("json", when={"mode": "special"})
    def conditional(value: int, mode: str = "normal") -> int:
        return value + 1

    smonitor.configure(enabled=False, handlers=[])

    plain_seconds = timeit(lambda: plain(1), number=number)
    decorated_seconds = timeit(lambda: decorated(1), number=number)
    conditional_seconds = timeit(lambda: conditional(1), number=number)
    print(
        json.dumps(
            {
                "calls": number,
                "plain_ns": plain_seconds / number * 1e9,
                "digest_ns": decorated_seconds / number * 1e9,
                "overhead_ns": (decorated_seconds - plain_seconds) / number * 1e9,
                "conditional_miss_ns": conditional_seconds / number * 1e9,
            }
        )
    )


if __name__ == "__main__":
    main()
