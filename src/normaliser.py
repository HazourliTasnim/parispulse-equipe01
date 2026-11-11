"""Mise au format commun. Responsable : R3 (extraction extensible)."""


def normaliser(brut):
    """Brut -> colonnes counter_id, site_id, ts_utc, count, source, extraction_date,
    sur une grille horaire complète en UTC (heure absente = ligne avec count vide).

    Reprendre normaliser() de phase0.py, en l'étendant à plusieurs compteurs.
    """
    raise NotImplementedError


def resoudre_chevauchement(flux, archives):
    """Période commune flux / archives : le flux récent fait foi ;
    les écarts de valeur sont listés (pour la fiche), jamais corrigés en silence."""
    raise NotImplementedError
