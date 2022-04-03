from typing import Optional

from pydantic import Field, BaseModel
from pydantic.generics import GenericModel


class ApiError(BaseModel):
    code: int = Field("", title="错误码")
    desc: str = Field("", title="错误描述")


class ApiResponse(GenericModel):
    error: Optional[ApiError] = None


class Pagination(BaseModel):
    page: Optional[int] = Field(1, title="页数")
    page_size: Optional[int] = Field(10, title="每页数量")
    total: Optional[int] = Field(0, title="总数量")