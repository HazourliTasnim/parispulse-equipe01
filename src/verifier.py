"""ParisPulse – Équipe 1 – Vérifications avant la réunion.

Lève les incertitudes de la v0 en interrogeant l'API Open Data Paris :
  1. Taille du réseau : combien de compteurs et de sites, distribution des heures
  2. Journées manquantes : sont-elles communes à tout le réseau ?
  3. Convention de l'heure : une journée manquante couvre-t-elle 00 h–23 h (début d'heure)
     ou 01 h–00 h (fin d'heure) ?
  4. Doublons : les compteurs à 9 381 heures ont-ils des heures en double ?
  5. Pics et zéros sur les 10 plus gros compteurs : pic du matin, zéros en heure chargée

Usage : python src/verifier.py
Résultat : affiché à l'écran et écrit dans docs/verifications_AAAA-MM-JJ.md
"""
import datetime as dt
import pathlib
import urllib.parse

import pandas as pd

BASE = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/comptage-velo-donnees-compteurs"
TZ = "Europe/Paris"
ROOT = pathlib.Path(__file__).resolve().parents[1]
LIGNES = []


def dire(texte=""):
    print(texte)
    LIGNES.append(texte)


def export(**params):
    """Export CSV de l'API (sans limite de lignes)."""
    params = {"delimiter": ";", "timezone": TZ, **params}
    url = f"{BASE}/exports/csv?{urllib.parse.urlencode(params)}"
    return pd.read_csv(url, sep=";", dtype=str)


# ------------------------------------------------------------ 1. réseau
def reseau():
    dire("## 1. Taille du réseau (flux 13 mois)")
    df = export(select="id_compteur, nom_compteur, id, count(*) as n_heures, sum(sum_counts) as total",
                group_by="id_compteur, nom_compteur, id")
    df["n_heures"] = df["n_heures"].astype(int)
    df["total"] = pd.to_numeric(df["total"])
    dire(f"- Compteurs : **{len(df)}** ; sites : **{df['id'].nunique()}**")
    par_site = df.groupby("id").size().value_counts().sort_index()
    dire("- Compteurs par site : " + ", ".join(f"{k} compteur(s) → {v} sites" for k, v in par_site.items()))
    mode = int(df["n_heures"].mode().iloc[0])
    dire(f"- Nombre d'heures le plus fréquent : {mode} ({(df['n_heures'] == mode).sum()} compteurs)")
    dire(f"- Au-dessus : {(df['n_heures'] > mode).sum()} ; en dessous : {(df['n_heures'] < mode).sum()} "
         f"(dont {(df['n_heures'] < 0.9 * mode).sum()} sous 90 %)")
    df.sort_values("total", ascending=False).to_csv(ROOT / "docs/inventaire_rapide.csv", index=False)
    dire("- Liste complète : `docs/inventaire_rapide.csv`")
    return df, mode


# ------------------------------------------------------------ 2 et 3. jours manquants et convention
def jours():
    dire("\n## 2. Journées manquantes et 3. convention de l'heure")
    df = export(select="count(*) as n", group_by='date_format(date, "yyyy-MM-dd") as jour')
    df["n"] = df["n"].astype(int)
    df["jour"] = pd.to_datetime(df["jour"])
    df = df.set_index("jour")["n"].sort_index()
    complet = pd.date_range(df.index.min(), df.index.max(), freq="D")
    df = df.reindex(complet, fill_value=0)
    normal = df.median()
    dire(f"- Lignes par jour sur tout le réseau : médiane {normal:.0f} (≈ compteurs × 24)")
    bas = df[df < 0.5 * normal]
    bas = bas[(bas.index != df.index.min()) & (bas.index != df.index.max())]   # bornes exclues
    if bas.empty:
        dire("- Aucune journée vide à l'échelle du réseau.")
    for jour, n in bas.items():
        avant = df.get(jour - pd.Timedelta(days=1), 0)
        apres = df.get(jour + pd.Timedelta(days=1), 0)
        dire(f"- **{jour:%d/%m/%Y}** : {n} lignes ({n / normal:.0%} d'un jour normal) ; "
             f"veille {avant / normal:.0%}, lendemain {apres / normal:.0%}")
    dire("")
    dire("Lecture pour la convention : si la journée manquante est vide de 00 h à 23 h en heure de Paris "
         "et que la veille et le lendemain sont complets (≈ 100 %), les horodatages marquent le **début** "
         "de l'heure. S'ils marquaient la fin, le lendemain perdrait une heure (≈ 96 %) et la journée "
         "manquante garderait une heure (≈ 4 %).")
    return df, normal


# ------------------------------------------------------------ 4. doublons
def doublons(reseau_df, mode):
    dire("\n## 4. Doublons")
    suspects = reseau_df[reseau_df["n_heures"] > mode].sort_values("n_heures", ascending=False).head(5)
    if suspects.empty:
        dire("- Aucun compteur au-dessus du nombre d'heures habituel.")
    for _, r in suspects.iterrows():
        d = export(select="date, sum_counts", where=f'id_compteur="{r["id_compteur"]}"')
        ts = pd.to_datetime(d["date"], utc=True, format="ISO8601")
        dup = ts[ts.duplicated(keep=False)]
        debut, fin = ts.min().tz_convert(TZ), ts.max().tz_convert(TZ)
        dire(f"- {r['nom_compteur']} ({r['n_heures']} h) : {dup.nunique()} heures en double ; "
             f"période {debut:%d/%m/%Y %H h} → {fin:%d/%m/%Y %H h}")


# ------------------------------------------------------------ 5. pics et zéros
def pics_zeros(reseau_df):
    dire("\n## 5. Pics et zéros sur les 10 plus gros compteurs")
    top = reseau_df.sort_values("total", ascending=False).head(10)
    ids = ", ".join(f'"{i}"' for i in top["id_compteur"])
    d = export(select="id_compteur, date, sum_counts", where=f"id_compteur in ({ids})")
    d["ts"] = pd.to_datetime(d["date"], utc=True, format="ISO8601").dt.tz_convert(TZ)
    d["n"] = pd.to_numeric(d["sum_counts"])
    d["h"] = d["ts"].dt.hour
    sem = d[d["ts"].dt.day_of_week < 5]
    noms = top.set_index("id_compteur")["nom_compteur"]
    dire("| Compteur | Pic matin | Pic soir | Zéros en heure chargée | Dernière heure |")
    dire("|---|---|---|---|---|")
    for cid, g in sem.groupby("id_compteur"):
        prof = g.groupby("h")["n"].mean()
        matin, soir = prof.loc[5:12].idxmax(), prof.loc[14:21].idxmax()
        charge = prof[prof > 100].index                       # heures habituellement chargées
        zeros = g[(g["n"] == 0) & g["h"].isin(charge)]
        dernier = d.loc[d["id_compteur"] == cid, "ts"].max()
        dire(f"| {noms.get(cid, cid)} | {matin} h | {soir} h | {len(zeros)} | {dernier:%d/%m %H h} |")
    dire("")
    dire("Lecture : si la majorité des compteurs culmine à 9 h, le pic de Sébastopol n'est pas une anomalie. "
         "Les zéros en heure chargée mesurent la fréquence des zéros isolés suspects.")


if __name__ == "__main__":
    dire(f"# Vérifications du {dt.date.today():%d/%m/%Y}\n")
    etapes = [("réseau", reseau), ("jours", jours)]
    res = {}
    for nom, f in etapes:
        try:
            res[nom] = f()
        except Exception as e:                       # une étape en échec n'arrête pas les autres
            dire(f"- ⚠️ Étape « {nom} » impossible : {e}")
    if "réseau" in res:
        for nom, f, args in [("doublons", doublons, res["réseau"]), ("pics", pics_zeros, res["réseau"][:1])]:
            try:
                f(*args)
            except Exception as e:
                dire(f"- ⚠️ Étape « {nom} » impossible : {e}")
    sortie = ROOT / f"docs/verifications_{dt.date.today()}.md"
    sortie.write_text("\n".join(LIGNES), encoding="utf-8")
    print(f"\nRésultats écrits dans {sortie}")
