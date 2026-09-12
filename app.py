# app.py
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from banco import (
    cadastrar_diretor, listar_diretores, cadastrar_filme, listar_filmes, 
    obter_ou_criar_diretor, obter_filme_por_id, buscar_filmes, atualizar_filme, 
    excluir_filme, obter_diretor_por_id, listar_filmes_por_diretor, 
    listar_diretores_com_contagem, excluir_diretor, atualizar_diretor, atualizar_sinopse
)
from validacoes import validar_diretor, validar_filme

app = Flask(__name__)

# Listagem

@app.route("/")
def listar():
    """Página inicial com listagem de filmes."""
    termo = request.args.get("termo", "").strip().lower()
    msg = request.args.get("msg", "")

    if termo:
        filmes = buscar_filmes(termo)
    else:
        filmes = listar_filmes()

    return render_template("lista.html", filmes=filmes, msg=msg)

@app.route("/diretores")
def listar_diretores_pagina():
    msg = request.args.get("msg", "")
    diretores = listar_diretores_com_contagem()
    return render_template("diretores.html", diretores=diretores, msg=msg)


# Cadastro

@app.route("/cadastrar_diretor", methods=["GET", "POST"])
def cadastro_diretor():
    """Página de cadastro dos diretores."""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        nacionalidade = request.form.get("nacionalidade", "").strip()
        data_nascimento = request.form.get("data_nascimento", "").strip()

        valido, erro = validar_diretor(nome, nacionalidade, data_nascimento)

        if not valido:
            return render_template(
                "form_diretor.html",
                erro=erro,
                nome=nome,
                nacionalidade=nacionalidade,
                data_nascimento=data_nascimento
            )

        try:
            cadastrar_diretor(nome, nacionalidade, data_nascimento)
            return redirect(url_for("listar_diretores_pagina", msg="Diretor cadastrado com sucesso!"))
        except ValueError as e:
            # Captura a regra de validação disparada pelo banco de dados (Item 2.5)
            return render_template(
                "form_diretor.html",
                erro=str(e),
                nome=nome,
                nacionalidade=nacionalidade,
                data_nascimento=data_nascimento
            )

    return render_template("form_diretor.html")
    

@app.route("/cadastrar_filme", methods=["GET", "POST"])
@app.route("/novo", methods=["GET", "POST"])  # Alias para conformidade do item 2.2
def cadastro_filme():
    """Página de cadastro dos filmes."""
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        ano = request.form.get("ano", "").strip()
        genero = request.form.get("genero", "").strip()
        diretor_nome = request.form.get("diretor_nome", "").strip()
        nota = request.form.get("nota", "").strip()
        estudio = request.form.get("estudio", "").strip()
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
                diretor_nome=diretor_nome,
                nota=nota,
                estudio=estudio,
                imagem_url=imagem_url,
                diretores=listar_diretores()
            )

        try:
            cadastrar_filme(titulo, ano, genero, diretor_id, nota, estudio, imagem_url)
            return redirect(url_for("listar", msg="Filme cadastrado com sucesso!"))
        except ValueError as e:
            # Captura a regra de validação disparada pelo banco de dados (Item 2.5)
            return render_template(
                "form_filme.html",
                erro=str(e),
                titulo=titulo,
                ano=ano,
                genero=genero,
                diretor_nome=diretor_nome,
                nota=nota,
                estudio=estudio,
                imagem_url=imagem_url,
                diretores=listar_diretores()
            )

    diretores = listar_diretores()
    return render_template("form_filme.html", diretores=diretores)


# Detalhe

@app.route("/filme/<int:id_filme>")
def detalhe_filme(id_filme):
    """Página de detalhes do filme e diretor."""
    filme = obter_filme_por_id(id_filme)

    if filme is None:
        return render_template("erro.html", mensagem=f"Filme com ID {id_filme} não encontrado"), 404
    
    return render_template("detalhe.html", filme=filme)

@app.route("/diretores/<int:id_diretor>")
def detalhe_diretor(id_diretor):
    """Exibe o perfil do diretor e a lista de filmes dirigidos por ele."""
    diretor = obter_diretor_por_id(id_diretor)

    if diretor is None:
        return render_template("erro.html", mensagem=f"Diretor com ID {id_diretor} não encontrado."), 404

    filmes = listar_filmes_por_diretor(id_diretor)
    return render_template("detalhe_diretor.html", diretor=diretor, filmes=filmes)


# Buscar (Corrigido)

@app.route("/buscar")
def buscar_filme_rota():
    """Busca por nome. O termo vem na URL."""
    termo = request.args.get("termo", "").strip().lower()

    encontrados = []
    if termo:
        encontrados = buscar_filmes(termo)

    return render_template("busca.html", filmes=encontrados, termo=termo)


# Editar

@app.route("/filme/<int:id_filme>/editar", methods=["GET", "POST"])
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
                imagem_url=imagem_url,
                edicao=True,
                id_filme=id_filme
            )

        atualizar_filme(id_filme, titulo, ano, genero, diretor_id, nota, estudio, imagem_url)
        return redirect(url_for("listar", msg="Filme atualizado com sucesso!"))

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
        imagem_url=filme["imagem_url"],
        id_filme=id_filme
    )

@app.route("/diretores/<int:id_diretor>/editar", methods=["GET", "POST"])
def editar_diretor(id_diretor):
    diretor = obter_diretor_por_id(id_diretor)
    if diretor is None:
        return render_template("erro.html", mensagem=f"Diretor com ID {id_diretor} não foi encontrado"), 404

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        nacionalidade = request.form.get("nacionalidade", "").strip()
        data_nascimento = request.form.get("data_nascimento", "").strip()

        valido, erro = validar_diretor(nome, nacionalidade, data_nascimento)

        if not valido:
            return render_template(
                "form_diretor.html",
                erro=erro,
                nome=nome,
                nacionalidade=nacionalidade,
                data_nascimento=data_nascimento,
                edicao=True,
                id_diretor=id_diretor
            )

        atualizar_diretor(id_diretor, nome, nacionalidade, data_nascimento)
        return redirect(url_for("listar_diretores_pagina", msg="Diretor atualizado com sucesso!"))

    return render_template(
        "form_diretor.html",
        nome=diretor["nome"],
        nacionalidade=diretor["nacionalidade"],
        data_nascimento=diretor["data_nascimento"],
        edicao=True,
        id_diretor=id_diretor
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

@app.route("/diretores/<int:id_diretor>/deletar", methods=["POST"])
def deletar_diretor(id_diretor):
    excluir_diretor(id_diretor)
    return redirect(url_for("listar_diretores_pagina", msg="Diretor excluído com sucesso!"))

@app.route('/filme/<int:id_filme>/sinopse', methods=['POST'])
def salvar_sinopse(id_filme):
    nova_sinopse = request.form.get('sinopse')
    atualizar_sinopse(id_filme, nova_sinopse)
    return redirect(url_for('detalhe_filme', id_filme=id_filme))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('erro.html', mensagem="Página não encontrada (404)."), 404

if __name__ == "__main__":
    app.run(debug=True)