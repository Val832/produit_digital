# Projet d'évaluation du prix d'un bien immobilier dans Paris dans l'application Airbnb

## Objectif

Créer une application qui a pour but d'estimer le prix de votre bien immobilier situé à Paris sur l'application Airbnb.  Elle vous permettra de proposer votre logement au juste prix en fonction des caractéristiques et de la localité de votre bien.

## Détails des dossiers et fichiers

VBA : Dossier contenant le fichier Excel FormulaireAIRBNB.xlsm
data : Dossier contenant des fichiers de nettoyage de la base de données
src : Dossier source. Il contient deux sous-dossiers : 
- data_science : Sous-dossier contenant les scripts pour réaliser le modèle.
- df_manipulation : Sous-dossier contenant les scripts pour la transformation de la base.
tests : Dossier contenant les tests unitaires.
utils : Dossier contenant un fichier txt donnant la liste des variables indicatrices créées dans la base de données.
venv : Dossier contenant l'environnement virtuel
README.txt : Fichier présentant l'organisation du projet et aidant à la manipulation des fichiers.
requirements.txt : Fichier listant les packages Python requis pour pouvoir utiliser l'application.  

De plus, un dictionnaire des variables de la base de données est disponible dans le wiki. 

## Prise en main de l'application

### Objectif : Recueillir un certain nombre de caractéristiques sur votre logement pour pouvoir fournir celles-ci à l'algorithme de prédiction qui vous fournira ensuite une estimation de votre bien immobilier.

### Étapes : 
i. Dans la feuille Dashboard du fichier Excel FormulaireAIRBNB.xlsm, cliquez sur le bouton « Estimer le prix d'une nuit dans mon bien à Paris, sur AirBNB ».
ii. Renseignez les différentes informations demandées sur votre logement.
iii. Cliquez sur Valider dans le formulaire pour voir apparaître le prix auquel vous pouvez louer votre bien pour une nuit.

## Détails des étapes de développement

1. ## Préparation de la base de données

- ### Objectif : Disposer d'une base de données claire qui permet ensuite de choisir les variables explicatives à prendre.

- ### Étapes : 
i. Sélectionner les variables choisies utiles à la prédiction du prix et standardiser le nom de ces variables.
ii. Corriger les valeurs manquantes et les valeurs extrêmes. 
iii. Créer des nouvelles variables indicatrices qui affichent 1 si cette caractéristique est présente dans la description de ce bien ou 0 sinon. 

2. ## Réaliser l'algorithme de prédiction

- ### Objectif : Prédire le prix d'un bien en fonction de plusieurs variables explicatives données par l'utilisateur dans le formulaire.

- ### Étapes : 
i. Réaliser plusieurs modèles de prédiction : régression linéaire, Ridge, LASSO et XGBOOST.
ii. Comparer leurs performances pour déterminer lequel de ces modèles est le plus efficace.
iii. Réaliser des tests unitaires pour valider la robustesse de l'algorithme choisi.

## Remarques importantes :

Veillez à activer votre environnement virtuel si vous en avez un :
# Sur Mac / Linux
source venv/bin/activate
# Sur Windows
.\venv\Scripts\activate

Assurez-vous que toutes les dépendances requises sont installées en utilisant
pip install -r requirements.txt
