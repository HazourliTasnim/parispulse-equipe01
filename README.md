# ParisPulse – Équipe 1 : données et contexte

Inventaire du réseau de compteurs vélo de Paris, séries contrôlées et contexte (calendrier, météo),
livrés aux autres équipes selon `docs/contrat_donnees.md` (v1.1, à valider).

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
python src/verifier_contrat.py                                # vérifications sur tout le réseau et les sources
python src/comparer_archive_flux.py                           # concordance archive 2025 / flux
python src/pipeline.py                                        # chaîne complète (en construction)
```

## Organisation du code

| Fichier | Rôle | Responsable |
|---|---|---|
| `src/commun.py` | Constantes partagées (clé, colonnes, chemins, trous du réseau) | Tous |
| `src/sources.py`, `src/normaliser.py` | Flux et archives, grille horaire UTC, raccordement | R3 – extraction extensible |
| `src/calendrier.py`, `src/meteo.py` | Colonnes de temps, jours fériés, vacances, météo | R2 – enrichissement |
| `src/qualite.py` | Indicateurs de qualité (R4) et statut des compteurs (R1) | R4 / R1 |
| `src/imputation.py` | Estimations dans `count_filled` | R4 – qualité et horodatage |
| `src/assembler.py`, `src/pipeline.py` | Jointures, contrôles, livraison | Tous |
| `src/phase0.py`, `src/verifier_contrat.py`, `src/comparer_archive_flux.py` | Outils de la phase de vérification | — |

## Dossiers

- `data/raw/` : fichiers téléchargés, jamais modifiés (non versionnés, retéléchargeables)
- `data/processed/` : fichiers livrés aux autres équipes (CSV)
- `docs/` : contrat de données, décisions, rapports de vérification, fiches

## Documents

- `docs/contrat_donnees.md` : ce que nous livrons, et les questions à valider
- `docs/decisions.md` : chaque décision, sa raison et son auteur
- `docs/verifications_contrat_2026-11-11.md`, `docs/qualite_reseau.csv`, `docs/recouvrement_archive_flux.csv` : résultats des vérifications

## Sources

- Comptage vélo – flux 13 mois et archives 2016–2025, Ville de Paris (opendata.paris.fr), licence ODbL
- Jours fériés : calendrier.api.gouv.fr ; vacances scolaires : data.education.gouv.fr
- Météo prévue : Open-Meteo, Previous Runs API (CC BY 4.0) ; météo observée : Météo-France, données horaires (Licence Ouverte 2.0)

Les dates d'extraction figurent dans le nom de chaque fichier brut et dans la colonne `extraction_date`.
