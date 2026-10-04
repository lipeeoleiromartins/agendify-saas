import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Chave secreta obrigatória para o funcionamento de mensagens flash e sessões
    app.config['SECRET_KEY'] = 'agendify-super-secret-key-2026'
    
    # Caminho absoluto para a raiz do projeto (agendify-saas)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        from app.models.models import User, Client, Service, Appointment
        db.create_all()
        
    # --- REGISTO DE BLUEPRINTS ---
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.clients import clients_bp
    app.register_blueprint(clients_bp)

    from app.services import services_bp
    app.register_blueprint(services_bp)

    from app.appointments import appointments_bp
    app.register_blueprint(appointments_bp)
    
    # Rota principal temporária
    @app.route('/')
    def index():
        return "Bem-vindo ao Agendify SaaS! <a href='/login'>Fazer Login</a> | <a href='/register'>Registar</a>"

    return app