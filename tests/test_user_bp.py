import unittest
from app import create_app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def test_greetings_page(self):
        """Тест маршруту /hi/<name>."""
        response = self.client.get("/users/hi/John/?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        """Тест маршруту /admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

if __name__ == "__main__":
    unittest.main()
