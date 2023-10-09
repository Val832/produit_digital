# Les bonnes pratiques de git

Création d'un environnement virtuel (/environement/venv), cela nous permettra à tous de travailler avec la même version de python.
Création d'un fichier requirements.txt, cela nous permettra d'avoir les même versions de packages, on évitera les " ça marche sur mon ordi pourtant..."

En bref, l'utilisation de ces pratiques nous permettra une facilité de partage et de collaboration. Mais aussi d'opérer des changements uniquement dans l'environnement virtuel ce qui a pour avantage de ne créer aucun conflit avec d'autres projets en cours utilisant aussi python.



à chaque installation de package :

    quand j'installe un package :
    pip install

    cela me permet de le rendre dispo pour les autres développeurs :
    pip freeze > requirements.txt

    les autres développeurs se mettent à jour :
    pip install -r requirements.txt


Une branche pour chacun d'entre nous a été créée

    Vous pouvez afficher toutes les branches dispo avec la commande :
    git branch

    Pour vous placer sur votre branche de dev :

    git checkout <branch_name>


Avant de bosser sur votre branche, récupérez les changements opérés sur le dépôt distant

    git pull origin

    On active l'environnement virtuel nommé "venv" pour ce projet

    Windows : venv\Scripts\activate
    Unix/MacOS : source venv/bin/activate


Si un nouveau fichier est créé

    git add file_name ou git add . permet d'ajouter tous les nouveaux fichiers crées

    git commit -m "message"

    Quand vous avez fini de bosser, envoyez les modifications vers le dépôt distant

    git push origin


Phase de test et demande de fusion

    Avant de faire une demande de merge on s'assure que nos modifications n'ont pas entraîné de régressions par rapport aux tests.

    Si tout est ok aller dans git lab :

    Dans la barre latérale gauche onglet requêtes de fusion -> nouvelle requête de fusion
    séléction de la branche source donc votre branche de dev -> comparer les branches et continuer

