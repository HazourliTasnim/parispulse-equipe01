# ParisPulse – Équipe 1 : données et contexte

Inventaire du réseau de compteurs vélo de Paris, séries contrôlées et contexte (calendrier, météo),
livrés aux autres équipes selon `docs/contrat_donnees.md` (v1.0).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Commandes

```bash
python src/phase0.py lister                                   # classement des compteurs
python src/phase0.py extraire --compteur 100057445-104057445  # v0 : un compteur, contrôlé
python src/verifier.py                                        # vérifications sur tout le réseau
python src/pipeline.py                                        # chaîne complète (en construction)
```

## Organisation du code

| Fichier | Rôle | Responsable |
|---|---|---|
| `src/commun.py` | Constantes partagées (clé, colonnes, chemins) | Les deux |
| `src/sources.py`, `src/normaliser.py` | Flux 13 mois et archives, grille horaire UTC | Binôme |
| `src/calendrier.py`, `src/meteo.py` | Colonnes de temps, jours fériés, vacances, météo | Binôme |
| `src/qualite.py`, `src/imputation.py` | Indicateurs de qualité, statuts, estimations | Nihed |
| `src/assembler.py`, `src/pipeline.py` | Jointures, contrôles, livraison | Les deux |

## Dossiers

- `data/raw/` : fichiers téléchargés, jamais modifiés (non versionnés, retéléchargeables)
- `data/processed/` : fichiers livrés aux autres équipes (CSV)
- `docs/` : contrat de données, décisions, fiches, vérifications

## Lire les données livrées

```python
import pandas as pd
df = pd.read_csv("data/processed/counts_v0_2026-11-10.csv", dtype={"counter_id": str, "site_id": str})
df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True)
df["ts_local"] = df["ts_utc"].dt.tz_convert("Europe/Paris")
```

## Sources

- Comptage vélo – Données compteurs (flux 13 mois), Ville de Paris, licence ODbL
  https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/
- Comptage vélo – Historique (archives 2016–2025), Ville de Paris, licence ODbL
  https://opendata.paris.fr/explore/dataset/comptage-velo-historique-donnees-compteurs/
- Météo : Open-Meteo (prévisions archivées et observations) – à intégrer en v2
- Jours fériés et vacances scolaires (zone C) – à intégrer en v2

Les dates d'extraction figurent dans le nom de chaque fichier brut et dans la colonne `extraction_date`.
