from typing import Optional

from ninja import Query

from restapi import api
from restapi.schema import ApiResponse, ApiError
from restapi.user.schema import RoleRep, RoleListRsp
from unit.commmon import PageUtil, handle_pagination
from user.models import Role, Permission


@api.post(
    "/role/create",
    response=Optional[ApiResponse],
    tags=["角色管理"],
    summary="创建角色"
)
def create_role_info(request, role_info: RoleRep):
    if Role.objects.filter(title=role_info.title).exists():
        return ApiResponse(
            error=ApiError(
                code=400,
                desc=f"{role_info.title}已经存在"
            )
        )
    role = Role.objects.create(
        title=role_info.title,
        desc=role_info.desc,
    )
    perm_list = Permission.objects.filter(id__in=role_info.p_id)
    role.permissions.add(*perm_list)
    role.save()


@api.put(
    "/role/update",
    response=Optional[ApiResponse],
    tags=["角色管理"],
    summary="角色更新"
)
def update_role_info(request, role_info: RoleRep):
    try:
        role = Role.objects.get(pk=role_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code=400,
                desc=f"数据不存在"
            )
        )
    if role.title != role_info.title:
        if Role.objects.filter(title=role_info.title).exsits():
            return ApiResponse(
                error=ApiError(
                    code=400,
                    desc=f"{role_info.title}已经存在"
                )
            )
    perm_list = Permission.objects.filter(id__in=role_info.p_id)
    role.title = role_info.title
    role.desc = role_info.desc
    role.permissions.set(perm_list)
    role.save()


@api.get(
    "/role/list",
    response=Optional[RoleListRsp],
    tags=["角色管理"],
    summary="角色列表"
)
def get_role_list(request,
                  query: str = Query(None, title="查询信息"),
                  page: int = 1,
                  page_size: int = 10):
    role_list = Role.objects.all()
    if query:
        role_list = Role.objects.filter(title=query)

    total = role_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(role_list[page_info.start():page_info.end()].all())
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }
