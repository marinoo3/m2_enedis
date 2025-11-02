# Documentation technique – Application web France Énergie

## Aperçu général
<p align="center" margin="2rem">
  <img src="https://raw.githubusercontent.com/marinoo3/m2_enedis/refs/heads/main/documentations/Schema%20Architercture.svg">
</p>

## Gestion des données

1. **Sources de données**

**ENEDIS** : Source de données utilisée pour la visualisation cartographique. Elles peuvent être actualisées dynamiquement via l’API d’ENEDIS.

**ADEME** : Source de données utilisée pour les graphiques et l’entraînement des modèles. Seules les données du département de la Haute-Savoie (74) sont utilisées. Cette source sert également de complément à ENEDIS pour retrouver les coordonnées géographiques des adresses.

**data.gouv** : Le dataset "communes-france-2025" est utilisé pour compléter les données d’ENEDIS et de l’ADEME. Il contient des variables démographiques pour chaque commune de France.

2. **Stockage des données**

Toutes les données sont stockées au format CSV. Les jeux de données initiaux se trouvent dans le répertoire `application/datasets`. Les versions actualisées sont stockées dans le volume de l’application, par défaut `/volume` (il est possible de modifier le chemin de ce répertoire avec la variable d’environnement `MOUNT_PATH`).

## Fonctionnement de l’application

1. **Interface graphique**

L’interface utilisateur est conçue en HTML/CSS. Des scripts JavaScript assurent la communication avec le backend Python. Jinja2 est utilisé dans les templates HTML pour générer dynamiquement le contenu.

2. **Backend**

Le backend, construit avec Flask, utilise des blueprints pour structurer les différentes parties de l'application :

- **Main** [ `/` ] : Sert les routes de l’application pour rendre les différentes pages HTML.
- **Ajax** [ `/ajax` ] : Composé de plusieurs fonctions destinées à être appelées par le JavaScript. Il constitue l’API interne de l’application.

## REST API

L'API, également développée avec Flask, expose publiquement les modèles de machine learning. Elle est accessible depuis la route /api/v1 et comprend deux endpoints qui permettent de faire de l'inférence sur les modèles avec les variables renseignées par l'utilisateur. Elle renvoie le résultat au format JSON.

## Packages utilisés

- **Flask** : Framework web utilisé pour développer l'API et structurer le backend de l'application.
- **gunicorn** : Serveur WSGI utilisé pour déployer l'application en production.
- **requests** : Librairie pour effectuer des requêtes HTTP vers des APIs externes.
- **pandas** + **numpy** : Outils de manipulation et d'analyse de données, permettant un traitement efficace des datasets.
- **scipy** : Fournit des algorithmes et des fonctions mathématiques avancés pour les calculs statistiques.
- **scikit-learn** : Bibliothèque de machine learning pour la création et l'entraînement des modèles.
- **plotly** : Outil de création de graphiques interactifs intégrés dans l'interface de l'application.

## Executer l'app en local avec Docker

1. Aller dans le dossier `web`
```bash
cd web
```

2. Construire l'image Docker
```bash
docker build -t france-energie .
```

3. Lancer l'image Docker
```bash
docker run -p 8000:8000 france-energie
```

4. L'application est hébergée sur le port `8000`, ouvrir un navigateur et se rendre à l'adresse http://0.0.0.0:8000/

## Structure de l'application
```bash
web/
    ├── application/
        ├── custom/
            ... app modules
        ├── datasets/
            ├── communes-france-2025-light.csv
            ├── communes.csv
            └── logement-74-light.csv
        ├── static/
            ├── css/
                ... CSS files
            ├── images/
                ... Images and SVGs
            └── js/
                ... JavaScript files
        ├── templates/
            ... HTML files
        ├── __init__.py
        ├── ajax.py
        ├── api.py
        └── routes.py
    ├── app.py
    ├── Dockerfile
    └── requirements.txt
```
