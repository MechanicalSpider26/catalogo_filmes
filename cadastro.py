import sqlite3
import os

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
            estudio       TEXT    NOT NULL
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

def cadastrar_filme(titulo, ano, genero, diretor_id, nota, estudio):
    """Cadastra um filme no banco de dados."""
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (titulo, ano, genero, diretor_id, nota, estudio)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, ano, genero, diretor_id, nota, estudio))
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