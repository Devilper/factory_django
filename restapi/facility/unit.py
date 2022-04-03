from typing import Optional

from django.db.models import Q
from ninja import Query

from facility.models import Repair, Facility
from restapi import api
from restapi.facility.schema import ListRsp, RepairSchema, DataRsp, RepairRep, FacilitySchema, FacilityRep
from restapi.schema import ApiResponse, ApiError

from unit.commmon import PageUtil, handle_pagination
from user.models import UserProfile


@api.post(
    "/unit/create",
    response=Optional[ApiResponse],
    tags=["设备管理"],
    summary="设备创建"
)
def create_unit_info(request, unit_info: FacilityRep):
    try:
        user = UserProfile.objects.get(pk=unit_info.buyer)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    Facility.objects.create(
        version=unit_info.version,
        facility_name=unit_info.facility_name,
        price=unit_info.price,
        buyer=user,
    )


@api.get(
    "/unit/list",
    response=ListRsp[FacilitySchema],
    tags=["设备管理"],
    summary="设备列表"
)
def get_repair_info(request,
                    query: str = Query(None, title=""),
                    page: int = 1,
                    page_size: int = 10
                    ):
    facility = Facility.objects
    if query:
       facility = facility.filter(Q(facility_name=query) |
                                  Q(buyer__username=query) |
                                  Q(version=query)
                                  )

    total = facility.count()
    page_info = PageUtil(page, page_size)
    list_data = list(facility.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/unit/info",
    response=DataRsp[RepairSchema],
    tags=["设备管理"],
    summary="设备信息"
)
def get_user_salary(request,
                    id: int = Query(None, title="")
                    ):
    try:
        facility = Facility.objects.get(pk=id)
    except Exception:
        return DataRsp(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    return {"data": facility}


@api.put(
    "/unit/update",
    response=Optional[ApiResponse],
    tags=["设备管理"],
    summary="设备更新"
)
def update_salary_info(request,
                       unit_info: FacilityRep):
    try:
        facility = Facility.objects.get(pk=unit_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        user = UserProfile.objects.get(pk=unit_info.buyer)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    facility.version = unit_info.version
    facility.facility_name = unit_info.facility_name
    facility.price = unit_info.price
    facility.buyer = user

    facility.save()
