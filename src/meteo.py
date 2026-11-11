"""Météo, point Paris centre. Responsable : R2 (enrichissement)."""


def table_meteo(debut, fin):
    """Une ligne par ts_utc :
    - temp_prev, rain_prev, wind_prev : Open-Meteo Previous Runs API, variables *_previous_day1
      (émises au moins 24 h avant l'heure visée) ; vent converti de km/h en m/s ; absent avant 2024 ;
    - temp_obs, rain_obs, wind_obs : Météo-France, Paris-Montsouris (75114001), heures UTC,
      pour l'analyse seulement.
    Vérifier le décalage horaire en comparant pluie et chute des comptages."""
    raise NotImplementedError
