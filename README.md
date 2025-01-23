# Mise à jour des données pour le suivi des taux de pénétration

###1. Configuration
- installer python et cloner le projet en local
- installer pandas : `pip install pandas` ou `python -m pip install pandas`

###2. Récupération des données
- Bénéficiaires : https://poem.travail-emploi.gouv.fr/donnee/contrat-dengagement-jeune-en-missions-locales-stocks => "Exporter les Séries du dispositif" => dézipper et enregistrer en écrasant les fichiers précédents dans data_beneficiaire
- Conseillers : fichiers reçus par mail via l'adresse statistiques@pass-emploi.beta.gouv.fr => enregistrer dans data_conseiller en renommant {structure}_{date_fin_du_mois}.xlsx
  - Milo : fichier reçu chaque semaine => prendre celui le plus proche de la fin du mois
  - FT : fichier reçu chaque mois autour du 10
  - BRSA : A confirmer
  - AIJ : A mettre en place

###3. Exécution
`python main.py`

###4. MAJ sur metabase
Uploader via "Remplacer toutes les données de ce modèle"
   - `conseillers_par_departement.csv` => https://stats.pass-emploi.beta.gouv.fr/model/686-conseillers-par-departement
   - `evolution_conseillers_structure_national.csv` => https://stats.pass-emploi.beta.gouv.fr/model/1008-evolution-conseillers-structure-national
   - `stock jeunes par departement.csv` => https://stats.pass-emploi.beta.gouv.fr/model/538-stock-jeunes-par-departement
     
