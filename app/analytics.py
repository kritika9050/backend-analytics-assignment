from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AnalyticsSummary, RevenueTrend, TopCustomer

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def refresh_analytics_tables(db: Session):
    # SQLite-compatible cleanup
    db.execute(text("DELETE FROM analytics_summary"))
    db.execute(text("DELETE FROM revenue_trends"))
    db.execute(text("DELETE FROM top_customers"))

    db.execute(text("""
        INSERT INTO analytics_summary (
            id,
            total_orders,
            total_revenue,
            total_refunds,
            net_revenue,
            average_order_value,
            repeat_customer_revenue
        )
        WITH order_stats AS (
            SELECT
                COUNT(*) AS total_orders,
                COALESCE(SUM(order_amount), 0) AS total_revenue,
                COALESCE(AVG(order_amount), 0) AS average_order_value
            FROM orders
            WHERE status = 'completed'
        ),
        refund_stats AS (
            SELECT COALESCE(SUM(refund_amount), 0) AS total_refunds
            FROM refunds
        ),
        repeat_stats AS (
            SELECT COALESCE(SUM(customer_revenue), 0) AS repeat_customer_revenue
            FROM (
                SELECT customer_id, SUM(order_amount) AS customer_revenue, COUNT(*) AS order_count
                FROM orders
                WHERE status = 'completed'
                GROUP BY customer_id
                HAVING COUNT(*) > 1
            ) x
        )
        SELECT
            1,
            os.total_orders,
            os.total_revenue,
            rs.total_refunds,
            os.total_revenue - rs.total_refunds,
            os.average_order_value,
            reps.repeat_customer_revenue
        FROM order_stats os, refund_stats rs, repeat_stats reps
    """))

    db.execute(text("""
        INSERT INTO revenue_trends (month, total_revenue, total_refunds, net_revenue)
        WITH monthly_orders AS (
            SELECT
                strftime('%Y-%m', order_date) AS month,
                COALESCE(SUM(order_amount), 0) AS total_revenue
            FROM orders
            WHERE status = 'completed'
            GROUP BY strftime('%Y-%m', order_date)
        ),
        monthly_refunds AS (
            SELECT
                strftime('%Y-%m', refund_date) AS month,
                COALESCE(SUM(refund_amount), 0) AS total_refunds
            FROM refunds
            GROUP BY strftime('%Y-%m', refund_date)
        ),
        months AS (
            SELECT month FROM monthly_orders
            UNION
            SELECT month FROM monthly_refunds
        )
        SELECT
            m.month,
            COALESCE(o.total_revenue, 0) AS total_revenue,
            COALESCE(r.total_refunds, 0) AS total_refunds,
            COALESCE(o.total_revenue, 0) - COALESCE(r.total_refunds, 0) AS net_revenue
        FROM months m
        LEFT JOIN monthly_orders o ON o.month = m.month
        LEFT JOIN monthly_refunds r ON r.month = m.month
        ORDER BY m.month
    """))

    db.execute(text("""
        INSERT INTO top_customers (customer_id, customer_name, total_spend, order_count)
        SELECT
            c.id,
            c.name,
            SUM(o.order_amount) AS total_spend,
            COUNT(o.id) AS order_count
        FROM customers c
        JOIN orders o ON o.customer_id = c.id
        WHERE o.status = 'completed'
        GROUP BY c.id, c.name
        ORDER BY total_spend DESC
        LIMIT 100
    """))

    db.commit()


@router.post("/refresh")
def refresh_analytics(db: Session = Depends(get_db)):
    refresh_analytics_tables(db)
    return {"message": "Analytics tables refreshed successfully"}


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    summary = db.query(AnalyticsSummary).filter(AnalyticsSummary.id == 1).first()
    if not summary:
        return {"message": "Analytics not generated yet. Run POST /analytics/refresh."}
    return summary


@router.get("/revenue-trends")
def get_revenue_trends(db: Session = Depends(get_db)):
    return db.query(RevenueTrend).order_by(RevenueTrend.month).all()


@router.get("/top-customers")
def get_top_customers(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    return db.query(TopCustomer).order_by(TopCustomer.total_spend.desc()).limit(limit).all()


@router.get("/repeat-customer-revenue")
def get_repeat_customer_revenue(db: Session = Depends(get_db)):
    summary = db.query(AnalyticsSummary).filter(AnalyticsSummary.id == 1).first()
    if not summary:
        return {"message": "Analytics not generated yet. Run POST /analytics/refresh."}
    return {"repeat_customer_revenue": summary.repeat_customer_revenue}