class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///nasausers_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'  # Secret key for testing
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

# Function to create the Flask application with test configurations
def create_test_app():
    from flask import Flask
    from models import connect_db

    app = Flask(__name__)
    app.config.from_object(TestConfig)

    # Database configuration for tests
    connect_db(app)

    return app
