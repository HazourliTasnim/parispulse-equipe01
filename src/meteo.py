"""Météo, point Paris centre. Responsable : binôme (axe Sources et contexte)."""


def table_meteo(debut, fin):
    """Une ligne par ts_utc :
    - temp_prev, rain_prev, wind_prev : prévisions archivées Open-Meteo, émises AVANT l'heure ;
    - temp_obs, rain_obs, wind_obs : observations, pour l'analyse seulement.
    Vérifier le décalage horaire en comparant pluie et chute des comptages."""
    raise NotImplementedError
