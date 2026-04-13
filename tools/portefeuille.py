# tools/portefeuille.py – B1 : Calcul de portefeuille boursier via yfinance

import yfinance as yf

# Mapping des symboles locaux vers les tickers Yahoo Finance
TICKER_MAP = {
    "LVMH": "MC.PA",
    "AIR":  "AIR.PA",
}


def calculer_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur totale d'un portefeuille d'actions.
    Entrée : "SYMBOLE:QUANTITE|SYMBOLE:QUANTITE"
    Exemple : "AAPL:10|MSFT:5|TSLA:3"
    Retourne la valeur de chaque ligne, la valeur totale et la variation globale du jour.
    """
    lignes_input = [l.strip() for l in input_str.strip().split('|') if l.strip()]

    resultats = []
    valeur_totale = 0.0
    variation_ponderee = 0.0

    for ligne in lignes_input:
        if ':' not in ligne:
            resultats.append(f"  Format invalide : '{ligne}' (attendu SYMBOLE:QUANTITE)")
            continue

        symbole, quantite_str = ligne.split(':', 1)
        symbole = symbole.strip().upper()

        try:
            quantite = float(quantite_str.strip())
        except ValueError:
            resultats.append(f"  {symbole}: quantité invalide '{quantite_str}'")
            continue

        ticker_symbol = TICKER_MAP.get(symbole, symbole)

        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="2d")

            if hist.empty:
                resultats.append(f"  {symbole}: données indisponibles")
                continue

            cours = hist['Close'].iloc[-1]
            valeur_ligne = cours * quantite

            if len(hist) >= 2:
                cours_veille = hist['Close'].iloc[-2]
                variation_pct = ((cours - cours_veille) / cours_veille) * 100
            else:
                variation_pct = 0.0

            tendance = '📈' if variation_pct >= 0 else '📉'
            resultats.append(
                f"  {symbole} {tendance} : {cours:.2f} $ × {quantite:.0f} = {valeur_ligne:.2f} $ ({variation_pct:+.2f}%)"
            )
            valeur_totale += valeur_ligne
            variation_ponderee += variation_pct * valeur_ligne

        except Exception as e:
            resultats.append(f"  {symbole}: erreur — {e}")

    if not resultats:
        return "Aucune ligne de portefeuille valide."

    variation_globale = (variation_ponderee / valeur_totale) if valeur_totale > 0 else 0.0
    tendance_globale = '📈' if variation_globale >= 0 else '📉'

    output = "=== PORTEFEUILLE ===\n"
    output += '\n'.join(resultats)
    output += f"\n{'─' * 45}\n"
    output += f"Valeur totale : {valeur_totale:,.2f} $ {tendance_globale} ({variation_globale:+.2f}%)"
    return output
