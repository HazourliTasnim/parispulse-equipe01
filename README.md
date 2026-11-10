# ParisPulse – Équipe 1 : données et contexte

## Installation
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

## Phase 0
python src/phase0.py lister
python src/phase0.py extraire --compteur ID

## Organisation
- data/raw/       fichiers téléchargés, jamais modifiés (non versionnés)
- data/processed/ fichiers livrés aux autres équipes
- src/            scripts
- docs/           contrat de données, fiches, décisions

## Sources
- Comptage vélo – Données compteurs (flux 13 mois), Ville de Paris, licence ODbL
  https://opendata.paris.fr/explore/dataset/comptage-velo-donnees-compteurs/
- Comptage vélo – Historique (archives 2016–2025), Ville de Paris, licence ODbL
  https://opendata.paris.fr/explore/dataset/comptage-velo-historique-donnees-compteurs/
Les dates d'extraction figurent dans le nom de chaque fichier brut.
