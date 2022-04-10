from typing import Optional

from ninja import Query

from restapi import api

from restapi.schema import ApiResponse, ApiError
from restapi.views import get_user_info
from restapi.warehouse.schema import ListRsp, ProduceDiarySchema, ProduceDiaryRep
from unit.commmon import PageUtil, handle_pagination
from user.models import UserProfile

from warehouse.models import ProduceDiary, Product, ProduceDiaryStatus, Warehouse


@api.get(
    "/produce/list",
    response=ListRsp[ProduceDiarySchema],
    tags=["生产管理"],
    summary="生产单列表"
)
def get_produce_info(request,
                     product_name: str = Query(None, title="名称"),
                     staff_name: str = Query(None, title="员工"),
                     page: int = 1,
                     page_size: int = 10,
                     ):
    produce_diary = ProduceDiary.objects
    if product_name:
        produce_diary = produce_diary.filter(product_name__product_name=product_name)
    if staff_name:
        produce_diary = produce_diary.filter(staff_name__username=staff_name)

    total = produce_diary.count()
    page_info = PageUtil(page, page_size)
    list_data = list(produce_diary.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.post(
    "/produce/create",
    response=Optional[ApiResponse],
    tags=["生产管理"],
    summary="新建生产单"
)
def create_produce_info(request,
                        product_info: ProduceDiaryRep):
    product = Product.objects.filter(product_name=product_info.product_name).first()
    if not product:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    user = UserProfile.objects.filter(username=product_info.staff_name).first()
    if not user:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    ProduceDiary.objects.create(
        staff_name=user,
        product_name=product,
        today_done_num=product_info.today_done_num,
        qualified_num=product_info.qualified_num,
        unit=product_info.unit
    )


@api.get(
    "/produce/confirm",
    response=Optional[ApiResponse],
    tags=["生产管理"],
    summary="审核生产单"
)
def audit_produce_info(request,
                        id: int = Query(None, title=""),
                        ):
    try:
        produce_diary = ProduceDiary.objects.get(pk=id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    if produce_diary.status != ProduceDiaryStatus.EDIT:
        return ApiResponse(
            error=ApiError(
                desc="只有编辑状态下才能审核"
            )
        )
    produce_diary.status = ProduceDiaryStatus.CONFIRM
    produce_diary.save()

    Warehouse.objects.create(
        product_name=produce_diary.product_name,
        number=produce_diary.qualified_num,
        unit=produce_diary.unit,
    )


@api.put(
    "/produce/update",
    response=Optional[ApiResponse],
    tags=["生产管理"],
    summary="编辑生产单"
)
def audit_produce_info(request,
                        product_info: ProduceDiaryRep,
                        ):
    try:
        produce_diary = ProduceDiary.objects.get(pk=product_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    if produce_diary.status != ProduceDiaryStatus.EDIT:
        return ApiResponse(
            error=ApiError(
                desc="只有编辑状态下才能修改"
            )
        )
    product = Product.objects.filter(product_name=product_info.product_name).first()
    if not product:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    user = UserProfile.objects.filter(username=product_info.staff_name).first()
    if not user:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    produce_diary.staff_name = user,
    produce_diary.product_name = product,
    produce_diary.today_done_num = product_info.today_done_num,
    produce_diary.qualified_num = product_info.qualified_num,
    produce_diary.unit = product_info.unit

    produce_diary.save()

