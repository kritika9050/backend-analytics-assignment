from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer, Order, Refund
from app.seed import generate_customers, generate_orders, generate_refunds, BATCH_SIZE
from app.analytics import refresh_analytics_tables

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


def bulk_load(db: Session, model, generator_func):
    db.query(model).delete()
    db.commit()

    inserted = 0
    batch = []
    for row in generator_func():
        batch.append(row)
        if len(batch) >= BATCH_SIZE:
            db.bulk_insert_mappings(model, batch)
            db.commit()
            inserted += len(batch)
            batch.clear()

    if batch:
        db.bulk_insert_mappings(model, batch)
        db.commit()
        inserted += len(batch)

    return inserted


@router.post("/customers")
def ingest_customers(db: Session = Depends(get_db)):
    count = bulk_load(db, Customer, generate_customers)
    return {"message": "Customers ingested", "count": count}


@router.post("/orders")
def ingest_orders(db: Session = Depends(get_db)):
    count = bulk_load(db, Order, generate_orders)
    return {"message": "Orders ingested", "count": count}


@router.post("/refunds")
def ingest_refunds(db: Session = Depends(get_db)):
    count = bulk_load(db, Refund, generate_refunds)
    return {"message": "Refunds ingested", "count": count}


@router.post("/all")
def ingest_all(db: Session = Depends(get_db)):
    customers = bulk_load(db, Customer, generate_customers)
    orders = bulk_load(db, Order, generate_orders)
    refunds = bulk_load(db, Refund, generate_refunds)
    refresh_analytics_tables(db)
    return {
        "message": "All datasets ingested and analytics refreshed",
        "customers": customers,
        "orders": orders,
        "refunds": refunds,
    }
