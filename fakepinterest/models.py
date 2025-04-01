# criar a estrutura do banco de dados
from fakepinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# criando as classes dos modelos do banco de dados
# todas as classes criadas vão ser sub classes da database.
# cada atributo da subclasse vai ser uma coluna da tabaela


#passando para o python que essa é a função responsavel por buscar um usuario
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # realizando a busca no banco de dados pelo id dele

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer,primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto",backref="usuario", lazy=True) # criando o relacionamento entre as tabelas para sempre buscar a foto do usuario


class Foto(database.Model):
    id = database.Column(database.Integer,primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime,nullable=False, default=datetime.today())
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuario.id'),nullable=False) # criando a chave estrangeira