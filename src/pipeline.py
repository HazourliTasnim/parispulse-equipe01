"""Chaîne complète en une commande : python src/pipeline.py

Écrit un fichier data/processed/counts/<counter_id>.csv.gz par compteur et data/processed/meta.csv.
"""
import sources, normaliser, qualite, imputation, calendrier, meteo, assembler
from commun import PROCESSED


def main(compteurs=None):
    brut = sources.telecharger_flux(compteurs)
    df = normaliser.normaliser(brut)
    df = calendrier.colonnes_temps(df)
    df = qualite.ajouter_indicateurs(df)
    df = imputation.imputer_journees(df)
    df = imputation.imputer_heures(df, methode="à choisir après le test")
    n = len(df)
    debut, fin = df["ts_utc"].min(), df["ts_utc"].max()
    final = assembler.assembler(df, calendrier.table_calendrier(debut, fin), meteo.table_meteo(debut, fin))
    assembler.controler(final, n)
    (PROCESSED / "counts").mkdir(parents=True, exist_ok=True)
    for cid, g in final.groupby("counter_id"):
        g.to_csv(PROCESSED / "counts" / f"{cid}.csv.gz", index=False)


if __name__ == "__main__":
    main()
