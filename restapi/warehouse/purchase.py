from typing import Optional

from ninja import Query

from restapi import api

from restapi.schema import ApiResponse, ApiError
from restapi.views import get_user_info
from restapi.warehouse.schema import ListRsp, PurchaseListSchema, PurchaseListStatusEnum, PurchaseListRep
from unit.commmon import PageUtil, handle_pagination
from user.models import UserProfile

from warehouse.models import WarehouseSource, PurchaseList, Goods, PurchaseListStatus


@api.get(
    "/purchase/list",
    response=ListRsp[PurchaseListSchema],
    tags=["采购管理"],
    summary="采购单列表"
)
def get_purchase_info(request,
                      good_name: str = Query(None, title="名称"),
                      status: Optional[PurchaseListStatusEnum] = Query(None, title="名称"),
                      page: int = 1,
                      page_size: int = 10,
                      ):
    purchase_list = PurchaseList.objects
    if good_name:
        purchase_list = purchase_list.filter(good_name=good_name)
    if status:
        purchase_list = purchase_list.filter(status=status)

    total = purchase_list.count()
    page_info = PageUtil(page, page_size)
    list_data = list(purchase_list.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.post(
    "/purchase/create",
    response=Optional[ApiResponse],
    tags=["采购管理"],
    summary="新建采购单"
)
def create_purchase_info(request,
                         purchase_info: PurchaseListRep):
    print(purchase_info)
    good = Goods.objects.filter(id=int(purchase_info.good_name)).first()
    if not good:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    user_info = get_user_info(request)
    print(user_info)
    user = UserProfile.objects.filter(id=user_info.get("id")).first()
    if not user:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到1"
            )
        )
    PurchaseList.objects.create(
        good_name=good,
        good_version=purchase_info.good_version,
        good_num=purchase_info.good_num,
        apply_staff_name=user,
        price=purchase_info.price,
        total_price=purchase_info.total_price,
        status=PurchaseListStatus.EDIT,
        unit=purchase_info.unit
    )


@api.get(
    "/purchase/audit",
    response=Optional[ApiResponse],
    tags=["采购管理"],
    summary="审核采购单"
)
def audit_purchase_info(request,
                        id: int = Query(None, title=""),
                        ):
    try:
        purchase_list = PurchaseList.objects.get(pk=id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    if purchase_list.status != PurchaseListStatus.EDIT:
        return ApiResponse(
            error=ApiError(
                desc="只有编辑状态下才能审核"
            )
        )
    user_info = get_user_info(request)
    user = UserProfile.objects.get(pk=user_info.get("id"))
    purchase_list.sanction_staff_name = user
    purchase_list.status = PurchaseListStatus.AUDIT
    purchase_list.save()


@api.get(
    "/purchase/purchase",
    response=Optional[ApiResponse],
    tags=["采购管理"],
    summary="采购采购单"
)
def audit_purchase_info(request,
                        id: int = Query(None, title=""),
                        ):
    try:
        purchase_list = PurchaseList.objects.get(pk=id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    if purchase_list.status != PurchaseListStatus.AUDIT:
        return ApiResponse(
            error=ApiError(
                desc="只有审批状态下才能采购"
            )
        )
    user_info = get_user_info(request)
    user = UserProfile.objects.get(pk=user_info.get("id"))
    purchase_list.buyer_name = user
    purchase_list.status = PurchaseListStatus.PURCHASE
    purchase_list.save()

    good = Goods.objects.filter(good_name=purchase_list.good_name).first()

    WarehouseSource.objects.create(
        source_name=good,
        number=purchase_list.good_num,
        unit=purchase_list.unit
    )


@api.put(
    "/purchase/update",
    response=Optional[ApiResponse],
    tags=["采购管理"],
    summary="编辑采购单"
)
def create_purchase_info(request,
                         purchase_info: PurchaseListRep):
    try:
        purchase_list = PurchaseList.objects.get(pk=purchase_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    if purchase_list.status != PurchaseListStatus.EDIT:
        return ApiResponse(
            error=ApiError(
                desc="只有编辑状态下才能修改"
            )
        )

    good = Goods.objects.filter(id=purchase_info.good_name).first()
    if not good:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    user_info = get_user_info(request)
    user = UserProfile.objects.filter(id=user_info.get("id")).first()
    if not user:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )

    purchase_list.good_name = purchase_info.good_name
    purchase_list.good_version = purchase_info.good_version
    purchase_list.good_num = purchase_info.good_num
    purchase_list.apply_staff_name = user
    purchase_list.price = purchase_info.price
    purchase_list.total_price = purchase_info.total_price
    purchase_list.status = PurchaseListStatus.EDIT
    purchase_list.unit = purchase_info.unit
    purchase_list.save()
