from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from utils.validations import validate_email, validate_cpf

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Defina sua chave secreta aqui

app.permanent_session_lifetime = timedelta(minutes=5)

# SQL ALCHEMY CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bibliomania'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    cpf = db.Column("cpf", db.String(12))
    password = db.Column("password", db.String(100))
    user_type = db.Column("user_type", db.String(100))
    phonenumber = db.Column("phonenumber", db.String(100))

    def __init__(self, name, email, cpf, password, default_role, phonenumber):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
        self.user_type = default_role
        self.phonenumber = phonenumber

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
        nome = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]

        if not nome or not cpf or not email or not password or not phonenumber:
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("signup"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("signup"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("signup"))

        found_user_email = User.query.filter_by(email=email).first()
        found_user_cpf = User.query.filter_by(cpf=cpf).first()

        if found_user_email or found_user_cpf:
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        else:
            new_user = User(nome, email, cpf, password, "user", phonenumber)
            db.session.add(new_user)
            db.session.commit()
            session["email"] = email
            session["password"] = password
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))

    # Se o usuário já estiver logado
    else:
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
