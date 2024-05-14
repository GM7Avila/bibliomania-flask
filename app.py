from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Defina sua chave secreta aqui

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

if __name__ == "__main__":
    app.run(debug=True)
