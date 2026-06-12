# Large Data Analytics Backend Assignment

## Objective

Build a backend service that generates large datasets, exposes mock paginated APIs, ingests data into PostgreSQL, and provides analytics endpoints with response times consistently below 2 seconds.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Locust

## Dataset Size

- 100,000 Customers
- 1,000,000 Orders
- 200,000 Refunds

A fixed seed is used to make data generation reproducible.

## Architecture

```text
Mock APIs -> Ingestion Service -> PostgreSQL -> Pre-aggregated Analytics Tables -> Analytics APIs
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-github-repo-url>
cd backend-assignment
```

### 2. Run With Docker

```bash
docker compose up --build
```

API will run at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Important APIs

### Health Check

```http
GET /
```

### Mock APIs

```http
GET /mock/customers?page=1&limit=1000
GET /mock/orders?page=1&limit=1000
GET /mock/refunds?page=1&limit=1000
```

### Ingestion APIs

```http
POST /ingest/customers
POST /ingest/orders
POST /ingest/refunds
POST /ingest/all
```

`POST /ingest/all` loads all datasets and refreshes analytics tables.

### Analytics APIs

```http
GET /analytics/summary
GET /analytics/revenue-trends
GET /analytics/top-customers?limit=10
GET /analytics/repeat-customer-revenue
POST /analytics/refresh
```

## Database Design

### customers

Stores customer master data.

### orders

Stores transactional order data with customer relation.

### refunds

Stores refund data linked to orders and customers.

### analytics_summary

Stores precomputed summary metrics:

- Total Orders
- Total Revenue
- Total Refunds
- Net Revenue
- Average Order Value
- Repeat Customer Revenue

### revenue_trends

Stores monthly revenue, refunds, and net revenue.

### top_customers

Stores top 100 customers by spend.

## Optimization Decisions

1. **Bulk Insert**  
   Data ingestion uses SQLAlchemy `bulk_insert_mappings` in batches of 10,000 records.

2. **Indexes**  
   Indexes are added on frequently queried columns:

   - `orders.customer_id`
   - `orders.order_date`
   - `refunds.order_id`
   - `refunds.customer_id`
   - `refunds.refund_date`

3. **Pre-Aggregation**  
   Analytics endpoints read from summary tables instead of scanning 1M+ rows per request.

4. **Fast Analytics Reads**  
   `/analytics/summary`, `/analytics/revenue-trends`, and `/analytics/top-customers` query small precomputed tables, enabling sub-2-second responses.

## Load Testing

Install Locust if running locally:

```bash
pip install locust
```

Run load test:

```bash
locust -f load_tests/locustfile.py --host http://localhost:8000
```

Open:

```text
http://localhost:8089
```

Suggested test:

```text
Concurrent users: 50
Spawn rate: 10 users/second
Duration: 2-5 minutes
```

Expected result:

```text
Average response time: under 500 ms
95th percentile: under 2 seconds
Failures: 0
```

## Loom Video Explanation Points

1. Project objective
2. Tech stack
3. Folder structure
4. Mock paginated APIs
5. Ingestion process
6. PostgreSQL tables and indexes
7. Analytics APIs
8. Pre-aggregation strategy
9. Load test results
10. Final conclusion
