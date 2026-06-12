# Large Data Analytics Backend

## Overview
This project is a backend analytics platform built using FastAPI and SQLAlchemy. It generates large datasets, exposes paginated mock APIs, ingests data into a relational database, and provides analytics endpoints.

### Dataset Sizes
- 100,000 Customers
- 1,000,000 Orders
- 200,000 Refunds

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite (Demo)
- PostgreSQL Ready

## Setup

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Swagger:
http://127.0.0.1:8000/docs

## APIs

### Mock APIs
- GET /mock/customers
- GET /mock/orders
- GET /mock/refunds

### Ingestion
- POST /ingest/customers
- POST /ingest/orders
- POST /ingest/refunds

### Analytics
- POST /analytics/refresh
- GET /analytics/summary
- GET /analytics/revenue-trends
- GET /analytics/top-customers
- GET /analytics/repeat-customer-revenue

## Performance Optimizations
- Bulk ingestion
- Pagination
- Pre-aggregated analytics tables
- SQL aggregation queries

## Database Note
The architecture is PostgreSQL-ready via SQLAlchemy. SQLite was used for local demonstration.
