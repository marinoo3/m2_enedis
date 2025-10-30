## Gestion des données

1. **Sources de données**

**ENEDIS** : Source de données utilisée pour la visualisation cartographique. Elles peuvent être actualisées dynamiquement via l’API d’ENEDIS.

**ADEME** : Source de données utilisée pour les graphiques et l’entraînement des modèles. Seules les données du département de la Haute-Savoie (74) sont utilisées. Cette source sert également de complément à ENEDIS pour retrouver les coordonnées géographiques des adresses.

**data.gouv** : Le dataset "communes-france-2025" est utilisé pour compléter les données d’ENEDIS et de l’ADEME. Il contient des variables démographiques pour chaque commune de France.

1. **Stockage des données**

Toutes les données sont stockées au format CSV. Les jeux de données initiaux se trouvent dans le répertoire `application/datasets`. Les versions actualisées sont stockées dans le volume de l’application, par défaut `/volume` (il est possible de modifier le chemin de ce répertoire avec la variable d’environnement `MOUNT_PATH`).

## Fonctionnement de l’application

1. **Interface graphique**

L’interface utilisateur est conçue en HTML/CSS. Des scripts JavaScript assurent la communication avec le backend Python. Jinja2 est utilisé dans les templates HTML pour générer dynamiquement le contenu.

1. **Backend**

Le backend, construit avec Flask, utilise des blueprints pour structurer les différentes parties de l'application :

- **Main** [ `/` ] : Sert les routes de l’application pour rendre les différentes pages HTML.
- **Ajax** [ `/ajax` ] : Composé de plusieurs fonctions destinées à être appelées par le JavaScript. Il constitue l’API interne de l’application.

## API REST

L’API, également développée avec Flask, expose publiquement les modèles de machine learning. Elle est accessible depuis la route `/api/v1` et comprend deux endpoints qui permettent d’inférence sur les modèle avec les variables renseignées par l’utilisateur. Renvoi le résultat au format JSON.

## Technologies utilisées

**Python :** Langage principal utilisé pour la collecte et la gestion des données, le développement des modèles ainsi que pour le backend de l’application.

**Flask :** Utilisé pour développer l’API ainsi que pour construire l’application web.

**HTML / CSS / JS :** Pour la conception de l’interface utilisateur.

**Gunicorn :** Serveur de déploiement utilisé pour faire tourner l’application.
