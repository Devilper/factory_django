import datetime
from typing import Optional

from ninja import Query

from order.models import Orders, OrderStatusChoice
from restapi import api
from restapi.order.schema import OrderRep, OrderSchema

from restapi.schema import ApiResponse, ApiError
from restapi.views import get_user_info
from restapi.warehouse.schema import GoodsRep, ListRsp, GoodsSchema
from unit.commmon import PageUtil, handle_pagination

from user.models import UserProfile
from warehouse.models import Product, Warehouse


@api.post(
    "/order/create",
    response=Optional[ApiResponse],
    tags=["订单管理"],
    summary="订单创建"
)
def create_order_info(request, order_info: OrderRep):
    product = Product.objects.filter(id=order_info.order_name).first()
    if not product:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )

    Orders.objects.create(order_name=product,
                          order_client=order_info.order_client,
                          order_number=order_info.order_number,
                          order_price=order_info.order_price,
                          order_total_price=order_info.order_total_price,
                          order_supplement=order_info.order_supplement
                          )


@api.get(
    "/order/list",
    response=ListRsp[OrderSchema],
    tags=["订单管理"],
    summary="订单列表"
)
def get_orders(request,
               query: str = Query(None, title="名称"),
               page: int = 1,
               page_size: int = 10,
               ):
    orders = Orders.objects
    if query:
        orders = orders.filter(order_client__contains=query)
    total = orders.count()
    page_info = PageUtil(page, page_size)
    list_data = list(orders.all()[page_info.start():page_info.end()])

    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.put(
    "/order/update",
    response=Optional[ApiResponse],
    tags=["订单管理"],
    summary="订单修改"
)
def update_order(request,
                 order_info: OrderRep):
    try:
        order = Orders.objects.get(pk=order_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    order.order_number = order_info.order_number
    order.order_price = order_info.order_price
    order.order_total_price = order_info.order_total_price
    order.order_supplement = order_info.order_supplement
    order.save()


@api.get(
    "/order/confirm",
    response=Optional[ApiResponse],
    tags=["订单管理"],
    summary="订单完成"
)
def update_order(request,
                 id: int = Query(None, title="")):
    try:
        order = Orders.objects.get(pk=id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                desc="数据未找到"
            )
        )
    order.order_end = datetime.datetime.now()
    order.status = OrderStatusChoice.Finish
    products = Warehouse.objects.filter(product_name__id=order.order_name.id).order_by("-current_time")
    num = order.order_number
    total_num = 0
    for product in products:
        total_num += product.number
    if total_num < num:
        return ApiResponse(
            error=ApiError(
                desc="库存不足"
            )
        )
    for product in products:
        if num <= 0:
            break
        if product.number <= num:
            product.delete()
            num -= product.number
        else:
            product.number = num - product.number
            product.save()
            num = 0

    order.save()
