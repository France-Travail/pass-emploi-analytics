import pandas as pd
import os


def write_df_beneficiaire(path):
    path_ml = os.path.join(path, "CEJ_ML_stk.xlsx")
    path_ft = os.path.join(path, "CEJ_PE_stk.xlsx")
    df_ml = pd.read_excel(path_ml, sheet_name="Département", skiprows=1)
    df_ft = pd.read_excel(path_ft, sheet_name="Département", skiprows=1)
    df_ml["structure"] = "MILO"
    df_ft["structure"] = "POLE_EMPLOI"
    df = pd.concat([df_ml, df_ft])
    df_pivoted = df.melt(
        id_vars=["structure", "Code_Département"],
        var_name="mois",
        value_name="nb_jeunes_cej",
        value_vars=[
            col
            for col in df.columns
            if col
            not in [
                "Code_Région",
                "Libellé_Région",
                "Code_Département",
                "Libellé_Département",
            ]
        ],
    )
    df_pivoted["mois"] = df_pivoted["mois"] + "-01"
    df_pivoted["nb_jeunes_cej"] = df_pivoted["nb_jeunes_cej"].replace({"-": 0})
    df_pivoted = df_pivoted.sort_values(
        ["mois", "structure", "Code_Département"]
    )
    df_pivoted.to_csv("outputs/stock_jeunes_par_departement.csv", index=None)
