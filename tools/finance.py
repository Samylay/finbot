# tools/finance.py – A2 : Cours boursiers réels via yfinance

import yfinance as yf

# Mapping des symboles locaux vers les tickers Yahoo Finance
TICKER_MAP = {
    "LVMH": "MC.PA",
    "AIR":  "AIR.PA",
}

# Mapping crypto : symbole → paire USD sur Yahoo Finance
def _ticker_crypto(symbole: str) -> str:
    return f"{symbole}-USD"


def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours réel d'une action (prix, variation du jour, volume)."""
    symbole = symbole.strip().upper()
    ticker_symbol = TICKER_MAP.get(symbole, symbole)
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="2d")
        if hist.empty:
            return f"Action '{symbole}' introuvable ou données indisponibles."

        cours = hist['Close'].iloc[-1]
        volume = int(hist['Volume'].iloc[-1])

        if len(hist) >= 2:
            cours_veille = hist['Close'].iloc[-2]
            variation_pct = ((cours - cours_veille) / cours_veille) * 100
        else:
            variation_pct = 0.0

        tendance = '📈' if variation_pct >= 0 else '📉'
        return (f"{symbole} {tendance} : {cours:.2f} $ "
                f"({variation_pct:+.2f}%) | Volume : {volume:,}")
    except Exception as e:
        return f"Erreur lors de la récupération de '{symbole}' : {e}"


def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours réel d'une crypto (prix, variation du jour, volume)."""
    symbole = symbole.strip().upper()
    ticker_symbol = _ticker_crypto(symbole)
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="2d")
        if hist.empty:
            return f"Crypto '{symbole}' introuvable ou données indisponibles."

        cours = hist['Close'].iloc[-1]
        volume = int(hist['Volume'].iloc[-1])

        if len(hist) >= 2:
            cours_veille = hist['Close'].iloc[-2]
            variation_pct = ((cours - cours_veille) / cours_veille) * 100
        else:
            variation_pct = 0.0

        tendance = '📈' if variation_pct >= 0 else '📉'
        return (f"{symbole} {tendance} : {cours:.2f} USD "
                f"({variation_pct:+.2f}%) | Volume : {volume:,}")
    except Exception as e:
        return f"Erreur lors de la récupération de '{symbole}' : {e}"
