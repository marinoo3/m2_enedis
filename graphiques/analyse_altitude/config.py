"""
Fichier de configuration centralisé pour l'analyse Mountain Energy Score
Département de la Haute-Savoie (74)

Ce fichier contient tous les paramètres configurables du projet :
- Informations sur le département étudié
- Tranches d'altitude adaptées au relief savoyard
- Chemins des fichiers et dossiers
- Paramètres pour les visualisations
"""

from pathlib import Path
import pandas as pd

# ============================================================================
# DÉPARTEMENT ÉTUDIÉ
# ============================================================================

DEPARTEMENT = "74"
NOM_DEPARTEMENT = "Haute-Savoie"
NOM_DEPARTEMENT_AVEC_ARTICLE = "de la Haute-Savoie"

# ============================================================================
# CHEMINS DES FICHIERS
# ============================================================================

# Définition des chemins relatifs pour la portabilité du code
DATA_PATH = Path("data") / "raw"
DATA_PROCESSED_PATH = Path("data") / "processed"
GRAPHIQUES_PATH = Path("graphiques")

# Création automatique des dossiers de sortie s'ils n'existent pas
DATA_PROCESSED_PATH.mkdir(exist_ok=True)
GRAPHIQUES_PATH.mkdir(exist_ok=True)

# ============================================================================
# TRANCHES D'ALTITUDE
# ============================================================================
# Les tranches sont adaptées au relief de la Haute-Savoie
# qui présente des altitudes beaucoup plus élevées que la moyenne nationale
# (le département contient le Mont Blanc à 4810m)

SEUILS_ALTITUDE = [600, 1200, 1800, 2500]

LABELS_ALTITUDE = [
    "0-600m (Vallée)",           # Zones basses : Annecy, Thonon-les-Bains
    "600-1200m (Colline)",       # Moyenne montagne
    "1200-1800m (Montagne)",     # Haute montagne habitée
    "1800-2500m (Haute montagne)",  # Limite des habitations permanentes
    ">2500m (Très haute montagne)"  # Zones peu habitées
]

# ============================================================================
# FONCTION DE CATÉGORISATION
# ============================================================================

def categoriser_altitude(altitude):
    """
    Affecte chaque logement à une tranche d'altitude
    
    Cette fonction permet de regrouper les logements selon leur altitude
    pour faciliter les analyses comparatives entre vallées et montagnes.
    
    Args:
        altitude (float): Altitude du logement en mètres
        
    Returns:
        str: Label de la tranche d'altitude correspondante
    """
    # Gestion des valeurs manquantes
    if pd.isna(altitude):
        return 'Non renseigné'
    
    # Attribution de la tranche selon les seuils définis
    if altitude < 600:
        return "0-600m (Vallée)"
    elif altitude < 1200:
        return "600-1200m (Colline)"
    elif altitude < 1800:
        return "1200-1800m (Montagne)"
    elif altitude < 2500:
        return "1800-2500m (Haute montagne)"
    else:
        return ">2500m (Très haute montagne)"

# ============================================================================
# PARAMÈTRES DE VISUALISATION
# ============================================================================

# Palette de couleurs standardisée pour les étiquettes DPE
# Suit la charte graphique officielle des diagnostics de performance énergétique
COULEURS_DPE = {
    'A': '#00A651',
    'B': '#50B847',
    'C': '#C8D220',
    'D': '#FDEE00',
    'E': '#FEB700',
    'F': '#F0832A',
    'G': '#ED1C24'
}

# Palette pour les tranches d'altitude (dégradé vert → rouge)
COULEURS_ALTITUDE = {
    "0-600m (Vallée)": '#27ae60',
    "600-1200m (Colline)": '#f39c12',
    "1200-1800m (Montagne)": '#e74c3c',
    "1800-2500m (Haute montagne)": '#9b59b6',
    ">2500m (Très haute montagne)": '#34495e'
}

# ============================================================================
# PARAMÈTRES DE CALCUL ÉCONOMIQUE
# ============================================================================

# Prix moyen de l'électricité en France en 2025 (tarif réglementé)
PRIX_ELECTRICITE = 0.20  # €/kWh

# Surface de référence utilisée pour les calculs de surcoût
# Correspond à la surface médiane d'un logement français
SURFACE_REFERENCE = 70  # m²

# ============================================================================
# PARAMÈTRES DE VISUALISATION - PERFORMANCE
# ============================================================================

# Limite d'échantillonnage pour les scatter plots (performance navigateur)
# Au-delà de ce seuil, un échantillon aléatoire est utilisé pour l'affichage
# Mettre à None pour désactiver l'échantillonnage (attention : fichiers HTML lourds)
TAILLE_ECHANTILLON_SCATTER = 10000

# ============================================================================
# PARAMÈTRES DE VALIDATION
# ============================================================================

# Valeurs attendues pour détecter d'éventuelles anomalies dans les données
ALTITUDE_MIN_ATTENDUE = 300   # Lac Léman (point le plus bas du département)
ALTITUDE_MAX_ATTENDUE = 4810  # Mont Blanc
NB_COMMUNES_MIN = 250         # Nombre de communes en Haute-Savoie

# Message de confirmation du chargement de la configuration
print(f"✅ Configuration chargée : Département {DEPARTEMENT} - {NOM_DEPARTEMENT}")