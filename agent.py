# agent.py
import os

from langchain_classic.tools import Tool
from tools.database       import rechercher_client, rechercher_produit
from tools.finance        import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs        import calculer_tva, calculer_interets_composes, calculer_marge, calculer_mensualite_pret
from tools.api_publique   import convertir_devise
from tools.recommendation import resumer_texte, formater_rapport, extraire_mots_cles, recommander_produits
from tools.portefeuille   import calculer_portefeuille

# ── B2 : PythonREPLTool ───────────────────────────────────────────────────────
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
python_repl.description = (
    'Exécute du code Python pour des calculs complexes ou traitements '
    'de données non couverts par les autres outils. '
    'Entrée : code Python valide sous forme de chaîne.'
)
# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.

# ── A3 : Recherche web (TavilySearch) ────────────────────────────────────────
from langchain_community.tools.tavily_search import TavilySearchResults

tavily = TavilySearchResults(max_results=3)


tools = [
    # ── Outil 1 : Base de données (A1) ───────────────────────────────────────
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),

    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),

    # ── Outil 2 : Données financières (A2) ───────────────────────────────────
    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier réel d\'une action via yfinance. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),

    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours réel d\'une crypto via yfinance. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),

    # ── Outil B1 : Portefeuille boursier ─────────────────────────────────────
    Tool(name='calculer_portefeuille', func=calculer_portefeuille,
         description='Calcule la valeur totale d\'un portefeuille d\'actions avec cours réels. '
                     'Entrée : "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE" ex "AAPL:10|MSFT:5|TSLA:3".'),

    # ── Outil 3 : Calculs financiers ─────────────────────────────────────────
    Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'),

    Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'),

    Tool(name='calculer_marge', func=calculer_marge,
         description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'),

    Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'),

    # ── Outil 4 : API publique ────────────────────────────────────────────────
    Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'),

    # ── Outil 5 : Transformation de texte ────────────────────────────────────
    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),

    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),

    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),

    # ── Outil 6 : Recommandation produits ────────────────────────────────────
    Tool(name='recommander_produits', func=recommander_produits,
         description='Recommande des produits selon budget, catégorie et type de compte. '
                     'Entrée : "budget,categorie,type_compte" ex "300,Informatique,Premium".'),

    # ── Outil 7 : Recherche web (A3) ─────────────────────────────────────────
    Tool(name='recherche_web', func=tavily.run,
         description='Recherche web en temps réel : actualités financières, informations '
                     'sur une entreprise, résultats trimestriels, cours récents. '
                     'Entrée : question en langage naturel.'),

    # ── Outil B2 : Python REPL ───────────────────────────────────────────────
    python_repl,
]

from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_classic import hub


def creer_agent():
    """Crée et retourne un agent LangChain ReAct configuré."""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    return agent_executor
