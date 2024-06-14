from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from escola import app, db
from modelos import Candidato, Usuario
from funcoes import recuperaImagem, deletaArquivo, FormularioAluno, FormularioUsuario, FormularioCandidato
import time
import os

#Definição da rota index
#Os valores devem ser consultados a partir do banco de dados
@app.route('/')
def index():
    listaAlunos = Candidato.query.order_by(Candidato.id)
    return render_template('lista.html', titulo='Lista de candidatos', candidatos=listaAlunos)


#Criação da rota novo, que renderiza a página Novo, caso o usuário tenha feito o login
@app.route('/novo')
def novo():
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioAluno()
    return render_template('novo.html', titulo='Cadastro de um novo candidato', form=form)


#Rota acionada pelo formulário novo.html que permite a criação de um novo aluno
#Após isso, o registro do aluno é salvo no banco de dados
@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioAluno(request.form)
    if not form.validate_on_submit():
        return redirect(url_for('novo'))
    nome = form.nome.data
    candidato = Candidato.query.filter_by(nome=nome).first()
    if candidato:
        flash('Candidato já cadastrado')
        return redirect(url_for('novo'))
    novoAluno = Candidato(nome=nome)
    db.session.add(novoAluno)
    db.session.commit()
    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/foto{novoAluno.id}-{timestamp}.png')
    return redirect(url_for('index'))


#Criação da rota para realização do login do usuário
@app.route('/login')
def login():
    form = FormularioUsuario()
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, form=form)


#Criação da rota autenticar acionada através do formulário login.html
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuario.query.filter_by(login=form.login.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
            session['usuarioLogado'] = usuario.login
            flash(usuario.login + ' logado com sucesso!')
            proximaPagina = request.form['proxima']
            return redirect(proximaPagina)
        else:
            flash('Usuário não logado.')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))


# Criação da rota para logout
@app.route('/logout')
def logout():
    session['usuarioLogado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


#Rota destinada para recuperar os dados de um aluno selecionado
#Será renderizada a página editar.html
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    consultaAluno = Candidato.query.filter_by(id=id).first()
    form = FormularioCandidato(request.form)
    form.nome.data = consultaAluno.nome
    imagemAluno = recuperaImagem(id)
    return render_template('editar.html', titulo='Editar dados do candidato', Candidato=consultaAluno, imagemAluno=imagemAluno, form=form)


#Rota para atualizar os dados de um aluno
#Esta rota é chamada através do arquivo editar.html
@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioAluno(request.form)
    if form.validate_on_submit():
        alunoConsulta = Candidato.query.filter_by(id=request.form['id']).first()
        alunoConsulta.nome = form.nome.data
        db.session.add(alunoConsulta)
        db.session.commit()
        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deletaArquivo(alunoConsulta.id)
        arquivo.save(f'{upload_path}/foto{alunoConsulta.id}-{timestamp}.png')
    return redirect(url_for('index'))


#Rota reservada para fazer a exclusão de um aluno
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuarioLogado' not in session or session['usuarioLogado'] == None:
        return redirect(url_for('login'))

    alunoConsulta = Candidato.query.filter_by(id=id).first()
    Candidato.query.filter_by(id=id).delete()
    db.session.commit()
    deletaArquivo(alunoConsulta.id)
    flash('Candidato excluído com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<nomeArquivo>')
def imagem(nomeArquivo):
    return send_from_directory('uploads', nomeArquivo)

@app.route('/olhar', methods=['POST',])
def olhar():
    form = FormularioAluno(request.form)
    if form.validate_on_submit():
        alunoConsulta = Candidato.query.filter_by(id=request.form['id']).first()
        alunoConsulta.nome = form.nome.data
    return redirect(url_for('index'))

@app.route('/votos')
def votos():
    listaAlunos = Candidato.query.order_by(Candidato.id)
    return render_template('votos.html', titulo='Votação', candidatos=listaAlunos)

@app.route('/confirma')
def confirma():
    votin = Candidato.voto
    if confirma:
        votin = votin + 1
    return render_template('confirma.html')