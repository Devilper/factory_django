from typing import Optional

from ninja import Query

from restapi import api

from restapi.schema import ApiResponse, ApiError
from restapi.warehouse.schema import ListRsp, ProductSchema, WarehouseSchema, WarehouseSourceSchema
from unit.commmon import PageUtil, handle_pagination

from warehouse.models import Warehouse, WarehouseSource


@api.get(
    "/product/warehouse/list",
    response=ListRsp[WarehouseSchema],
    tags=["仓库管理"],
    summary="产品仓库列表"
)
def get_product_warehouse_info(request,
                               query: str = Query(None, title="名称"),
                               page: int = 1,
                               page_size: int = 10,
                               ):
    warehouse = Warehouse.objects
    if query:
        warehouse = warehouse.filter(product_name__product_name=query)
    total = warehouse.count()
    page_info = PageUtil(page, page_size)
    list_data = list(warehouse.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }


@api.get(
    "/good/warehouse/list",
    response=ListRsp[WarehouseSourceSchema],
    tags=["仓库管理"],
    summary="原料仓库列表"
)
def get_good_warehouse_info(request,
                            query: str = Query(None, title="名称"),
                            page: int = 1,
                            page_size: int = 10,
                            ):
    warehouse = WarehouseSource.objects
    if query:
        warehouse = warehouse.filter(source_name__good_name=query)
    total = warehouse.count()
    page_info = PageUtil(page, page_size)
    list_data = list(warehouse.all()[page_info.start():page_info.end()])
    return {
        "list": list_data,
        "pagination": handle_pagination(page, page_size, total)
    }
