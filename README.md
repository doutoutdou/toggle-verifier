# toggle-verifier

## But
Projet ayant pour but d'automatiser la vérification des toggles.  

Il vient vérifier que pour un composant à livrer, tous les toggles de ce composant sont ok (compare contenu fichier référence avec conf dans git).  

## Endpoint
Tout est dans le fichier `swagger.yml`

Si projet démarré alors se rendre sur `/api/ui/`

un endpoint est exposé sur `/api/verify/{toggle_tag}`, celui ci effectue les actions suivantes : 

1. Récupère sur GIT le fichier contenant la conf globale des toggles attendue pour la version passée en paramètre ([exemple ici](https://git.ra1.intra.groupama.fr/GSB932/conf-toggle/-/blob/master/test_ok.json)) ou alors dans le repertoire `examples`   
1.1. une 404 est retournée si ce fichier n'est pas trouvé
2. Pour chaque projet detecté dans le fichier :
   1. si `"tag": "develop"` alors on ignore ce projet (develop veut dire que le projet ne sera pas installé dans cette version  
   2. sinon, pour le tag indiqué, on regarde si les toggles de ce fichier correspondent aux toggles indiqués dans les fichiers de configuration openshift (pour le tag donné) (pour tous les environnements indiqués dans le fichier des toggles)  
3. La réponse retournée suite à ce traitement peut alors être :  
   1. 200 : Si tous les toggles sont trouvés, alors la réponse indique que c'est un succès  
   2. 206 : Sinon la liste des toggles qui ne correspondent pas est retournée)  

## Stack technique
Ce projet est en python et se base sur le framework Flask avec une surcouche Connexion (qui permet de gérer des endpoints via un fichier swagger directement notamment).

Un peu de doc : 
* https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-fr
* https://realpython.com/flask-connexion-rest-api/
* https://connexion.readthedocs.io/en/latest/

## Prérequis
Python >= 3.7

## Comment lancer le bazar ?

### Sans docker

#### Création virtualenv
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

#### Téléchargement dépendances
Pour télécharger toutes les dépendances (à refaire si tu changes de virtual env)
```bash
pip install -r requirements.txt
```
* Puis jouer la commande suivante : `python -m pip install -c requirements.txt`

#### Démarrage appli
##### Via commande python
```bash
python sample/app.py
# Ou
cd sample
python app.py
```

##### Via Flask
```bash
# On indique ici le nom du fichier, à faire 1 seul fois
export FLASK_APP=sample/app
# Pour démarrer
flask run
```

Démarrer via Flask permet de profiter de fonctionnalités supplémentaires, par exemple le debug.   
De la doc [par ici](https://flask.palletsprojects.com/en/2.0.x/quickstart/)

### Avec docker
Pas de rechargement à chaud, à utiliser pour déploiement
#### Build image
pour pip, il faut que le proxy soit configuré, le mieux est d'avoir la conf sur votre machine 
et de passer les arguments au moment du build.
```bash
docker build -t toggle-verifier --build-arg http_proxy=$HTTP_PROXY --build-arg https_proxy=$HTTP_PROXY --network=host .
```

#### Run
```bash
 docker run -p 5000:5000 -d --name toggle-verifier-container toggle-verifier
 ```

L'api est ensuite accessible sur le port 5000

## En cas de mise à jour
### Ajout de dépendance
Si ajout de dépendance alors il faut faire un `pip freeze > requirements.txt`.  
Cela permet de mettre à jour le fichier indiquant les dépendances à télécharger.


## Doc
### virtualEnv
https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html

### Pour virer les logs https en insecure
export PYTHONWARNINGS="ignore:Unverified HTTPS request"