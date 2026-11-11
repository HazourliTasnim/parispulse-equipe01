# ParisPulse : contrat de données (v1.0 – proposition de l'équipe 1, 10/11/2026)

Ce contrat décrit exactement ce que l'équipe 1 livre aux autres équipes, en particulier à l'équipe 2.
Toute modification passe par un accord entre équipes et donne une nouvelle version datée (section 9).

## 1. Unité et clés

- **Unité** : un compteur (un sens de circulation à un endroit) × une heure.
- **Clé des comptages** : `(counter_id, ts_utc)`, unique.
- **Clé des métadonnées** : `counter_id`, unique.
- **Granularité** : comptages horaires par compteur, avec sens de circulation, uniquement.
  Les comptages par site au quart d'heure, sans distinction de sens, ne sont jamais mélangés aux
  comptages horaires (règle du sujet).
- **Sites à deux sens** : un site peut porter deux compteurs, un par sens. Les deux sens restent séparés
  dans les fichiers ; `site_id` permet de les regrouper. Les sites réservés au test partent avec
  tous leurs compteurs (« gardez ensemble les directions d'un même site »).

## 2. Table des comptages : `data/processed/counts/<counter_id>.csv.gz`

Une ligne par compteur et par heure, sur une grille horaire complète : une heure sans mesure existe,
avec `count` vide.

| Famille | Colonne | Type | Définition |
|---|---|---|---|
| Identité | `counter_id` | texte | Identifiant du compteur |
| Identité | `site_id` | texte | Identifiant du site physique |
| Temps | `ts_utc` | date UTC | Début de l'heure comptée, en UTC (colonne de calcul) |
| Temps | `ts_local` | date Europe/Paris | Même instant à Paris (affichage) |
| Temps | `date_local` | date | Jour calendaire à Paris |
| Temps | `hour` | entier 0–23 | Heure locale |
| Temps | `day_of_week` | entier 0–6 | 0 = lundi |
| Temps | `is_weekend` | booléen | Samedi ou dimanche |
| Temps | `month` | entier 1–12 | Mois |
| Mesure | `count` | réel | Valeur **mesurée** par la Ville ; vide si absente. Jamais modifiée |
| Mesure | `count_filled` | réel | `count` si mesuré, sinon valeur estimée (section 4) |
| Imputation | `is_imputed` | booléen | Vrai si `count_filled` est une estimation |
| Imputation | `imputation_method` | texte | `none`, `J-14`, `J-21`, `J-28`, ou la méthode des heures isolées |
| Qualité | `is_missing` | booléen | La mesure de cette heure est absente de la source |
| Qualité | `is_network_gap` | booléen | Journée absente sur tout le réseau (22/08, 23/09, 04/10, 25/10/2026) |
| Qualité | `in_zero_run` | booléen | Zéro appartenant à une suite d'au moins 24 h |
| Qualité | `is_zero_suspect` | booléen | Zéro isolé à une heure habituellement chargée (section 5) |
| Qualité | `is_dst_day` | booléen | Jour de changement d'heure (23 h ou 25 h) |
| Calendrier | `is_holiday` | booléen | Jour férié officiel (métropole) |
| Calendrier | `holiday_name` | texte | Nom du jour férié, sinon vide |
| Calendrier | `is_school_holiday` | booléen | Vacances scolaires, zone C (Paris) |
| Météo connue à l'avance | `temp_prev`, `rain_prev`, `wind_prev` | réel | Prévision archivée, émise avant l'heure prévue |
| Météo observée | `temp_obs`, `rain_obs`, `wind_obs` | réel | Observation : **analyse seulement, jamais en entrée de prévision** |
| Traçabilité | `source` | texte | `flux_13_mois` ou `archive_AAAA` |
| Traçabilité | `extraction_date` | date | Date du téléchargement |

## 3. Table des métadonnées : `data/processed/meta.csv`

| Colonne | Définition |
|---|---|
| `counter_id`, `site_id` | Identifiants |
| `counter_name`, `site_name` | Libellés de la source |
| `direction` | Sens tiré du nom (`S-N`, `NO-SE`…), vide si non indiqué |
| `n_counters_site` | Nombre de compteurs sur le site (1 ou 2) |
| `lat`, `lon` | Coordonnées WGS84 |
| `installation_date` | Date d'installation du site |
| `first_obs_utc`, `last_obs_utc` | Bornes observées |
| `coverage` | Part des heures mesurées entre les bornes |
| `n_hours_zero_run`, `n_zero_suspect` | Volume des problèmes de zéros |
| `profile` | `domicile_travail` ou `loisir` (rapport semaine / week-end) |
| `status` | `retenu`, `rejete`, `incertain`, `reserve_test` |
| `status_reason` | Raison du statut, en une phrase |

## 4. Valeurs manquantes : règles d'imputation

`count` n'est **jamais** modifié. L'estimation va dans `count_filled`, toujours marquée.

**Journées entières manquantes** (dont les 4 journées absentes du réseau) :
1. même heure locale, **J-14** (même jour de la semaine) ;
2. si J-14 est absent, férié ou lui-même estimé : J-21, puis J-28 ;
3. sinon : `count_filled` reste vide et le cas est listé dans la fiche.
Le 25/10/2026 (25 h) : les deux heures « 2 h » reçoivent la valeur de 2 h à J-14.

**Heures isolées manquantes** (1 à quelques heures dans une journée mesurée) : méthode retenue par un
test, avant la v2. On masque des heures réellement mesurées, on les estime avec chaque méthode,
et on garde celle qui a la plus petite erreur moyenne :
- M1 : moyenne des 2 heures précédentes ;
- M2 : moyenne de l'heure précédente et de l'heure suivante ;
- M3 : même heure à J-7 ;
- M4 : même heure à J-7, ajustée par le niveau des heures précédentes du jour.
M2 utilise l'heure suivante : acceptable pour nettoyer l'historique d'apprentissage, **interdite** dans
une fenêtre de test (fuite d'information).

**Évaluation** : l'erreur se calcule uniquement sur les heures réellement mesurées
(`is_missing = False`), jamais sur `count_filled` estimé.

## 5. Zéros

- Un zéro n'est **jamais** remplacé ni transformé en valeur manquante (règle du sujet).
- `in_zero_run` : zéro dans une suite d'au moins 24 h consécutives.
- `is_zero_suspect` (règle v1) : `count = 0`, hors suite longue, alors que la médiane du même compteur,
  même heure, même type de jour (semaine / week-end) sur les 28 jours précédents est d'au moins
  50 vélos. Calcul sur le passé seulement.
- Le traitement (garder ou écarter ces heures à l'apprentissage) sera décidé par une expérience
  avec les équipes 2 et 4.

## 6. Format CSV

- Séparateur virgule, UTF-8, point décimal, une ligne d'en-tête.
- Dates ISO 8601 avec décalage : `2026-11-04 17:00:00+00:00`.
- Booléens `True` / `False` ; case vide = valeur absente (jamais `0` ni `NA`).
- Un fichier par compteur, compressé (`.csv.gz`), pour rester sous la limite de GitHub.
- Ne pas réenregistrer les fichiers dans Excel.
- Lecture :

```python
import pandas as pd
df = pd.read_csv("data/processed/counts/100057445-104057445.csv.gz",
                 dtype={"counter_id": str, "site_id": str})
df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True)
df["ts_local"] = df["ts_utc"].dt.tz_convert("Europe/Paris")
```

## 7. Sources et priorités

- Flux 13 mois glissants et archives 2016–2025 (Ville de Paris, licence ODbL).
- Période commune aux deux sources : chaque extraction est datée ; en cas d'écart, le flux récent fait
  foi et l'écart est listé dans la fiche.
- Jours fériés : API officielle des jours fériés (métropole) ; vacances : calendrier scolaire zone C.
- Météo : Open-Meteo (prévisions archivées et observations), point de Paris centre.

## 8. Calendrier de livraison

| Version | Contenu | Échéance |
|---|---|---|
| v0 | 1 compteur, flux 13 mois | Livrée (10/11) |
| v1 | Inventaire, statuts, échantillon, sites réservés ; indicateurs de qualité | Fin J1 / début J2 |
| v2 | + imputation, calendrier, météo, sur l'échantillon | J2 midi |
| v3 | Version finale : tous les compteurs retenus, archives intégrées, pipeline en une commande | J3 |

## 9. Modifications

Toute modification de colonne, de règle ou de format : accord des équipes concernées, nouvelle version
de ce fichier, note dans `docs/decisions.md`, message sur le canal commun.
