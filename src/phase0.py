"""ParisPulse – Équipe 1 – Phase 0.

Extrait UN compteur du flux récent Open Data Paris, le met au format du
contrat de données, lance les contrôles et produit une fiche de livraison.

Usage :
  python src/phase0.py lister                      # classement des compteurs
  python src/phase0.py extraire --compteur ID      # via l'API
  python src/phase0.py extraire --fichier brut.csv --compteur ID  # export manuel

Dépendances : pandas, matplotlib, tabulate
"""
import argparse
import datetime as dt
import pathlib
import sys
import urllib.parse

import numpy as np
import pandas as pd

BASE = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets"
DS = "comptage-velo-donnees-compteurs"
TZ = "Europe/Paris"
SEUIL_ZEROS_H = 24          # suite de zéros considérée comme « longue »
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, OUT, DOCS = ROOT / "data/raw", ROOT / "data/processed", ROOT / "docs"

# Noms techniques (API) et libellés (exports du site / archives) -> contrat
COLONNES = {
    "id_compteur": "counter_id", "Identifiant du compteur": "counter_id",
    "nom_compteur": "counter_name", "Nom du compteur": "counter_name",
    "id": "site_id", "Identifiant du site de comptage": "site_id",
    "name": "site_name", "Nom du site de comptage": "site_name",
    "sum_counts": "count", "Comptage horaire": "count",
    "date": "date_source", "Date et heure de comptage": "date_source",
    "installation_date": "installation_date",
    "Date d'installation du site de comptage": "installation_date",
    "coordinates": "coordinates", "Coordonnées géographiques": "coordinates",
}


def url_api(chemin, **params):
    return f"{BASE}/{DS}/{chemin}?{urllib.parse.urlencode(params)}"


# ---------------------------------------------------------------- lister
def lister(n=40):
    """Classe les compteurs par volume et nombre d'heures (aide au choix)."""
    url = url_api(
        "records",
        select="id_compteur, nom_compteur, sum(sum_counts) as total, count(*) as n_heures",
        group_by="id_compteur, nom_compteur",
        order_by="total desc", limit=n,
    )
    print("Requête :", url, "\n")
    df = pd.read_json(url)["results"].apply(pd.Series)
    df["moy_horaire"] = (df["total"] / df["n_heures"]).round(1)
    print(df.to_string(index=False))
    print("\nChoisir un compteur à fort volume ET n_heures proche du maximum.")


# ---------------------------------------------------------------- lecture
def lire_brut(compteur, fichier=None):
    today = dt.date.today().isoformat()
    if fichier:
        brut = pd.read_csv(fichier, sep=None, engine="python", dtype=str)
        provenance = f"fichier manuel {pathlib.Path(fichier).name}"
    else:
        url = url_api("exports/csv", where=f'id_compteur="{compteur}"', delimiter=";")
        print("Téléchargement :", url)
        brut = pd.read_csv(url, sep=";", dtype=str)
        provenance = f"API {DS}"
    RAW.mkdir(parents=True, exist_ok=True)
    chemin = RAW / f"{DS}_{compteur}_{today}.csv"
    brut.to_csv(chemin, index=False)          # copie brute, jamais modifiée
    return brut, f"{provenance}, extrait le {today}", chemin


# ---------------------------------------------------------------- normalisation
def normaliser(brut, compteur, provenance):
    alertes = []
    df = brut.rename(columns={c: COLONNES[c] for c in brut.columns if c in COLONNES})
    manquantes = {"counter_id", "count", "date_source"} - set(df.columns)
    if manquantes:
        sys.exit(f"Colonnes introuvables : {manquantes}. Colonnes lues : {list(brut.columns)}")
    df = df[df["counter_id"].astype(str) == str(compteur)].copy()
    if df.empty:
        sys.exit(f"Aucune ligne pour le compteur {compteur}.")

    # Horodatage : on exige un décalage explicite pour convertir en UTC.
    exemple = str(df["date_source"].iloc[0])
    avec_decalage = exemple.endswith("Z") or exemple[-6] in "+-"
    if avec_decalage:
        df["ts_utc"] = pd.to_datetime(df["date_source"], utc=True, format="ISO8601")
    else:
        alertes.append("Dates SANS fuseau : interprétées en heure de Paris (à confirmer).")
        loc = pd.to_datetime(df["date_source"], format="ISO8601")
        df["ts_utc"] = loc.dt.tz_localize(TZ, ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")
        if df["ts_utc"].isna().any():
            alertes.append(f"{df['ts_utc'].isna().sum()} heures ambiguës au changement d'heure écartées.")
            df = df.dropna(subset=["ts_utc"])
    if (df["ts_utc"].dt.minute != 0).any():
        alertes.append("Horodatages hors de l'heure pile : granularité à vérifier.")

    df["count"] = pd.to_numeric(df["count"], errors="coerce")
    if (df["count"] < 0).any():
        alertes.append(f"{(df['count'] < 0).sum()} valeurs négatives.")

    # Doublons : même heure plusieurs fois
    dup = df[df.duplicated("ts_utc", keep=False)]
    n_dup = dup["ts_utc"].nunique()
    conflits = int((dup.groupby("ts_utc")["count"].nunique() > 1).sum()) if n_dup else 0
    if n_dup:
        alertes.append(f"{n_dup} heures en double, dont {conflits} avec des valeurs différentes "
                       "(première valeur gardée).")
    df = df.sort_values("ts_utc", kind="stable").drop_duplicates("ts_utc", keep="first")

    # Grille horaire complète -> heures absentes explicites
    grille = pd.DataFrame({"ts_utc": pd.date_range(df["ts_utc"].min(), df["ts_utc"].max(),
                                                   freq="h", tz="UTC")})
    serie = grille.merge(df[["ts_utc", "count"]], on="ts_utc", how="left")
    serie["is_missing"] = serie["count"].isna()

    # Longues suites de zéros (signalées, jamais remplacées)
    est_zero = serie["count"].eq(0)
    bloc = (est_zero != est_zero.shift()).cumsum()
    longueur = est_zero.groupby(bloc).transform("sum").where(est_zero, 0)
    serie["in_zero_run"] = longueur >= SEUIL_ZEROS_H

    premiere = df.iloc[0]
    serie.insert(0, "counter_id", str(compteur))
    serie.insert(1, "site_id", str(premiere.get("site_id", "")))
    serie["ts_local"] = serie["ts_utc"].dt.tz_convert(TZ)
    serie["source"] = provenance
    serie = serie[["counter_id", "site_id", "ts_utc", "ts_local", "count",
                   "is_missing", "in_zero_run", "source"]]

    lat = lon = np.nan
    coord = premiere.get("coordinates")
    if isinstance(coord, str) and "," in coord:
        lat, lon = (float(x) for x in coord.split(",")[:2])
    meta = {
        "counter_id": str(compteur), "site_id": str(premiere.get("site_id", "")),
        "counter_name": premiere.get("counter_name", ""), "site_name": premiere.get("site_name", ""),
        "lat": lat, "lon": lon, "installation_date": premiere.get("installation_date", ""),
        "first_obs_utc": serie["ts_utc"].min(), "last_obs_utc": serie["ts_utc"].max(),
        "coverage": round(1 - serie["is_missing"].mean(), 4),
        "status": "retenu", "status_reason": "compteur de démarrage (phase 0)",
    }
    return serie, meta, alertes, {"n_dup": n_dup, "conflits": conflits}


# ---------------------------------------------------------------- contrôles
def trous(serie):
    m = serie["is_missing"]
    bloc = (m != m.shift()).cumsum()
    g = serie[m].groupby(bloc[m])["ts_local"].agg(["min", "max", "size"])
    g = g.rename(columns={"min": "debut", "max": "fin", "size": "heures"})
    return g.reset_index(drop=True)


def plus_longue_suite_zeros(serie):
    z = serie["count"].eq(0)
    bloc = (z != z.shift()).cumsum()
    tailles = serie[z].groupby(bloc[z]).agg(debut=("ts_local", "min"), heures=("ts_local", "size"))
    return tailles.sort_values("heures", ascending=False).head(1)


def profil(serie):
    s = serie.dropna(subset=["count"]).copy()
    s["heure"] = s["ts_local"].dt.hour
    s["type_jour"] = np.where(s["ts_local"].dt.day_of_week < 5, "semaine", "week-end")
    return s.pivot_table(index="heure", columns="type_jour", values="count", aggfunc="mean")


def controles(serie, alertes):
    p = profil(serie)
    if "semaine" in p:
        matin = p["semaine"].loc[5:12].idxmax()
        soir = p["semaine"].loc[14:21].idxmax()
        if not (7 <= matin <= 9 and 16 <= soir <= 19):
            alertes.append(f"Pics en semaine à {matin} h et {soir} h (attendu ~8 h et ~18 h) : "
                           "vérifier le fuseau et la convention de l'heure.")
    # Changements d'heure : heures réellement présentes ces jours-là (23 et 25 attendus)
    obs = serie[~serie["is_missing"]]
    jours = obs.groupby(obs["ts_local"].dt.date).size()
    tous = serie.groupby(serie["ts_local"].dt.date).size()
    jours_dst = tous[tous.isin([23, 25])]
    ecarts = {d: (int(jours.get(d, 0)), int(n)) for d, n in jours_dst.items()}
    return p, ecarts


# ---------------------------------------------------------------- sorties
def figures(serie, p, compteur):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(13, 4))
    s = serie.set_index("ts_local")["count"]
    dernier = s.index.max()
    # Lundi 0 h de la dernière semaine (partielle) -> on trace la semaine pleine d'avant
    fin = dernier.normalize() - pd.Timedelta(days=dernier.day_of_week)
    if dernier.hour == 23 and dernier.day_of_week == 6:
        fin = fin + pd.Timedelta(days=7)   # la dernière semaine est déjà complète
    debut = fin - pd.Timedelta(days=7)
    s[debut:fin - pd.Timedelta(hours=1)].plot(
        ax=ax[0], title=f"Semaine du {debut:%d/%m/%Y} (lundi → dimanche)")
    p.plot(ax=ax[1], marker="o", title="Profil horaire moyen (heure de Paris)")
    ax[1].set_xticks(range(0, 24, 2))
    fig.tight_layout()
    chemin = OUT / f"phase0_{compteur}.png"
    fig.savefig(chemin, dpi=110)
    return chemin


def ecrire_fiche(serie, meta, alertes, stats, p, ecarts, chemins):
    t, z = trous(serie), plus_longue_suite_zeros(serie)
    lignes = [
        f"# Compteur v0 : {meta['counter_name']}",
        "",
        f"- **counter_id** : `{meta['counter_id']}` ; **site_id** : `{meta['site_id']}` ({meta['site_name']})",
        f"- **Coordonnées** : {meta['lat']}, {meta['lon']} ; installation : {meta['installation_date']}",
        f"- **Période (heure de Paris)** : {serie['ts_local'].min()} → {serie['ts_local'].max()}",
        f"- **Provenance** : {serie['source'].iloc[0]}",
        f"- **Couverture** : {meta['coverage']:.2%} des heures ({serie['is_missing'].sum()} absentes, "
        f"{len(t)} trous)",
        f"- **Doublons** : {stats['n_dup']} heures, dont {stats['conflits']} en conflit",
        f"- **Plus longue suite de zéros** : "
        + (f"{int(z['heures'].iloc[0])} h à partir du {z['debut'].iloc[0]}" if len(z) else "aucune"),
        f"- **Heures dans une suite ≥ {SEUIL_ZEROS_H} h de zéros** : {int(serie['in_zero_run'].sum())}",
        f"- **Changements d'heure (heures présentes / attendues)** : "
        + (", ".join(f"{d} : {a}/{b}" for d, (a, b) in ecarts.items()) or "aucun dans la période"),
        "",
        "## Alertes",
        *([f"- {a}" for a in alertes] or ["- Aucune"]),
        "",
        "## Trous (heure de Paris)",
        t.head(20).to_markdown(index=False) if len(t) else "Aucun",
        "",
        "## Profil horaire moyen",
        p.round(1).to_markdown(),
        "",
        "## Fichiers livrés",
        *[f"- `{c.relative_to(ROOT)}`" for c in chemins],
        "",
        "## Conventions",
        "- `ts_utc` = début de l'heure en UTC ; `ts_local` = même instant à Paris.",
        "- `count` vide = mesure absente ; un zéro reste un zéro.",
        f"- `in_zero_run` = zéro dans une suite d'au moins {SEUIL_ZEROS_H} h (signalé, non corrigé).",
        "- Limites : flux 13 mois seulement, pas de météo ni d'archives.",
    ]
    chemin = DOCS / f"fiche_compteur_{meta['counter_id']}.md"
    chemin.write_text("\n".join(lignes), encoding="utf-8")
    return chemin


def extraire(compteur, fichier=None):
    for d in (OUT, DOCS):
        d.mkdir(parents=True, exist_ok=True)
    brut, provenance, chemin_brut = lire_brut(compteur, fichier)
    serie, meta, alertes, stats = normaliser(brut, compteur, provenance)
    p, ecarts = controles(serie, alertes)
    today = dt.date.today().isoformat()
    f_counts = OUT / f"counts_v0_{today}.csv"
    f_meta = OUT / f"meta_v0_{today}.csv"
    # CSV : virgule, UTF-8, dates ISO 8601 avec décalage, case vide = valeur absente
    serie.to_csv(f_counts, index=False, encoding="utf-8")
    pd.DataFrame([meta]).to_csv(f_meta, index=False, encoding="utf-8")
    f_png = figures(serie, p, compteur)
    fiche = ecrire_fiche(serie, meta, alertes, stats, p, ecarts,
                         [chemin_brut, f_counts, f_meta, f_png])
    print(f"\nFiche : {fiche}\nAlertes :", *(alertes or ["aucune"]), sep="\n- ")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("action", choices=["lister", "extraire"])
    ap.add_argument("--compteur")
    ap.add_argument("--fichier", help="CSV téléchargé à la main si l'API ne répond pas")
    a = ap.parse_args()
    if a.action == "lister":
        lister()
    else:
        if not a.compteur:
            ap.error("--compteur est obligatoire pour extraire")
        extraire(a.compteur, a.fichier)
