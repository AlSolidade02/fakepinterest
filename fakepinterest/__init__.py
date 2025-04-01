# blibiotecas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app  = Flask(__name__)
# configuração
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "sitefake"
app.config["UPLOAD_FOLDER"] = "static/fotos_post"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage" #pagina que vai ter login e senha

#arquivos de apoio
from fakepinterest import router



