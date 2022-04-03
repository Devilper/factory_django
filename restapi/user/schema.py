import datetime
from typing import Optional, List, TypeVar, Generic

from ninja import Schema, ModelSchema
from pydantic import Field, BaseModel
from pydantic.generics import GenericModel

from restapi.schema import ApiResponse, Pagination, ApiError
from user.models import UserProfile, Role, Menu, Permission, Action

DataType = TypeVar('DataType')
ListDataType = TypeVar('ListDataType')


class ActionSchema(ModelSchema):
    class Config:
        model = Action
        model_fields = "__all__"


class MenuSchema(ModelSchema):
    class Config:
        model = Menu
        model_fields = "__all__"


class PermissionSchema(ModelSchema):
    class Config:
        model = Permission
        model_fields = "__all__"


class RoleSchema(ModelSchema):
    class Config:
        model = Role
        model_fields = "__all__"


class UserSchema(ModelSchema):
    roles: List[RoleSchema]

    class Config:
        model = UserProfile
        model_exclude = ["password"]


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
    role: Optional[list] = Field(None, title="")


class LoginRep(BaseModel):
    staff_code: Optional[str] = Field(None, title="")
    password: Optional[str] = Field(None, title="")


class RoleRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    title: Optional[str] = Field(None, title="角色名称")
    desc: Optional[str] = Field(None, title="角色描述")
    p_id: Optional[list] = Field(None, title="拥有的所有权限")


class ActionRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    title: Optional[str] = Field(None, title="操作标题")
    code: Optional[str] = Field(None, title="方法")


class PermissionRep(BaseModel):
    id: Optional[int] = Field(None, title="")
    title: Optional[str] = Field(None, title="权限标题")
    url: Optional[str] = Field(None, title="含正则的URL")
    action: Optional[int] = Field(None, title="操作")
    parent: Optional[int] = Field(None, title="父权限")
    menu: Optional[int] = Field(None, title="菜单")


class MenuRep(BaseModel):
    id: Optional[int] = Field(0, title="")
    title: Optional[str] = Field(None, title="菜单名称")
    icon: Optional[str] = Field(None, title="icon")
    position: Optional[int] = Field(None, title="职责")


class LoginRsp(ApiResponse, BaseModel):
    token: Optional[str] = Field(None, title="")


class UserListRsp(ApiResponse):
    list: List[Optional[UserSchema]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class UserInfoRsp(ApiResponse):
    data: Optional[UserSchema] = Field(default=None, title="详细信息")


class RoleListRsp(ApiResponse):
    list: List[Optional[RoleSchema]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class PermissionListRsp(ApiResponse):
    list: List[Optional[PermissionSchema]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class ActionListRsp(ApiResponse):
    list: List[Optional[ActionSchema]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class MenuListRsp(ApiResponse):
    list: List[Optional[MenuSchema]] = Field(default_factory=[], title="列表数据")
    pagination: Optional[Pagination] = Field(default=None, title="分页信息")


class MenuTreeRsp(ApiResponse, Generic[ListDataType]):
    list: Optional[ListDataType] = Field(default=[], title="权限数数据")
