"""Constantes et outils partagés par tous les modules (voir docs/contrat_donnees.md)."""
import pathlib

import pandas as pd

TZ = "Europe/Paris"
CLE = ["counter_id", "ts_utc"]                       # clé unique des comptages
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
PROCESSED = ROOT / "data/processed"
JOURNEES_ABSENTES_RESEAU = pd.to_datetime(
    ["2026-08-22", "2026-09-23", "2026-10-04", "2026-10-25"]).date
# Trous communs à tout le réseau (vérifiés le 11/11/2026), en UTC, bornes incluses
TROUS_RESEAU_UTC = [
    ("2025-10-26 00:00", "2025-10-26 00:00"),   # 2 h heure d'été, heure doublée absente
    ("2026-07-01 22:00", "2026-07-01 23:00"),   # 02/07/2026 0 h–2 h (Paris)
    ("2026-07-05 22:00", "2026-07-05 23:00"),   # 06/07/2026 0 h–2 h (Paris)
    ("2026-08-21 22:00", "2026-08-22 21:00"),
    ("2026-09-22 22:00", "2026-09-23 21:00"),
    ("2026-10-03 22:00", "2026-10-04 21:00"),
    ("2026-10-24 22:00", "2026-10-25 22:00"),   # 25 h (passage à l'heure d'hiver)
]

# Ordre des colonnes de la table finale (section 2 du contrat)
COLONNES = [
    "counter_id", "site_id",
    "ts_utc", "ts_local", "date_local", "hour", "day_of_week", "is_weekend", "month",
    "count", "count_filled", "is_imputed", "imputation_method",
    "is_missing", "is_network_gap", "in_zero_run", "is_zero_suspect", "is_dst_day",
    "is_holiday", "holiday_name", "is_school_holiday",
    "temp_prev", "rain_prev", "wind_prev", "temp_obs", "rain_obs", "wind_obs",
    "source", "extraction_date",
]


def lire_comptages(chemin):
    """Lit un fichier de comptages livré et rétablit les types."""
    df = pd.read_csv(chemin, dtype={"counter_id": str, "site_id": str})
    df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True)
    df["ts_local"] = df["ts_utc"].dt.tz_convert(TZ)
    return df
