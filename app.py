from flask import redirect, url_for, render_template, request, session, flash
from functools import wraps
from app.utils.validations import validate_email, validate_cpf
from app.models.User import User
from app import app, db
from scripts.populate_book_table import populate_book_table


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "email" in session:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    return redirect(url_for("user"))

@app.route("/login", methods=["POST", "GET"])
@already_logged_in
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        # limpando os dados da sessão antiga
        session.pop("email", None)
        session.pop("password", None)

        found_user = User.query.filter_by(email=email).first()
        if found_user and found_user.check_password(password):
            session["email"] = email
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("user"))
        else:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for("login"))

    return render_template("sign-in-template.html")


@app.route("/signup", methods=["POST", "GET"])
@already_logged_in
def signup():
    if request.method == "POST":
        nome = request.form["input_nome"]
        cpf = request.form["input_cpf"]
        email = request.form["input_email"]
        password = request.form["input_password"]
        phonenumber = request.form["input_telefone"]

        if not all([nome, cpf, email, password, phonenumber]):
            flash("Por favor, preencha todos os campos.", "error")
            return redirect(url_for("signup"))

        if not validate_email(email):
            flash("E-mail inválido.", "error")
            return redirect(url_for("signup"))

        if not validate_cpf(cpf):
            flash("CPF inválido.", "error")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first() or User.query.filter_by(cpf=cpf).first():
            flash("Email ou cpf já cadastrado!", "error")
            return redirect(url_for("signup"))

        try:
            new_user = User(nome, email, cpf, password, "user", phonenumber)
            db.session.add(new_user)
            db.session.commit()
            session["email"] = email
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Erro ao cadastrar o usuário.", "error")
            app.logger.error(f"Erro ao cadastrar usuário: {e}")
            return redirect(url_for("signup"))

    return render_template("sign-up-template.html")


@app.route("/user")
@login_required
def user():
    email = session["email"]
    return render_template("base.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))




"""
ROTAS BOOK
"""

"""
CONFIG
"""
with app.app_context():
    db.create_all()
    populate_book_table()

if __name__ == "__main__":
    app.run(debug=True)



