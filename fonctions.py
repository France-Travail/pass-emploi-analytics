import pandas as pd
import os


def get_files(structure, path):
    all_files = os.listdir(path)
    files = [f for f in all_files if structure in f]
    dates = [f.split('_')[1].split('.')[0] for f in files]
    dates = ['{}-{}-{}'.format(d[-4:], d[-6:-4], d[:2]) for d in dates]
    return files, dates

def get_df_milo(path):
    files, dates = get_files(structure='MILO', path=path)
    df_milo_dpt = pd.DataFrame()
    for f, m in zip(files, dates):
        file = os.path.join(path, f)
        df = pd.read_excel(file, header=4)
        df_gpd = df.groupby('code_departement').agg(nb_conseillers = ('nb_conseillers_actifs', 'sum')).reset_index()
        df_gpd['mois'] = m
        df_milo_dpt = pd.concat([df_milo_dpt, df_gpd])
    df_milo_dpt['structure'] = 'MILO'
    return df_milo_dpt

def get_df_ft(path):
    files, dates = get_files(structure='FT', path=path)
    df_ft_dpt = pd.DataFrame()
    for f, m in zip(files, dates):
        file = os.path.join(path, f)
        df = pd.read_excel(file, header=2)
        check = df.iloc[-1]['Nb conseillers']
        df['DT'] = df['DT'].replace({
            'Total DT DT BASSE-TERRE ET MGTE': 'Total DT DT BASSE-TERRE ET MGTE 971',
            'Total DT Direction Territoriale' : 'Total 972',
            'Total DT DIRECTION DU RESEAU': 'Total 976',
            'Total DT GARD LOZERE': 'Total DT GARD 30',
            'Total DT AUDE - ARIEGE': 'Total DT AUDE - 11'
        })
        df = df[~df['DT'].isin(['Total DT DT 2A 2B CORSE', 'Total DT DT 0405 - Alpes'])]
        df.loc[df['Agence'].isin(['AJACCIO', 'PROPRIANO']), 'code_departement'] = '2A'
        df.loc[df['Agence'].isin(['BASTIA', 'ILE ROUSSE', 'PLAINE ORIENTALE']), 'code_departement'] = '2B'
        if m == "2024-07-31":
            df.loc[df['Agence'].isin(['BRIANCON', 'GAP']), 'code_departement'] = '05'
            df.loc[df['Agence'].isin(['DIGNE', 'MANOSQUE']), 'code_departement'] = '04'
        df = df[
            (df['DT'].apply(lambda x: 'total' in str(x).lower() if x==x else False)) | 
            (df['code_departement'].notnull())
        ]
        df.loc[df['code_departement'].isna(), 'code_departement'] = df['DT'].apply(
            lambda x: "".join([s for s in x.split() if s.isdigit()])
        ).replace({'0': '973'})
        df_gpd = df.groupby('code_departement').agg(nb_conseillers = ("Nb conseillers", 'sum')).reset_index()
        df_gpd['mois'] = m
        if  df_gpd['nb_conseillers'].sum() == check:
            pass
        else:
            print('Erreur traitement fichier FT pour le mois ', m)
            print('Valeur attendue : ' , check, ' conseillers')
            print('Valeur obtenue après aggrégation : ',  df_gpd['nb_conseillers'].sum())
            break
        df_ft_dpt = pd.concat([df_ft_dpt, df_gpd])
    df_ft_dpt['structure'] = 'POLE_EMPLOI'
    return df_ft_dpt

def get_df_aij(path):
    #lecture referentiel
    table = pd.read_csv('referentiel_dpt.csv')
    files, dates = get_files(structure='AIJ', path=path)
    df_aij_dpt = pd.DataFrame()
    for f, m in zip(files, dates):
        file = os.path.join(path, f)
        df_aij = pd.read_excel(file)
        df_aij = df_aij[df_aij['DEPARTEMENT'].notnull()].merge(table, left_on='DEPARTEMENT', right_on='dpt')
        df_aij = df_aij.groupby('code_departement').agg(nb_conseillers = ("Nb ptf AIJ IND", 'sum')).reset_index()
        df_aij['code_departement'] = df_aij['code_departement'].apply(lambda x: x.zfill(2))
        df_aij['mois'] = m
        df_aij_dpt = pd.concat([df_aij_dpt, df_aij])
    df_aij_dpt['structure'] = 'POLE_EMPLOI_AIJ'
    return df_aij_dpt

def get_df_brsa(path):
    files, dates = get_files(structure='BRSA', path=path)
    df_brsa_dpt = pd.DataFrame()
    for f, m in zip(files, dates):
        file = os.path.join(path, f)
        df = pd.read_excel(file, header=2)
        check = df[df['Département'] == 'Total']['Nb de conseiller'].sum()
        df['Département'] = df['Département'].replace(
            {
                'Corse': 'Haute-Corse',
                'Bas-Rhin (CEA)': 'Bas-Rhin',
                'Côte d\'Or': 'Côte-d\'Or',
                'Métropole de Lyon': 'Rhône',
                'Nouveau Rhône': 'Rhône',
                'Réunion (La)': 'La Réunion',
                'Seine maritime': 'Seine-Maritime',
            }
        )
        df = df[df['Département'] != 'Total']
        table = pd.read_csv('referentiel_dpt.csv')
        df = df[df['Département'].notnull()].merge(table, how='outer', left_on='Département', right_on='dpt')
        df = df.groupby('code_departement').agg(nb_conseillers = ("Nb de conseiller", 'sum')).reset_index()
        df['code_departement'] = df['code_departement'].apply(lambda x: x.zfill(2))
        df['mois'] = m
        if df['nb_conseillers'].sum() != check:
            print('Erreur traitement fichier FT pour le mois ', m)
            print('Valeur attendue : ' , check, ' conseillers')
            print('Valeur obtenue après aggrégation : ',  df['nb_conseillers'].sum())
            break
        else:
            pass
        df_brsa_dpt = pd.concat([df_brsa_dpt, df])
    df_brsa_dpt['structure'] = 'POLE_EMPLOI_BRSA'
    df_brsa_dpt['nb_conseillers'] = df_brsa_dpt['nb_conseillers'].apply(int)
    return df_brsa_dpt

def write_dfs_conseiller(path):
    df_ft = get_df_brsa(path)
    df_milo = get_df_brsa(path)
    df_aij = get_df_brsa(path)
    df_brsa = get_df_brsa(path)
    full_df = pd.concat([df_ft, df_milo, df_aij, df_brsa])
    full_df['nb_conseillers'] = full_df['nb_conseillers'].apply(int)
    # DF par départements
    full_df.to_csv("conseillers_par_departement.csv")
    # DF national
    df_national = pd.read_csv('evolution_conseillers_structure_national.csv')
    df_national = pd.concat([
        df_national,
        full_df.groupby(['mois', 'structure']).sum()[['nb_conseillers']].reset_index().rename(
            {
                'nb_conseillers': "Nb Conseillers Cej",
                'mois': 'Mois',
                'structure': 'Structure'
            }, 
            axis=1)
    ]).drop_duplicates()
    df_national.to_csv('evolution_conseillers_structure_national.csv', index=False)
