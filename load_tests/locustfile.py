from locust import HttpUser, task, between


class AnalyticsUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def summary(self):
        self.client.get("/analytics/summary")

    @task(2)
    def revenue_trends(self):
        self.client.get("/analytics/revenue-trends")

    @task(2)
    def top_customers(self):
        self.client.get("/analytics/top-customers?limit=10")

    @task(1)
    def repeat_customer_revenue(self):
        self.client.get("/analytics/repeat-customer-revenue")
