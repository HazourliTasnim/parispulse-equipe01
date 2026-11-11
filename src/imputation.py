"""Estimation des valeurs manquantes dans count_filled. Responsable : Nihed (axe Qualité).

`count` n'est jamais modifié ; chaque estimation est marquée is_imputed / imputation_method.
"""


def imputer_journees(df):
    """Journées entières manquantes : même heure locale à J-14, puis J-21, J-28
    (si absent, férié ou déjà estimé). Le 25/10/2026, les deux heures « 2 h » prennent 2 h à J-14."""
    raise NotImplementedError


def imputer_heures(df, methode):
    """Heures isolées manquantes, avec la méthode retenue par tester_methodes()."""
    raise NotImplementedError


def tester_methodes(df, n_heures=1000, graine=0):
    """Masque des heures réellement mesurées, les estime avec M1 à M4, renvoie l'erreur
    moyenne (MAE) de chaque méthode. M2 (heure suivante) : historique d'apprentissage seulement."""
    raise NotImplementedError
