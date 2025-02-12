from typing import Annotated, NewType
from pydantic import Field


EntityId = Annotated[int | str, Field(union_mode="left_to_right")]
EntityIdOptional = Annotated[
    int | str | None, Field(default=None, union_mode="left_to_right")
]
Total = NewType("Total", int)
