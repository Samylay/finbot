from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_classic.agents import tool
from langchain_experimental.tools import PythonREPLTool

from tools.finance import obtenir_cours_action

load_dotenv()

# ── LLM ──────────────────────────────────────────────────────────────────────
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0
)

# ── Tools ─────────────────────────────────────────────────────────────────────
@tool
def get_stock_price(symbole: str) -> str:
    """
    Retourne le cours actuel simulé d'une action boursière.
    Exemples de symboles : AAPL, MSFT, TSLA, GOOGL, LVMH, AIR
    """
    return obtenir_cours_action(symbole)

python_tool = PythonREPLTool()

tools = [get_stock_price, python_tool]

# ── Prompt ────────────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Tu es un assistant analyste financier.\n"
     "- Pour récupérer le cours d'une action, utilise get_stock_price.\n"
     "- Pour TOUT calcul mathématique, utilise TOUJOURS python_tool avec print().\n"
     "- Ne calcule JAMAIS de tête."),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

# ── Agent ─────────────────────────────────────────────────────────────────────
agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Test 1 – Résumé financier
    print("\n=== Test 1 – Résumé financier ===")
    response = agent_executor.invoke({
        "input": "Donne-moi un résumé en 5 lignes sur l'état financier de l'action Apple."
    })
    print(response["output"])

    # Test 2 – Comparaison
    print("\n=== Test 2 – Comparaison ===")
    response = agent_executor.invoke({
        "input": "Compare les actions Apple et Microsoft."
    })
    print(response["output"])

    # Test 3 – Projection investissement (doit utiliser python_tool)
    print("\n=== Test 3 – Projection investissement ===")
    response = agent_executor.invoke({
        "input": "Si j'investis 5000€ sur Apple et que l'action augmente de 8%, combien aurai-je ?"
    })
    print(response["output"])

    # Test 4 – Analyse complète
    print("\n=== Test 4 – Analyse complète ===")
    response = agent_executor.invoke({
        "input": (
            "Analyse l'action Tesla et dis-moi si un investissement de 3000€ "
            "avec une croissance estimée de 5% serait intéressant."
        )
    })
    print(response["output"])
