from typing import Optional

from django.db.models import Q
from ninja import Query

from facility.models import Repair, Facility
from restapi import api
from restapi.facility.schema import ListRsp, RepairSchema, DataRsp, RepairRep
from restapi.schema import ApiResponse, ApiError

from unit.commmon import PageUtil, handle_pagination
from user.models import UserProfile


@api.post(
    "/repair/create",
    response=Optional[ApiResponse],
    tags=["设备维修"],
    summary="维修单创建"
)
def create_repair_info(request, repair_info: RepairRep):
    try:
        facility = Facility.objects.get(pk=repair_info.facility_id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        user = UserProfile.objects.get(pk=repair_info.baoxiu_staff_name)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        repair_user = UserProfile.objects.get(pk=repair_info.repair_staff_name)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    Repair.objects.create(
        facility_id=facility,
        baoxiu_staff_name=user,
        baoxiu_staff_tel=repair_info.baoxiu_staff_tel,
        baoxiu_complementary=repair_info.baoxiu_complementary,
        repair_staff_name=repair_user
    )


@api.get(
    "/repair/list",
    response=ListRsp[RepairSchema],
    tags=["设备维修"],
    summary="维修单"
)
def get_repair_info(request,
                    query: str = Query(None, title=""),
                    page: int = 1,
                    page_size: int = 10
                    ):
    repair = Repair.objects
    if query:
       repair = repair.filter(Q(facility_id__facility_name=query) |
                              Q(baoxiu_staff_name__username=query) |
                              Q(repair_staff_name__username=query)
                              )

    total = repair.count()
    page_info = PageUtil(page, page_size)
    list_data = list(repair.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/repair/info",
    response=DataRsp[RepairSchema],
    tags=["设备维修"],
    summary="设备维修信息"
)
def get_user_salary(request,
                    id: int = Query(None, title="")
                    ):
    try:
        repair = Repair.objects.get(pk=id)
    except Exception:
        return DataRsp(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    return {"data": repair}


@api.put(
    "/repair/update",
    response=Optional[ApiResponse],
    tags=["设备维修"],
    summary="设备维修更新"
)
def update_salary_info(request,
                       repair_info: RepairRep):
    try:
        repair = Repair.objects.get(pk=repair_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        facility = Facility.objects.get(pk=repair_info.facility_id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        user = UserProfile.objects.get(pk=repair_info.baoxiu_staff_name)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    try:
        repair_user = UserProfile.objects.get(pk=repair_info.repair_staff_name)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )

    repair.facility_id = facility
    repair.baoxiu_staff_name = user
    repair.baoxiu_staff_tel = repair_info.baoxiu_staff_tel
    repair.baoxiu_complementary = repair_info.baoxiu_complementary
    repair.repair_staff_name = repair_user
    repair.save()
