"""Téléchargement des sources brutes. Responsable : binôme (axe Sources et contexte).

Chaque fichier brut est écrit dans data/raw/ avec sa date d'extraction, et jamais modifié.
"""


def telecharger_flux(compteurs=None):
    """Flux 13 mois glissants (API Open Data Paris), pour une liste de compteurs ou tous.

    Retour : DataFrame brut (colonnes de la source), plus la colonne `extraction_date`.
    """
    raise NotImplementedError("À faire : reprendre lire_brut() de phase0.py")


def telecharger_archives(annees=range(2016, 2026)):
    """Archives annuelles, comptages HORAIRES PAR COMPTEUR uniquement
    (jamais le produit au quart d'heure par site).

    À vérifier année par année : noms de colonnes, séparateur, format et fuseau des dates.
    """
    raise NotImplementedError
