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
