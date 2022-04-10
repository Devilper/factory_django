from typing import Optional, List

from django.contrib.auth.hashers import make_password, check_password
# from ninja import Query
from ninja import Query

from restapi import api
from restapi.schema import ApiResponse, ApiError
from restapi.user.schema import UserRep, LoginRsp, LoginRep, UserListRsp, UserInfoRsp, MenuTreeRsp
from restapi.views import get_user_info
from unit.commmon import PageUtil, handle_pagination
from unit.custom_jwt import get_jwt_token, decode_jwt
from user.models import UserProfile, Role
from user.views import InitPermission


@api.post(
    "/user/create",
    response=Optional[ApiResponse],
    tags=["用户"],
    summary="创建员工"
)
def create_user_info(request, user: UserRep):
    print(f"user:{user}")
    role = Role.objects.filter(id__in=user.role).all()

    if UserProfile.objects.filter(id_card=user.id_card).exists():
        return ApiResponse(
            error=ApiError(
                code=400,
                desc="身份信息已经存在"
            )
        )
    user_model = UserProfile.objects.create(
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
    )
    user_model.roles.add(*role)
    user_model.save()


@api.get(
    "/user/list",
    response=Optional[UserListRsp],
    tags=["用户"],
    summary="查询员工列表"
)
def get_user_list(request,
                  query: str = Query(None, title="查询信息"),
                  page: int = 1,
                  page_size: int = 10):
    user_list = UserProfile.objects.filter(is_active=True)
    if query:
        user_list = user_list.filter(username=query)

    total = user_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(user_list[page_info.start():page_info.end()].all())
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/user/info",
    response=Optional[UserInfoRsp],
    tags=["用户"],
    summary="查询员工信息"
)
def get_users_info(request, u_id: Optional[int] = Query(None, title="")):
    user = UserProfile.objects.filter(id=u_id)
    if not user.first():
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    return {
        "data": user.first()
    }


@api.put(
    "/user/update",
    response=Optional[ApiResponse],
    tags=["用户"],
    summary="更新员工信息"
)
def update_user_info(request, user: UserRep):

    user_info = UserProfile.objects.filter(id=user.u_id).first()
    if not user_info:
        return ApiResponse(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )

    user_info.staff_phone = user.staff_phone
    user_info.staff_age = user.staff_age
    user_info.staff_home = user.staff_home
    user_info.staff_gender = user.staff_gender
    user_info.staff_nationality = user.staff_nationality
    user_info.id_card = user.id_card
    user_info.address = user.address
    user_info.salary_pre_hour = user.salary_pre_hour
    user_info.password = make_password(user.password)

    roles = Role.objects.filter(id__in=user.role).all()
    user_info.roles.add(*roles)
    user_info.save()


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
        return ApiResponse(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    user_info.is_active = False
    user_info.save()


@api.post(
    "login",
    response=Optional[LoginRsp],
    tags=["用户"],
    summary="登录"
)
def login(request,
          login_info: Optional[LoginRep]):

    user_info = UserProfile.objects.filter(staff_code=login_info.staff_code).first()
    if user_info:
        # 校验密码
        if check_password(login_info.password, user_info.password):
            # 创建token

            token = get_jwt_token(user_info.username, user_info.staff_code, user_info.id)
            return LoginRsp(
                token=token,
            )
        else:
            return LoginRsp(
                error=ApiError(
                    code=400,
                    desc="账号密码错误"
                )
            )
    else:
        return LoginRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )


@api.get(
    "menu/tree",
    response=Optional[MenuTreeRsp],
    tags=["用户"],
    summary="登录"
)
def get_menu_tree(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    user_info = decode_jwt(token)
    user = UserProfile.objects.filter(staff_code=user_info["staff_code"]).first()
    menus_dict = InitPermission(user).init_menus_dict()
    menu_tree = [menu for menu in menus_dict.values()]
    return {
        "list": menu_tree
    }


@api.get(
    "/user/person",
    response=Optional[UserInfoRsp],
    tags=["用户"],
    summary="查询员工信息"
)
def get_user(request):
    user_info = get_user_info(request)
    print(user_info)
    user = UserProfile.objects.filter(id=user_info.get("id"))
    if not user.first():
        return UserInfoRsp(
            error=ApiError(
                code=400,
                desc="数据未找到"
            )
        )
    return {
        "data": user.first()
    }