from typing import Optional, List, Generic, TypeVar

from ninja import ModelSchema, Schema
from pydantic import BaseModel, Field

from finance.models import Salary
from restapi.schema import ApiResponse, Pagination
from restapi.user.schema import UserSchema

DataType = TypeVar('DataType')


class SalaryRepSchema(BaseModel):
    staff_name: Optional[str] = Field(None, title="")
    attend_days: Optional[float] = Field(None, title="")
    leave_days: Optional[float] = Field(None, title="")
    overtime: Optional[float] = Field(None, title="")
    base_salary: Optional[float] = Field(None, title="")
    overtime_salary: Optional[float] = Field(None, title="")
    kouchu: Optional[float] = Field(None, title="")
    allowance: Optional[float] = Field(None, title="")
    should_pay: Optional[float] = Field(None, title="")
    tax: Optional[float] = Field(None, title="")
    actual_pay: Optional[float] = Field(None, title="")
    current_time: Optional[str] = Field(None, title="")


class SalaryRep(BaseModel):
    list: List[Optional[SalaryRepSchema]] = Field(default_factory=[], title="")


class UserNameSchema(Schema):
    username: Optional[str] = Field(None, title="")


class SalarySchema(ModelSchema):
    staff_name: Optional[UserNameSchema]

    class Config:
        model = Salary
        model_exclude = ['absent_days', 'business_days', 'zaotui_days', 'late_days']


class ListRsp(ApiResponse, Generic[DataType]):
    list: List[Optional[DataType]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")