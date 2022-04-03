from typing import Optional

from ninja import Query

from finance.models import Salary
from restapi import api
from restapi.finance.schema import SalaryRep, ListRsp, SalarySchema
from restapi.schema import ApiResponse
from restapi.user.schema import ActionRep
from restapi.views import get_user_info
from unit.commmon import PageUtil, handle_pagination
from unit.custom_jwt import decode_jwt

from user.models import Action, UserProfile


@api.post(
    "/finance/create",
    response=Optional[ApiResponse],
    tags=["工资管理"],
    summary="工资单创建"
)
def create_salary_info(request, salary_info: SalaryRep):
    """
    excel 导入
    :param request:
    :param salary_info:
    :return:
    """

    staff_name_list = []
    for salary in salary_info.list:
        staff_name_list.append(salary.staff_name)
    users = UserProfile.objects.filter(username__in=staff_name_list).all()
    user_dict = {user.username: user for user in users}
    salary_list = []
    for salary in salary_info.list:
        if user_dict.get(salary.staff_name):
            salary_list.append(Salary(
                staff_name=user_dict.get(salary.staff_name),
                attend_days=salary.attend_days,
                leave_days=salary.leave_days,
                overtime=salary.overtime,
                base_salary=salary.base_salary,
                overtime_salary=salary.overtime_salary,
                kouchu=salary.kouchu,
                allowance=salary.allowance,
                should_pay=salary.should_pay,
                tax=salary.tax,
                actual_pay=salary.actual_pay,
            ))

    Salary.objects.bulk_create(salary_list)
    return {}


@api.get(
    "/finance/list",
    response=ListRsp[SalarySchema],
    tags=["工资管理"],
    summary="工资单"
)
def get_salary_info(request,
                    start_time: str = Query(None, title="起始时间"),
                    end_time: str = Query(None, title="结束时间"),
                    user_name: str = Query(None, title="员工名称"),
                    page: int = 1,
                    page_size: int = 10
                    ):
    salary = Salary.objects
    if user_name:
        salary = salary.filter(staff_name__username=user_name)
    if start_time and end_time:
        salary = salary.filter(current_time__range=(start_time, end_time))
    total = salary.count()
    page_info = PageUtil(page, page_size)
    list_data = list(salary.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/finance/info",
    response=Optional[SalarySchema],
    tags=["工资管理"],
    summary="个人工资信息"
)
def get_user_salary(request,
                    page: int = 1,
                    page_size: int = 10,
                    ):
    user = get_user_info(request)
    salary = Salary.objects.objects.filter(staff_name__id=user.get("id"))
    total = salary.count()
    page_info = PageUtil(page, page_size)
    list_data = list(salary.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.put(
    "/finance/update",
    response=Optional[ApiResponse],
    tags=["工资管理"],
    summary="个人工资信息"
)
def update_salary_info(request,
                       ):
    ...