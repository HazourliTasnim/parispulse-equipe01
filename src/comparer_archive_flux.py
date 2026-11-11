"""Diagnostic du recouvrement archive 2025 / flux 13 mois (oct.–déc. 2025).

Pourquoi les valeurs ne coïncident-elles à aucun décalage ? Ce script compare, pour quelques
compteurs présents dans les deux sources : valeurs alignées côte à côte, corrélation et écart
pour chaque décalage de -2 h à +2 h.

Usage : python src/comparer_archive_flux.py
Prérequis : avoir lancé verifier_contrat.py (flux en cache et archive 2025 téléchargée).
"""
import io
import pathlib
import zipfile

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
TZ = "Europe/Paris"

flux = pd.read_csv(sorted(RAW.glob("flux_complet_*.csv.gz"))[-1], dtype=str)
flux["ts"] = pd.to_datetime(flux["date"], utc=True, format="ISO8601")
flux["n"] = pd.to_numeric(flux["sum_counts"])

z = zipfile.ZipFile(next((RAW / "archives").glob("2025*compteurs*")))
arc = pd.read_csv(io.BytesIO(z.read(z.namelist()[0])), sep=",", dtype=str, encoding="latin-1")
arc["ts"] = pd.to_datetime(arc["Date et heure de comptage"], utc=True, format="mixed")
arc["n"] = pd.to_numeric(arc["Comptage horaire"].str.replace(",", "."), errors="coerce")
arc["id"] = arc["Identifiant du compteur"].str.strip()

communs = sorted(set(arc["id"]) & set(flux["id_compteur"]))
print(f"Compteurs : archive {arc['id'].nunique()}, flux {flux['id_compteur'].nunique()}, communs {len(communs)}")
print(f"Seulement dans l'archive : {arc['id'].nunique() - len(communs)} ; seulement dans le flux : "
      f"{flux['id_compteur'].nunique() - len(communs)}")
print("Exemples de valeurs brutes de l'archive :", arc["Comptage horaire"].head(5).tolist())

cibles = ["100057445-104057445"] + [c for c in communs if c != "100057445-104057445"][:4]
for cid in cibles:
    a = arc[arc["id"] == cid].set_index("ts")["n"].sort_index()
    f = flux[flux["id_compteur"] == cid].set_index("ts")["n"].sort_index()
    nom = arc.loc[arc["id"] == cid, "Nom du compteur"].iloc[0] if len(a) else cid
    print(f"\n=== {nom} ({cid}) : archive {len(a)} h, flux {len(f)} h")
    for dec in (-2, -1, 0, 1, 2):
        ad = a.copy()
        ad.index = ad.index + pd.Timedelta(hours=dec)
        c = ad.index.intersection(f.index)
        if len(c) < 24:
            continue
        x, y = ad.loc[c], f.loc[c]
        print(f"  décalage {dec:+d} h : {len(c)} h communes, identiques {(x == y).mean():.1%}, "
              f"corrélation {x.corr(y):.3f}, écart moyen {(x - y).abs().mean():.1f}, rapport médian "
              f"{(x / y.where(y > 0)).median():.2f}")
    c = a.index.intersection(f.index)[:8]
    if len(c):
        print("  Côte à côte (heure de Paris | archive | flux) :")
        for t in c:
            print(f"    {t.tz_convert(TZ):%d/%m/%Y %H h} | {a.loc[t]} | {f.loc[t]}")

# ------------------------------------------------------------- bilan sur tous les compteurs communs
lignes = []
for cid in communs:
    a = arc[arc["id"] == cid].drop_duplicates("ts").set_index("ts")["n"]
    f = flux[flux["id_compteur"] == cid].drop_duplicates("ts").set_index("ts")["n"]
    c = a.index.intersection(f.index)
    if not len(c):
        continue
    x, y = a.loc[c], f.loc[c]
    lignes.append({"counter_id": cid, "heures_communes": len(c),
                   "identiques": round((x == y).mean(), 3),
                   "rapport_median_archive_sur_flux": round((x / y.where(y > 0)).median(), 3),
                   "zeros_archive_seulement": int(((x == 0) & (y > 0)).sum()),
                   "zeros_flux_seulement": int(((y == 0) & (x > 0)).sum())})
b = pd.DataFrame(lignes)
(ROOT / "docs").mkdir(exist_ok=True)
b.to_csv(ROOT / "docs/recouvrement_archive_flux.csv", index=False)
print(f"\n=== Bilan sur {len(b)} compteurs communs (période oct.–déc. 2025)")
print(f"- Valeurs identiques à 100 % : {(b['identiques'] >= 0.999).sum()}")
print(f"- Identiques à plus de 95 % : {(b['identiques'] >= 0.95).sum()}")
ecart = b[(b["identiques"] < 0.95)]
print(f"- Différents (< 95 % identiques) : {len(ecart)}")
print(f"  dont archive plus basse de plus de 5 % (rapport médian < 0,95) : {(ecart['rapport_median_archive_sur_flux'] < 0.95).sum()}")
print(f"  dont archive plus haute de plus de 5 % (rapport médian > 1,05) : {(ecart['rapport_median_archive_sur_flux'] > 1.05).sum()}")
print(f"  dont zéros dans l'archive là où le flux a des vélos (> 24 h) : {(ecart['zeros_archive_seulement'] > 24).sum()}")
print("- Détail : docs/recouvrement_archive_flux.csv")
