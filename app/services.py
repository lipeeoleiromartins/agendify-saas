from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.models import Service

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/')
def list_services():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    servicos = Service.query.filter_by(user_id=user_id).all()
    
    return render_template('services.html', servicos=servicos)


@services_bp.route('/add', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        duracao = request.form.get('duracao')
        
        novo_servico = Service(
            nome=nome,
            preco=float(preco) if preco else 0.0,
            duracao_minutos=int(duracao) if duracao else 30,
            user_id=session['user_id']
        )
        
        db.session.add(novo_servico)
        db.session.commit()
        
        flash('Serviço adicionado com sucesso!', 'success')
        return redirect(url_for('services.list_services'))
        
    return render_template('add_service.html')