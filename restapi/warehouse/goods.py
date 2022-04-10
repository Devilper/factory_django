from typing import Optional

from ninja import Query

from restapi import api

from restapi.schema import ApiResponse, ApiError
from restapi.views import get_user_info
from restapi.warehouse.schema import GoodsRep, ListRsp, GoodsSchema
from unit.commmon import PageUtil, handle_pagination

from user.models import UserProfile
from warehouse.models import Goods


@api.post(
    "/good/create",
    response=Optional[ApiResponse],
    tags=["产品管理"],
    summary="产品创建"
)
def create_good_info(request, good_info: GoodsRep):
    """
    :param request:
    :param good_info:
    :return:
    """

    Goods.objects.create(good_name=good_info.good_name)


@api.get(
    "/good/list",
    response=ListRsp[GoodsSchema],
    tags=["产品管理"],
    summary="产品列表"
)
def get_good_info(request,
                  query: str = Query(None, title="名称"),
                  ):
    good = Goods.objects
    if query:
        good = good.filter(good_name=query)

    list_data = list(good.order_by('id').all())
    return {
        "list": list_data,
    }


@api.put(
    "/good/update",
    response=Optional[ApiResponse],
    tags=["产品管理"],
    summary="个人工资信息"
)
def update_good_info(request,
                     good_info: GoodsRep):
    try:
        good = Goods.objects.get(pk=good_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    good.good_name = good_info.good_name
    good.save()
