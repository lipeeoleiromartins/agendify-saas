from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relações
    clientes = db.relationship('Client', backref='usuario', lazy=True, cascade='all, delete-orphan')
    servicos = db.relationship('Service', backref='usuario', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Appointment', backref='usuario', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira para ligar ao utilizador dono do cliente
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relação com agendamentos
    agendamentos = db.relationship('Appointment', backref='cliente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Client {self.nome}>'


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False) # Ex: 30 min, 60 min
    
    # Chave estrangeira para o utilizador
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relação com agendamentos
    agendamentos = db.relationship('Appointment', backref='servico', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Service {self.nome}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), default='Agendado') # Agendado, Concluído, Cancelado
    
    # Chaves estrangeiras (Liga o agendamento ao utilizador, ao cliente e ao serviço)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id} - {self.data_hora}>'