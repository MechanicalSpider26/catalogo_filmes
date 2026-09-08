import sqlite3
import os
from flask import request

def conectar_banco():
    """Conecta ao banco SQLite e cria a tabela se nao existir."""
    os.makedirs('dados', exist_ok=True)
    conn = sqlite3.connect('dados/cinema.db')
    conn.row_factory = sqlite3.Row   

    conn.execute('PRAGMA foreign_keys = ON;')


    conn.execute('''
        CREATE TABLE IF NOT EXISTS diretores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nacionalidade TEXT NOT NULL,
            data_nascimento TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS filmes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo        TEXT    NOT NULL,
            ano           INTEGER NOT NULL,
            genero        TEXT    NOT NULL,
            diretor_id    INTEGER NOT NULL REFERENCES diretores(id),
            nota          REAL    NOT NULL,
            estudio       TEXT    NOT NULL,
            imagem_url    TEXT,
            sinopse       TEXT
        )
    ''')
    conn.commit()
    return conn

def cadastrar_diretor(nome, nacionalidade, data_nascimento):
    """Cadastra um novo diretor no banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diretores (nome, nacionalidade, data_nascimento)
        VALUES (?, ?, ?)
    ''', (nome, nacionalidade, data_nascimento))
    conn.commit()
    conn.close()

def listar_diretores():
    """Retorna uma lista de todos os diretores cadastrados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diretores ORDER BY nome')
    diretores = cursor.fetchall()
    conn.close()
    return diretores

def cadastrar_filme(titulo, ano, genero, diretor_id, nota, estudio, imagem_url):
    """Cadastra um filme no banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (titulo, ano, genero, diretor_id, nota, estudio, imagem_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, ano, genero, diretor_id, nota, estudio, imagem_url))
    conn.commit()
    conn.close()

def listar_filmes():
    """Retorna uma lista com todos os filmes cadastrados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT filmes.*, diretores.nome AS diretor_nome
        FROM filmes
        JOIN diretores ON filmes.diretor_id = diretores.id
        ORDER BY filmes.titulo
    ''')
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def obter_ou_criar_diretor(nome_diretor):
    """Busca o id do diretor pelo nome. Se não existir, cadastra um novo."""
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Busca insensível a maiúsculas/minúsculas
    cursor.execute("SELECT id FROM diretores WHERE LOWER(nome) = LOWER(?)", (nome_diretor.strip(),))
    resultado = cursor.fetchone()
    
    if resultado:
        diretor_id = resultado['id'] # Ou resultado[0] dependendo do row_factory
    else:
        cursor.execute('''
            INSERT INTO diretores (nome, nacionalidade, data_nascimento)
            VALUES (?, 'Não informada', 'Não informada')
        ''', (nome_diretor.strip(),))
        conn.commit()
        diretor_id = cursor.lastrowid
        
    conn.close()
    return diretor_id

def obter_filme_por_id(id_filme):
    """Busca o filme e os dados do seu diretor pelo ID."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            filmes.*, 
            diretores.nome AS diretor_nome, 
            diretores.nacionalidade AS diretor_nacionalidade, 
            diretores.data_nascimento AS diretor_nascimento
        FROM filmes
        JOIN diretores ON filmes.diretor_id = diretores.id
        WHERE filmes.id = ?
    ''', (id_filme,))
    filme = cursor.fetchone()
    conn.close()
    return filme

def buscar_filmes(termo):
    """Busca filmes pelo título, gênero ou nome do diretor."""
    conn = conectar_banco()
    
    # Prepara o termo para buscar qualquer trecho da palavra
    padrao = f'%{termo}%'
    
    filmes = conn.execute('''
        SELECT 
            filmes.*, 
            diretores.nome AS diretor_nome
        FROM filmes
        JOIN diretores ON filmes.diretor_id = diretores.id
        WHERE 
            LOWER(filmes.titulo) LIKE ? 
            OR LOWER(filmes.genero) LIKE ? 
            OR LOWER(diretores.nome) LIKE ?
        ORDER BY filmes.titulo
    ''', (padrao, padrao, padrao)).fetchall()
    
    conn.close()
    return filmes

def atualizar_filme(id_filme, titulo, ano, genero, diretor_id, nota, estudio, imagem_url):
    """Atualiza um filme existente pelo ID."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE filmes
        SET titulo = ?, ano = ?, genero = ?, diretor_id = ?, nota = ?, estudio = ?, imagem_url = ?
        WHERE id = ?
    ''', (titulo, ano, genero, diretor_id, nota, estudio, imagem_url, id_filme))
    conn.commit()
    conn.close()

def excluir_filme(id_filme):
    """Remove um filme do banco de dados pelo ID."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM filmes WHERE id = ?', (id_filme,))
    conn.commit()
    conn.close()

def obter_diretor_por_id(id_diretor):
    """Busca os dados do diretor pelo ID."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diretores WHERE id = ?', (id_diretor,))
    diretor = cursor.fetchone()
    conn.close()
    return diretor

def listar_filmes_por_diretor(id_diretor):
    """Busca todos os filmes dirigidos por um diretor específico."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filmes WHERE diretor_id = ? ORDER BY titulo', (id_diretor,))
    filmes = cursor.fetchall()
    conn.close()
    return filmes

def listar_diretores_com_contagem():
    """Retorna todos os diretores com a contagem de filmes associados."""
    conn = conectar_banco()
    diretores = conn.execute('''
        SELECT d.id, d.nome, d.nacionalidade, d.data_nascimento, COUNT(f.id) as total_filmes 
        FROM diretores d 
        LEFT JOIN filmes f ON d.id = f.diretor_id 
        GROUP BY d.id, d.nome, d.nacionalidade, d.data_nascimento
        ORDER BY d.nome ASC
    ''').fetchall()
    conn.close()
    return diretores


def obter_diretor_por_id(id_diretor):
    """Busca um único diretor pelo ID."""
    conn = conectar_banco()
    diretor = conn.execute("SELECT * FROM diretores WHERE id = ?", (id_diretor,)).fetchone()
    conn.close()
    return diretor

def atualizar_diretor(id_diretor, nome, nacionalidade, data_nascimento):
    """Atualiza todos os dados do diretor no banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE diretores 
        SET nome = ?, nacionalidade = ?, data_nascimento = ?
        WHERE id = ?
    ''', (nome, nacionalidade, data_nascimento, id_diretor))
    conn.commit()
    conn.close()


def excluir_diretor(id_diretor):
    """Desvincula o diretor dos filmes e o remove do banco."""
    conn = conectar_banco()
    conn.execute("UPDATE filmes SET diretor_id = NULL WHERE diretor_id = ?", (id_diretor,))
    conn.execute("DELETE FROM diretores WHERE id = ?", (id_diretor,))
    conn.commit()
    conn.close()

def atualizar_sinopse(id_filme, nova_sinopse):
    """Atualiza a sinopse do filme no banco de dados"""
    conn = conectar_banco()
    conn.execute(
        "UPDATE filmes SET sinopse = ? WHERE id = ?", (nova_sinopse, id_filme))
    conn.commit()
    conn.close()