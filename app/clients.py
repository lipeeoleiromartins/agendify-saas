from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.models import Client, User

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/')
def list_clients():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Buscar apenas os clientes associados ao utilizador com sessão iniciada
    user_id = session['user_id']
    clientes = Client.query.filter_by(user_id=user_id).all()
    
    return render_template('clients.html', clientes=clientes)


@clients_bp.route('/add', methods=['GET', 'POST'])
def add_client():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        email = request.form.get('email')
        
        novo_cliente = Client(
            nome=nome,
            telefone=telefone,
            email=email,
            user_id=session['user_id']
        )
        
        db.session.add(novo_cliente)
        db.session.commit()
        
        flash('Cliente adicionado com sucesso!', 'success')
        return redirect(url_for('clients.list_clients'))
        
    return render_template('add_client.html')