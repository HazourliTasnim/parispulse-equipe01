# Vérifications du 10/11/2026

## 1. Taille du réseau (flux 13 mois)
- Compteurs : **113** ; sites : **82**
- Compteurs par site : 1 compteur(s) → 51 sites, 2 compteur(s) → 31 sites
- Nombre d'heures le plus fréquent : 9377 (52 compteurs)
- Au-dessus : 27 ; en dessous : 34 (dont 5 sous 90 %)
- Liste complète : `docs/inventaire_rapide.csv`

## 2. Journées manquantes et 3. convention de l'heure
- Lignes par jour sur tout le réseau : médiane 2664 (≈ compteurs × 24)
- **22/08/2026** : 0 lignes (0% d'un jour normal) ; veille 97%, lendemain 97%
- **23/09/2026** : 0 lignes (0% d'un jour normal) ; veille 97%, lendemain 97%
- **04/10/2026** : 0 lignes (0% d'un jour normal) ; veille 97%, lendemain 97%
- **25/10/2026** : 0 lignes (0% d'un jour normal) ; veille 97%, lendemain 96%

Lecture pour la convention : si la journée manquante est vide de 00 h à 23 h en heure de Paris et que la veille et le lendemain sont complets (≈ 100 %), les horodatages marquent le **début** de l'heure. S'ils marquaient la fin, le lendemain perdrait une heure (≈ 96 %) et la journée manquante garderait une heure (≈ 4 %).

## 4. Doublons
- Voie Georges Pompidou SO-NE (9381 h) : 0 heures en double ; période 11/10/2025 02 h → 09/11/2026 23 h
- Pont National SO-NE (9381 h) : 0 heures en double ; période 11/10/2025 02 h → 09/11/2026 23 h
- 62 boulevard Ney E-O (9381 h) : 0 heures en double ; période 11/10/2025 02 h → 09/11/2026 23 h
- Face au 25 quai de l'Oise NE-SO (9381 h) : 0 heures en double ; période 11/10/2025 02 h → 09/11/2026 23 h
- Face au 25 quai de l'Oise SO-NE (9381 h) : 0 heures en double ; période 11/10/2025 02 h → 09/11/2026 23 h

## 5. Pics et zéros sur les 10 plus gros compteurs
| Compteur | Pic matin | Pic soir | Zéros en heure chargée | Dernière heure |
|---|---|---|---|---|
| 67 boulevard Voltaire SE-NO | 9 h | 18 h | 0 | 09/11 23 h |
| 89 boulevard de Magenta NO-SE | 9 h | 18 h | 0 | 09/11 23 h |
| 102 boulevard de Magenta SE-NO | 9 h | 19 h | 0 | 09/11 23 h |
| 35 boulevard de Ménilmontant NO-SE | 9 h | 18 h | 71 | 09/11 23 h |
| Totem 64 Rue de Rivoli E-O | 9 h | 18 h | 0 | 09/11 23 h |
| Totem 64 Rue de Rivoli O-E | 12 h | 18 h | 1 | 09/11 23 h |
| 38 rue Turbigo SO-NE | 12 h | 18 h | 0 | 09/11 23 h |
| Quai d'Orsay E-O | 9 h | 18 h | 0 | 09/11 23 h |
| Totem 73 boulevard de Sébastopol N-S | 9 h | 18 h | 0 | 09/11 23 h |
| Totem 73 boulevard de Sébastopol S-N | 9 h | 18 h | 1 | 09/11 23 h |

Lecture : si la majorité des compteurs culmine à 9 h, le pic de Sébastopol n'est pas une anomalie. Les zéros en heure chargée mesurent la fréquence des zéros isolés suspects.