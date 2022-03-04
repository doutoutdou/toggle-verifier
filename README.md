# toggle-verifier

## But
Projet ayant pour but d'automatiser la vérification des toggles.  

Il vient vérifier que pour un composant à livrer, tous les toggles de ce composant sont ok (compare contenu fichier référence avec conf dans git).  

## Stack technique
Ce projet est en python et se base sur le framework Flask avec une surcouche Connexion (qui permet de gérer des endpoints via un fichier swagger directement notamment).

Un peu de doc : 
* https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-fr
* https://realpython.com/flask-connexion-rest-api/
* https://connexion.readthedocs.io/en/latest/


## Prérequis
Python >= 3.7

## Comment lancer le bazard ?

### Création virtualenv
Il est conseillé de se creer un virtual env, pour cela on installe l'outil qui va bien :
```bash
pip install virtualenv
```

Puis on crée un virtual env, ici très bien nommé `venv1`, la regex du gitignore se base dessus (.\*venv\*)
```bash
virtualenv venv1
```

On l'active pour pouvoir l'utiliser
```bash
source venv1/bin/activate
```

On pourrait aussi utiliser virtualenvwrapper pour améliorer la gestion

### Téléchargement dépendances
Pour télécharger toutes les dépendances (à refaire si tu changes de virtual env)
```bash
pip install -r requirements.txt
```
* Puis jouer la commande suivante : `python -m pip install -c requirements.txt`

### Démarrage appli
#### Via commande python
```bash
python app.py
```

#### Via Flask
```bash
# On indique ici le nom du fichier, à faire 1 seul fois
export FLASK_APP=app
# Pour démarrer
flask run
```

Démarrer via Flask permet de profiter de fonctionnalités supplémentaires, par exemple le debug.   
De la doc [par ici](https://flask.palletsprojects.com/en/2.0.x/quickstart/)

## En cas de mise à jour
### Ajout de dépendance
Si ajout de dépendance alors il faut faire un `pip freeze > requirements.txt`.  
Cela permet de mettre à jour le fichier indiquant les dépendances à télécharger.


## Doc
### virtualEnv
https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html
### Pour virer les logs https en insecure
export PYTHONWARNINGS="ignore:Unverified HTTPS request"