
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from cadastro import (cadastrar_diretor, listar_diretores,
    cadastrar_filme, listar_filmes, obter_ou_criar_diretor, obter_filme_por_id, buscar_filmes, atualizar_filme, 
    excluir_filme, obter_diretor_por_id, listar_filmes_por_diretor)

from validacoes import validar_diretor, validar_filme

app = Flask(__name__)

# Listagem

@app.route("/")
def listar():
    """Pagina inicial"""
    termo = request.args.get("termo", "").strip().lower()
    msg = request.args.get("msg","")

    if termo:
        filmes = buscar_filmes(termo)
    else:
        filmes = listar_filmes()

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
        diretor_nome=request.form.get("diretor_nome")
        nota=request.form.get("nota")
        estudio=request.form.get("estudio")
        imagem_url = request.form.get("imagem_url", "").strip()

        diretor_id = obter_ou_criar_diretor(diretor_nome) if diretor_nome else None

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

# Detalhe

@app.route("/filme/<int:id_filme>")
def detalhe_filme(id_filme):
    """Pagina de detalhes do filme e diretor"""
    filme = obter_filme_por_id(id_filme)

    if filme is None:
        return render_template("erro.html", mensagem=f"filme com ID {id_filme} não encontrado"), 404
    
    return render_template("detalhe.html", filme=filme)

@app.route("/diretor/<int:id_diretor>")
def detalhe_diretor(id_diretor):
    """Exibe o perfil do diretor e a lista de filmes dirigidos por ele."""
    diretor = obter_diretor_por_id(id_diretor)

    if diretor is None:
        return render_template("erro.html", mensagem=f"Diretor com ID {id_diretor} não encontrado."), 404

    filmes = listar_filmes_por_diretor(id_diretor)
    return render_template("detalhe_diretor.html", diretor=diretor, filmes=filmes)

# Buscar

@app.route("/buscar")
def buscar_filme():
    """Busca por nome. O termo vem na URL"""
    termo = request.args.get("termo", "").strip().lower()

    encontrados = []
    if termo:
        encontrados = buscar_filme(termo)

    return render_template("busca.html",termo=termo)

# Editar

@app.route("/filme/<int:id_filme>/editar", methods=["GET","POST"])
def editar_filme(id_filme):
    """GET exibe os dados preenchidos; POST aplica as correções."""
    filme = obter_filme_por_id(id_filme)

    if filme is None:
        return render_template("erro.html", mensagem=f"Filme com ID {id_filme} não foi encontrado"), 404

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        ano = request.form.get("ano", "").strip()
        genero = request.form.get("genero", "").strip()
        diretor_nome = request.form.get("diretor_nome", "").strip()
        nota = request.form.get("nota", "").strip()
        estudio = request.form.get("estudio", "").strip()
        imagem_url = request.form.get("imagem_url", "").strip()

        # Reutiliza a função de pegar/criar diretor caso o nome tenha mudado
        diretor_id = obter_ou_criar_diretor(diretor_nome) if diretor_nome else None

        valido, erro = validar_filme(titulo, ano, genero, diretor_id, nota, estudio)

        if not valido:
            return render_template(
                "form_filme.html",
                diretores=listar_diretores(),
                erro=erro,
                titulo=titulo,
                ano=ano,
                genero=genero,
                diretor_nome=diretor_nome,
                nota=nota,
                estudio=estudio,
                edicao=True,
                id_filme=id_filme
            )

        atualizar_filme(id_filme, titulo, ano, genero, diretor_id, nota, estudio)
        return redirect(url_for("listar", msg="Filme atualizado com sucesso!"))

    # No GET, passa os valores vindos do banco para popular os inputs
    return render_template(
        "form_filme.html",
        diretores=listar_diretores(),
        titulo=filme["titulo"],
        ano=filme["ano"],
        genero=filme["genero"],
        diretor_nome=filme["diretor_nome"],
        nota=filme["nota"],
        estudio=filme["estudio"],
        edicao=True,
        id_filme=id_filme
    )

# Excluir

@app.route("/filme/<int:id_filme>/excluir", methods=["POST"])
def excluir(id_filme):
    """Exclui o filme do banco de dados. Aceita SOMENTE requisições POST."""
    filme = obter_filme_por_id(id_filme)

    if filme is None:
        return render_template("erro.html", mensagem=f"Filme com ID {id_filme} não encontrado."), 404

    excluir_filme(id_filme)
    return redirect(url_for("listar", msg=f"Filme '{filme['titulo']}' excluído com sucesso!"))

if __name__ == "__main__":
    app.run(debug=True)