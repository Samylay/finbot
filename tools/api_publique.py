import requests
 
API_BASE_URL = 'https://api.frankfurter.app'
 
def convertir_devise(input_str: str) -> str:
    """
    Convertit un montant entre deux devises via l'API Frankfurter.
    Entrée : "montant,devise_source,devise_cible"
    Exemple : "100,USD,EUR" → convertit 100 dollars en euros
    """
    parties = [partie.strip() for partie in input_str.strip().split(',')]
    if len(parties) != 3:
        return (
            "Format invalide. Utilise : montant,devise_source,devise_cible "
            'ex "100,USD,EUR".'
        )

    try:
        montant = float(parties[0])
    except ValueError:
        return f"Montant invalide : '{parties[0]}'"

    devise_from = parties[1].upper()
    devise_to = parties[2].upper()
 
    url = f"{API_BASE_URL}/latest"
    params = {'amount': montant, 'from': devise_from, 'to': devise_to}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        montant_converti = data['rates'][devise_to]
    except requests.RequestException as exc:
        return f"Erreur API devise : {exc}"
    except KeyError:
        return f"Conversion indisponible pour {devise_from} -> {devise_to}."

    taux = montant_converti / montant if montant else 0
 
    return (
        f"{montant:.2f} {devise_from} = {montant_converti:.2f} {devise_to}\n"
        f"Taux : 1 {devise_from} = {taux:.4f} {devise_to}"
    )


