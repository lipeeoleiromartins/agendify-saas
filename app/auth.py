from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Este email já está registado.', 'danger')
            return redirect(url_for('auth.register'))
        
        senha_hash = generate_password_hash(senha)
        novo_usuario = User(nome=nome, email=email, senha_hash=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso! Podes fazer login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = User.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha_hash, senha):
            # Guardar o ID e o nome na sessão do Flask
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nome
            
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Email ou palavra-passe incorretos.', 'danger')
            
    return render_template('login.html')


@auth.route('/dashboard')
def dashboard():
    # Verificar se o utilizador está com sessão iniciada
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
        
    return render_template('dashboard.html', nome=session.get('user_name'))


@auth.route('/logout')
def logout():
    session.clear()
    flash('Sessão terminada com sucesso.', 'success')
    return redirect(url_for('auth.login'))