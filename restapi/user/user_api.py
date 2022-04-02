from typing import Optional

from django.contrib.auth.hashers import make_password
from ninja import Query

from restapi import api
from restapi.schema import ApiResponse, ApiError
from restapi.user.schema import UserInfoRsp, UserRep, UserRsp
from user.models import UserProfile, Position


@api.post(
    "/user/create",
    response=Optional[UserInfoRsp],
    tags=["用户"],
    summary="创建员工"
)
def create_user_info(request, user: UserRep):
    try:
        position = Position.objects.get(pk=user.position)
    except Exception as e:
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    if UserProfile.objects.filter(id_card=user.id_card).exists():
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="身份信息已经存在"
            )
        )
    user_model = UserProfile(
        password=make_password(user.password),
        username=user.username,
        staff_code=user.staff_code,
        staff_phone=user.staff_phone,
        staff_age=user.staff_age,
        staff_home=user.staff_home,
        staff_gender=user.staff_gender,
        staff_nationality=user.staff_nationality,
        id_card=user.id_card,
        address=user.address,
        salary_pre_hour=user.salary_pre_hour,
        position=position
    )
    user_model.save()
    return UserInfoRsp()


@api.get(
    "/user/list",
    response=Optional[UserRsp],
    tags=["用户"],
    summary="查询员工列表"
)
def get_user_list(request):
    list_data = list(UserProfile.objects.filter(is_active=True).all())
    return {
        "list": list_data
    }


@api.get(
    "/user/info",
    response=Optional[UserInfoRsp],
    tags=["用户"],
    summary="查询员工信息"
)
def get_user_info(request, u_id: Optional[int] = Query(None, title="")):
    try:
        user = UserProfile.objects.get(pk=u_id)
    except Exception as e:
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    return {
        "data": user
    }


@api.get(
    "/user/update",
    response=Optional[UserInfoRsp],
    tags=["用户"],
    summary="更新员工信息"
)
def update_user_info(request, user: UserRep):
    try:
        user_info = UserProfile.objects.get(pk=user.u_id)
    except Exception as e:
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    user.password = make_password(user.password)
    user_info.update(*user)


@api.delete(
    "/user/delete",
    response=Optional[ApiResponse],
    tags=["用户"],
    summary="作废员工信息"
)
def delete_user_info(request,
                     u_id: Optional[int] = Query(None)):
    try:
        user_info = UserProfile.objects.get(pk=u_id)
    except Exception as e:
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    user_info.is_active = False
    user_info.save()

