from write_df_beneficiaire import write_df_beneficiaire
from write_df_conseiller import write_df_conseiller


path_conseiller = "inputs/data_conseiller/"
path_beneficiaire = "inputs/data_beneficiaire/"

print("Ecriture fichiers conseiller...")
write_df_conseiller(path_conseiller)
print("OK")

print("Ecriture fichier beneficiaire...")
write_df_beneficiaire(path_beneficiaire)
print("OK")
