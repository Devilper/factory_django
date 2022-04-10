from typing import Optional

from ninja import Query

from restapi import api

from restapi.schema import ApiResponse, ApiError
from restapi.warehouse.schema import ProductRep, ListRsp, ProductSchema

from warehouse.models import Product


@api.post(
    "/product/create",
    response=Optional[ApiResponse],
    tags=["产品管理"],
    summary="产品创建"
)
def create_product_info(request, product_info: ProductRep):
    """
    :param request:
    :param product_info:
    :return:
    """

    Product.objects.create(product_name=product_info.product_name,
                           product_version=product_info.product_version)


@api.get(
    "/product/list",
    response=ListRsp[ProductSchema],
    tags=["产品管理"],
    summary="产品列表"
)
def get_product_info(request,
                     query: str = Query(None, title="名称"),
                     ):
    product = Product.objects
    if query:
        product = product.filter(product_name=query)

    list_data = list(product.order_by("id").all())
    return {
        "list": list_data,
    }


@api.put(
    "/product/update",
    response=Optional[ApiResponse],
    tags=["产品管理"],
    summary="个人工资信息"
)
def update_product_info(request,
                        product_info: ProductRep):
    try:
        product = Product.objects.get(pk=product_info.id)
    except Exception as e:
        return ApiResponse(
            error=ApiError(
                code="400",
                desc="数据未找到"
            )
        )
    product.product_name = product_info.product_name
    product.product_version = product_info.product_version
    product.save()
