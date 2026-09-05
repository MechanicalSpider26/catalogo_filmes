
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from cadastro import (conectar_banco, cadastrar_diretor, listar_diretores,
    cadastrar_filme, listar_filmes)

from validacoes import validar_diretor, validar_filme

app = Flask(__name__)

# Listagem

@app.route("/")
def listar():
    """Pagina inicial"""
    filmes = listar_filmes()
    msg = request.args.get("msg","")
    return render_template("lista.html", filmes=filmes, msg=msg)


# Cadastro

@app.route("/cadastrar_diretor", methods=["GET", "POST"])
def cadastro_diretor():
    """Pagina de cadastro dos diretores"""
    if request.method == "POST":
        nome = request.form.get("nome")
        nacionalidade = request.form.get("nacionalidade")
        data_nascimento = request.form.get("data_nascimento")

        valido, erro = validar_diretor(nome, nacionalidade, data_nascimento)

        if not valido:
            return render_template(
                "form_diretor.html",
                erro=erro,
                nome=nome,
                nacionalidade=nacionalidade,
                data_nascimento=data_nascimento
            )

        cadastrar_diretor(nome,nacionalidade,data_nascimento)
        return redirect(url_for("listar", msg="Diretor cadastrado com sucesso!"))

    return render_template("form_diretor.html")
    

@app.route("/cadastrar_filme", methods=["GET","POST"])
def cadastro_filme():
    """Pagina de cadastro dos filmes"""
    if request.method == "POST":
        titulo=request.form.get("titulo")
        ano=request.form.get("ano")
        genero=request.form.get("genero")
        diretor_id=request.form.get("diretor_id")
        nota=request.form.get("nota")
        estudio=request.form.get("estudio")

        valido, erro = validar_filme(titulo, ano, genero, diretor_id, nota, estudio)

        if not valido:
            return render_template(
                "form_filme.html",
                erro=erro,
                titulo=titulo,
                ano=ano,
                genero=genero,
                diretor_id=diretor_id,
                nota=nota,
                estudio=estudio
            )

        cadastrar_filme(titulo, ano, genero, diretor_id, nota, estudio)
        return redirect(url_for("listar", msg="Filme cadastrado com sucesso"))

    diretores = listar_diretores()
    return render_template("form_filme.html", diretores=diretores)

if __name__ == "__main__":
    app.run(debug=True)