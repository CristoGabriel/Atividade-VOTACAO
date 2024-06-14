#Instalação do Mysql Connector Python
import mysql.connector
from mysql.connector import errorcode

#Estabelecer a conexão
#Atenção no usuário e senha de conexão
print("Conexão a ser estabelecida...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='130388'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuário ou senha inválida')
      else:
            print(err)

#Criação da estrutura do banco de dados
cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `escola`;")
cursor.execute("CREATE DATABASE `escola`;")
cursor.execute("USE `escola`;")

#Criar as tabelas
TABLES = {}
TABLES['candidato'] = ('''
      CREATE TABLE `candidato` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `telefone` varchar(10),
      `voto` int(11),
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuario'] = ('''
      CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `login` varchar(20) NOT NULL,
      `senha` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

#Criação das tabelas dentro da estrutura do banco de dados
for tabelaNome in TABLES:
      tabelaSQL = TABLES[tabelaNome]
      try:
            print('Criação da tabela {}:'.format(tabelaNome), end=' ')
            cursor.execute(tabelaSQL)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# Inserção de Usuário
usuarioSQL = 'INSERT INTO usuario (login, senha) VALUES (%s, %s)'
usuarios = [
    ("fabianotaguchi", "123456"),
    ("teste", "teste"),
    ("adm", "adm"),
    ("root", "root"),
]
cursor.executemany(usuarioSQL, usuarios)
cursor.execute('select * from escola.usuario')
print(' -------------  Usuários:  -------------')
for usuario in cursor.fetchall():
    print(usuario[1])

# Inserção do aluno
alunoSQL = 'INSERT INTO candidato (nome, telefone, voto) VALUES (%s, %s, %s)'
candidato = [
    ("Fabiano","1234567891","0"),
    ("João","1234567891","0"),
    ("Patricia","1234567891","0")
]
cursor.executemany(alunoSQL, candidato)
cursor.execute('select * from escola.Candidato')
print(' -------------  Candidatos:  -------------')
for candidato in cursor.fetchall():
    print(candidato[1])

conn.commit()
#Fechamento da conexão
cursor.close()
conn.close()

