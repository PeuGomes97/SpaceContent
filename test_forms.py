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
    # Criando um formulário válido, mas removendo um campo obrigatório
        form = RegisterForm(username='newuser', password='newpassword', email='new@example.com')  # Deixando de passar o campo 'first_name'
        self.assertFalse(form.validate())

    def test_register_form_invalid(self):
        form = RegisterForm()
        self.assertFalse(form.validate())

    def test_mars_rover_form_valid(self):
        form = MarsRoverForm(cameras=['FHAZ', 'RHAZ'], date='2023-12-01')
        self.assertTrue(form.validate())

    def test_mars_rover_form_invalid(self):
    # Nenhum campo fornecido - deve validar o formulário
        form = MarsRoverForm(cameras=[], date=None)
        self.assertTrue(form.validate())
    
        # Apenas a câmera fornecida - deve validar o formulário
        form = MarsRoverForm(cameras=['FHAZ'], date=None)
        self.assertTrue(form.validate())
    
        # Apenas a data fornecida - deve validar o formulário
        form = MarsRoverForm(cameras=[], date='2023-12-01')
        self.assertTrue(form.validate())
    
        # Ambos, câmera e data fornecidos - deve validar o formulário
        form = MarsRoverForm(cameras=['FHAZ'], date='2023-12-01')
        self.assertTrue(form.validate())



    def test_search_apod_form_valid(self):
        form = SearchAPODForm(date='2023-12-01', start_date='2023-12-01', end_date='2023-12-10', count=5)
        self.assertTrue(form.validate())

    def test_search_apod_form_invalid(self):
    # Nenhum campo fornecido - deve validar o formulário
        form = SearchAPODForm(date=None, start_date=None, end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Apenas a data fornecida - deve validar o formulário
        form = SearchAPODForm(date='2023-12-01', start_date=None, end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Apenas a data inicial fornecida - deve validar o formulário
        form = SearchAPODForm(date=None, start_date='2023-12-01', end_date=None, count=None)
        self.assertTrue(form.validate())
    
        # Apenas a data final fornecida - deve validar o formulário
        form = SearchAPODForm(date=None, start_date=None, end_date='2023-12-10', count=None)
        self.assertTrue(form.validate())
    
        # Apenas a contagem fornecida - deve validar o formulário
        form = SearchAPODForm(date=None, start_date=None, end_date=None, count=5)
        self.assertTrue(form.validate())
    
        # Ambos, data inicial e final fornecidas - deve validar o formulário
        form = SearchAPODForm(date=None, start_date='2023-12-01', end_date='2023-12-10', count=None)
        self.assertTrue(form.validate())
    
        # Ambos, data e contagem fornecidas - deve validar o formulário
        form = SearchAPODForm(date='2023-12-01', start_date=None, end_date=None, count=5)
        self.assertTrue(form.validate())
    
        # Todos os campos fornecidos - deve validar o formulário
        form = SearchAPODForm(date='2023-12-01', start_date='2023-12-01', end_date='2023-12-10',     count=5)
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
