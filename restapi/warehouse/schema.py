from enum import IntEnum
from typing import TypeVar, Generic, List, Optional

from ninja import ModelSchema
from pydantic import Field, BaseModel

from restapi.facility.schema import FacilitySchema
from restapi.schema import ApiResponse, Pagination
from restapi.user.schema import UserSchema
from warehouse.models import Product, Goods, Warehouse, WarehouseSource, PurchaseList, ProduceDiary

DataType = TypeVar('DataType')


class PurchaseListStatusEnum(IntEnum):
    """
    EDIT = 1, "编辑"
    AUDIT = 2, "审核"
    PURCHASE = 3, "采购"
    """
    UNKNOW = 0
    EDIT = 1
    AUDIT = 2
    PURCHASE = 3


class ProductSchema(ModelSchema):

    class Config:
        model = Product
        model_fields = "__all__"


class GoodsSchema(ModelSchema):

    class Config:
        model = Goods
        model_fields = "__all__"


class WarehouseSchema(ModelSchema):
    product_name: Optional[ProductSchema]

    class Config:
        model = Warehouse
        model_fields = "__all__"


class WarehouseSourceSchema(ModelSchema):
    source_name: Optional[GoodsSchema]

    class Config:
        model = WarehouseSource
        model_fields = "__all__"


class PurchaseListSchema(ModelSchema):
    apply_staff_name: Optional[UserSchema]
    sanction_staff_name: Optional[UserSchema]
    buyer_name: Optional[UserSchema]
    good_name: Optional[GoodsSchema]

    class Config:
        model = PurchaseList
        model_fields = "__all__"


class ProduceDiarySchema(ModelSchema):
    staff_name: Optional[UserSchema]
    product_name: Optional[ProductSchema]

    class Config:
        model = ProduceDiary
        model_fields = "__all__"


class ListRsp(ApiResponse, Generic[DataType]):
    list: List[Optional[DataType]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class DataRsp(ApiResponse, Generic[DataType]):
    data: List[Optional[DataType]] = Field(default=None, title="列表数据")


class ProductRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    product_name: Optional[str] = Field(None, title="产品")
    product_version: Optional[str] = Field(None, title="产品型号")


class GoodsRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    good_name: Optional[str] = Field(None, title="原料")


class WarehouseRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    product_name: Optional[int] = Field(None, title="产品")
    number: Optional[int] = Field(None, title="数量")
    unit: Optional[str] = Field(None, title="单位")


class WarehouseSourceRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    source_name: Optional[int] = Field(None, title="原料")
    number: Optional[int] = Field(None, title="数量")
    unit: Optional[str] = Field(None, title="单位")


class PurchaseListRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    good_name: Optional[str] = Field(None, title="品名")
    good_version: Optional[str] = Field(None, title="型号")
    good_num: Optional[int] = Field(None, title="数量")
    # apply_staff_name: Optional[int] = Field(None, title="申请人")
    price: Optional[int] = Field(None, title="单价")
    total_price: Optional[int] = Field(None, title="总价")
    unit: Optional[str] = Field(None, title="单位")


class ProduceDiaryRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    staff_name: Optional[str] = Field(None, title="员工")
    product_name: Optional[str] = Field(None, title="产品")
    today_done_num: Optional[int] = Field(None, title="今日产量")
    qualified_num: Optional[int] = Field(None, title="合格量")
    unit: Optional[str] = Field(None, title="单位")
