# Projet d'évaluation du prix d'un bien immobilier dans Paris dans l'application Airbnb

# Objectif

Créer une application qui a pour but d'estimer le prix de votre bien immobilier situé à Paris sur l'application Airbnb.
Elle vous permettra de proposer votre logement au juste prix en fonction des caractéristiques et de la localité de votre
bien.

# Détails du développement de l'application

# 1. Nettoyage de la base de données

    - Objectif : Disposer d'une base de données claire qui permet ensuite de choisir les variables explicatives à prendre.

    - Étapes : 

        i. Identifier des variables utiles pour notre algorithme de prédiction.
        ii. Extraire des caractéristiques de certaines variables, par exemple dans la description du bien.
        iii. Créer des nouvelles variables indicatrices qui affichent 1 si cette caractéristique est présente dans la 
        description de ce bien ou 0 sinon.  

# 2. Réaliser l'interface VBA

    - Objectif : Disposer d'un formulaire VBA qui demande à l'utilisateur un certain nombre de caractéristiques sur
    son logement.

    - Étapes : 
        
        i. Réaliser une interface de saisie qui demande à l'utilisateur des informations sur son logement.
        ii. Réaliser une interface de résultats montrant à l'utilisateur une estimation de son bien immobilier.
        iii. Connecter ces deux interfaces VBA à un script Python calculant le prix du bien immobilier de l'utilisateur.

# 3. Réaliser l'algorithme de prédiction

    - Objectif : Disposer d'un algorithme permettant de prédire la variable prix du bien en fonction de plusieurs
    variables explicatives données par l'utilisateur.

    - Étapes : 

        i. Réaliser un premier algorithme de régression linéaire multiple.
        ii. Réaliser d'autres algorithmes de prédiction et choisir quel est le plus adapté à ces données.
        iii. Réaliser des tests unitaires pour valider la robustesse de l'algorithme choisi.
