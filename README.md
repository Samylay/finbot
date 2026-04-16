# FinBot

Agent conversationnel d'analyse financière basé sur LangChain (architecture tool-calling).

## Stack

- `gpt-4o` via `langchain-openai`
- `yfinance` pour les données boursières en temps réel
- `langchain-experimental` pour l'exécution de code Python (calculs)
- `langchain-tavily` pour la recherche web
- `SQLite` pour la base clients/produits

## Structure

```
projet_finbot/
├── agent.py          # Définition des outils et création de l'agent
├── main.py           # Point d'entrée interactif + scénarios de démo
├── init_db.py        # Initialisation de la base SQLite (à lancer une fois)
├── requirements.txt
├── .env
└── tools/
    ├── finance.py        # get_stock_price, get_stock_news, cours crypto
    ├── calculs.py        # TVA, intérêts composés, marges, mensualités, PythonREPL
    ├── database.py       # Recherche clients et produits (SQLite)
    ├── api_publique.py   # Conversion de devises (API Frankfurter)
    ├── recommendation.py # Recommandation produits, résumé texte, extraction mots-clés
    └── portefeuille.py   # Calcul de valeur de portefeuille multi-actifs
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine :

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...   # optionnel, active la recherche web
```

## Utilisation

```bash
# Initialiser la base de données (une seule fois)
python init_db.py

# Lancer l'agent
python main.py
```

Taper `menu` pour lancer les scénarios de démo, ou poser directement une question.

## Outils disponibles

| Outil | Description |
|---|---|
| `get_stock_price` | Cours, variation du jour et volume d'une action (yfinance) |
| `get_stock_news` | 5 dernières actualités d'une action (yfinance) |
| `cours_crypto` | Cours d'une crypto en USD (yfinance) |
| `calculer_portefeuille` | Valeur totale d'un portefeuille `AAPL:10\|MSFT:5` |
| `python_repl` | Exécution de code Python pour les calculs |
| `calculer_tva` | Prix HT → TVA + TTC |
| `calculer_interets` | Intérêts composés |
| `calculer_marge` | Marge commerciale |
| `calculer_mensualite` | Mensualité de prêt |
| `convertir_devise` | Conversion de devises en temps réel |
| `rechercher_client` | Lookup client par nom ou ID |
| `rechercher_produit` | Lookup produit par nom ou ID |
| `recommander_produits` | Recommandation par budget, catégorie et type de compte |
| `recherche_web` | Recherche web via Tavily |

## Scénarios de test

```
1. Donne-moi un résumé en 5 lignes sur l'état financier de l'action Apple.
2. Compare les actions Apple et Microsoft.
3. Si j'investis 5000€ sur Apple et que l'action augmente de 8%, combien aurai-je ?
4. Analyse l'action Tesla et dis-moi si un investissement de 3000€ avec une croissance de 5% serait intéressant.
```
