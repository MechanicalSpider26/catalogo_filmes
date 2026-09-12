# dados_iniciais.py
import os
import sqlite3

def inicializar_banco():
    caminho_db = os.path.join('dados', 'cinema.db')
    
    if os.path.exists(caminho_db):
        os.remove(caminho_db)
        print("Banco de dados antigo removido.")

    os.makedirs('dados', exist_ok=True)
    conn = sqlite3.connect(caminho_db)
    conn.execute('PRAGMA foreign_keys = ON;')

    conn.execute('''
        CREATE TABLE diretores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            nacionalidade TEXT NOT NULL,
            data_nascimento TEXT NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE filmes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo        TEXT    NOT NULL UNIQUE,
            ano           INTEGER NOT NULL,
            genero        TEXT    NOT NULL,
            diretor_id    INTEGER NOT NULL REFERENCES diretores(id) ON DELETE CASCADE,
            nota          REAL    NOT NULL,
            estudio       TEXT    NOT NULL,
            imagem_url    TEXT,
            sinopse       TEXT
        )
    ''')

    # Inserção de Diretores (4 diretores)
    diretores = [
        ("Christopher Nolan", "Britânico", "1970-07-30"),
        ("Quentin Tarantino", "Norte-Americano", "1963-03-27"),
        ("Greta Gerwig", "Norte-Americana", "1983-08-04"),
        ("Guillermo del Toro", "Mexicano", "1964-10-09") # Diretor sem filmes cadastrados
    ]

    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO diretores (nome, nacionalidade, data_nascimento)
        VALUES (?, ?, ?)
    ''', diretores)

    # Inserção de Filmes (4 filmes)
    filmes = [
        ("Oppenheimer", 2023, "Biografia", 1, 8.9, "Universal Pictures", "https://via.placeholder.com/300x450", "História do físico J. Robert Oppenheimer."),
        ("Inception", 2010, "Ficção Científica", 1, 8.8, "Warner Bros.", "https://via.placeholder.com/300x450", "Um ladrão que rouba segredos corporativos através de sonhos."),
        ("Pulp Fiction", 1994, "Crime", 2, 8.9, "Miramax", "https://via.placeholder.com/300x450", "As vidas de dois assassinos da máfia se cruzam."),
        ("Barbie", 2023, "Comédia/Fantasia", 3, 7.0, "Warner Bros.", "https://via.placeholder.com/300x450", "Barbie e Ken deixam Barbieland rumo ao mundo real.")
    ]

    cursor.executemany('''
        INSERT INTO filmes (titulo, ano, genero, diretor_id, nota, estudio, imagem_url, sinopse)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', filmes)

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso com dados iniciais!")

if __name__ == "__main__":
    inicializar_banco()