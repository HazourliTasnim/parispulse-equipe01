# ParisPulse : contrat de données de l'équipe 1

**Version 1.1 – proposition soumise aux équipes 2 à 5 (à valider) – 11/11/2026**

Ce contrat décrit ce que l'équipe 1 livre : les comptages contrôlés, le contexte (calendrier, météo),
les localisations et la provenance. Les règles s'appuient sur des vérifications faites sur les données
(`docs/verifications_contrat_2026-11-11.md`, `docs/recouvrement_archive_flux.csv`). Une fois validé, le contrat
est figé ; toute modification passe par un accord et une nouvelle version (section 11).

## 1. Sources vérifiées

| Source | Format constaté | Couverture vérifiée | Licence |
|---|---|---|---|
| Ville de Paris – flux 13 mois (API) | UTF-8, `;`, dates ISO 8601 avec décalage | 113 compteurs, fenêtre glissante, J-1 | ODbL |
| Ville de Paris – archives 2016–2025, fichiers **par compteur et par heure** | 2025 : latin-1, `,`, dates `2025-05-06 14:00:00.000 +0200` ; noms de fichiers variables | 2025 : 171 compteurs ; autres années à vérifier | ODbL |
| calendrier.api.gouv.fr – jours fériés métropole | JSON | 2006 → 2031 | à confirmer |
| data.education.gouv.fr – calendrier scolaire | CSV | Paris : 2023-2024 → 2027-2028 (avant : filtrer « Zone C ») | à confirmer |
| Open-Meteo – Previous Runs API, prévision de la veille | JSON, UTC | 100 % sur la période du flux ; avant 2024 : température seule | CC BY 4.0 |
| Météo-France – observations horaires, Paris-Montsouris (75114001) | CSV gzip, heures UTC | 2025 → aujourd'hui : T 100 %, RR1 99,3 %, FF 100 % | Licence Ouverte 2.0 |

Les fichiers d'archives **par site au quart d'heure, sans sens**, ne sont jamais empilés avec les comptages
horaires par compteur.

## 2. Unité, clés, sens de circulation

- **Unité** : un compteur × une heure. Un compteur = un sens de circulation sur un site.
- **Clé des comptages** : `(counter_id, ts_utc)`, unique (0 doublon vérifié sur les 113 compteurs du flux).
- Selon la Ville, un site porte un compteur (aménagement unidirectionnel) ou deux (bidirectionnel).
  Vérifié : 51 sites à 1 compteur, 31 à 2 compteurs, tous de sens opposés.
- Les sens restent séparés ; `site_id` permet de les regrouper. Les sites réservés au test partent avec
  tous leurs compteurs.

## 3. Temps

- `ts_utc` : début de l'heure comptée, en UTC (colonne de calcul) ; `ts_local` : heure de Paris (affichage).
- L'horodatage de la Ville est conservé tel quel. **Vérifié : l'archive 2025 et le flux suivent la même
  convention** (valeurs identiques sans décalage sur 57 compteurs). Les années 2016–2024 sont vérifiées une
  par une ; en cas de doute non résolu, la période retenue est justifiée plutôt que de supposer un fuseau.

## 4. Raccordement archives / flux

- Sur la période commune, **le flux fait foi** (publication la plus récente).
- Vérifié sur oct.–déc. 2025 : 57 des 106 compteurs communs ont des valeurs identiques. **49 diffèrent**,
  presque tous sur des **sites bidirectionnels** (48 compteurs sur 56) : dans l'archive, un sens est
  quasi vide (3 à 15 % du flux) et l'autre légèrement plus bas (90 à 97 %). Les sites unidirectionnels
  concordent (49 sur 50).
- Règle : l'historique d'archive est utilisé **au niveau du compteur** seulement s'il concorde avec le flux
  sur la période commune ; sinon le compteur ne garde que l'historique du flux, et la raison est notée.
- Métadonnée `archive_concordance` : `identique`, `ecart`, `non_comparable`.

## 5. Table des comptages

Une ligne par compteur et par heure, sur une grille horaire complète : une heure sans mesure existe,
avec `count` vide.

| Famille | Colonne | Définition |
|---|---|---|
| Identité | `counter_id`, `site_id` | Identifiants de la Ville |
| Temps | `ts_utc`, `ts_local`, `date_local`, `hour`, `day_of_week` (0 = lundi), `is_weekend`, `month` | Section 3 |
| Mesure | `count` | Valeur mesurée ; vide si absente ; **jamais modifiée** |
| Mesure | `count_filled`, `is_imputed`, `imputation_method` | Estimation (section 7), toujours marquée |
| Qualité | `is_missing` | Mesure absente de la source |
| Qualité | `is_network_gap` | Heure absente sur tout le réseau (section 6) |
| Qualité | `in_zero_run` | Zéro dans une suite d'au moins 24 h |
| Qualité | `is_zero_suspect` | Zéro isolé à une heure habituellement chargée |
| Qualité | `is_dst_day` | Jour de changement d'heure (23 h ou 25 h) |
| Calendrier | `is_holiday`, `holiday_name`, `is_school_holiday` | Connus à l'avance |
| Météo connue à l'avance | `temp_prev` (°C), `rain_prev` (mm), `wind_prev` (m/s), `meteo_emission` | Prévision de la veille (section 8) |
| Météo observée | `temp_obs` (°C), `rain_obs` (mm), `wind_obs` (m/s) | Analyse après coup seulement |
| Traçabilité | `source`, `extraction_date` | `flux_13_mois` ou `archive_AAAA` ; date du téléchargement |

## 6. Trous connus, communs à tout le réseau (vérifiés)

| Période (heure de Paris) | Durée |
|---|---|
| 26/10/2025, 2 h (heure d'été, heure doublée) | 1 h |
| 02/07/2026 et 06/07/2026, 0 h–2 h | 2 × 2 h |
| 22/08, 23/09, 04/10 et 25/10/2026 | 4 journées |

Ces heures ont `is_network_gap = True`. Le début de la fenêtre glissante n'est pas un trou.

## 7. Valeurs manquantes et zéros

- **Journée entière manquante** : même heure locale à J-14 (disponible à 100 % pour les 4 journées), puis
  J-21, J-28 ; sinon `count_filled` reste vide.
- **Heure isolée manquante** : méthode choisie par un test sur des heures mesurées masquées (M1 à M4).
  Une méthode utilisant une heure postérieure à la date de prévision est interdite en test.
- **Évaluation** : uniquement sur les heures réellement mesurées.
- **Zéros** : jamais remplacés. Vérifié : 12 compteurs ont des suites de zéros ≥ 24 h (13 512 h), dont des
  pannes de site entier (Porte de Bagnolet, Batignolles) et un compteur hors service (106 av. Denfert-Rochereau).
  La règle v1 de `is_zero_suspect` signale 1 123 heures sur 58 compteurs, dont des zéros probablement réels
  (fermetures des Champs-Élysées, du pont de la Concorde) : elle sera calibrée avant la v1.

## 8. Météo et règle de non-fuite

- À chaque date de prévision, seules les informations déjà disponibles sont utilisables.
- `*_prev` : Open-Meteo `previous_day1`, prévision émise au moins 24 h avant l'heure visée, donc disponible
  avant 00 h (heure de Paris) du jour concerné. Disponible pour la période du flux ; **absente avant 2024**
  (sauf la température) : pour les archives anciennes, pas de météo prévue.
- `*_obs` : Météo-France, Paris-Montsouris, réservées à l'analyse.
- Unités harmonisées : °C, mm, m/s (le vent d'Open-Meteo, en km/h, est converti).
- Contrôles de jointure : lieu, heures, unités, nombre de lignes avant / après.

## 9. Table des métadonnées

| Colonne | Définition |
|---|---|
| `counter_id`, `site_id`, `counter_name`, `site_name`, `direction` | Identité et sens |
| `site_type` | `unidirectionnel` ou `bidirectionnel` |
| `lat`, `lon` | Coordonnées WGS84 |
| `installation_date`, `first_obs_utc`, `last_obs_utc`, `history_days` | Dates et ancienneté |
| `coverage` | Part des heures mesurées **depuis la première mesure** |
| `n_hours_zero_run`, `n_zero_suspect` | Volume des problèmes de zéros |
| `archive_concordance` | Section 4 |
| `profile` | `domicile_travail` ou `loisir` |
| `status` | `retenu`, `rejete`, `incertain`, `reserve_test`, `reserve_robustesse` |
| `status_reason` | Raison du statut |

## 10. Fichiers, format, livraisons

- `data/processed/counts/<counter_id>.csv.gz` (un fichier par compteur), `data/processed/meta.csv`,
  `docs/dictionnaire.md`, `docs/provenance.md`.
- CSV : virgule, UTF-8, point décimal, dates ISO 8601 avec décalage, `True` / `False`, case vide = absent.

| Version | Contenu | Échéance |
|---|---|---|
| v0 | 1 compteur (Sébastopol S-N), flux 13 mois | Livrée |
| v1 | Inventaire, statuts, échantillon, sites réservés, indicateurs de qualité | Fin J1 / début J2 |
| v2 | + estimations, calendrier, météo, sur l'échantillon | J2 midi |
| v3 | Version finale : extension, archives concordantes, pipeline en une commande | J3 |

## 11. Questions à valider par les équipes

| # | Question | Équipes | Proposition |
|---|---|---|---|
| 1 | Unité compteur × heure, clé `(counter_id, ts_utc)`, CSV | Toutes | Oui |
| 2 | Calculs en `ts_utc`, horodatage de la Ville conservé | Toutes | Oui |
| 3 | Estimation J-14 dans `count_filled`, `count` intact | 2, 4 | Oui ; l'équipe 2 garde sa règle de remplacement si elle le souhaite |
| 4 | Zéros signalés, jamais remplacés | 2, 4 | Oui |
| 5 | Heure d'origine des prévisions | 2, 3, 4 | 00 h, heure de Paris |
| 6 | Sites réservés (test et robustesse) | 3, 4 | Choisis avec l'équipe 4, sens réunis |
| 7 | Historique des sites bidirectionnels limité au flux quand l'archive ne concorde pas | 2, 3, 4 | Oui |
| 8 | Format de lecture pour l'application | 5 | Un fichier par compteur + `meta.csv` |
| 9 | Canal de communication et contacts | Toutes | Un canal commun, un contact par équipe |

Toute modification après validation : accord des équipes concernées, nouvelle version datée de ce fichier,
note dans `docs/decisions.md`, message sur le canal commun.
