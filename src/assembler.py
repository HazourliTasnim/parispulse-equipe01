"""Jointures et contrôles finaux. Responsables : les deux."""
from commun import CLE, COLONNES


def assembler(comptages, calendrier, meteo):
    """Joint sur CLE (comptages), date_local (calendrier), ts_utc (météo) ; ordonne selon COLONNES."""
    raise NotImplementedError


def controler(df, n_lignes_avant):
    """Contrôles de livraison : clé unique, nombre de lignes inchangé, colonnes du contrat présentes,
    toute estimation marquée is_imputed. Lève une erreur claire au premier problème."""
    assert not df.duplicated(CLE).any(), "Clé (counter_id, ts_utc) en double"
    assert len(df) == n_lignes_avant, "Une jointure a ajouté ou retiré des lignes"
    manquantes = set(COLONNES) - set(df.columns)
    assert not manquantes, f"Colonnes manquantes : {sorted(manquantes)}"
    assert not (df["count_filled"].notna() & df["count"].isna() & ~df["is_imputed"]).any(), \
        "Valeur estimée non marquée"
