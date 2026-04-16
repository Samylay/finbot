# agent.py
import os

from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from tools.api_publique   import convertir_devise
from tools.calculs        import (
    calculer_tva,
    calculer_interets_composes,
    calculer_marge,
    calculer_mensualite_pret,
    python_repl_tool,
)
from tools.database       import rechercher_client, rechercher_produit
from tools.finance        import obtenir_cours_action, obtenir_cours_crypto, get_stock_news
from tools.portefeuille   import calculer_portefeuille
from tools.recommendation import resumer_texte, formater_rapport, extraire_mots_cles, recommander_produits


def _make_tavily_tool():
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return lambda q: "Recherche web indisponible : TAVILY_API_KEY manquante."
    return TavilySearchResults(max_results=3).run


tools = [
    # ── Outil 1 : Base de données (A1) ───────────────────────────────────────
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),

    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),

    # ── Outil 2 : Données financières (A2) ───────────────────────────────────
    Tool(name='get_stock_price', func=obtenir_cours_action,
         description='Cours boursier réel d\'une action via yfinance. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),

    Tool(name='get_stock_news', func=get_stock_news,
         description='5 dernières actualités d\'une action via yfinance. '
                     'Entrée : symbole majuscule ex AAPL, TSLA.'),

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
    Tool(name='recherche_web', func=_make_tavily_tool(),
         description='Recherche web en temps réel : actualités financières, informations '
                     'sur une entreprise, résultats trimestriels, cours récents. '
                     'Entrée : question en langage naturel.'),

]

if python_repl_tool is not None:
    tools.append(python_repl_tool)


def creer_agent():
    if not os.getenv('OPENAI_API_KEY'):
        raise RuntimeError("OPENAI_API_KEY manquante.")

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es un assistant analyste financier.\n"
         "- Pour le cours ou les infos d'une action, utilise get_stock_price.\n"
         "- Pour les actualités d'une action, utilise get_stock_news.\n"
         "- Pour TOUT calcul mathématique, utilise TOUJOURS Python_REPL avec print().\n"
         "- Ne calcule jamais de tête."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )
