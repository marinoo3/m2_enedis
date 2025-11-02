# Documentation Fonctionnelle - France Énergie

## Présentation

**France Énergie** est une application web interactive permettant d'explorer et d'analyser la performance énergétique des logements en France. Elle s'appuie sur les données officielles de l'ADEME et d'Enedis pour évaluer le DPE d'un logement et sa consommation énergétique.

**URL** : [https://france-energie.koyeb.app/](https://france-energie.koyeb.app/)

---

## Pages de l'application

### Page "Contexte"

**Intérêt** : Introduction et présentation du projet France Énergie. Cette page présente le contexte du projet, développé dans le cadre du Master 2 SISE. 

**Utilisation** : Point d'entrée informatif pour comprendre la mission et les objectifs de l'application.

---

### Page "Carte"

**Intérêt** : Vue géographique interactive des données de consommation énergétique par commune avec modes de visualisation multiples (heat map ou points), recherche de lieux, filtres avancés et export des cartes.

**Fonctionnalités** :
- **Modes de visualisation** : Basculer entre vue "Heat Map" (carte de chaleur) et "Points" (marqueurs individuels)
- **Barre de recherche** : Recherche d'un lieu spécifique (commune, adresse) avec positionnement automatique sur la carte
- Cartographie interactive Leaflet (navigation, zoom, déplacement)
- **Métriques disponibles** : Consommation totale (MWh) ou Consommation par habitant (MWh)
- Tableau des communes avec 8 colonnes : code commune, nom, année, logements, densité population, altitude, consommation totale (MWh), consommation par habitant (MWh)
- **Filtres dynamiques** : code de commune, année (2018-2024), densité de population (slider 0-28220), altitude (slider 0-4808m)
- Téléchargement de la carte en PNG

**Utilisation** : Saisir un lieu dans la barre de recherche ou naviguer manuellement. Basculer entre heat map et points selon les besoins d'analyse. Utiliser les filtres pour cibler des communes spécifiques. Télécharger les visualisations pour rapports.

---

### Page "Statistiques"

**Intérêt** : Analyse approfondie de l'impact de l'altitude sur la consommation énergétique en Haute-Savoie (74) à travers 5 visualisations interactives. Exploite 200 000 logements DPE de Haute-Savoie incluant les données d'altitude.

**Graphiques** :

**📊 1. Corrélation Altitude × Consommation**
- Nuage de points avec régression linéaire : **+8,6 kWh/m²/an par 100m d'altitude** (R² = 0,077, p < 0,001)
- Confirme l'altitude comme facteur explicatif majeur de la consommation énergétique
- Graphique Plotly interactif (zoom, survol)

**📊 2. Distribution par tranche d'altitude**
- Boxplot 4 tranches : Vallée 0-600m, Colline 600-1200m, Montagne 1200-1800m, Haute montagne 1800-2500m
- Progression médiane : 175 kWh/m²/an (vallée) → 277 kWh/m²/an (montagne), soit **+58%**
- **Pallier à 1200m** : consommation se stabilise au-delà, identifiant la zone 600-1200m comme transition critique

**📊 3. Surcoût financier par tranche**
- Barplot : surcoût annuel (logement 70m², électricité 0,20€/kWh)
- **Colline : +290€/an | Montagne : +1 363€/an** (+114€/mois) vs vallée
- Quantification de l'impact budgétaire pour les ménages en altitude

**📊 4. Passoires thermiques par altitude**
- Barres empilées : répartition DPE (A-G) par tranche
- **11,1% de F-G en vallée vs 26,9% en montagne** (ratio 2,4)
- Surreprésentation des classes défavorables traduisant un décalage structurel du parc immobilier

**📊 5. Période construction × Altitude**
- Heatmap : périodes de construction × tranches d'altitude
- Logements pré-1975 en montagne : **364 kWh/m²/an** (3,3× supérieur au récent en vallée)

**Utilisation** : Consultation séquentielle des graphiques Plotly avec interactions (zoom, survol pour détails).

---

### Page "Prédictions"

**Intérêt** : Prédire la classe DPE et la consommation énergétique d'un logement via modèles de machine learning entraînés sur les données ADEME et Enedis.

**Fonctionnalités** :

**Partie Saisie - Informations du logement** :
- **Adresse ou code postal** : Recherche avec carte interactive associée pour localisation précise
- **Surface habitable** : En m²
- **Année de construction** : Saisie numérique
- **Type de bâtiment** : Menu déroulant (maison, appartement, etc.)
- **Type d'énergie de chauffage** : Menu déroulant (électricité, gaz, fioul, bois, etc.)
- **Logement traversant** : Menu déroulant (oui/non)
- **Isolation extérieure** : Menu déroulant (oui/non)

**Partie Prédictions** (affichage après validation, quelques secondes de traitement) :
- **Étiquette DPE** : Classification A à G avec indication "Passoire thermique" (F-G) ou "Non passoire" (A-E)
- **Consommation estimée de chauffage** : En kWh/an

**Utilisation** : Remplir le formulaire avec les caractéristiques du logement. Valider et patienter quelques secondes pour obtenir l'étiquette DPE prédite et la consommation estimée, sans nécessiter de DPE officiel payant.

---

### Page "API"

**Intérêt** : API REST permettant d'évaluer la performance énergétique des logements situés dans le département du Rhône (69). Obtenir rapidement une estimation du coût annuel de chauffage et une prédiction de l'étiquette DPE d'un bien immobilier de manière programmatique.

**Fonctionnalités** :
- **Documentation** : URL de l'API et 2 endpoints GET disponibles (`/consommation_chauffage` et `/etiquette_dpe`)
- **Exemples de code** : cURL, Python et R pour faciliter l'intégration
- **Playground interactif** :
  - 2 onglets : "Consommation de chauffage" et "Étiquette DPE"
  - Formulaire de paramètres (surface habitable, altitude, année construction, zone climatique, type bâtiment, etc.)
  - Exécution en temps réel des requêtes GET
  - Affichage instantané de la réponse JSON

**Utilisation** : Consulter les endpoints disponibles dans la section Documentation. Copier les exemples de code (cURL, Python, R) pour intégrer l'API dans vos applications. Tester les requêtes directement dans le playground en renseignant les paramètres du logement.

---

### Page "À propos"

**Intérêt** : Accès au dépôt GitHub du projet pour consulter le code source, la documentation technique et contribuer au développement.

**Utilisation** : Redirection vers le repository Git du projet contenant le code source, les modèles de machine learning, la documentation technique et les instructions d'installation pour déploiement local ou contribution au projet.
