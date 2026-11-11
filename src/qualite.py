"""Indicateurs de qualité et statut des compteurs. Responsable : R4 (qualité et horodatage) ; statut_compteurs : R1 (réseau et sélection)."""


def ajouter_indicateurs(df):
    """Ajoute is_missing, is_network_gap, in_zero_run, is_zero_suspect, is_dst_day.

    Règles (contrat, section 5) :
    - in_zero_run : zéro dans une suite d'au moins 24 h consécutives ;
    - is_zero_suspect : count == 0, hors suite longue, et médiane du même compteur,
      même heure, même type de jour sur les 28 jours PRÉCÉDENTS >= 50 ;
    - is_network_gap : date_local dans commun.JOURNEES_ABSENTES_RESEAU ;
    - is_dst_day : journée locale de 23 h ou 25 h.
    Ne modifie jamais `count`.
    """
    raise NotImplementedError


def statut_compteurs(df, meta):
    """Complète les métadonnées : coverage, n_hours_zero_run, n_zero_suspect, profile,
    direction, n_counters_site, status, status_reason."""
    raise NotImplementedError
