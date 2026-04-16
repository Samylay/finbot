# tools/calculs.py

try:
    from langchain_experimental.tools import PythonREPLTool
except ImportError:
    PythonREPLTool = None


python_repl_tool = PythonREPLTool() if PythonREPLTool is not None else None
if python_repl_tool is not None:
    python_repl_tool.description = (
        "Execute du code Python pour les calculs complexes. "
        "Utilise print(...) pour retourner un resultat lisible."
    )

 
def calculer_tva(input_str: str) -> str:
    """Calcule TVA et prix TTC. Entrée : "prix_ht,taux_tva" ex: "100,20" """
    parties = input_str.strip().split(',')
    prix_ht, taux_tva = float(parties[0]), float(parties[1])
    montant_tva = prix_ht * (taux_tva / 100)
    prix_ttc = prix_ht + montant_tva
    return f"HT: {prix_ht:.2f}€  TVA({taux_tva}%): {montant_tva:.2f}€  TTC: {prix_ttc:.2f}€"
 
def calculer_interets_composes(input_str: str) -> str:
    """Intérêts composés. Entrée : "capital,taux_annuel,duree_annees" """
    c, t, n = input_str.strip().split(',')
    capital, taux, duree = float(c), float(t), int(n)
    capital_final = capital * ((1 + taux/100) ** duree)
    return f"Capital final : {capital_final:,.2f}€ (gain : {capital_final-capital:,.2f}€)"
 
def calculer_marge(input_str: str) -> str:
    """Marge commerciale. Entrée : "prix_vente,cout_achat" """
    pv, ca = input_str.strip().split(',')
    prix_vente, cout_achat = float(pv), float(ca)
    marge = prix_vente - cout_achat
    taux_marge = (marge / cout_achat) * 100
    return f"Marge : {marge:.2f}€ | Taux de marge : {taux_marge:.1f}%"
 
def calculer_mensualite_pret(input_str: str) -> str:
    """Mensualité de prêt. Entrée : "capital,taux_annuel,duree_mois" """
    c, t, d = input_str.strip().split(',')
    K, r, n = float(c), float(t)/100/12, int(d)
    if n <= 0:
        return "Erreur : la duree doit etre superieure a 0."
    if r == 0:
        M = K / n
    else:
        M = K * (r * (1+r)**n) / ((1+r)**n - 1)
    return f"Mensualité : {M:.2f}€/mois | Coût total : {M*n:,.2f}€"
