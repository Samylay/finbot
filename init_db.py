# init_db.py – A1 : Initialisation de la base de données SQLite
# Exécuter une fois : python init_db.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id              TEXT PRIMARY KEY,
            nom             TEXT NOT NULL,
            email           TEXT,
            ville           TEXT,
            solde_compte    REAL,
            type_compte     TEXT,
            date_inscription TEXT,
            achats_total    REAL
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS produits (
            id       TEXT PRIMARY KEY,
            nom      TEXT NOT NULL,
            prix_ht  REAL,
            stock    INTEGER
        )
    ''')

    clients = [
        ('C001', 'Marie Dupont',   'marie.dupont@email.fr', 'Paris', 15420.50, 'Premium',  '2021-03-15', 8750.00),
        ('C002', 'Jean Martin',    None,                    None,     3200.00,  'Standard', None,         None),
        ('C003', 'Sophie Bernard', None,                    None,    28900.00,  'VIP',      None,         None),
        ('C004', 'Lucas Petit',    None,                    None,      750.00,  'Standard', None,         None),
    ]

    produits = [
        ('P001', 'Ordinateur portable Pro', 899.00, 45),
        ('P002', 'Souris ergonomique',       49.90, 120),
        ('P003', 'Bureau réglable',         350.00,  18),
        ('P004', 'Casque audio sans fil',   129.00,  67),
        ('P005', 'Écran 27 pouces 4K',      549.00,  30),
    ]

    cur.executemany('INSERT OR IGNORE INTO clients VALUES (?,?,?,?,?,?,?,?)', clients)
    cur.executemany('INSERT OR IGNORE INTO produits VALUES (?,?,?,?)', produits)

    conn.commit()
    conn.close()
    print(f"✓ Base de données initialisée : {DB_PATH}")
    print(f"  {len(clients)} clients | {len(produits)} produits")


if __name__ == '__main__':
    init_db()
