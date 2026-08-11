import sqlite3
from contextlib import contextmanager

DB_PATH = "loja.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                link_pagamento TEXT,
                ativo INTEGER DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                produto_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pendente',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
        """)


def listar_produtos():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM produtos WHERE ativo = 1 ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


def buscar_produto(produto_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM produtos WHERE id = ? AND ativo = 1", (produto_id,)
        ).fetchone()
        return dict(row) if row else None


def adicionar_produto(nome, descricao, preco, link_pagamento):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO produtos (nome, descricao, preco, link_pagamento) VALUES (?, ?, ?, ?)",
            (nome, descricao, preco, link_pagamento),
        )
        return cur.lastrowid


def remover_produto(produto_id):
    with get_conn() as conn:
        conn.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (produto_id,))


def criar_pedido(chat_id, produto_id):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO pedidos (chat_id, produto_id) VALUES (?, ?)",
            (chat_id, produto_id),
        )
        return cur.lastrowid0
