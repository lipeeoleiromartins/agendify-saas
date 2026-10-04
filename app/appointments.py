from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.models import Appointment, Client, Service
from datetime import datetime, timedelta

appointments_bp = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointments_bp.route('/')
def list_appointments():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    
    # Obter a data do filtro através do parâmetro GET
    data_filtro = request.args.get('data')
    
    query = Appointment.query.filter_by(user_id=user_id)
    
    if data_filtro:
        try:
            data_obj = datetime.strptime(data_filtro, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Appointment.data_hora) == data_obj)
        except ValueError:
            flash('Formato de data inválido para o filtro.', 'danger')
            
    agendamentos = query.all()
    
    return render_template('appointments.html', agendamentos=agendamentos, data_filtro=data_filtro)

@appointments_bp.route('/add', methods=['GET', 'POST'])
def add_appointment():
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    clientes = Client.query.filter_by(user_id=user_id).all()
    servicos = Service.query.filter_by(user_id=user_id).all()
    
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        service_id = request.form.get('service_id')
        data_hora_str = request.form.get('data_hora') # formato yyyy-mm-ddTHH:MM
        
        try:
            novo_inicio = datetime.strptime(data_hora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Data e hora inválidas.', 'danger')
            return redirect(url_for('appointments.add_appointment'))
        
        # Obter o serviço para saber a duração
        servico = Service.query.get(service_id)
        if not servico:
            flash('Serviço inválido.', 'danger')
            return redirect(url_for('appointments.add_appointment'))
            
        duracao_minutos = servico.duracao_minutos or 30
        novo_fim = novo_inicio + timedelta(minutes=duracao_minutos)
        
        # Verificar se já existem agendamentos do utilizador que colidem com este intervalo
        agendamentos_existentes = Appointment.query.filter_by(user_id=user_id, status='Agendado').all()
        
        conflito = False
        for ag in agendamentos_existentes:
            outro_servico = Service.query.get(ag.service_id)
            outro_duracao = outro_servico.duracao_minutos if outro_servico else 30
            
            outro_inicio = ag.data_hora
            outro_fim = outro_inicio + timedelta(minutes=outro_duracao)
            
            # Lógica de sobreposição de horários
            if (novo_inicio < outro_fim) and (novo_fim > outro_inicio):
                conflito = True
                break
                
        if conflito:
            flash('Erro: Já existe um agendamento nesse horário ou há sobreposição com outro serviço!', 'danger')
            return redirect(url_for('appointments.add_appointment'))
        
        # Criar o agendamento se estiver livre
        novo_agendamento = Appointment(
            data_hora=novo_inicio,
            client_id=int(client_id),
            service_id=int(service_id),
            user_id=user_id,
            status='Agendado'
        )
        
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('appointments.list_appointments'))
        
    return render_template('add_appointment.html', clientes=clientes, servicos=servicos)

@appointments_bp.route('/<int:id>/status/<novo_status>', methods=['POST'])
def update_status(id, novo_status):
    if 'user_id' not in session:
        flash('Por favor, faz login primeiro.', 'danger')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    agendamento = Appointment.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    if novo_status in ['Concluído', 'Cancelado', 'Agendado']:
        agendamento.status = novo_status
        db.session.commit()
        flash(f'Estado do agendamento atualizado para: {novo_status}', 'success')
    else:
        flash('Estado inválido.', 'danger')
        
    return redirect(url_for('appointments.list_appointments'))