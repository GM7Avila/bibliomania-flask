from flask import redirect, url_for, render_template, request, session, flash
from app.utils.validations import validate_email, validate_cpf
from app.models.User import User
from app import app, db

"""
ROTAS DO USER
"""
# TODO:
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]

        # limpando os dados da sessão antiga
        session.pop("email", None)
        session.pop("password", None)

        found_user = User.query.filter_by(email=email).first()
        if found_user:
            if found_user.check_password(password):
                session["email"] = email
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("user"))
            else:
                flash("Email ou senha inválidos!", "error")
                return redirect(url_for("login"))
        else:
            flash("Email ou senha inválidos!", "error")
            return redirect(url_for("login"))


        return redirect(url_for("user"))
    else:
        if "email" in session:
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

        if not all([nome, cpf, email, password, phonenumber]):
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

    # TODO: tratar caso o usuário tenha session
    # Se o usuário já estiver logado
    else:
        if "email" in session:
            return redirect(url_for("user"))

        # Se não estiver logado, renderizar o template de cadastro
        return render_template("sign-up-template.html")

# TODO:
@app.route("/user")
def user():
    if "email" in session:
        email = session["email"]
        return f"<h1>Session log</h1><p>User: {email}</p>"
    else:
        return redirect(url_for("login"))

# TODO:
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

if __name__ == "__main__":
    app.run(debug=True)