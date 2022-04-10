import collections
import datetime
from typing import Optional

from ninja import Query

from factory_django.settings import BASE_WORK_TIME
from finance.models import Attendance
from restapi import api
from restapi.finance.schema import AttendanceRep, ListRsp, AttendanceSchema, DataRsp, TotalAttendanceSchema
from restapi.schema import ApiResponse
from restapi.user.schema import ActionRep
from restapi.views import get_user_info, int_time_to_str, str_time_to_int, datetime_to_int
from unit.commmon import PageUtil, handle_pagination
from unit.custom_jwt import decode_jwt

from user.models import Action, UserProfile


@api.post(
    "/attendance/create",
    response=Optional[ApiResponse],
    tags=["考勤管理"],
    summary="考勤记录创建"
)
def create_attendance_info(request, attendance_info: AttendanceRep):
    """
    excel 导入
    :param request:
    :param attendance_info:
    :return:
    """
    print(attendance_info)
    staff_name_list = []
    for attendance in attendance_info.list:
        staff_name_list.append(attendance.staff_name)
    users = UserProfile.objects.filter(username__in=staff_name_list).all()
    user_dict = {user.username: user for user in users}

    attendance_list = []
    for attendance in attendance_info.list:
        if user_dict.get(attendance.staff_name):
            print(attendance.supplement)
            attendance_list.append(Attendance(
                staff_name=user_dict.get(attendance.staff_name),
                current_time=attendance.current_time,
                flag_leave=_handle_bool(attendance.flag_leave),
                flag_business=_handle_bool(attendance.flag_business),
                start_time=_handle_time(attendance.current_time, attendance.start_time),
                end_time=_handle_time(attendance.current_time, attendance.end_time),
                supplement=attendance.supplement if attendance.supplement else "无",
            ))

    Attendance.objects.bulk_create(attendance_list)


@api.get(
    "/attendance/list",
    response=ListRsp[AttendanceSchema],
    tags=["考勤管理"],
    summary="考勤列表"
)
def get_attendance_info(request,
                    start_time: str = Query(None, title="起始时间"),
                    end_time: str = Query(None, title="结束时间"),
                    user_name: str = Query(None, title="员工名称"),
                    page: int = 1,
                    page_size: int = 10
                    ):
    attendance = Attendance.objects
    if user_name:
        attendance = attendance.filter(staff_name__username=user_name)
    if start_time and end_time:
        attendance = attendance.filter(current_time__range=(start_time, end_time))
    total = attendance.count()
    page_info = PageUtil(page, page_size)
    list_data = list(attendance.all()[page_info.start():page_info.end()])

    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/attendance/info",
    response=ListRsp[TotalAttendanceSchema],
    tags=["考勤管理"],
    summary="个人考勤汇总"
)
def get_user_attendance(request,
                        current_time: str = Query(None, title=""),
                        user_id: str = Query(None, title=""),
                        ):
    if not current_time:
        current_time = datetime.datetime.now().date()
        year = current_time.year
        month = current_time.month
    else:
        year, month = current_time.split("-")
    current_time = f"{year}-{month}"
    attendance_qs = Attendance.objects.filter(current_time__year=year,
                                              current_time__month=month)
    if user_id:
        attendance_qs = attendance_qs.filter(staff_name__id=user_id)

    data = attendance_qs.all()
    user_dict = collections.defaultdict(list)
    for i in data:
        user_dict[i.staff_name.id].append(i)
    data_list = []
    for user, attendance in user_dict.items():
        leave_day, business_day, overtime, work_day = _attendance_group_by(attendance)
        data_list.append(TotalAttendanceSchema(
            current_time=current_time,
            staff_name=attendance[0].staff_name.username,
            leave_day=leave_day,
            business_day=business_day,
            overtime=overtime / 3600,
            work_day=work_day,
        ))

    return ListRsp(
        list=data_list
    )


@api.get(
    "/attendance/person",
    response=ListRsp[AttendanceSchema],
    tags=["考勤管理"],
    summary="个人工资信息"
)
def update_attendance_info(request):
    user = get_user_info(request)
    attendance = Attendance.objects.filter(staff_name__id=user.get('id'))
    now_date = datetime.datetime.now().date()
    start_date = datetime.date(now_date.year, now_date.month, day=1)

    attendance = attendance.filter(current_time__range=[start_date, now_date])

    list_data = list(attendance.order_by("-current_time").all())
    return {
        "list": list_data,
        "pagination": handle_pagination(1, 1, 0)
    }


def _attendance_group_by(attendance_qs):
    leave_day = 0
    business_day = 0
    overtime = 0
    work_day = 0
    for attendance in attendance_qs:
        if attendance.flag_leave:
            leave_day += 1
        else:
            if attendance.flag_business:
                business_day += 1
            day_over_time = datetime_to_int(attendance.end_time) - \
                            datetime_to_int(attendance.start_time) - \
                            BASE_WORK_TIME
            if day_over_time > 0:
                overtime += day_over_time
            work_day += 1

    return leave_day, business_day, overtime, work_day


def _handle_time(handle_data, handle_time):
    handle_value = f"{handle_data} {handle_time}"
    return handle_value


def _handle_bool(bool_str):
    if bool_str == "是":
        return True
    else:
        return False
