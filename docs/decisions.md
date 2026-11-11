# Journal des décisions – Équipe 1

| Date | Décision | Raison | Qui |
|---|---|---|---|
| 10/11 | Dépôt : `data/raw/` non versionné, fichiers livrés versionnés | Le brut se retélécharge ; les livrables doivent être partagés | Équipe |
| 10/11 | Stockage du temps en UTC (`ts_utc`), affichage en heure de Paris (`ts_local`) | Évite les heures manquantes ou doublées aux changements d'heure | Équipe |
| 10/11 | Compteur de démarrage v0 : Totem 73 bd de Sébastopol S-N | Plus fort volume du réseau, couverture quasi maximale | Équipe |
| 10/11 | v0 livrée : couverture 98,9 %, 0 doublon, aucune suite de zéros ≥ 24 h | Chaîne complète validée sur un cas simple | Nihed |
| 10/11 | 4 journées absentes sur tout le réseau (22/08, 23/09, 04/10, 25/10/2026) | Vérifié sur les 113 compteurs : trous de publication de la Ville | Nihed |
| 10/11 | Le 25/10/2026 (passage à l'heure d'hiver) est absent ; 1 h manque le 26/10/2025 | La source gère mal les journées de 25 h | Nihed |
| 10/11 | Convention de l'heure : on garde l'horodatage de la Ville | Documentation muette, données non concluantes ; sans effet sur les scores si tout le monde l'utilise | Équipe |
| 10/11 | Pas de doublons sur les compteurs à 9 381 h | Vérifié sur 5 compteurs | Nihed |
| 10/11 | Format de livraison : CSV (compressé, un fichier par compteur pour la version finale) | Format demandé ; limite de 100 Mo par fichier sur GitHub | Équipe |
| 10/11 | Sens de circulation : comptages horaires par compteur avec sens, jamais mélangés au quart d'heure par site ; sens d'un même site réservés ensemble | Règles du sujet | Équipe |
| 10/11 | Journées manquantes : estimation à J-14 (puis J-21, J-28) dans `count_filled`, marquée `is_imputed` | Même jour de la semaine, information passée uniquement | Équipe |
| 10/11 | Heures isolées manquantes : méthode choisie par un test (M1 à M4) sur des heures masquées | Choisir la plus précise plutôt que supposer | Équipe |
| 10/11 | Zéros suspects laissés à zéro et signalés par `is_zero_suspect` | Le sujet interdit de les remplacer automatiquement ; traitement décidé par une expérience | Équipe |
| 10/11 | `count` n'est jamais modifié ; l'erreur se calcule sur les heures réellement mesurées | Le sujet demande l'erreur « sur les heures réellement mesurées » | Équipe |
| 10/11 | Zéro isolé suspect sur Sébastopol S-N le 07/04/2026 à 16 h ; 71 zéros en heure chargée à Ménilmontant NO-SE | Cas d'étude pour l'approfondissement | Nihed |
| 11/11 | L'équipe compte 4 membres : rôles R1 (réseau et sélection), R2 (enrichissement), R3 (extraction extensible), R4 (qualité et horodatage) | Répartition proposée par l'énoncé | Équipe |
| 11/11 | Trous communs au réseau confirmés : 26/10/2025 2 h (heure doublée), 02/07 et 06/07/2026 0 h–2 h, 4 journées | `verifier_contrat.py` sur les 113 compteurs | Nihed |
| 11/11 | 0 doublon sur les 113 compteurs ; sens opposés sur les 31 sites bidirectionnels | `verifier_contrat.py` | Nihed |
| 11/11 | Couverture mesurée depuis la première mesure + ancienneté séparée | Les 5 compteurs « sous 90 % » sont récents, pas en panne | Nihed |
| 11/11 | 106 av. Denfert-Rochereau NE-SO candidat `rejete` | Zéro partout dans le flux et l'archive | Nihed |
| 11/11 | Archive 2025 : même convention horaire que le flux | Valeurs identiques sans décalage sur 57 compteurs | Nihed |
| 11/11 | Archive utilisée au niveau compteur seulement si elle concorde avec le flux ; le flux fait foi | 48 des 56 compteurs bidirectionnels diffèrent (un sens quasi vide dans l'archive) ; 49 des 50 unidirectionnels concordent | Nihed |
| 11/11 | Météo prévue : Open-Meteo `previous_day1` ; observée : Météo-France Montsouris ; unités °C, mm, m/s | Bulletin disponible avant la date de prévision ; vérifié à 100 % sur la période du flux | Nihed |
| 11/11 | Règle des zéros suspects à calibrer avant la v1 | 1 123 h sur 58 compteurs, dont des fermetures probablement réelles | Nihed |
