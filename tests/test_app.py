import unittest
from app import app


class NetworkMonitorAPITest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_system_endpoint(self):
        response = self.client.get("/api/system")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        for key in ("cpu", "ram", "disk", "uptime", "ip", "upload", "download", "latency"):
            self.assertIn(key, data)

    def test_metrics_endpoint(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"system_cpu_usage_percent", response.data)


if __name__ == "__main__":
    unittest.main()
