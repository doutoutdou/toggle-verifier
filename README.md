# toggle-verifier

## But

Projet ayant pour but d'automatiser la vérification des toggles.

Il vient vérifier que pour un composant à livrer, tous les toggles de ce composant sont ok (compare contenu fichier
référence avec conf dans git).

## Fonctionnement résumé

### Swagger
Tout est dans le fichier `swagger.yml`.  
Si projet démarré alors se rendre sur `/api/ui/`.  

### Endpoint verify
un endpoint est exposé sur `/api/verify/{toggle_tag}`, celui ci effectue les actions suivantes :

1. Récupère sur GIT le fichier contenant la conf globale des toggles attendue pour la version passée en
   paramètre ([exemple ici](https://git.ra1.intra.groupama.fr/GSB932/conf-toggle/-/blob/master/test_ok.json))    
   1.1. une 404 est retournée si ce fichier n'est pas trouvé
2. Pour chaque projet detecté dans le fichier :
    1. si `"tag": "develop"` alors on ignore ce projet (develop veut dire que le projet ne sera pas installé dans cette
       version
    2. sinon, pour le tag indiqué, on regarde si les toggles de ce fichier correspondent aux toggles indiqués dans les
       fichiers de configuration openshift (pour le tag donné) (pour tous les environnements indiqués dans le fichier
       des toggles)
3. La réponse retournée suite à ce traitement peut alors être :
    1. 200 : Si tous les toggles sont trouvés, alors la réponse indique que c'est un succès
    2. 206 : Sinon la liste des toggles qui ne correspondent pas est retournée)

## Fonctionnement détaillé

### Fichier source des toggles

Le fichier source est le fichier utilisé comme référence pour les toggles et leurs valeurs.  
Il est présent sur GIT et est modifié au fur et a mesure des livraisons

```json
[
  {
    "projet": "ecli-bff", => le nom du projet à aller chercher dans git (pas utilisé si suricate)
    "tag": "1.12.2", => le tag à vérifier pour le projet (pas utilisé si suricate), si tag = develop alors projet ignoré
    "suricate": "true", => clé optionnelle qui indique si la conf se trouve dans suricate (sinon on va chercher dans le projet lui même)
    "toggles": [ => liste des toggles
      {
        "ittFm_mise_en_place_dtrh": [ => le nom du toggle
          {
            "d": "true", => la valeur attendue pour chaque environnement
            "k": "true",
            "r": "true",
            "m": "false",
            "q": "true",
            "p": "true"
          }
        ],
        "documentsMetier_refm_filtragePage": [
          {
            "d": "true",
            "k": "true",
            "r": "true",
            "m": "false",
            "q": "true",
            "p": "true"
          }
        ],
        "use-refm-for-marques": [
          {
            "d": { => dans le cas dun toggle avec une strategy, on la définit de cette manière, strategy que si toggle dans suricate
              "value": "true",
              "strategyParams": "RENAULT,DACIA,GANAS,GEV,GPAT,GPREV,GPMA,NAT"
            }
          }
        ]
      }
    ]
  },
  {
   "projet":"ecli-fo",
   "tag":"2022.0301.1",
   "toggles":[
      {
         "CONF_TOGGLES_SYNTHESE_DEVIS_REFONTE_MUTUALISATION_SANTE_AUTO_MRH":[
            {
               "d":"true",
               "k":"true",
               "r":"true",
               "m":"true",
               "dmz-q":"false",
               "dmz":"false"
            }
         ],
        "CONF_TOGGLES_BANDEAU_PRESENCE_COTISATIONS_IMPAYEES": [
           {
               "d":"true",
               "k":"true",
               "r":"true",
               "m":"true",
               "dmz-q":"false",
               "dmz":"false"
            }
        ]
      }
   ]
}
]
```

### Fichier source transformé

Pour faciliter le traitement, le fichier source est utilisé pour traiter les toggles projet par projet. Cela permet ainsi de vérifier tous les toggles projet par projet.   

Voir le code `verifier.py#build_toggle_dict_by_env`.

Par exemple pour le ecli-bff on obtient :
```json
{
  "ecli-bff": {
    "d": {
      "documentsMetier_refm_filtragePage": {
        "value": "true"
      },
      "ittFm_mise_en_place_dtrh": {
        "value": "true"
      },
      "use-refm-for-marques": {
        "strategyParams": "RENAULT,DACIA,GANAS,GEV,GPAT,GPREV,GPMA,NAT",
        "value": "true"
      }
    },
    suite ...
  }
}
```

pour le ecli-fo :
```json
{
  "ecli-fo": {
    "d": {
      "CONF_TOGGLES_SYNTHESE_DEVIS_REFONTE_MUTUALISATION_SANTE_AUTO_MRH": {
        "value": "true"
      },
      "CONF_TOGGLES_BANDEAU_PRESENCE_COTISATIONS_IMPAYEES": {
        "value": "true"
      }
    },
    suite ...
  }
}  
```
### Fichiers contenant les toggles pour une version
2 types de fichiers sont traités, les fichiers configmap et les fichiers "suricate"

#### Fichier configmap
Un fichier configmap peut contenir des toggles, dans ce cas il est de la forme `cle=valeur`
Par exemple : 
```text
CONF_TOGGLES_PAIEMENT_COTISATIONS_ENABLED=true
CONF_TOGGLES_PAIEMENT_COTISATIONS_DISABLED_FOR="BAN", "GAG", "GSP", "GVC"
CONF_TOGGLES_VERIFICATION_STATUS_PAYBOX=true
CONF_TOGGLES_TMA_MODAL=false
CONF_TOGGLES_TCHAT_GENESYS="GOC", "GCM", "GNE", "GSU"
CONF_TOGGLES_DISPLAY_PERF=true
CONF_TOGGLES_DISPLAY_INFOS_MATERIELS_TRACTES=true
CONF_TOGGLES_USE_ECLI_SVC_DOCUMENT=true
CONF_TOGGLES_USE_BFF_DOCUMENT_CONTRAT=true
CONF_TOGGLES_HIDE_ATPG_FOR_PUMA=true
CONF_TOGGLES_USE_SIPS_SERVICES=true
```

ce type de fichier est traité dans `verifier.py#search_toggle_in_configuration_files`.


#### Fichier suricate
Les fichiers présents dans suricate (abus de langage ...) sont eux en `.yml` et peuvent contenir une strategyPattern

```yaml

oyster:
  toggles:
    - name: marque-groupama-enabled
      active: false
    - name: recuperationRemboursementsSante_surchargeCaisseAvecGGVIE_PourLesGanUniquement
      active: true
    - name: recuperationDocumentsMetierGestion_surchargeCaisseGanAvecGGVIE_PourLesGanUniquement
      active: true
    - name: use-refm
      active: true
    - name: use-refm-for-marques
      active: true
      strategyParams:
        values: 'RENAULT,DACIA,GANAS,GEV,GPAT,GPREV,GPMA,NAT'
    - name: not-use-refm-for-entites
      active: true
      strategyParams:
        values: 'GAG'
```

ce type de fichier est traité dans `verifier.py#search_toggle_in_suricate_files`.


### Fichier retour
Pour chaque projet, on vient chercher dans les fichiers `configmap.properties` ou dans `suricate` les toggles.   
On compare alors le nom du toggle, sa valeur et sa strategy (si présente).  

Si tous les toggles de tous les projets correspondent à l'attendu, alors rien n'est retourné.  
Si par contre des toggles ne correspondent pas, alors une liste des toggles non trouvés par projet et par environnement est retournée.  

Par exemple : 
```json
{
  "ecli-bff": {
    "d": {
      "documentsMetier_refm_filtragePage": {
        "value": "true"
      },
      "ittFm_mise_en_place_dtrh": {
        "value": "true"
      }
    }
  },
  "ecli-fo": {
    "k": {
      "CONF_TOGGLES_BANDEAU_PRESENCE_COTISATIONS_IMPAYEES": {
        "value": "true"
      },
      "CONF_TOGGLES_DETAIL_CONTRAT_VIE_AFFICHAGE_TAUX_VALEUR_DECIMALE": {
        "value": "true"
      },
      "CONF_TOGGLES_DETAIL_CONTRAT_VIE_EPARGNE_DISPLAY_PERFORMANCE_MODE_GESTION": {
        "value": "true"
      },
      "CONF_TOGGLES_DETAIL_CONTRAT_VIE_NOUVEAUX_PROFILS_RISQUE_DURABLES": {
        "value": "true"
      },
      "CONF_TOGGLES_DETAIL_CONTRAT_VIE_PREVOYANCE_RETRAITE_AFFICHAGE_DATE_MAJ_STATUT_CONTRAT_REDUIT_OU_SUSPENDU": {
        "value": "true"
      }
    }
  }
}
```

## Stack technique

Ce projet est en python et se base sur le framework Flask avec une surcouche Connexion (qui permet de gérer des
endpoints via un fichier swagger directement notamment).

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

pour pip, il faut que le proxy soit configuré, le mieux est d'avoir la conf sur votre machine et de passer les arguments
au moment du build.

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