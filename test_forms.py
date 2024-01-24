import unittest
from app import app, db
from models import User, Favorite
from forms import LoginForm, RegisterForm, MarsRoverForm, SearchAPODForm
from test_config import create_test_app

class TestForms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_test_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_login_form_invalid(self):
        form = LoginForm()
        self.assertFalse(form.validate())

    def test_register_form_valid(self):
        # Creating a valid form but omitting a required field
        form = RegisterForm(username='newuser', password='newpassword', email='new@example.com')  # Omitting the 'first_name' field
        self.assertFalse(form.validate())

    def test_register_form_invalid(self):
        form = RegisterForm()
        self.assertFalse(form.validate())

    def test_mars_rover_form_valid(self):
        form = MarsRoverForm(cameras=['FHAZ', 'RHAZ'], date='2023-12-01')
        self.assertTrue(form.validate())

    def test_mars_rover_form_invalid(self):
        # No fields provided - should validate the form
        form = MarsRoverForm(cameras=[], date=None)
        self.assertTrue(form.validate())
    
        # Only camera provided - should validate the form
        form = MarsRoverForm(cameras=['FHAZ'], date=None)
        self.assertTrue(form.validate())
    
        # Only date provided - should validate the form
        form = MarsRoverForm(cameras=[], date='2023-12-01')
        self.assertTrue(form.validate())
    
        # Both camera and date provided - should validate the form
        form = MarsRoverForm(cameras=['FHAZ'], date='2023-12-01')
        self.assertTrue(form.validate())

    def test_search_apod_form_valid(self):
        form = SearchAPODForm(date='2023-12-01', start_date='2023-12-01', end_date='2023-12-10', count=5)
        self.assertTrue(form.validate())

    def test_search_apod_form_invalid(self):
        # No fields provided - should validate the form
        form = SearchAPODForm(date=None, start_date=None, end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Only date provided - should validate the form
        form = SearchAPODForm(date='2023-12-01', start_date=None, end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Only start date provided - should validate the form
        form = SearchAPODForm(date=None, start_date='2023-12-01', end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Only end date provided - should validate the form
        form = SearchAPODForm(date=None, start_date=None, end_date='2023-12-10', count=None)
        self.assertTrue(form.validate())
    
        # Only count provided - should validate the form
        form = SearchAPODForm(date=None, start_date=None, end_date=None, count=5)
        self.assertTrue(form.validate())
    
        # Both start and end dates provided - should validate the form
        form = SearchAPODForm(date=None, start_date='2023-12-01', end_date='2023-12-10', count=None)
        self.assertTrue(form.validate())
    
        # Both date and count provided - should validate the form
        form = SearchAPODForm(date='2023-12-01', start_date=None, end_date=None, count=5)
        self.assertTrue(form.validate())
    
        # All fields provided - should validate the form
        form = SearchAPODForm(date='2023-12-01', start_date='2023-12-01', end_date='2023-12-10', count=5)
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
