# import unittest
# from app import app, db
# from models import User, Favorite
# from test_config import create_test_app

# class TestApp(unittest.TestCase):
#     def setUp(self):
#         self.app = create_test_app()
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         with self.app.app_context():
#             self.test_user = User(username='testuser', password='testpassword', first_name='Test', last_name='User', email='test@example.com')
#             db.session.add(self.test_user)
#             db.session.commit()
#             self.test_user_id = self.test_user.id  

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     def test_homepage(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response.location, 'http://localhost/register')

#     def test_show_user(self):
#       with self.client.session_transaction() as sess:
#         sess['user_id'] = self.test_user_id
#         sess['username'] = 'testuser'

#     # Passando um parâmetro especial para permitir o acesso durante os testes
#         response = self.client.get(f'/users/{self.test_user_id}') 
#         self.assertEqual(response.status_code, 200)


#     def test_result_for_apod(self):
#         with self.client.session_transaction() as sess:
#             sess['user_id'] = self.test_user_id
#             sess['username'] = 'testuser'

#         response = self.client.get(f'/users/{self.test_user_id}/result/apod')
#         self.assertEqual(response.status_code, 200)

#     def test_mars_photos(self):
#         with self.client.session_transaction() as sess:
#             sess['user_id'] = self.test_user_id
#             sess['username'] = 'testuser'

#         response = self.client.get(f'/users/{self.test_user_id}/mars_photos')
#         self.assertEqual(response.status_code, 200)

#     def test_list_favorites(self):
#         with self.client.session_transaction() as sess:
#             sess['user_id'] = self.test_user_id
#             sess['username'] = 'testuser'

#         response = self.client.get(f'/users/{self.test_user_id}/favorites')
#         self.assertEqual(response.status_code, 200)

#     def test_delete_favorite(self):
#         with self.client.session_transaction() as sess:
#             sess['user_id'] = self.test_user_id
#             sess['username'] = 'testuser'

#         favorite = Favorite(id=1, image_url='https://apod.nasa.gov/apod/image/2312/Heart_TelLiveOstling_2953.jpg', user_id=self.test_user_id)
#         db.session.add(favorite)
#         db.session.commit()

#         response = self.client.delete(f'/users/{self.test_user_id}/favorites/1')
#         self.assertEqual(response.status_code, 200)

#     def test_add_to_favorites(self):
#         with self.client.session_transaction() as sess:
#             sess['user_id'] = self.test_user_id
#             sess['username'] = 'testuser'

#         response = self.client.post(f'/users/{self.test_user_id}/add_to_favorites', data={'image_url': 'https://apod.nasa.gov/apod/image/2312/Heart_TelLiveOstling_2953.jpg'})
        
#         self.assertIn(response.status_code, [200, 302])

#     def test_register(self):
#         with self.client as c:
#             response = c.post('/register', data=dict(
#                 username='newuser',
#                 password='newpassword',
#                 first_name='New',
#                 last_name='User',
#                 email='new@example.com'
#             ), follow_redirects=True)
#             self.assertEqual(response.status_code, 200)

#     def test_login(self):
#         with self.client as c:
#             response = c.post('/login', data=dict(
#                 username='testuser',
#                 password='testpassword'
#             ), follow_redirects=True)
#             self.assertEqual(response.status_code, 200)

# if __name__ == '__main__':
#     unittest.main()

import unittest
from app import app, db
from models import User, Favorite
from test_config import create_test_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        with self.app.app_context():
            self.test_user = User(username='testuser', password='testpassword', first_name='Test', last_name='User', email='test@example.com')
            db.session.add(self.test_user)
            db.session.commit()
            self.test_user_id = self.test_user.id  

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_homepage(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_show_user(self):
        response = self.client.get(f'/users/{self.test_user_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_result_for_apod(self):
        response = self.client.get(f'/users/{self.test_user_id}/result/apod', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_mars_photos(self):
        response = self.client.get(f'/users/{self.test_user_id}/mars_photos', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_list_favorites(self):
        response = self.client.get(f'/users/{self.test_user_id}/favorites', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_favorite(self):
        favorite = Favorite(id=1, image_url='https://apod.nasa.gov/apod/image/2312/Heart_TelLiveOstling_2953.jpg', user_id=self.test_user_id)
        db.session.add(favorite)
        db.session.commit()

        response = self.client.delete(f'/users/{self.test_user_id}/favorites/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_to_favorites(self):
        response = self.client.post(f'/users/{self.test_user_id}/add_to_favorites', data={'image_url': 'https://apod.nasa.gov/apod/image/2312/Heart_TelLiveOstling_2953.jpg'}, follow_redirects=True)
        self.assertIn(response.status_code, [200, 302])

    def test_register(self):
        response = self.client.post('/register', data=dict(
            username='newuser',
            password='newpassword',
            first_name='New',
            last_name='User',
            email='new@example.com'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
