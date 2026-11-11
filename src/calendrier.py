"""Colonnes de temps et calendrier. Responsable : binôme (axe Sources et contexte)."""


def colonnes_temps(df):
    """Ajoute ts_local, date_local, hour, day_of_week (0 = lundi), is_weekend, month."""
    raise NotImplementedError


def table_calendrier(debut, fin):
    """Une ligne par date_local : is_holiday, holiday_name (jours fériés métropole),
    is_school_holiday (zone C). Sources datées et citées dans le README."""
    raise NotImplementedError
