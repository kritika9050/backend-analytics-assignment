import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
from sqlalchemy.orm import Session
from app.config import settings
from app.models import Customer, Order, Refund

fake = Faker()

CUSTOMER_COUNT = 100_000
ORDER_COUNT = 1_000_000
REFUND_COUNT = 200_000
BATCH_SIZE = 10_000

COUNTRIES = ["India", "USA", "UK", "Canada", "Australia", "Germany", "UAE"]
STATUSES = ["completed", "completed", "completed", "completed", "cancelled"]
REASONS = ["damaged", "late_delivery", "wrong_item", "customer_request", "quality_issue"]


def reset_seed():
    random.seed(settings.seed)
    Faker.seed(settings.seed)


def generate_customers():
    reset_seed()
    base_date = datetime(2023, 1, 1)
    for i in range(1, CUSTOMER_COUNT + 1):
        yield {
            "id": i,
            "name": fake.name(),
            "email": f"customer{i}@example.com",
            "country": random.choice(COUNTRIES),
            "created_at": base_date + timedelta(days=random.randint(0, 900)),
        }


def generate_orders():
    reset_seed()
    base_date = datetime(2024, 1, 1).date()
    for i in range(1, ORDER_COUNT + 1):
        amount = Decimal(random.randint(1000, 200000)) / Decimal("100")
        yield {
            "id": i,
            "customer_id": random.randint(1, CUSTOMER_COUNT),
            "order_amount": amount,
            "order_date": base_date + timedelta(days=random.randint(0, 730)),
            "status": random.choice(STATUSES),
        }


def generate_refunds():
    reset_seed()
    base_date = datetime(2024, 1, 1).date()
    for i in range(1, REFUND_COUNT + 1):
        order_id = random.randint(1, ORDER_COUNT)
        amount = Decimal(random.randint(500, 50000)) / Decimal("100")
        yield {
            "id": i,
            "order_id": order_id,
            "customer_id": random.randint(1, CUSTOMER_COUNT),
            "refund_amount": amount,
            "refund_date": base_date + timedelta(days=random.randint(0, 730)),
            "reason": random.choice(REASONS),
        }


def paginate(generator_func, page: int, limit: int, total: int):
    start = (page - 1) * limit
    end = start + limit
    data = []
    for idx, item in enumerate(generator_func()):
        if idx >= end:
            break
        if idx >= start:
            data.append(item)
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "has_next": end < total,
        "data": data,
    }


def seed_database(db: Session):
    db.query(Refund).delete()
    db.query(Order).delete()
    db.query(Customer).delete()
    db.commit()

    for generator, model in [
        (generate_customers, Customer),
        (generate_orders, Order),
        (generate_refunds, Refund),
    ]:
        batch = []
        for row in generator():
            batch.append(row)
            if len(batch) >= BATCH_SIZE:
                db.bulk_insert_mappings(model, batch)
                db.commit()
                batch.clear()
        if batch:
            db.bulk_insert_mappings(model, batch)
            db.commit()
