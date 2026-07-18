from typing import List, TypeVar

T = TypeVar("T")


def compute_next_cursor(items: List[T], id_field: str = "id") -> str | None:
    if len(items) == 0:
        return None
    item = items[-1]
    return str(getattr(item, id_field))
