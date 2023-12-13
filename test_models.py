# test_models.py

import unittest
from test_config import create_test_app
from models import db, User, Favorite

class TestModels(unittest.TestCase):

    def setUp(self):
        """Config before each test"""
        self.app = create_test_app()
        self.client = self.app.test_client()

        # Contexto de aplicação para o banco de dados
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Limpeza após cada teste"""
        with self.app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_user_registration(self):
        """Teste de registro de usuário"""
        with self.app.app_context():
            user = User.register(
                username='testuser',
                password='testpassword',
                first_name='Test',
                last_name='User',
                email='test@example.com'
            )

            self.assertEqual(user.username, 'testuser')
            self.assertTrue(user.password.startswith('$2b$'))
            self.assertEqual(user.first_name, 'Test')
            self.assertEqual(user.last_name, 'User')
            self.assertEqual(user.email, 'test@example.com')

    def test_user_authentication(self):
        """Teste de autenticação do usuário"""
        with self.app.app_context():
            User.register(
                username='testuser',
                password='testpassword',
                first_name='Test',
                last_name='User',
                email='test@example.com'
            )

            auth_user = User.authenticate('testuser', 'testpassword')
            self.assertIsNotNone(auth_user)
            self.assertEqual(auth_user.username, 'testuser')

    def test_favorite_relationship(self):
        """Teste do relacionamento de favoritos entre User e Favorite"""
        with self.app.app_context():
            user = User.register(
                username='testuser',
                password='testpassword',
                first_name='Test',
                last_name='User',
                email='test@example.com'
            )

            favorite = Favorite(user_id=user.id, image_url='https://apod.nasa.gov/apod/image/2312/ArcticNight_Cobianchi_2048.jpg')
            db.session.add(favorite)
            db.session.commit()

            self.assertEqual(len(user.favorites), 1)
            self.assertEqual(user.favorites[0].image_url, 'https://apod.nasa.gov/apod/image/2312/ArcticNight_Cobianchi_2048.jpg')


if __name__ == '__main__':
    unittest.main()

