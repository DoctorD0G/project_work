import json
from enum import Enum, unique
from typing import Optional, Any, List, Literal

from fastapi_pagination import Params
from pydantic import BaseModel, field_validator, ConfigDict


class PaginationParams(BaseModel):
    page: int
    size: int


@unique
class ResponseState(Enum):
    success = "success"
    error = "error"


class BaseResponse(BaseModel):
    state: Literal[ResponseState.success, ResponseState.error]
    error_text: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class ResultResponse(BaseResponse):
    result: Optional[Any] = None


class PageDto(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int


class TablePagination(Params):
    sort_field: Optional[str] = None
    sort_descending: Optional[bool] = None
    filter: Optional[Any] = {}

    @field_validator("filter")
    def filter_convert(cls, v, values):  # noqa: B902
        return json.loads(v) if v else None
