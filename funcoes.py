import os
from escola import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioAluno(FlaskForm):
    nome = StringField('Nome do Candidato:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Cadastrar')

class FormularioCandidato(FlaskForm):
    nome = StringField('Nome do Candidato:', [validators.DataRequired(), validators.Length(min=1, max=50)])
    salvar = SubmitField('Cadastrar')

class FormularioUsuario(FlaskForm):
    login = StringField('Login', [validators.DataRequired(), validators.Length(min=1, max=20)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=20)])
    logar = SubmitField('Login')

def recuperaImagem(id):
    for nomeArquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'foto{id}' in nomeArquivo:
            return nomeArquivo
    return 'padrao.jpeg'

def deletaArquivo(id):
    arquivo = recuperaImagem(id)
    if arquivo != 'padrao.jpeg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
