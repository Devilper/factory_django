from typing import Optional

from ninja import Query

from restapi import api
from restapi.schema import ApiResponse, ApiError
from restapi.user.schema import PermissionSchema, PermissionRep, PermissionListRsp
from unit.commmon import PageUtil, handle_pagination
from user.models import Permission, Action, Menu


@api.post(
    "/permission/create",
    response=Optional[ApiResponse],
    tags=["权限管理"],
    summary="创建权限"
)
def create_permission_info(request, permission_info: PermissionRep):
    permission = Permission.objects.create(
        title=permission_info.title,
        url=permission_info.url,
    )
    if permission_info.parent:
        p_perm = Permission.objects.filter(id=permission_info.parent).first()
        permission.parent = p_perm
    if permission_info.action:
        permission.action = Action.objects.filter(id=permission_info.action).first()
    if permission_info.menu:
        permission.menu = Menu.objects.filter(id=permission_info.menu).first()
    permission.save()


@api.put(
    "/permission/update",
    response=Optional[ApiResponse],
    tags=["权限管理"],
    summary="权限更新"
)
def update_permission_info(request, permission_info: PermissionRep):
    try:
        permission = Permission.objects.get(pk=permission_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code=400,
                desc=f"数据不存在"
            )
        )
    if permission.title != permission_info.title:
        if Permission.objects.filter(title=permission_info.title).exists():
            return ApiResponse(
                error=ApiError(
                    code=400,
                    desc=f"数据{permission_info.title}已存在"
                )
            )
    permission.title = permission_info.title
    permission.url = permission_info.url

    if permission_info.parent:
        p_perm = Permission.objects.filter(id=permission_info.parent).first()
        permission.parent = p_perm
    if permission_info.action:
        permission.action = Action.objects.filter(id=permission_info.action).first()
    if permission_info.menu:
        permission.menu = Menu.objects.filter(id=permission_info.menu).first()
    print("ssdddaadsada")
    print(permission)
    permission.save()


@api.get(
    "/permission/list",
    response=Optional[PermissionListRsp],
    tags=["权限管理"],
    summary="权限列表"
)
def get_permission_list(request,
                        query: str = Query(None, title="查询信息"),
                        page: int = 1,
                        page_size: int = 10):
    permission_list = Permission.objects.all()
    if query:
        permission_list = Permission.objects.filter(title=query)

    total = permission_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(permission_list[page_info.start():page_info.end()].all())
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }
