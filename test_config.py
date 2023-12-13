class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///nasausers_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'  # Chave secreta para testes
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

# Função para criar a aplicação Flask com as configurações de teste
def create_test_app():
    from flask import Flask
    from models import connect_db

    app = Flask(__name__)
    app.config.from_object(TestConfig)

    # Configuração do banco de dados para os testes
    connect_db(app)

    return app
