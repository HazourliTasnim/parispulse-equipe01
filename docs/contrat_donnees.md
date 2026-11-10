# ParisPulse : contrat de données (BROUILLON v0, proposé par l'équipe 1)

À amender en réunion. Toute modification ultérieure = nouvelle version datée.

## 1. Table des comptages : `data/processed/counts_vX_AAAA-MM-JJ.parquet`

Une ligne par compteur et par heure, grille horaire complète (les heures absentes existent, avec `count` vide).

| Colonne | Type | Définition |
|---|---|---|
| `counter_id` | texte | Identifiant du compteur (un sens de circulation) |
| `site_id` | texte | Identifiant du site physique (peut porter 2 compteurs) |
| `ts_utc` | datetime UTC | **Début** de l'heure comptée, en UTC |
| `ts_local` | datetime Europe/Paris | Même instant en heure de Paris (affichage) |
| `count` | réel | Passages sur [ts, ts + 1 h[ ; vide = mesure absente |
| `is_missing` | booléen | L'heure attendue est absente des fichiers source |
| `in_zero_run` | booléen | Zéro appartenant à une suite d'au moins 24 h (seuil à valider) |
| `source` | texte | Jeu d'origine et date d'extraction |

## 2. Table des métadonnées : `data/processed/meta_vX_AAAA-MM-JJ.parquet`

| Colonne | Définition |
|---|---|
| `counter_id`, `site_id` | Identifiants |
| `counter_name`, `site_name` | Libellés source |
| `lat`, `lon` | Coordonnées (WGS84) |
| `installation_date` | Date d'installation du site |
| `first_obs_utc`, `last_obs_utc` | Bornes observées |
| `coverage` | Part des heures présentes entre les bornes |
| `status` | `retenu` / `rejete` / `incertain` / `reserve_test` |
| `status_reason` | Raison du statut, en une phrase |

## 3. Règles

1. **Temps** : stockage en UTC, affichage en heure de Paris. Le comptage de « 8 h » couvre 8 h–9 h.
2. **Absences** : une heure absente reste vide. Un zéro reste un zéro. L'équipe 1 signale, elle ne corrige pas.
3. **Granularité** : comptages horaires par compteur uniquement. Les données au quart d'heure par site ne sont pas mélangées.
4. **Doublons** : une seule valeur par compteur et par heure ; les conflits sont listés dans la fiche du compteur.
5. **Versions** : un fichier livré n'est jamais écrasé ; chaque version a sa fiche dans `docs/`.
6. **Sites réservés** : la liste (`status = reserve_test`) est fixée par les équipes 1 et 4 ; personne ne l'utilise pour apprendre ou choisir un modèle.
7. **Contexte externe** (à partir de la v1) : colonnes ajoutées par jointure sur `ts_utc`, en distinguant :
   - l'information connue avant la prévision (calendrier, prévision météo publiée) ;
   - l'information observée après coup (météo mesurée), réservée à l'analyse.

## 4. Questions à trancher en réunion

- [ ] Convention de l'heure validée par les équipes 2, 4 et 5
- [ ] Seuil de `in_zero_run` (24 h ?)
- [ ] Format attendu par l'équipe 5 : fichier Parquet ou fonction Python `charger(counter_id, debut, fin)` ?
- [ ] L'équipe 2 veut-elle la météo dès la v1 ? Observée en « oracle » étiqueté, ou calendrier seul ?
- [ ] Combien de sites réservés pour l'équipe 3, et pour quand ?
- [ ] Qui livre les dates de test final (équipe 4) ?
- [ ] Canal de communication et contact « données » de chaque équipe
- [ ] Équipe 1 à deux personnes : quelle aide possible (contrôles par l'équipe 4, automatisation avec l'équipe 5) ?

## 5. Calendrier de livraison proposé

| Version | Contenu | Échéance |
|---|---|---|
| v0 | 1 compteur, flux 13 mois | Fin de matinée J1 |
| v1 | Inventaire + échantillon justifié + sites réservés | Fin de J1 / début de J2 |
| v2 | Contexte calendrier et météo joint | Milieu de J2 |
| v3 | Extension automatisée + bilan retenus / rejetés | J3 |
