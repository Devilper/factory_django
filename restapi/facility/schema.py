from typing import TypeVar, Generic, List, Optional

from ninja import ModelSchema
from pydantic import Field, BaseModel

from facility.models import Facility, Repair
from restapi.schema import ApiResponse, Pagination
from restapi.user.schema import UserSchema

DataType = TypeVar('DataType')


class FacilitySchema(ModelSchema):
    buyer: Optional[UserSchema]
    class Config:
        model = Facility
        model_fields = "__all__"


class RepairSchema(ModelSchema):
    facility_id: Optional[FacilitySchema]
    baoxiu_staff_name: Optional[UserSchema]
    repair_staff_name: Optional[UserSchema]

    class Config:
        model = Repair
        model_fields = "__all__"


class ListRsp(ApiResponse, Generic[DataType]):
    list: List[Optional[DataType]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class DataRsp(ApiResponse, Generic[DataType]):
    data: List[Optional[DataType]] = Field(default=None, title="列表数据")


class RepairRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    facility_id: Optional[int] = Field(None, title="故障设备")
    baoxiu_staff_name: Optional[int] = Field(None, title="报修人")
    baoxiu_staff_tel: Optional[str] = Field(None, title="联系方式")
    baoxiu_complementary: Optional[str] = Field(None, title="报修描述")
    repair_staff_name: Optional[int] = Field(None, title="维修人")


class FacilityRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    version: Optional[str] = Field(None, title="型号")
    facility_name: Optional[str] = Field(None, title="名称")
    price: Optional[int] = Field(None, title="价格")
    buyer: Optional[int] = Field(None, title="购买人")
