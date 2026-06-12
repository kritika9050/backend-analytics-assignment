from fastapi import APIRouter, Query
from app.seed import (
    CUSTOMER_COUNT,
    ORDER_COUNT,
    REFUND_COUNT,
    generate_customers,
    generate_orders,
    generate_refunds,
    paginate,
)

router = APIRouter(prefix="/mock", tags=["Mock APIs"])


@router.get("/customers")
def get_mock_customers(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    return paginate(generate_customers, page, limit, CUSTOMER_COUNT)


@router.get("/orders")
def get_mock_orders(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    return paginate(generate_orders, page, limit, ORDER_COUNT)


@router.get("/refunds")
def get_mock_refunds(page: int = Query(1, ge=1), limit: int = Query(1000, ge=1, le=10000)):
    return paginate(generate_refunds, page, limit, REFUND_COUNT)
