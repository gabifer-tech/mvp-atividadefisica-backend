import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "atividades.db"

TIPOS_ATIVIDADE = ["Corrida", "Caminhada", "Ciclismo", "Musculação", "Natação", "Surf", "Outro"]
INTENSIDADES = ["Baixa", "Média", "Alta"]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            data DATE NOT NULL,
            duracao INTEGER NOT NULL,
            distancia REAL,
            intensidade TEXT NOT NULL,
            observacoes TEXT
        )
        """
    )
    conn.commit()
    conn.close()
