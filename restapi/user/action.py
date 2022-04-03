from typing import Optional

from ninja import Query

from restapi import api
from restapi.schema import ApiResponse
from restapi.user.schema import ActionRep, ActionSchema, ActionListRsp
from unit.commmon import PageUtil, handle_pagination
from user.models import Action


@api.post(
    "/action/create",
    response=Optional[ApiResponse],
    tags=["操作管理"],
    summary="创建操作"
)
def create_action_info(request, action_info: ActionRep):
    if Action.objects.filter(title=action_info.title).exsits():
        return ApiResponse(
            error=400,
            desc=f"{action_info.title}已存在"
        )
    Action.objects.create(
        title=action_info.title,
        code=action_info.code,
    )


@api.put(
    "/action/update",
    response=Optional[ApiResponse],
    tags=["操作管理"],
    summary="操作更新"
)
def update_action_info(request, action_info: ActionRep):
    try:
        action = Action.objects.get(pk=action_info.a_id)
    except Exception as e:
        return ApiResponse(
            error=400,
            desc=f"数据未找到"
        )
    if action.title != action_info.title:
        if action.objects.filter(title=action_info.title).exsits():
            return ApiResponse(
                error=400,
                desc=f"{action_info.title}已存在"
            )
    action.update(*action_info)


@api.get(
    "/action/list",
    response=Optional[ActionListRsp],
    tags=["操作管理"],
    summary="操作列表"
)
def get_action_list(request,
                    query: str = Query(None, title="查询信息"),
                    page: int = 1,
                    page_size: int = 10):
    action_list = Action.objects.all()
    if query:
        action_list = Action.objects.filter(title=query)

    total = action_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(action_list[page_info.start():page_info.end()].all())
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }