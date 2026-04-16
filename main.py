import os

from dotenv import load_dotenv

from agent import creer_agent
from init_db import init_db


DEMO_PROMPTS = [
    "Donne-moi un resume en 5 lignes sur l'etat financier de l'action Apple.",
    "Compare les actions Apple et Microsoft.",
    "Si j'investis 5000 EUR sur Apple et que l'action augmente de 8%, combien aurai-je ?",
    (
        "Analyse l'action Tesla et dis-moi si un investissement de 3000 EUR "
        "avec une croissance estimee de 5% serait interessant."
    ),
    "Calcule la valeur du portefeuille AAPL:10|MSFT:5|TSLA:3.",
]


def verifier_configuration() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY manquante. Ajoute-la dans l'environnement ou dans un fichier .env."
        )


def executer_demos(agent) -> None:
    for index, prompt in enumerate(DEMO_PROMPTS, start=1):
        print(f"\n=== Demo {index} ===")
        print(f"Question: {prompt}")
        reponse = agent.invoke({"input": prompt})
        print(f"Reponse: {reponse['output']}")


def boucle_interactive(agent) -> None:
    print("\n" + "="*60)
    print("        FINBOT — AGENT D'ANALYSE FINANCIÈRE")
    print("="*60)
    print("  Tapez votre question ou 'menu' pour les options.")
    print("  'quit' ou 'exit' pour quitter.")
    
    while True:
        prompt = input("\nFinBot > ").strip()
        
        if not prompt:
            continue
            
        if prompt.lower() in ("quit", "exit", "q"):
            print("\nAu revoir !")
            break
        elif prompt.lower() == "menu":
            print("\nOptions :")
            print("  1. Lancer les demos")
            print("  2. Poser une question libre")
            print("  q. Quitter")
            choix = input("Choix : ").strip().lower()
            if choix == "1":
                executer_demos(agent)
            elif choix == "q":
                break
        else:
            try:
                print("Analyse en cours...")
                reponse = agent.invoke({"input": prompt})
                print(f"\nReponse: {reponse['output']}")
            except Exception as e:
                print(f"\nErreur : {e}")


def main() -> None:
    load_dotenv()
    init_db()
    
    try:
        verifier_configuration()
        print("Initialisation de l'agent...")
        agent = creer_agent()
        print("Agent prêt.")
        boucle_interactive(agent)
    except Exception as e:
        print(f"\nErreur fatale : {e}")


if __name__ == "__main__":
    main()
