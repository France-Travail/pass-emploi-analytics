from fonctions import write_dfs_conseiller, write_df_beneficiaire


path_conseiller = 'data_conseiller/'
path_beneficiaire = 'data_beneficiaire/'

print('Ecriture fichiers conseiller...')
write_dfs_conseiller(path_conseiller)
print('OK')

print('Ecriture fichier beneficiaire...')
write_df_beneficiaire(path_beneficiaire)
print('OK')