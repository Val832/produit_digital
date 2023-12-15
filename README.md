# 🏡 Projet de Prédiction des Prix de Location Airbnb à Paris

## 🎯 Description du Projet

### Objectifs
- Développer un outil 🛠️ avancé pour la prédiction des prix de location des logements Airbnb à Paris.
- Fournir des estimations 💸 précises des prix à la nuitée, basées sur les caractéristiques détaillées de chaque logement.
- Cible les chercheurs 🧑‍🔬, décideurs politiques 🏛️, journalistes 📰, analystes de marché 📈 et les particuliers souhaitant optimiser la valeur de leur bien à la location sur Airbnb.

### Fonctionnalités et Méthodologie
- **Estimations Personnalisées** 📋: Utilisation d'un formulaire pour permettre aux utilisateurs de recevoir des estimations basées sur des critères spécifiques.
- **Interface Utilisateur en VBA** 🖥️: Création d'une interface conviviale pour la saisie des données et l'affichage des résultats.
- **Traitement des Données en Excel** 📊: Analyse et traitement des données pour une approche robuste.

### Problématique
- Comble la lacune de l'outil d'estimation de prix proposé par Airbnb, en offrant des prévisions plus précises et détaillées 🎯.

## 📚 Utilisation et Sources des Données

### Source des Données : Inside Airbnb
- **Provenance** 🌐: Les données proviennent d'Inside Airbnb, une initiative indépendante offrant des analyses détaillées des listings Airbnb.
- **Contenu** 📄: Informations détaillées sur les listings parisiens, y compris emplacement, fréquence de location et revenus des hôtes.
- **Fiabilité** ✔️: Données régulièrement mises à jour pour garantir leur exactitude et pertinence.

Pour accéder à la base de données, visitez [Inside Airbnb](http://insideairbnb.com/get-the-data.html).

## 🛠️ Configuration et Utilisation

### Prérequis
Il est recommandé d'utiliser un environnement virtuel Python 🐍 pour gérer les dépendances du projet. Suivez ces étapes pour le configurer :

```bash
# Installation du package virtualenv
pip install virtualenv

# Création et activation de l'environnement virtuel
python3 -m venv env
source env/bin/activate

# Installation des dépendances
pip install -r requirements.txt
```

## 📂 Structure du Projet

- **VBA** 📁: Contient le fichier Excel `FormulaireAIRBNB.xlsm` pour l'interface utilisateur.
- **config** 📁: Inclut les URL et les chemins pour le téléchargement des bases de données.
- **src** 📁: Dossier source qui se divise en sous-dossiers pour la science des données (`data_science`) et la manipulation de données (`df_manipulation`).
- **tests** 📁: Contient les tests unitaires qui assurent la fiabilité du code.
- **venv** 📁: Dossier de l'environnement virtuel pour isoler les dépendances du projet.
- **README.md** 📄:Document qui décrit l'organisation et l'utilisation du projet.
- **requirements.txt** 📄:Recense les paquets Python nécessaires pour exécuter l'application.
- **dictionnaire des données** 📚: Consultez le [wiki du projet](https://github.com/Val832/produit_digital/wiki/Dictionnaire-des-variables) pour un dictionnaire des variables de la base de données.
- **Normes de code** 📚: Consultez le [wiki du projet](https://github.com/Val832/produit_digital/wiki/Dictionnaire-des-variables) pour consulter les normes de code de ce projet.

## 🚀 Utilisation du Projet

### ⏱️ Pour une Estimation Rapide

1. Ouvrez le fichier `FormulaireAIRBNB.xlsm` situé dans le dossier `VBA`.
2. Remplissez vos informations dans le formulaire VBA pour recevoir une estimation de prix.

### 🧐 Pour les plus Curieux 

#### Téléchargement et Préparation des Données

À partir de la racine du projet, lancez ces commandes pour préparer les données :

```bash
# Télécharger la base de données Airbnb de 2017
python -m src.df_manipulation.2017.download_db2017

# Créer les variables fictives pour la base de données de 2017
python -m src.df_manipulation.2017.create_dummies2017

# Télécharger la base de données Airbnb de 2023
python -m src.df_manipulation.2023.download_db2023

# Créer les variables fictives pour la base de données de 2023
python -m src.df_manipulation.2023.create_dummies2023
```

Après la préparation des données, dirigez-vous vers le dossier `src/data_science/models` pour explorer la construction des modèles prédictifs.
