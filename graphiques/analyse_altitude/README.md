# 🏔️ Mountain Energy Score - Haute-Savoie

**Analyse de l'impact de l'altitude sur la consommation énergétique des logements**

---

## 📊 Résultats Clés

- **+8,5 kWh/m²/an** de consommation par 100m d'altitude supplémentaire
- **61,3%** des logements situés en vallée (< 600m)
- **72,9%** des logements en classe énergétique C ou D

---

## 🚀 Installation et Utilisation

### Prérequis

```bash
# Installer les dépendances
pip install -r requirements.txt
```

### Données requises

Placer le fichier `logements_74.csv` (387MB) dans le dossier `data/raw/`

### Étape 1 : Préparation des données

```bash
python 01_preparation_donnees.py
```

### Étape 2 : Génération des graphiques

#### Option A : Tout régénérer d'un coup

```bash
python 99_regenerer_tout.py
```

#### Option B : Graphique par graphique

```bash
python 02_graphique_scatter.py
python 03_graphique_boxplot.py
python 04_graphique_barplot.py
python 05_graphique_barres_dpe.py
python 06_graphique_periode_construction.py
```

### Étape 3 : Consulter les résultats

Ouvrir dans un navigateur :
```
../mountain_energy_score_rapport_complet.html
```

---

## 📁 Structure

```
analyse_altitude/
├── 01_preparation_donnees.py          # Préparation et nettoyage
├── 02_graphique_scatter.py            # Régression altitude × consommation
├── 03_graphique_boxplot.py            # Distribution par tranche
├── 04_graphique_barplot.py            # Consommation moyenne
├── 05_graphique_barres_dpe.py         # Répartition DPE
├── 06_graphique_periode_construction.py # Évolution temporelle
├── 07_page_complete.py                # Génération rapport
├── 08_generer_html_standalone.py      # Version standalone
├── 99_regenerer_tout.py               # Régénération complète
├── config.py                          # Configuration centrale
├── requirements.txt                   # Dépendances Python
├── data/
│   └── raw/                          # Données brutes (logements_74.csv)
└── _documentation/                    # Documentation technique
```

---

## 📈 Données

**Source** : Base ADEME des Diagnostics de Performance Énergétique (DPE)
- Département : Haute-Savoie (74)
- Logements analysés : 202 829
- Fichier : `logements_74.csv` (387 MB)

---

## 🛠️ Configuration

Le fichier `config.py` centralise tous les paramètres :
- Tranches d'altitude adaptées au relief savoyard
- Palette DPE officielle
- Chemins de fichiers

---

## 📝 Méthodologie

**Modèle** : Régression linéaire `Consommation = a × Altitude + b`

**Résultats statistiques** :
- Pente : 0,0855 kWh/m²/an par mètre d'altitude
- R² : 0,071 (7,1% de variance expliquée)
- p-value : < 0,001 (hautement significatif)

---

## 📚 Dépendances

- `pandas` >= 2.0.0
- `numpy` >= 1.24.0
- `plotly` >= 5.14.0
- `scipy` >= 1.10.0
