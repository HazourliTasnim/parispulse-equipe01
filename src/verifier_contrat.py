"""ParisPulse – Équipe 1 – Vérifications avant de présenter le contrat de données.

A. Flux 13 mois, tout le réseau (téléchargé une fois, puis mis en cache) :
   A1 heures absentes sur tout le réseau (journées et petits trous communs)
   A2 changements d'heure          A3 doublons sur les 113 compteurs
   A4 couverture et compteurs < 90 %   A5 suites de zéros et zéros suspects (règle v1)
   A6 sens de circulation et sites      A7 faisabilité de l'estimation J-14
B. Archives 2016–2025 : liste des fichiers, format, convention horaire comparée au flux
C. Contexte : jours fériés, vacances zone C, météo prévue (Open-Meteo), météo observée (Météo-France)

Usage :  python src/verifier_contrat.py                 (tout, archives 2025 seulement)
         python src/verifier_contrat.py --sans-archives
Sorties : docs/verifications_contrat_AAAA-MM-JJ.md et docs/qualite_reseau.csv
"""
import argparse
import datetime as dt
import gzip
import io
import json
import pathlib
import re
import urllib.parse
import urllib.request
import zipfile

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW, DOCS = ROOT / "data/raw", ROOT / "docs"
TZ = "Europe/Paris"
ODS = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets"
FLUX, HIST = "comptage-velo-donnees-compteurs", "comptage-velo-historique-donnees-compteurs"
PARIS = (48.8566, 2.3522)
TODAY = dt.date.today()
LIGNES = []


def dire(t=""):
    print(t)
    LIGNES.append(str(t))


def telecharger(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ParisPulse-equipe1"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def get_json(url):
    return json.loads(telecharger(url))


def etape(titre):
    def deco(f):
        def run(*a, **k):
            dire(f"\n## {titre}")
            try:
                return f(*a, **k)
            except Exception as e:
                dire(f"- ⚠️ Étape impossible : {type(e).__name__} : {e}")
        return run
    return deco


# =============================================================== A. flux
def charger_flux():
    cache = RAW / f"flux_complet_{TODAY}.csv.gz"
    if cache.exists():
        df = pd.read_csv(cache, dtype=str)
    else:
        p = {"select": "id_compteur, nom_compteur, id, date, sum_counts", "delimiter": ";"}
        print("Téléchargement du flux complet (1 à 3 minutes)…")
        df = pd.read_csv(io.BytesIO(telecharger(f"{ODS}/{FLUX}/exports/csv?{urllib.parse.urlencode(p)}")),
                         sep=";", dtype=str)
        RAW.mkdir(parents=True, exist_ok=True)
        df.to_csv(cache, index=False)
    df["ts"] = pd.to_datetime(df["date"], utc=True, format="ISO8601")
    df["n"] = pd.to_numeric(df["sum_counts"])
    return df


@etape("A1. Heures absentes sur tout le réseau")
def trous_reseau(df):
    par_h = df.groupby("ts").size()
    grille = pd.date_range(par_h.index.min(), par_h.index.max(), freq="h")
    par_h = par_h.reindex(grille, fill_value=0)
    normal = par_h.median()
    bas = par_h < 0.5 * normal
    bloc = (bas != bas.shift()).cumsum()
    periodes = [(g.index.min(), g.index.max(), len(g)) for _, g in par_h[bas].groupby(bloc[bas])]
    dire(f"- Grille : {len(grille)} heures ; médiane {normal:.0f} compteurs présents par heure")
    dire(f"- Périodes où moins de la moitié du réseau est présente : {len(periodes)}")
    for d, f, n in periodes:
        dire(f"  - {d.tz_convert(TZ):%d/%m/%Y %H h} → {f.tz_convert(TZ):%d/%m/%Y %H h} (heure de Paris) : {n} h")
    return par_h, periodes


@etape("A2. Changements d'heure")
def changements_heure(df, par_h):
    for jour in ["2025-10-26", "2026-03-29", "2026-10-25"]:
        debut = pd.Timestamp(jour).tz_localize(TZ).tz_convert("UTC")
        fin = (pd.Timestamp(jour) + pd.Timedelta(days=1)).tz_localize(TZ).tz_convert("UTC")
        heures = pd.date_range(debut, fin, freq="h", inclusive="left")
        vals = par_h.reindex(heures, fill_value=0)
        vides = [t for t, v in vals.items() if v < 0.5 * par_h.median()]
        detail = ", ".join(f"{t.tz_convert(TZ):%H h (UTC%z)}" for t in vides[:6])
        dire(f"- {jour} : {len(heures)} heures attendues ; {len(vides)} heure(s) quasi vide(s)"
             + (f" : {detail}{' …' if len(vides) > 6 else ''}" if vides else ""))


@etape("A3. Doublons (113 compteurs)")
def doublons(df):
    dup = df[df.duplicated(["id_compteur", "ts"], keep=False)]
    dire(f"- Lignes en double : {len(dup)} ; compteurs concernés : {dup['id_compteur'].nunique()}")
    if len(dup):
        conflits = dup.groupby(["id_compteur", "ts"])["n"].nunique().gt(1).sum()
        dire(f"- Heures en double avec valeurs différentes : {conflits}")


def series(df):
    for cid, g in df.drop_duplicates(["id_compteur", "ts"]).groupby("id_compteur"):
        s = g.set_index("ts")["n"].sort_index()
        yield cid, g["nom_compteur"].iloc[0], g["id"].iloc[0], s.reindex(
            pd.date_range(s.index.min(), s.index.max(), freq="h"))


@etape("A4–A5. Couverture, suites de zéros, zéros suspects (tous les compteurs)")
def qualite(df, grille_totale):
    lignes = []
    for cid, nom, site, s in series(df):
        est_zero = s.eq(0)
        bloc = (est_zero != est_zero.shift()).cumsum()
        long = est_zero.groupby(bloc).transform("sum").where(est_zero, 0) >= 24
        runs = s[long].groupby(bloc[long]).apply(lambda x: (x.index.min(), len(x)))
        loc = s.index.tz_convert(TZ)
        cle = pd.Series(loc.hour * 10 + (loc.day_of_week >= 5), index=s.index)
        med = pd.Series(np.nan, index=s.index)
        for _, idx in cle.groupby(cle).groups.items():
            sub = s.loc[idx].dropna()
            if len(sub):
                med.loc[sub.index] = sub.rolling("28D", closed="left").median()
        suspect = est_zero & ~long & (med >= 50)
        lignes.append({
            "counter_id": cid, "nom": nom, "site_id": site,
            "heures_mesurees": int(s.notna().sum()),
            "couverture": round(s.notna().sum() / grille_totale, 4),
            "plus_long_trou_h": int(s.isna().groupby((s.notna()).cumsum()).sum().max()),
            "heures_zero_run": int(long.sum()), "nb_zero_runs": len(runs),
            "premier_zero_run": "" if not len(runs) else f"{runs.iloc[0][0].tz_convert(TZ):%d/%m/%Y} ({runs.iloc[0][1]} h)",
            "zeros_suspects": int(suspect.sum()),
            "mediane_horaire": float(s.median()),
        })
    q = pd.DataFrame(lignes).sort_values("couverture")
    q.to_csv(DOCS / "qualite_reseau.csv", index=False)
    dire(f"- Détail par compteur : `docs/qualite_reseau.csv` ({len(q)} compteurs)")
    dire(f"- Couverture < 90 % : {(q['couverture'] < 0.9).sum()} compteurs")
    for _, r in q[q["couverture"] < 0.9].iterrows():
        dire(f"  - {r['nom']} : {r['couverture']:.1%}, plus long trou {r['plus_long_trou_h']} h")
    dire(f"- Compteurs avec une suite de zéros ≥ 24 h : {(q['nb_zero_runs'] > 0).sum()} "
         f"({q['heures_zero_run'].sum()} heures au total)")
    for _, r in q[q["nb_zero_runs"] > 0].sort_values("heures_zero_run", ascending=False).head(10).iterrows():
        dire(f"  - {r['nom']} : {r['heures_zero_run']} h en {r['nb_zero_runs']} suite(s), dès le {r['premier_zero_run']}")
    dire(f"- Zéros suspects (règle v1, hors suites longues) : {q['zeros_suspects'].sum()} heures "
         f"sur {(q['zeros_suspects'] > 0).sum()} compteurs")
    for _, r in q.sort_values("zeros_suspects", ascending=False).head(8).iterrows():
        if r["zeros_suspects"]:
            dire(f"  - {r['nom']} : {r['zeros_suspects']}")
    men = q[q["nom"].str.contains("Ménilmontant", case=False)]
    for _, r in men.iterrows():
        dire(f"- Zoom {r['nom']} : {r['heures_zero_run']} h en suites longues, {r['zeros_suspects']} zéros suspects isolés")
    return q


@etape("A6. Sens de circulation et sites")
def sens(df):
    c = df.drop_duplicates("id_compteur")[["id_compteur", "nom_compteur", "id"]].copy()
    c["direction"] = c["nom_compteur"].str.extract(r"([NSEO]{1,2}-[NSEO]{1,2})\s*$", expand=False)
    dire(f"- Compteurs sans sens dans le nom : {c['direction'].isna().sum()}")
    for n in c.loc[c["direction"].isna(), "nom_compteur"].head(10):
        dire(f"  - {n}")
    par_site = c.groupby("id")
    deux = par_site.filter(lambda g: len(g) == 2).groupby("id")["direction"].apply(list)
    oppose = deux.apply(lambda d: None not in d and isinstance(d[0], str) and isinstance(d[1], str)
                        and d[0].split("-") == d[1].split("-")[::-1])
    dire(f"- Sites à 2 compteurs : {len(deux)} ; sens exactement opposés : {int(oppose.sum())}")
    for site, d in deux[~oppose].items():
        dire(f"  - site {site} : {d}")
    plus = par_site.size()[par_site.size() > 2]
    dire(f"- Sites à plus de 2 compteurs : {len(plus)}")


@etape("A7. Faisabilité de l'estimation J-14 pour les journées absentes du réseau")
def faisabilite_j14(par_h, periodes):
    normal = par_h.median()
    for d, f, n in periodes:
        if n < 20:
            continue
        for k in (14, 21, 28):
            ref = par_h.reindex(pd.date_range(d - pd.Timedelta(days=k), f - pd.Timedelta(days=k), freq="h"))
            part = (ref >= 0.5 * normal).mean()
            dire(f"- {d.tz_convert(TZ):%d/%m/%Y} : J-{k} présent à {part:.0%}")
            if part > 0.95:
                break


# =============================================================== B. archives
@etape("B. Archives 2016–2025")
def archives(flux, toutes=False):
    att = get_json(f"{ODS}/{HIST}/attachments")
    items = att.get("attachments", att.get("results", []))
    dire(f"- Pièces jointes : {len(items)}")
    for a in items:
        dire(f"  - {a.get('metas', {}).get('title') or a.get('id')} → {a.get('href', '')}")
    cibles = [a for a in items if re.search(r"compteur", json.dumps(a), re.I)
              and not re.search(r"site", (a.get("metas", {}).get("title") or ""), re.I)]
    if not toutes:
        cibles = [a for a in cibles if "2025" in json.dumps(a)][:1]
    for a in cibles:
        nom = a.get("metas", {}).get("title") or a.get("id")
        fichier = RAW / "archives" / re.sub(r"[^\w.-]", "_", nom)
        if fichier.exists():
            brut = fichier.read_bytes()
        else:
            brut = telecharger(a["href"])
            fichier.parent.mkdir(parents=True, exist_ok=True)
            fichier.write_bytes(brut)
        if brut[:2] == b"PK":
            z = zipfile.ZipFile(io.BytesIO(brut))
            brut = z.read(z.namelist()[0])
        elif brut[:2] == b"\x1f\x8b":
            brut = gzip.decompress(brut)
        encodage = "utf-8"
        try:
            brut.decode("utf-8")
        except UnicodeDecodeError:
            encodage = "latin-1"
        sep = ";" if brut[:2000].count(b";") > brut[:2000].count(b",") else ","
        arc = pd.read_csv(io.BytesIO(brut), sep=sep, dtype=str, encoding=encodage)
        dire(f"  - Encodage : {encodage} ; séparateur : « {sep} »")
        dire(f"- **{nom}** : {len(arc)} lignes ; colonnes : {list(arc.columns)}")
        col_date = next(c for c in arc.columns if "date" in c.lower() and "install" not in c.lower())
        col_id = next(c for c in arc.columns if "identifiant du compteur" in c.lower() or c == "id_compteur")
        col_n = next(c for c in arc.columns if "comptage" in c.lower() or c == "sum_counts")
        dire(f"  - Exemple de date : `{arc[col_date].iloc[0]}` (colonne « {col_date} »)")
        arc["ts"] = pd.to_datetime(arc[col_date], utc=True, format="ISO8601", errors="coerce")
        dire(f"  - Dates illisibles : {arc['ts'].isna().sum()} ; période {arc['ts'].min()} → {arc['ts'].max()}")
        dire(f"  - Compteurs : {arc[col_id].nunique()} ; doublons : {arc.duplicated([col_id, 'ts']).sum()}")
        if "2025" in nom:
            comparer_flux_archive(flux, arc.rename(columns={col_id: "id_compteur"}), col_n)


def comparer_flux_archive(flux, arc, col_n):
    cid = "100057445-104057445"
    a = arc[arc["id_compteur"] == cid].set_index("ts")[col_n].astype(float)
    f = flux[flux["id_compteur"] == cid].set_index("ts")["n"]
    commun = a.index.intersection(f.index)
    dire(f"  - Sébastopol S-N sur la période commune : {len(commun)} heures")
    for dec in (-1, 0, 1):
        ad = a.copy()
        ad.index = ad.index + pd.Timedelta(hours=dec)
        c = ad.index.intersection(f.index)
        egal = (ad.loc[c] == f.loc[c]).mean() if len(c) else float("nan")
        dire(f"    - décalage {dec:+d} h : {egal:.1%} de valeurs identiques ({len(c)} heures)")
    dire("  - Lecture : le décalage à ~100 % donne la convention de l'archive par rapport au flux.")


# =============================================================== C. contexte
@etape("C1. Jours fériés (calendrier.api.gouv.fr)")
def feries():
    j = get_json("https://calendrier.api.gouv.fr/jours-feries/metropole.json")
    annees = sorted({k[:4] for k in j})
    dire(f"- {len(j)} jours fériés, années {annees[0]} → {annees[-1]}")
    dire(f"- Exemples 2026 : {[f'{k} {v}' for k, v in j.items() if k.startswith('2026')][:4]}")


@etape("C2. Vacances scolaires zone C (data.education.gouv.fr)")
def vacances():
    url = ("https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
           "fr-en-calendrier-scolaire/exports/csv?delimiter=%3B")
    v = pd.read_csv(io.BytesIO(telecharger(url)), sep=";", dtype=str)
    dire(f"- {len(v)} lignes ; colonnes : {list(v.columns)}")
    paris = v[v.apply(lambda r: r.astype(str).str.contains("Paris").any(), axis=1)]
    col_annee = next((c for c in v.columns if "annee" in c.lower()), None)
    if col_annee:
        dire(f"- Années scolaires pour Paris : {sorted(paris[col_annee].dropna().unique())[-5:]}")
    dire(f"- Lignes Paris : {len(paris)} (à filtrer sur la population élèves)")


@etape("C3. Météo prévue : Open-Meteo, prévisions de la veille (Previous Runs API)")
def meteo_prevue():
    vars_ = "temperature_2m_previous_day1,precipitation_previous_day1,wind_speed_10m_previous_day1"
    for debut, fin in [("2025-10-11", "2026-11-09"), ("2023-06-01", "2023-06-07")]:
        p = {"latitude": PARIS[0], "longitude": PARIS[1], "hourly": vars_,
             "start_date": debut, "end_date": fin, "timezone": "GMT"}
        j = get_json("https://previous-runs-api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(p))
        h = pd.DataFrame(j["hourly"])
        rempli = h.drop(columns="time").notna().mean().round(3).to_dict()
        dire(f"- {debut} → {fin} : {len(h)} heures ; part renseignée {rempli}")
    dire(f"- Unités : {j.get('hourly_units')}")
    dire("- Lecture : `previous_day1` = prévision émise au moins 24 h avant l'heure visée, donc "
         "disponible avant 00 h du jour J pour toutes les heures de J.")


@etape("C4. Météo observée : Météo-France, horaires, département 75")
def meteo_observee():
    j = get_json("https://www.data.gouv.fr/api/1/datasets/donnees-climatologiques-de-base-horaires/")
    res = [r for r in j["resources"] if "H_75_" in (r.get("title", "") + r.get("url", ""))]
    for r in res:
        dire(f"- {r.get('title')} ({r.get('last_modified', '')[:10]})")
    dernier = next((r for r in res if "latest" in r.get("title", "") + r.get("url", "")), res[-1] if res else None)
    if dernier is None:
        dire("- Aucun fichier H_75 trouvé")
        return
    m = pd.read_csv(io.BytesIO(gzip.decompress(telecharger(dernier["url"]))), sep=";", dtype=str)
    mont = m[m["NUM_POSTE"].str.strip() == "75114001"]
    dire(f"- Fichier {dernier.get('title')} : {len(m)} lignes ; Paris-Montsouris (75114001) : {len(mont)} lignes")
    if len(mont):
        d = pd.to_datetime(mont["AAAAMMJJHH"], format="%Y%m%d%H")
        dire(f"- Période Montsouris (UTC) : {d.min()} → {d.max()}")
        for c in ["T", "RR1", "FF"]:
            if c in mont:
                dire(f"  - {c} renseigné à {pd.to_numeric(mont[c].str.replace(',', '.'), errors='coerce').notna().mean():.1%}")


# =============================================================== main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sans-archives", action="store_true")
    ap.add_argument("--toutes-archives", action="store_true")
    ap.add_argument("--seulement-archives", action="store_true")
    a = ap.parse_args()
    if a.seulement_archives:
        dire(f"# Vérification des archives – {TODAY:%d/%m/%Y}")
        archives(charger_flux(), toutes=a.toutes_archives)
        sortie = DOCS / f"verifications_archives_{TODAY}.md"
        sortie.write_text("\n".join(LIGNES), encoding="utf-8")
        print(f"\nRapport : {sortie}")
        raise SystemExit
    dire(f"# Vérifications avant le contrat – {TODAY:%d/%m/%Y}")
    flux = charger_flux()
    dire(f"\nFlux : {len(flux)} lignes, {flux['id_compteur'].nunique()} compteurs, "
         f"{flux['ts'].min().tz_convert(TZ):%d/%m/%Y %H h} → {flux['ts'].max().tz_convert(TZ):%d/%m/%Y %H h}")
    res = trous_reseau(flux)
    if res:
        par_h, periodes = res
        changements_heure(flux, par_h)
        faisabilite_j14(par_h, periodes)
    doublons(flux)
    grille = int((flux["ts"].max() - flux["ts"].min()) / pd.Timedelta(hours=1)) + 1
    qualite(flux, grille)
    sens(flux)
    if not a.sans_archives:
        archives(flux, toutes=a.toutes_archives)
    feries()
    vacances()
    meteo_prevue()
    meteo_observee()
    sortie = DOCS / f"verifications_contrat_{TODAY}.md"
    sortie.write_text("\n".join(LIGNES), encoding="utf-8")
    print(f"\nRapport : {sortie}")
