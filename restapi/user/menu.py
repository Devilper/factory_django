from typing import Optional

from ninja import Query

from restapi import api
from restapi.schema import ApiResponse, ApiError
from restapi.user.schema import MenuRep, MenuListRsp
from unit.commmon import PageUtil, handle_pagination
from user.models import Menu


@api.post(
    "/menu/create",
    response=Optional[ApiResponse],
    tags=["权限管理"],
    summary="创建权限"
)
def create_menu_info(request, menu_info: MenuRep):
    if Menu.objects.filter(title=menu_info.title).exists():
        return ApiResponse(
            error=ApiError(
                code=400,
                desc=f"{menu_info.title}已存在"
            )
        )
    Menu.objects.create(
        title=menu_info.title,
        icon=menu_info.icon,
        position=menu_info.position
    )


@api.put(
    "/menu/update",
    response=Optional[ApiResponse],
    tags=["权限管理"],
    summary="权限更新"
)
def update_menu_info(request, menu_info: MenuRep):
    try:
        menu = Menu.objects.get(pk=menu_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code=400,
                desc=f"数据未找到"
            )
        )
    if menu.title != menu_info.title:
        if Menu.objects.filter(title=menu_info.title).exists():
            return ApiResponse(
                error=ApiError(
                    code=400,
                    desc=f"{menu_info.title}已存在"
                )
            )
    menu.title = menu_info.title
    menu.icon = menu_info.icon
    menu.position = menu_info.position
    menu.save()


@api.get(
    "/menu/list",
    response=Optional[MenuListRsp],
    tags=["权限管理"],
    summary="权限列表"
)
def get_menu_list(request,
                  query: str = Query(None, title="查询信息"),
                  page: int = 1,
                  page_size: int = 10):
    menu_list = Menu.objects.all()
    if query:
        menu_list = Menu.objects.filter(title=query)

    total = menu_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(menu_list[page_info.start():page_info.end()].all())
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }