# Documentation Fonctionnelle - France Énergie

## Présentation

**France Énergie** est une application web interactive permettant d'explorer et d'analyser la performance énergétique des logements en France. Elle s'appuie sur les données officielles de l'ADEME et d'Enedis pour évaluer le DPE d'un logement et sa consommation énergétique.

**URL** : [https://france-energie.koyeb.app/](https://france-energie.koyeb.app/)

---

## Pages de l'application

### Page "Carte"

**Intérêt** : Point d'entrée principal offrant une vue géographique des données de consommation énergétique par commune.

**Fonctionnalités** :
- Cartographie interactive Leaflet avec heatmap de consommation ou clustering de points (navigation, zoom, info-bulle)
- Tableau des communes avec 8 colonnes : code commune, nom, année, logements, densité population, altitude, consommation totale (MWh), consommation par habitant (MWh)
- **Filtres dynamiques** : code de commune (input), année (select), densité de population (slider 0-28220), altitude (slider 0-4808m)
- Téléchargement de la carte en PNG
- Recherche de lieux depuis la barre de recherche
- Requête de données plus précise au zoom

**Utilisation** : Visualisation de la heatmap pour identifier les zones de forte/faible consommation ou du clustering de points pour avoir des informations sur des adresses. Utilisation des filtres (sliders et champs) pour affiner l'affichage du tableau des communes.

---

### Page "Statistiques"

**Intérêt** : Analyse approfondie de l'impact de l'altitude sur la consommation énergétique en Haute-Savoie (74) à travers 5 visualisations interactives. Exploite 200 000 logements DPE enrichis avec données d'élévation IGN.

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

**Intérêt** : _[En développement]_ Prédire la classe DPE et la consommation énergétique d'un logement via modèles de machine learning.

**Fonctionnalités prévues** : Formulaire de saisie (surface, année construction, chauffage, isolation, localisation, altitude) | Prédiction classe DPE (classification) et consommation (régression) | Affichage étiquette DPE colorée, coût annuel, recommandations

**Utilisation** : Saisie caractéristiques → prédiction instantanée DPE et consommation sans DPE officiel payant.

---

### Page "API"

**Intérêt** : _[En développement]_ Documentation API REST pour accès programmatique aux modèles de prédiction.

**Fonctionnalités prévues** : Documentation endpoints, exemples JSON, authentification, limites de taux

**Utilisation** : Intégration des prédictions dans applications tierces.

---

### Page "À propos"

**Intérêt** : Contexte du projet, sources de données et stack technique.

**Contenu** : Présentation projet M2 SISE, mission Enedis (impact DPE sur consommations), sources (APIs ADEME/Enedis, data.gouv), technologies (Python, Flask, Leaflet, Plotly, scikit-learn, Docker, Koyeb), crédits open source

---

## Fonctionnalités transversales

- **Interactivité** : Interface responsive, graphiques Plotly (zoom, survol), filtres dynamiques temps réel
- **Design** : Palette DPE officielle (vert A → rouge G), iconographie, typographie claire
- **Technologies** : Backend Python/Flask, Frontend HTML/CSS/JS, Leaflet, Plotly, Pandas/NumPy, scikit-learn, Docker/Koyeb
