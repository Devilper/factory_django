import datetime
from typing import Optional, List

from ninja import Schema, ModelSchema
from pydantic import Field, BaseModel

from restapi.schema import ApiResponse
from user.models import UserProfile, Position


class PositionSchema(ModelSchema):
    class Config:
        model = Position
        model_fields = "__all__"


class PositionRsp(BaseModel):
    list: List[Optional[PositionSchema]] = Field(default_factory=[], title="职位信息")


class UserSchema(ModelSchema):
    class Config:
        model = UserProfile
        model_exclude = ["password"]


class UserRsp(ApiResponse, BaseModel):
    list: List[Optional[UserSchema]] = Field(default_factory=[], title="员工信息")


class UserInfoRsp(ApiResponse, BaseModel):
    data: Optional[UserSchema] = Field(default=None, title="员工信息")


class UserRep(BaseModel):
    u_id: Optional[int] = Field(None, title="")
    username: Optional[str] = Field(None, title="")
    password: Optional[str] = Field(None, title="")
    staff_code: Optional[str] = Field(None, title="")
    staff_phone: Optional[str] = Field(None, title="")
    staff_age: Optional[int] = Field(None, title="")
    staff_home: Optional[str] = Field(None, title="")
    staff_gender: Optional[str] = Field(None, title="")
    staff_nationality: Optional[str] = Field(None, title="")
    id_card: Optional[str] = Field(None, title="")
    address: Optional[str] = Field(None, title="")
    salary_pre_hour: Optional[str] = Field(None, title="")
    position: Optional[int] = Field(None, title="")


class LoginRep(BaseModel):
    username: Optional[str] = Field(None, title="")
    password: Optional[str] = Field(None, title="")


class LoginRsp(ApiResponse, BaseModel):
    token: Optional[str] = Field(None, title="")



