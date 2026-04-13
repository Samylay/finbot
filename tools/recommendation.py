# TODO: Logique de recommandation d'investissement

import re
from datetime import datetime
 
def resumer_texte(texte: str) -> str:
    """Génère un résumé avec statistiques (mots, phrases, temps de lecture)."""
    nb_mots = len(texte.split())
    phrases = [p.strip() for p in re.split(r'[.!?]+', texte) if len(p.strip()) > 10]
    resume = '. '.join(phrases[:2]) + '.' if len(phrases) >= 2 else texte[:150]
    temps = max(1, nb_mots // 200)   # ~200 mots/minute
    return f"Résumé : {resume}\nMots : {nb_mots} | Temps lecture : {temps} min"
 
def formater_rapport(input_str: str) -> str:
    """Formate paires clé:valeur en rapport. Entrée : "Cle1:Val1|Cle2:Val2" """
    date = datetime.now().strftime('%d/%m/%Y %H:%M')
    if '|' in input_str and ':' in input_str:
        lignes = []
        for paire in input_str.split('|'):
            if ':' in paire:
                cle, val = paire.split(':', 1)
                lignes.append(f"  • {cle.strip()} : {val.strip()}")
        return f"=== RAPPORT ({date}) ===\n" + '\n'.join(lignes)
    return f"=== RAPPORT ({date}) ===\n  {input_str.strip()}"
 
def extraire_mots_cles(texte: str) -> str:
    """Extrait les mots-clés (filtre les mots vides français)."""
    mots_vides = {'le','la','les','un','une','des','de','du','en','et','ou',
                  'est','sont','à','au','aux','par','sur','dans','avec'}
    mots_nettoyes = re.sub(r'[^\w\s]', ' ', texte.lower()).split()
    compteur = {}
    for mot in mots_nettoyes:
        if mot not in mots_vides and len(mot) > 3:
            compteur[mot] = compteur.get(mot, 0) + 1
    tries = sorted(compteur.items(), key=lambda x: x[1], reverse=True)[:10]
    return '\n'.join([f"  {mot}: {freq}x" for mot, freq in tries])
# =========================================================================================
CATALOGUE = [
    # id       nom                          prix    catégorie      score  cible
    {'id':'P001','nom':'Ordinateur Pro',    'prix':899.00, 'cat':'Informatique','score':4.7,'cible':['Premium','VIP']},
    {'id':'P002','nom':'Souris ergonomique','prix':49.90,  'cat':'Informatique','score':4.4,'cible':['Standard','Premium','VIP']},
    {'id':'P003','nom':'Bureau réglable',   'prix':350.00, 'cat':'Mobilier',    'score':4.5,'cible':['Premium','VIP']},
    {'id':'P004','nom':'Casque audio',      'prix':129.00, 'cat':'Audio',       'score':4.5,'cible':['Standard','Premium','VIP']},
    {'id':'P005','nom':'Écran 27" 4K',     'prix':549.00, 'cat':'Informatique','score':4.6,'cible':['Premium','VIP']},
    {'id':'P008','nom':'Chaise ergonomique','prix':280.00, 'cat':'Mobilier',    'score':4.6,'cible':['Standard','Premium','VIP']},
]
 
def recommander_produits(input_str: str) -> str:
    """
    Recommande des produits selon budget, catégorie et type de compte.
    Entrée : "budget,categorie,type_compte"
    Exemple : "300,Informatique,Premium"
    """
    budget, categorie, type_compte = input_str.strip().split(',')
    budget = float(budget)
    filtres = [
        p for p in CATALOGUE
        if p['prix'] <= budget
        and (categorie.lower() == 'toutes' or p['cat'].lower() == categorie.lower())
        and type_compte in p['cible']
    ]
    if not filtres:
        return 'Aucun produit trouvé pour ces critères.'
    filtres.sort(key=lambda x: x['score'], reverse=True)
    result = f"Recommandations (budget {budget:.0f}€, {categorie}, {type_compte}) :\n"
    for i, p in enumerate(filtres[:5], 1):
        result += f"  {i}. {p['nom']} – {p['prix']:.2f}€ – ⭐{p['score']}\n"
    return result


