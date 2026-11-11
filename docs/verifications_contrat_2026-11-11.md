# Vérifications avant le contrat – 11/11/2026

Flux : 1035400 lignes, 113 compteurs, 11/10/2025 03 h → 10/11/2026 23 h

## A1. Heures absentes sur tout le réseau
- Grille : 9502 heures ; médiane 111 compteurs présents par heure
- Périodes où moins de la moitié du réseau est présente : 8
  - 11/10/2025 03 h → 12/10/2025 01 h (heure de Paris) : 23 h
  - 26/10/2025 02 h → 26/10/2025 02 h (heure de Paris) : 1 h
  - 02/07/2026 00 h → 02/07/2026 01 h (heure de Paris) : 2 h
  - 06/07/2026 00 h → 06/07/2026 01 h (heure de Paris) : 2 h
  - 22/08/2026 00 h → 22/08/2026 23 h (heure de Paris) : 24 h
  - 23/09/2026 00 h → 23/09/2026 23 h (heure de Paris) : 24 h
  - 04/10/2026 00 h → 04/10/2026 23 h (heure de Paris) : 24 h
  - 25/10/2026 00 h → 25/10/2026 23 h (heure de Paris) : 25 h

## A2. Changements d'heure
- 2025-10-26 : 25 heures attendues ; 1 heure(s) quasi vide(s) : 02 h (UTC+0200)
- 2026-03-29 : 23 heures attendues ; 0 heure(s) quasi vide(s)
- 2026-10-25 : 25 heures attendues ; 25 heure(s) quasi vide(s) : 00 h (UTC+0200), 01 h (UTC+0200), 02 h (UTC+0200), 02 h (UTC+0100), 03 h (UTC+0100), 04 h (UTC+0100) …

## A7. Faisabilité de l'estimation J-14 pour les journées absentes du réseau
- 11/10/2025 : J-14 présent à 0%
- 11/10/2025 : J-21 présent à 0%
- 11/10/2025 : J-28 présent à 0%
- 22/08/2026 : J-14 présent à 100%
- 23/09/2026 : J-14 présent à 100%
- 04/10/2026 : J-14 présent à 100%
- 25/10/2026 : J-14 présent à 100%

## A3. Doublons (113 compteurs)
- Lignes en double : 0 ; compteurs concernés : 0

## A4–A5. Couverture, suites de zéros, zéros suspects (tous les compteurs)
- Détail par compteur : `docs/qualite_reseau.csv` (113 compteurs)
- Couverture < 90 % : 5 compteurs
  - Face 104 rue d'Aubervilliers N-S : 33.1%, plus long trou 1 h
  - Face 104 rue d'Aubervilliers S-N : 33.1%, plus long trou 1 h
  - 39 quai François Mauriac NO-SE : 67.1%, plus long trou 26 h
  - 39 quai François Mauriac SE-NO : 67.1%, plus long trou 26 h
  - 106 avenue Denfert Rochereau NE-SO : 76.9%, plus long trou 8 h
- Compteurs avec une suite de zéros ≥ 24 h : 12 (13512 heures au total)
  - 106 avenue Denfert Rochereau NE-SO : 7303 h en 4 suite(s), dès le 12/10/2025 (336 h)
  - 24 boulevard Jourdan E-O : 3949 h en 2 suite(s), dès le 12/10/2025 (336 h)
  - 51 boulevard Masséna SO-NE : 923 h en 2 suite(s), dès le 12/10/2025 (336 h)
  - 12 avenue de la Porte de Bagnolet O-E : 357 h en 1 suite(s), dès le 30/03/2026 (357 h)
  - 12 avenue de la Porte de Bagnolet E-O : 356 h en 1 suite(s), dès le 30/03/2026 (356 h)
  - 72 boulevard Voltaire NO-SE : 137 h en 1 suite(s), dès le 19/10/2026 (137 h)
  - 29 boulevard des Batignolles E-O : 120 h en 1 suite(s), dès le 22/11/2025 (120 h)
  - 29 boulevard des Batignolles O-E : 117 h en 1 suite(s), dès le 22/11/2025 (117 h)
  - Totem Cours la Reine O-E : 88 h en 1 suite(s), dès le 26/06/2026 (88 h)
  - 35 boulevard de Ménilmontant NO-SE : 88 h en 1 suite(s), dès le 22/05/2026 (88 h)
- Zéros suspects (règle v1, hors suites longues) : 1123 heures sur 58 compteurs
  - 21 boulevard Auguste Blanqui SO-NE : 333
  - 180 avenue d'Italie N-S : 115
  - 243 boulevard Saint Germain NO-SE : 109
  - 35 boulevard de Ménilmontant NO-SE : 57
  - 33 avenue des Champs Elysées NO-SE : 55
  - 44 avenue des Champs Elysées SE-NO : 49
  - Pont de la Concorde N-S : 43
  - Pont de la Concorde S-N : 43
- Zoom Face au 21 boulevard de Ménilmontant SE-NO : 0 h en suites longues, 0 zéros suspects isolés
- Zoom 35 boulevard de Ménilmontant NO-SE : 88 h en suites longues, 57 zéros suspects isolés

## A6. Sens de circulation et sites
- Compteurs sans sens dans le nom : 0
- Sites à 2 compteurs : 31 ; sens exactement opposés : 31
- Sites à plus de 2 compteurs : 0

## B. Archives 2016–2025
- Pièces jointes : 20
  - 2018_comptage-velo-donnees-compteurs.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2018_comptage_velo_donnees_compteurs_csv_zip
  - 2018_comptage-velo-donnees-sites-comptage.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2018_comptage_velo_donnees_sites_comptage_csv_zip
  - 2019_comptage-velo-donnees-compteurs.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2019_comptage_velo_donnees_compteurs_csv_zip
  - 2019_comptage-velo-donnees-sites-comptage.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2019_comptage_velo_donnees_sites_comptage_csv_zip
  - 2020_comptage-velo-donnees-compteurs.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2020_comptage_velo_donnees_compteurs_csv_zip
  - 2020_comptage-velo-donnees-sites-comptage.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2020_comptage_velo_donnees_sites_comptage_csv_zip
  - 2021-comptage-velo-donnees-compteurs.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2021_comptage_velo_donnees_compteurs_csv_zip
  - 2021-comptage-velo-donnees-sites-comptage.csv.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2021_comptage_velo_donnees_sites_comptage_csv_zip
  - 2022-comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2022_comptage_velo_donnees_compteurs_zip
  - 2022-comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2022_comptage_velo_donnees_sites_comptage_zip
  - 2016_comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2016_comptage_velo_donnees_compteurs_zip
  - 2017_comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2017_comptage_velo_donnees_compteurs_zip
  - 2016_comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2016_comptage_velo_donnees_sites_comptage_zip
  - 2017_comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2017_comptage_velo_donnees_sites_comptage_zip
  - 2023_comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2023_comptage_velo_donnees_compteurs_zip
  - 2023-comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2023_comptage_velo_donnees_sites_comptage_zip
  - 2024-comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2024_comptage_velo_donnees_sites_comptage_zip
  - 2024-comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2024_comptage_velo_donnees_compteurs_zip
  - 2025-comptage-velo-donnees-sites-comptage.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2025_comptage_velo_donnees_sites_comptage_zip
  - 2025-comptage-velo-donnees-compteurs.zip → https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-historique-donnees-compteurs/attachments/2025_comptage_velo_donnees_compteurs_zip
- ⚠️ Étape impossible : UnicodeDecodeError : 'utf-8' codec can't decode byte 0xe9 in position 240: invalid continuation byte

## C1. Jours fériés (calendrier.api.gouv.fr)
- 285 jours fériés, années 2006 → 2031
- Exemples 2026 : ['2026-01-01 1er janvier', '2026-04-06 Lundi de Pâques', '2026-05-01 1er mai', '2026-05-08 8 mai']

## C2. Vacances scolaires zone C (data.education.gouv.fr)
- 2587 lignes ; colonnes : ['description', 'population', 'start_date', 'end_date', 'location', 'zones', 'annee_scolaire']
- Années scolaires pour Paris : ['2023-2024', '2024-2025', '2025-2026', '2026-2027', '2027-2028']
- Lignes Paris : 75 (à filtrer sur la population élèves)

## C3. Météo prévue : Open-Meteo, prévisions de la veille (Previous Runs API)
- 2025-10-11 → 2026-11-09 : 9480 heures ; part renseignée {'temperature_2m_previous_day1': 1.0, 'precipitation_previous_day1': 1.0, 'wind_speed_10m_previous_day1': 1.0}
- 2023-06-01 → 2023-06-07 : 168 heures ; part renseignée {'temperature_2m_previous_day1': 1.0, 'precipitation_previous_day1': 0.0, 'wind_speed_10m_previous_day1': 0.0}
- Unités : {'time': 'iso8601', 'temperature_2m_previous_day1': '°C', 'precipitation_previous_day1': 'mm', 'wind_speed_10m_previous_day1': 'km/h'}
- Lecture : `previous_day1` = prévision émise au moins 24 h avant l'heure visée, donc disponible avant 00 h du jour J pour toutes les heures de J.

## C4. Météo observée : Météo-France, horaires, département 75
- HOR_departement_75_periode_1810-1819 (2026-04-17)
- HOR_departement_75_periode_1820-1829 (2026-06-25)
- HOR_departement_75_periode_1830-1839 (2026-06-25)
- HOR_departement_75_periode_1840-1849 (2026-06-25)
- HOR_departement_75_periode_1850-1859 (2026-06-25)
- HOR_departement_75_periode_1860-1869 (2026-06-25)
- HOR_departement_75_periode_1870-1879 (2026-06-25)
- HOR_departement_75_periode_1880-1889 (2026-06-25)
- HOR_departement_75_periode_1890-1899 (2026-06-25)
- HOR_departement_75_periode_1900-1909 (2026-04-17)
- HOR_departement_75_periode_1910-1919 (2026-06-25)
- HOR_departement_75_periode_1920-1929 (2026-06-25)
- HOR_departement_75_periode_1930-1939 (2026-06-25)
- HOR_departement_75_periode_1940-1949 (2026-06-25)
- HOR_departement_75_periode_1950-1959 (2026-04-17)
- HOR_departement_75_periode_1960-1969 (2026-06-25)
- HOR_departement_75_periode_1970-1979 (2026-06-25)
- HOR_departement_75_periode_1980-1989 (2026-06-25)
- HOR_departement_75_periode_1990-1999 (2026-06-25)
- HOR_departement_75_periode_2000-2009 (2026-06-25)
- HOR_departement_75_periode_2010-2019 (2026-06-25)
- HOR_departement_75_periode_2020-2024 (2026-10-02)
- HOR_departement_75_periode_2025-2026 (2026-11-11)
- Fichier HOR_departement_75_periode_2025-2026 : 97764 lignes ; Paris-Montsouris (75114001) : 16301 lignes
- Période Montsouris (UTC) : 2025-01-01 00:00:00 → 2026-11-11 04:00:00
  - T renseigné à 100.0%
  - RR1 renseigné à 99.3%
  - FF renseigné à 100.0%