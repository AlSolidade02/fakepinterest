from fakepinterest import database, app
from fakepinterest.models import Usuario,Foto
from datetime import datetime


# contexto para criar um banco de dados
with app.app_context():
    #comando para criar o banco de dados
    database.create_all()


print(datetime.today())


'''Esse arquivo python é opcional caso não queria deixar na estrutura do projeto pode ser apagado'''