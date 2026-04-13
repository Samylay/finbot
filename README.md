# FinBot — Agent d'analyse financière

Agent conversationnel LangChain capable d'analyser des actions boursières, de faire des calculs financiers et de formuler des recommandations d'investissement.

## Structure du projet

```
projet_finbot/
├── main.py               # Point d'entrée : agent + tests
├── requirements.txt      # Dépendances Python
├── .env                  # Clé API (ne pas committer)
└── tools/
    ├── __init__.py
    ├── finance.py        # get_stock_price, get_stock_news (yfinance)
    ├── calculs.py        # PythonREPLTool pour les calculs
    ├── api_publique.py   # APIs externes (Tavily, Wikipedia…)
    ├── recommendation.py # Logique de recommandation
    └── database.py       # Historique / persistance
```

## Installation

```bash
# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## Configuration

Renseigner la clé OpenAI dans le fichier `.env` :

```
OPENAI_API_KEY=sk-...
```

## Utilisation

```bash
source venv/bin/activate
python main.py
```

## Outils de l'agent

| Outil | Fichier | Description |
|-------|---------|-------------|
| `get_stock_price` | `tools/finance.py` | Prix, secteur, variation 52 semaines |
| `get_stock_news` | `tools/finance.py` | 5 dernières actualités d'une action |
| `python_tool` | `tools/calculs.py` | Calculs mathématiques via REPL Python |

## Tests attendus

1. **Résumé financier** — état financier de l'action Apple en 5 lignes
2. **Comparaison** — Apple vs Microsoft
3. **Projection** — 5000€ sur Apple avec +8% (doit utiliser `python_tool`)
4. **Analyse complète** — Tesla avec croissance estimée de 5%
