from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    country: str
    created_at: datetime


class OrderOut(BaseModel):
    id: int
    customer_id: int
    order_amount: Decimal
    order_date: date
    status: str


class RefundOut(BaseModel):
    id: int
    order_id: int
    customer_id: int
    refund_amount: Decimal
    refund_date: date
    reason: str


class PaginatedResponse(BaseModel):
    page: int
    limit: int
    total: int
    has_next: bool
    data: list


class SummaryOut(BaseModel):
    total_orders: int
    total_revenue: Decimal
    total_refunds: Decimal
    net_revenue: Decimal
    average_order_value: Decimal
    repeat_customer_revenue: Decimal


class RevenueTrendOut(BaseModel):
    month: str
    total_revenue: Decimal
    total_refunds: Decimal
    net_revenue: Decimal


class TopCustomerOut(BaseModel):
    customer_id: int
    customer_name: str
    total_spend: Decimal
    order_count: int
