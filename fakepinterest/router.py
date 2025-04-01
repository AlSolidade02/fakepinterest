# Criar as rotas do site (links)
from flask import Flask,render_template,url_for,redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario,Foto
from flask_login import login_required, login_user,logout_user, current_user
from fakepinterest.forms import FormLogin,FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


# criação de rota principal
#decorator 
@app.route("/",methods=["GET", "POST"]) # Permitindo os metodos de consulta e envio de informação
def homepage():
    #fazendo login
    formlogin = FormLogin()
    # sistema de login 
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil",id_usuario= usuario.id))     
    # retono da rota principal
    return render_template("homepage.html", form=formlogin)
        

@app.route("/criarconta",methods=["GET", "POST"])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        #criptografando a senha
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data) 
        #salvando os dados que o usuario digitou no html 
        usuario = Usuario(username= formcriarconta.username.data, senha=senha, email= formcriarconta.email.data)

        # Armazenando todas as informações no banco de dados
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True) # logando na conta que acabou de ser criada
        return redirect(url_for("perfil",id_usuario= usuario.id))
    
    return render_template("criarconta.html", form=formcriarconta)

#criando rota para o perfil do usuario
@app.route("/perfil/<id_usuario>",methods=["GET", "POST"])
@login_required # restrigindo o acesso a essa rota sem que o usuario esteja logado
def perfil(id_usuario):

    if int(id_usuario) == int(current_user.id):
        # aqui o usuario está vendo o proprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salva o arquivo na pasta
            caminho_arquivo = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],nome_seguro)
            arquivo.save(caminho_arquivo)

            # registrar no banco
            foto = Foto(imagem = nome_seguro, id_usuario= current_user.id)
            database.session.add(foto)
            database.session.commit()

        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)

@app.route("/logout")
@login_required # restrigindo o acesso a essa rota sem que o usuario esteja logado
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)
