import unittest
from app import app  # Import your app object

class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        """Set up the test client."""
        self.client = app.test_client()
        self.client.testing = True

    def test_homepage(self):
        """Test if the homepage loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense Tracker', response.data)  # Check if the title is in the response

    def test_register(self):
        """Test if the registration page works."""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)  # Check if the register form is displayed

    def test_login(self):
        """Test if login is working."""
        response = self.client.post('/login', data=dict(
            username="testuser", password="testpass"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)  # Check if welcome message appears after login

    def test_add_expense(self):
        """Test if adding an expense works."""
        response = self.client.post('/add_expense', data=dict(
            category="Food", amount="50", date="2024-12-05"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense added successfully', response.data)  # Check for success message
