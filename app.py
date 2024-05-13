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
        return render_template("login.html")

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
    # session.pop("password", None) - limpa um item especifico

if __name__ == "__main__":
    app.run(debug=True)