from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, func
from sqlalchemy.orm import relationship
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False, unique=True, index=True)
    country = Column(String(80), nullable=False)
    created_at = Column(DateTime, nullable=False)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_amount = Column(Numeric(12, 2), nullable=False)
    order_date = Column(Date, nullable=False)
    status = Column(String(30), nullable=False)

    customer = relationship("Customer", back_populates="orders")


class Refund(Base):
    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    refund_amount = Column(Numeric(12, 2), nullable=False)
    refund_date = Column(Date, nullable=False)
    reason = Column(String(120), nullable=False)


class AnalyticsSummary(Base):
    __tablename__ = "analytics_summary"

    id = Column(Integer, primary_key=True, default=1)
    total_orders = Column(Integer, nullable=False, default=0)
    total_revenue = Column(Numeric(14, 2), nullable=False, default=0)
    total_refunds = Column(Numeric(14, 2), nullable=False, default=0)
    net_revenue = Column(Numeric(14, 2), nullable=False, default=0)
    average_order_value = Column(Numeric(12, 2), nullable=False, default=0)
    repeat_customer_revenue = Column(Numeric(14, 2), nullable=False, default=0)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class RevenueTrend(Base):
    __tablename__ = "revenue_trends"

    month = Column(String(7), primary_key=True)
    total_revenue = Column(Numeric(14, 2), nullable=False, default=0)
    total_refunds = Column(Numeric(14, 2), nullable=False, default=0)
    net_revenue = Column(Numeric(14, 2), nullable=False, default=0)


class TopCustomer(Base):
    __tablename__ = "top_customers"

    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(120), nullable=False)
    total_spend = Column(Numeric(14, 2), nullable=False, default=0)
    order_count = Column(Integer, nullable=False, default=0)


Index("idx_orders_customer_id", Order.customer_id)
Index("idx_orders_order_date", Order.order_date)
Index("idx_orders_customer_date", Order.customer_id, Order.order_date)
Index("idx_refunds_order_id", Refund.order_id)
Index("idx_refunds_customer_id", Refund.customer_id)
Index("idx_refunds_refund_date", Refund.refund_date)
