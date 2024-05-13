from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "sua_chave_secreta_aqui"  # Defina sua chave secreta aqui

"""
# Rota de login com requisições POST e GET.
# Armazena os valores de input_email e input_password na sessão ao receber uma requisição POST.
# Redireciona o usuário para a rota /user após receber uma requisição POST.
# Renderiza o template login.html ao receber uma requisição GET.
"""
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["input_email"]
        password = request.form["input_password"]
        session["email"] = email
        session["password"] = password
        return redirect(url_for("user"))
    else:
        return render_template("login.html")


"""
# Rota para exibir a sessão de usuário.
# Verifica se as chaves "email" e "password" estão presentes na sessão.
# Se sim, recupera os valores e retorna uma string HTML com os detalhes do usuário.
# Caso contrário, redireciona o usuário para a rota de login.
"""
@app.route("/user")
def user():
    if "email" in session and "password" in session:
        email = session["email"]
        password = session["password"]
        return f"<h1>Session log</h1><p>User: {email}</p> <p>Password: {password}</p>"
    else:
        return redirect(url_for("login"))

"""
# Rota para fazer logout.
# Limpa todos os dados da sessão.
# Redireciona o usuário de volta para a rota de login.
# A linha comentada session.pop("password", None) poderia ser usada para limpar um item específico da sessão, como a senha.
"""
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
    # session.pop("password", None)

"""
# Verifica se o módulo está sendo executado diretamente (não importado como um módulo).
# Se sim, inicia o servidor Flask com o modo de depuração ativado.
"""
if __name__ == "__main__":
    app.run(debug=True)