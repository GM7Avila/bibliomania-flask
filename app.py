from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Defina sua chave secreta aqui

app.permanent_session_lifetime = timedelta(minutes=5)

# SQL ALCHEMY COINFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bibliomania'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    cpf = db.Column("cpf", db.String(12))
    password = db.Column("password", db.String(100))
    user_type = db.Column("user_type", db.String(100))

    def __init__(self, name, email, cpf, password):
        default_role = "leitor"

        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
        self.user_type = default_role

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]
        session["email"] = email
        session["password"] = password
        return redirect(url_for("user"))
    else:
        if "email" in session and "password" in session:
            return redirect(url_for("user"))

        return render_template("sign-in-template.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        # Recuperando os dados do formulário
        nome = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        telefone = request.form["input_telefone"]
        # Salvar os dados no banco de dados ou em outro local adequado

        # Redirecionar para a página do usuário após o cadastro
        return redirect(url_for("user"))
    else:
        # Verificar se o usuário já está logado
        if "email" in session and "password" in session:
            return redirect(url_for("user"))

        # Se não estiver logado, renderizar o template de cadastro
        return render_template("sign-up-template.html")

@app.route("/user")
def user():
    if "email" in session and "password" in session:
        email = session["email"]
        password = session["password"]
        return f"<h1>Session log</h1><p>User: {email}</p> <p>Password: {password}</p>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
