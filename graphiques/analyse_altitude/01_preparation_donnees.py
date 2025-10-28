"""
Script de préparation des données
Mountain Energy Score - Haute-Savoie

Ce script effectue les opérations suivantes :
1. Chargement des données DPE du département 74
2. Nettoyage et validation des données
3. Ajout des catégories d'altitude
4. Export des données préparées pour les analyses

Note : L'altitude est directement disponible dans le fichier DPE
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

# Import de la configuration du projet
from config import (
    DEPARTEMENT, NOM_DEPARTEMENT,
    DATA_PATH, DATA_PROCESSED_PATH,
    categoriser_altitude
)

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print(f"PRÉPARATION DES DONNÉES - DÉPARTEMENT {DEPARTEMENT}")
print("="*80 + "\n")

# ============================================================================
# CHARGEMENT DES DONNÉES SOURCES
# ============================================================================

print("📂 Chargement des fichiers sources...\n")

# Chargement des données DPE (contient déjà l'altitude)
# low_memory=False évite les warnings sur les types de colonnes mixtes
fichier_dpe = DATA_PATH / f"logements_{DEPARTEMENT}.csv"
print(f"   → Lecture de {fichier_dpe.name}...")
df_logements = pd.read_csv(fichier_dpe, low_memory=False)
print(f"      ✅ {len(df_logements):,} logements chargés\n")

# ============================================================================
# SÉLECTION DES COLONNES UTILES
# ============================================================================

print("🔧 Sélection des colonnes pertinentes...\n")

# Colonnes essentielles pour l'analyse énergétique
colonnes_logements = [
    'numero_dpe',                          # Identifiant unique du DPE
    'code_insee_ban',                      # Code commune
    'nom_commune_ban',                     # Nom de la commune
    'etiquette_dpe',                       # Classe énergétique (A à G)
    'conso_5_usages_par_m2_ep',           # Consommation en kWh/m²/an
    'surface_habitable_logement',          # Surface en m² (pour calculs de coûts)
    'type_batiment',                       # Maison ou appartement
    'periode_construction',                # Époque de construction
    'type_energie_principale_chauffage',   # Type de chauffage utilisé
    'altitude_moyenne'                     # Altitude moyenne (déjà dans le DPE)
]

# Vérification de la présence des colonnes
colonnes_presentes = [col for col in colonnes_logements if col in df_logements.columns]
if len(colonnes_presentes) < len(colonnes_logements):
    colonnes_manquantes = set(colonnes_logements) - set(colonnes_presentes)
    print(f"   ⚠️  Colonnes manquantes : {colonnes_manquantes}")

df_preparation = df_logements[colonnes_presentes].copy()
print(f"   ✅ {len(colonnes_presentes)} colonnes sélectionnées\n")

# ============================================================================
# NETTOYAGE DES DONNÉES
# ============================================================================

print("🧹 Nettoyage des données...\n")

# Suppression des doublons de DPE (un logement peut avoir plusieurs DPE, on garde le plus récent)
nb_avant = len(df_preparation)
df_preparation = df_preparation.drop_duplicates(subset='numero_dpe', keep='first')
nb_supprimes = nb_avant - len(df_preparation)
print(f"   → Doublons supprimés : {nb_supprimes:,}")

# Suppression des lignes avec des valeurs manquantes critiques
# Ces variables sont indispensables pour l'analyse
df_preparation = df_preparation.dropna(subset=['code_insee_ban', 'etiquette_dpe', 'conso_5_usages_par_m2_ep'])
print(f"   → Lignes valides conservées : {len(df_preparation):,}")

# Vérification de la disponibilité des altitudes
nb_avec_altitude = df_preparation['altitude_moyenne'].notna().sum()
taux_altitude = (nb_avec_altitude / len(df_preparation)) * 100

print(f"   → Logements avec altitude : {nb_avec_altitude:,} ({taux_altitude:.1f}%)")

if taux_altitude < 95:
    print(f"   ⚠️  {len(df_preparation) - nb_avec_altitude:,} logements sans altitude")

print()

# ============================================================================
# DÉTECTION ET CORRECTION DES ANOMALIES
# ============================================================================

print("🔍 Détection et correction des anomalies...\n")

nb_avant_corrections = len(df_preparation)

# Anomalie 1 : Consommations aberrantes
# Consommations très élevées (> 1000 kWh/m²/an) sont souvent des erreurs de saisie
# La médiane est ~193 kWh/m²/an, au-delà de 1000 c'est suspect
anomalies_conso_hautes = df_preparation['conso_5_usages_par_m2_ep'] > 1000
nb_conso_hautes = anomalies_conso_hautes.sum()

if nb_conso_hautes > 0:
    print(f"   ⚠️  Consommations aberrantes (> 1000 kWh/m²/an) : {nb_conso_hautes:,}")
    print(f"      → Suppression de ces lignes (erreurs de saisie probables)")
    df_preparation = df_preparation[~anomalies_conso_hautes]

# Anomalie 2 : Consommations très basses
# Consommations < 10 kWh/m²/an sont impossibles (même pour maisons passives)
anomalies_conso_basses = df_preparation['conso_5_usages_par_m2_ep'] < 10
nb_conso_basses = anomalies_conso_basses.sum()

if nb_conso_basses > 0:
    print(f"   ⚠️  Consommations anormalement basses (< 10 kWh/m²/an) : {nb_conso_basses:,}")
    print(f"      → Suppression de ces lignes (erreurs de mesure)")
    df_preparation = df_preparation[~anomalies_conso_basses]

# Anomalie 3 : Altitudes aberrantes pour la Haute-Savoie
# Le département va de ~335m (Lac Léman) à ~2445m (haute montagne habitée)
# Au-delà de 3000m, il n'y a plus de logements permanents
anomalies_altitude_hautes = df_preparation['altitude_moyenne'] > 3000
nb_alt_hautes = anomalies_altitude_hautes.sum()

if nb_alt_hautes > 0:
    print(f"   ⚠️  Altitudes aberrantes (> 3000m) : {nb_alt_hautes:,}")
    print(f"      → Suppression de ces lignes (erreurs de géolocalisation)")
    df_preparation = df_preparation[~anomalies_altitude_hautes]

# Anomalie 4 : Surfaces aberrantes
# Les logements avec des surfaces extrêmes sont exclus car ils faussent les statistiques :
# - < 5m² : boxes/garages (hors périmètre des logements résidentiels) ou erreurs de saisie
# - > 500m² : immeubles entiers saisis comme logement unique (erreur administrative)
#             ou propriétés exceptionnelles (châteaux, manoirs) non représentatives
#
# Impact : ces logements (~734 soit 0.36%) fausseraient les comptages par catégorie DPE
# et ne reflètent pas le parc résidentiel typique. Leur exclusion garantit une analyse
# sur des logements comparables et représentatifs.
anomalies_surface_basses = df_preparation['surface_habitable_logement'] < 5
anomalies_surface_hautes = df_preparation['surface_habitable_logement'] > 500
nb_surf_basses = anomalies_surface_basses.sum()
nb_surf_hautes = anomalies_surface_hautes.sum()

if nb_surf_basses > 0:
    print(f"   ⚠️  Surfaces aberrantes (< 5m²) : {nb_surf_basses:,}")
    print(f"      → Suppression (box/garage, hors scope logement résidentiel)")
    df_preparation = df_preparation[~anomalies_surface_basses]

if nb_surf_hautes > 0:
    print(f"   ⚠️  Surfaces aberrantes (> 500m²) : {nb_surf_hautes:,}")
    print(f"      → Suppression (immeubles entiers comptés comme logements individuels)")
    print(f"      → Impact : évite de fausser les comptages DPE (ex: +533 en classe C)")
    df_preparation = df_preparation[~anomalies_surface_hautes]

# Résumé des corrections
nb_total_supprimes = nb_avant_corrections - len(df_preparation)

if nb_total_supprimes > 0:
    print(f"\n   ✅ Total anomalies corrigées : {nb_total_supprimes:,} lignes supprimées")
    print(f"      ({nb_total_supprimes/nb_avant_corrections*100:.2f}% des données)")
else:
    print(f"   ✅ Aucune anomalie détectée - Données de bonne qualité")

print()

# ============================================================================
# EXPLORATION DES DONNÉES
# ============================================================================

print("📊 Exploration des données nettoyées...\n")

# Statistiques sur les colonnes principales
print("   🔢 Statistiques par colonne :\n")

# 1. Consommation
conso = df_preparation['conso_5_usages_par_m2_ep']
print(f"      Consommation énergétique (kWh/m²/an) :")
print(f"         Min     : {conso.min():6.1f}")
print(f"         Q1      : {conso.quantile(0.25):6.1f}")
print(f"         Médiane : {conso.median():6.1f}")
print(f"         Q3      : {conso.quantile(0.75):6.1f}")
print(f"         Max     : {conso.max():6.1f}")
print(f"         Moyenne : {conso.mean():6.1f}")

# 2. Altitude
altitude = df_preparation['altitude_moyenne']
print(f"\n      Altitude (mètres) :")
print(f"         Min     : {altitude.min():6.0f}m")
print(f"         Q1      : {altitude.quantile(0.25):6.0f}m")
print(f"         Médiane : {altitude.median():6.0f}m")
print(f"         Q3      : {altitude.quantile(0.75):6.0f}m")
print(f"         Max     : {altitude.max():6.0f}m")
print(f"         Moyenne : {altitude.mean():6.0f}m")

# 3. Surface habitable
surface = df_preparation['surface_habitable_logement']
print(f"\n      Surface habitable (m²) :")
print(f"         Min     : {surface.min():6.0f}m²")
print(f"         Q1      : {surface.quantile(0.25):6.0f}m²")
print(f"         Médiane : {surface.median():6.0f}m²")
print(f"         Q3      : {surface.quantile(0.75):6.0f}m²")
print(f"         Max     : {surface.max():6.0f}m²")
print(f"         Moyenne : {surface.mean():6.0f}m²")

# 4. Répartition des étiquettes DPE
print(f"\n      Répartition des étiquettes DPE :")
dpe_counts = df_preparation['etiquette_dpe'].value_counts().sort_index()
for etiquette, count in dpe_counts.items():
    pct = count / len(df_preparation) * 100
    print(f"         {etiquette} : {count:7,} ({pct:5.1f}%)")

# 5. Répartition type de bâtiment
print(f"\n      Type de bâtiment :")
batiment_counts = df_preparation['type_batiment'].value_counts()
for type_bat, count in batiment_counts.items():
    pct = count / len(df_preparation) * 100
    print(f"         {type_bat:20s} : {count:7,} ({pct:5.1f}%)")

# 6. Répartition période de construction
print(f"\n      Période de construction :")
periode_counts = df_preparation['periode_construction'].value_counts().sort_index()
for periode, count in periode_counts.items():
    pct = count / len(df_preparation) * 100
    print(f"         {periode:20s} : {count:7,} ({pct:5.1f}%)")

print()

# ============================================================================
# AJOUT DES CATÉGORIES D'ALTITUDE
# ============================================================================

print(f"🏔️  Catégorisation des logements par tranche d'altitude...\n")

# Application de la fonction de catégorisation définie dans config.py
# Les tranches sont définies dans SEUILS_ALTITUDE (ex: 0-600m, 600-1200m, etc.)
df_preparation['tranche_altitude'] = df_preparation['altitude_moyenne'].apply(categoriser_altitude)

# Affichage de la répartition par tranche
print("   📊 Répartition des logements par tranche d'altitude :\n")
repartition = df_preparation['tranche_altitude'].value_counts().sort_index()

for tranche, effectif in repartition.items():
    pourcentage = (effectif / len(df_preparation)) * 100
    print(f"      {tranche:35s} : {effectif:8,} logements ({pourcentage:5.1f}%)")

print()

# ============================================================================
# EXPORT DES DONNÉES PRÉPARÉES
# ============================================================================

print("💾 Sauvegarde des données préparées...\n")

# Export du fichier CSV préparé et nettoyé
fichier_sortie = DATA_PROCESSED_PATH / f"logements_{DEPARTEMENT}_cleaned.csv"
df_preparation.to_csv(fichier_sortie, index=False)
print(f"   ✅ Fichier sauvegardé : {fichier_sortie}")
print(f"   📏 Dimensions : {len(df_preparation):,} lignes × {len(df_preparation.columns)} colonnes")

# Export des métadonnées au format JSON pour traçabilité
metadata = {
    'departement': str(DEPARTEMENT),
    'nom_departement': str(NOM_DEPARTEMENT),
    'nb_logements_total': int(len(df_preparation)),
    'nb_logements_avec_altitude': int(nb_avec_altitude),
    'taux_altitude_pct': float(taux_altitude),
    'altitude_min': float(df_preparation['altitude_moyenne'].min()),
    'altitude_max': float(df_preparation['altitude_moyenne'].max()),
    'altitude_moyenne': float(df_preparation['altitude_moyenne'].mean()),
    'conso_moyenne': float(df_preparation['conso_5_usages_par_m2_ep'].mean()),
    'conso_mediane': float(df_preparation['conso_5_usages_par_m2_ep'].median())
}

fichier_metadata = DATA_PROCESSED_PATH / f"metadata_{DEPARTEMENT}.json"
with open(fichier_metadata, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"   ✅ Métadonnées sauvegardées : {fichier_metadata}")

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================

print("\n" + "="*80)
print("✅ PRÉPARATION DES DONNÉES TERMINÉE AVEC SUCCÈS")
print("="*80)
print(f"\n📂 Fichier prêt pour l'analyse : {fichier_sortie}")
print(f"📊 {nb_avec_altitude:,} logements géolocalisés disponibles pour les graphiques\n")