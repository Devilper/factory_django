from typing import Optional, Generic, TypeVar, List

from ninja import ModelSchema
from pydantic import Field, BaseModel

from order.models import Orders
from restapi.schema import ApiResponse, Pagination
from restapi.warehouse.schema import ProductSchema

DataType = TypeVar('DataType')


class OrderSchema(ModelSchema):
    order_name: Optional[ProductSchema]

    class Config:
        model = Orders
        model_fields = "__all__"


class ListRsp(ApiResponse, Generic[DataType]):
    list: List[Optional[DataType]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class DataRsp(ApiResponse, Generic[DataType]):
    data: List[Optional[DataType]] = Field(default=None, title="列表数据")


class OrderRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    order_name: Optional[int] = Field(None, title="")
    order_client: Optional[str] = Field(None, title="")
    order_number: Optional[int] = Field(None, title="")
    order_price: Optional[int] = Field(None, title="")
    order_total_price: Optional[int] = Field(None, title="")
    order_end: Optional[int] = Field(None, title="")
    order_supplement: Optional[str] = Field(None, title="")