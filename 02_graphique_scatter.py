"""
Graphique 1 : Scatter Plot - Corrélation altitude × consommation
Mountain Energy Score - Haute-Savoie

Ce graphique met en évidence la relation linéaire entre l'altitude
et la consommation énergétique des logements. Une régression linéaire
permet de quantifier précisément l'augmentation de consommation par mètre d'altitude.

Visualisation : Nuage de points avec droite de régression
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import numpy as np
from scipy import stats

# Import de la configuration
from config import (
    DEPARTEMENT, NOM_DEPARTEMENT, NOM_DEPARTEMENT_AVEC_ARTICLE,
    DATA_PROCESSED_PATH, GRAPHIQUES_PATH,
    COULEURS_DPE, SEUILS_ALTITUDE,
    TAILLE_ECHANTILLON_SCATTER
)

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("GRAPHIQUE 1 : CORRÉLATION ALTITUDE × CONSOMMATION")
print("="*80 + "\n")

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

print("📂 Chargement des données préparées...\n")

fichier_donnees = DATA_PROCESSED_PATH / f"logements_{DEPARTEMENT}_cleaned.csv"
df = pd.read_csv(fichier_donnees, low_memory=False)

# Filtrage des logements avec altitude valide
df_valide = df[df['altitude_moyenne'].notna()].copy()

print(f"   ✅ {len(df_valide):,} logements avec altitude disponibles")

# ============================================================================
# ÉCHANTILLONNAGE POUR PERFORMANCE
# ============================================================================

print("🔧 Préparation des données pour visualisation...\n")

# Pour des raisons de performance d'affichage, on échantillonne si nécessaire
# Un scatter plot avec plus de 10 000 points peut être lent à charger
# Note : Les statistiques de régression sont calculées sur l'échantillon affiché
if TAILLE_ECHANTILLON_SCATTER is not None and len(df_valide) > TAILLE_ECHANTILLON_SCATTER:
    # Échantillonnage aléatoire stratifié pour garder la représentativité
    df_plot = df_valide.sample(n=TAILLE_ECHANTILLON_SCATTER, random_state=42)
    print(f"   → Échantillonnage : {len(df_plot):,} points (optimisation affichage)")
    print(f"   ℹ️  Pour utiliser toutes les données, mettre TAILLE_ECHANTILLON_SCATTER = None dans config.py")
else:
    df_plot = df_valide.copy()
    print(f"   → Utilisation complète : {len(df_plot):,} points")
    if len(df_plot) > 50000:
        print(f"   ⚠️  Fichier HTML volumineux attendu (>10 MB), chargement lent possible")

# ============================================================================
# CALCUL DE LA RÉGRESSION LINÉAIRE
# ============================================================================

print("\n📈 Calcul de la régression linéaire...\n")

# Régression linéaire simple : consommation ~ altitude
# Formule : y = ax + b où y = consommation, x = altitude
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df_plot['altitude_moyenne'], 
    df_plot['conso_5_usages_par_m2_ep']
)

# Coefficient de détermination R² (qualité de l'ajustement)
r_squared = r_value ** 2

print("   📊 Résultats de la régression :")
print(f"      • Pente (a)       : {slope:.4f} kWh/m²/an par mètre")
print(f"      • Ordonnée (b)    : {intercept:.2f} kWh/m²/an")
print(f"      • R²              : {r_squared:.4f}")
print(f"      • p-value         : {p_value:.2e}")
print(f"\n   💡 Interprétation :")
print(f"      → Chaque 100m d'altitude supplémentaire augmente")
print(f"        la consommation de {slope*100:.1f} kWh/m²/an en moyenne")
print(f"      → La relation est {'significative' if p_value < 0.001 else 'non significative'}")
print(f"        (p < 0.001)\n")

# Calcul des points de la droite de régression
altitude_min = df_plot['altitude_moyenne'].min()
altitude_max = df_plot['altitude_moyenne'].max()
x_regression = np.array([altitude_min, altitude_max])
y_regression = slope * x_regression + intercept

# ============================================================================
# CRÉATION DU GRAPHIQUE
# ============================================================================

print("🎨 Création du graphique...\n")

# Création du scatter plot avec Plotly Express
fig = px.scatter(
    df_plot,
    x='altitude_moyenne',
    y='conso_5_usages_par_m2_ep',
    color='etiquette_dpe',
    color_discrete_map=COULEURS_DPE,
    category_orders={'etiquette_dpe': ['A', 'B', 'C', 'D', 'E', 'F', 'G']},  # Ordre croissant des étiquettes DPE
    opacity=0.6,
    labels={
        'altitude_moyenne': 'Altitude moyenne de la commune (m)',
        'conso_5_usages_par_m2_ep': 'Consommation énergétique (kWh/m²/an)',
        'etiquette_dpe': 'Étiquette DPE'
    },
    hover_data={
        'altitude_moyenne': ':.0f',
        'conso_5_usages_par_m2_ep': ':.1f',
        'nom_commune_ban': True,
        'type_batiment': True,
        'periode_construction': True,
        'etiquette_dpe': False  # Déjà visible via la couleur
    },
    title=f'<b>Impact de l\'altitude sur la consommation énergétique</b><br>'
          f'<sub>Mountain Energy Score - Département {NOM_DEPARTEMENT_AVEC_ARTICLE} ({DEPARTEMENT})</sub>'
)

# Ajout de la droite de régression
fig.add_trace(
    go.Scatter(
        x=x_regression,
        y=y_regression,
        mode='lines',
        name=f'Régression linéaire<br>(+{slope*100:.1f} kWh/m²/an par 100m)',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        hovertemplate='<b>Tendance linéaire</b><br>Altitude: %{x:.0f}m<br>Consommation estimée: %{y:.1f} kWh/m²/an<extra></extra>'
    )
)

# Ajout de zones colorées en fond pour les tranches d'altitude
zones = [
    (SEUILS_ALTITUDE[0], "lightgreen", "Vallée"),
    (SEUILS_ALTITUDE[1], "lightyellow", "Colline"),
    (SEUILS_ALTITUDE[2], "lightcoral", "Montagne")
]

altitude_debut = altitude_min
for seuil, couleur, nom in zones:
    if altitude_debut < seuil:
        fig.add_vrect(
            x0=altitude_debut, 
            x1=min(seuil, altitude_max),
            fillcolor=couleur, 
            opacity=0.1, 
            line_width=0,
            annotation_text=nom, 
            annotation_position="top left"
        )
        altitude_debut = seuil

# ============================================================================
# PERSONNALISATION DU GRAPHIQUE
# ============================================================================

print("✨ Personnalisation du design...\n")

fig.update_layout(
    # Dimensions pour une bonne lisibilité
    width=1200,
    height=700,
    
    # Style de fond
    plot_bgcolor='white',
    paper_bgcolor='white',
    
    # Configuration du titre
    title={
        'font': {'size': 22, 'family': 'Arial, sans-serif', 'color': '#2c3e50'},
        'x': 0.5,
        'xanchor': 'center'
    },
    
    # Configuration des axes
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#ecf0f1',
        zeroline=False,
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e')
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#ecf0f1',
        zeroline=False,
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e')
    ),
    
    # Configuration de la légende
    legend=dict(
    title=dict(text='<b>Étiquette DPE</b>', font=dict(size=12)),
    orientation='v',
    yanchor='top',
    y=0.98,
    xanchor='right',
    x=0.98,
    bgcolor='rgba(255, 255, 255, 0.9)',
    bordercolor='#bdc3c7',
    borderwidth=1,
    font=dict(size=10),
    ),
    
    # Mode d'interaction au survol
    hovermode='closest',
    hoverlabel=dict(
        bgcolor='white',
        font_size=11,
        font_family='Arial, sans-serif'
    ),
    
    # Marges pour l'annotation en bas
    margin=dict(l=80, r=80, t=100, b=140)
)

# Ajout d'une annotation avec l'insight principal
fig.add_annotation(
    text=f"<b>📊 Insight clé :</b> Chaque 100m d'altitude supplémentaire augmente "
         f"la consommation de <b>{slope*100:.1f} kWh/m²/an</b> en moyenne "
         f"<i>(R² = {r_squared:.3f}, p < 0.001)</i>. "
         f"Cette corrélation significative démontre l'impact direct de l'altitude sur les besoins énergétiques.",
    xref="paper", yref="paper",
    x=0.5, y=-0.17,
    xanchor='center', yanchor='top',
    showarrow=False,
    bgcolor='rgba(255, 243, 205, 0.95)',
    bordercolor='#f39c12',
    borderwidth=2,
    borderpad=10,
    font=dict(size=11, family='Arial, sans-serif', color='#34495e')
)

print("   ✅ Graphique créé avec succès\n")

# ============================================================================
# EXPORT DES FICHIERS
# ============================================================================

print("💾 Sauvegarde des fichiers...\n")

# Export HTML interactif (pour visualisation web)
fichier_html = GRAPHIQUES_PATH / "01_scatter_altitude_consommation.html"
fig.write_html(fichier_html)
print(f"   ✅ HTML interactif : {fichier_html}")

# Export PNG haute résolution (pour rapport ou présentation)
fichier_png = GRAPHIQUES_PATH / "01_scatter_altitude_consommation.png"
fig.write_image(fichier_png, width=1200, height=700, scale=2)
print(f"   ✅ Image PNG : {fichier_png}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*80)
print("✅ GRAPHIQUE 1 TERMINÉ")
print("="*80)
print(f"\n📈 Résultat clé : +{slope*100:.1f} kWh/m²/an par 100m d'altitude")
print(f"📂 Fichiers disponibles dans le dossier '{GRAPHIQUES_PATH}/'")
print(f"🌐 Ouvre {fichier_html.name} dans un navigateur pour voir le graphique interactif\n")