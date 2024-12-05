import unittest
from app import create_app, db
from app.users.models import User

class UserViewsTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування тестового середовища."""
        self.app = create_app()
        self.app = create_app(config_name="config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Очистка тестового середовища."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_page(self):
        """Перевірка завантаження сторінки реєстрації."""
        response = self.client.get("/users/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sign Up", response.data)

    def test_login_page(self):
        """Перевірка завантаження сторінки входу."""
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)


class UserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування тестового середовища."""
        self.app = create_app()
        self.app = create_app(config_name="config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Очистка тестового середовища."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_registration(self):
        """Перевірка реєстрації користувача."""
        response = self.client.post('users/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password',
            'confirm_password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)


class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування тестового середовища."""
        self.app = create_app()
        self.app = create_app(config_name="config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('password')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        """Очистка тестового середовища."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_login(self):
        """Перевірка входу користувача."""
        response = self.client.post('/users/login', data={
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/account', response.headers['Location'])

    def test_user_login_invalid(self):
        """Перевірка невдалого входу користувача."""
        response = self.client.post("/users/login", data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid email or password", response.data)

    def test_logout_user(self):
        """Перевірка виходу користувача."""
        self.client.post("/users/login", data={
            'email': 'test@example.com',
            'password': 'password'
        })
        response = self.client.get("/users/logout", follow_redirects=True)
        self.assertIn(b"Logged out", response.data)

        # Перевірка, що користувач більше не залогінений
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()
