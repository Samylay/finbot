# tools/database.py – A1 : Base de données SQLite

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')


def _connect():
    return sqlite3.connect(DB_PATH)


def rechercher_client(query: str) -> str:
    """Recherche un client par ID ou par nom (partiel)."""
    query = query.strip()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT nom, solde_compte, type_compte FROM clients WHERE id = ?",
            (query.upper(),)
        )
        row = cur.fetchone()
        if not row:
            cur.execute(
                "SELECT nom, solde_compte, type_compte FROM clients WHERE LOWER(nom) LIKE ?",
                (f"%{query.lower()}%",)
            )
            row = cur.fetchone()

    if row:
        return f"Client : {row[0]} | Solde : {row[1]:.2f} € | Type de compte : {row[2]}"
    return f"Aucun client trouvé pour : '{query}'"


def rechercher_produit(query: str) -> str:
    """Recherche un produit par ID ou par nom. Retourne prix HT, TVA, prix TTC, stock."""
    query = query.strip()
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT nom, prix_ht, stock FROM produits WHERE id = ?",
            (query.upper(),)
        )
        row = cur.fetchone()
        if not row:
            cur.execute(
                "SELECT nom, prix_ht, stock FROM produits WHERE LOWER(nom) LIKE ?",
                (f"%{query.lower()}%",)
            )
            row = cur.fetchone()

    if row:
        tva = row[1] * 0.20
        prix_ttc = row[1] + tva
        return (f"Produit : {row[0]} | Prix HT : {row[1]:.2f} € "
                f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {row[2]}")
    return f"Aucun produit trouvé pour : '{query}'"
