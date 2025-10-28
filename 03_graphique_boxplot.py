"""
Graphique 2 : Boxplot - Distribution de la consommation par tranche d'altitude
Mountain Energy Score - Haute-Savoie

Ce graphique compare la distribution des consommations énergétiques
selon les tranches d'altitude. Les boxplots permettent de visualiser
les médianes, quartiles et valeurs extrêmes pour chaque zone.

Visualisation : Boîtes à moustaches (boxplots)
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Import de la configuration
from config import (
    DEPARTEMENT, NOM_DEPARTEMENT, NOM_DEPARTEMENT_AVEC_ARTICLE,
    DATA_PROCESSED_PATH, GRAPHIQUES_PATH,
    COULEURS_ALTITUDE, LABELS_ALTITUDE
)

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("GRAPHIQUE 2 : DISTRIBUTION PAR TRANCHE D'ALTITUDE")
print("="*80 + "\n")

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

print("📂 Chargement des données préparées...\n")

fichier_donnees = DATA_PROCESSED_PATH / f"logements_{DEPARTEMENT}_cleaned.csv"
df = pd.read_csv(fichier_donnees, low_memory=False)

# Filtrage des données valides + suppression des outliers extrêmes
# Les consommations > 1000 kWh/m²/an sont souvent des erreurs de saisie
df_valide = df[
    (df['altitude_moyenne'].notna()) & 
    (df['tranche_altitude'] != 'Non renseigné') &
    (df['conso_5_usages_par_m2_ep'] <= 1000)  # Limite supérieure réaliste
].copy()

print(f"   ✅ {len(df_valide):,} logements avec tranche d'altitude valide")
print(f"   ℹ️  Outliers > 1000 kWh/m²/an exclus pour lisibilité\n")

# ============================================================================
# CALCUL DES STATISTIQUES PAR TRANCHE
# ============================================================================

print("📊 Calcul des statistiques par tranche d'altitude...\n")

# Ordre des tranches pour l'affichage (du bas vers le haut)
ordre_tranches = [label for label in LABELS_ALTITUDE if label in df_valide['tranche_altitude'].unique()]

# Calcul des statistiques descriptives pour chaque tranche
stats_par_tranche = []

for tranche in ordre_tranches:
    donnees_tranche = df_valide[df_valide['tranche_altitude'] == tranche]['conso_5_usages_par_m2_ep']
    
    stats = {
        'tranche': tranche,
        'effectif': len(donnees_tranche),
        'mediane': donnees_tranche.median(),
        'moyenne': donnees_tranche.mean(),
        'q1': donnees_tranche.quantile(0.25),
        'q3': donnees_tranche.quantile(0.75),
        'min': donnees_tranche.min(),
        'max': donnees_tranche.max()
    }
    stats_par_tranche.append(stats)
    
    print(f"   {tranche:35s}")
    print(f"      Effectif : {stats['effectif']:8,} logements")
    print(f"      Médiane  : {stats['mediane']:6.0f} kWh/m²/an")
    print(f"      Moyenne  : {stats['moyenne']:6.0f} kWh/m²/an")
    print(f"      Q1-Q3    : {stats['q1']:6.0f} - {stats['q3']:6.0f} kWh/m²/an")
    print()

# Calcul des écarts entre tranches
if len(stats_par_tranche) >= 2:
    ecart_vallee_montagne = stats_par_tranche[-1]['mediane'] - stats_par_tranche[0]['mediane']
    pct_augmentation = (ecart_vallee_montagne / stats_par_tranche[0]['mediane']) * 100
    
    print(f"   💡 Écart vallée → montagne haute :")
    print(f"      Différence médiane : +{ecart_vallee_montagne:.0f} kWh/m²/an")
    print(f"      Augmentation       : +{pct_augmentation:.1f}%\n")

# ============================================================================
# CRÉATION DU GRAPHIQUE
# ============================================================================

print("🎨 Création du graphique boxplot...\n")

fig = go.Figure()

# Ajout d'un boxplot pour chaque tranche d'altitude
for tranche in ordre_tranches:
    donnees_tranche = df_valide[df_valide['tranche_altitude'] == tranche]['conso_5_usages_par_m2_ep']
    
    fig.add_trace(go.Box(
        y=donnees_tranche,
        name=tranche,
        marker_color=COULEURS_ALTITUDE.get(tranche, '#95a5a6'),
        boxmean='sd',  # Affiche aussi la moyenne avec écart-type
        hovertemplate=(
            '<b>%{fullData.name}</b><br>' +
            'Médiane: %{median:.0f} kWh/m²/an<br>' +
            'Q1: %{q1:.0f} kWh/m²/an<br>' +
            'Q3: %{q3:.0f} kWh/m²/an<br>' +
            'Min: %{min:.0f} kWh/m²/an<br>' +
            'Max: %{max:.0f} kWh/m²/an<br>' +
            '<extra></extra>'
        )
    ))

# ============================================================================
# PERSONNALISATION DU GRAPHIQUE
# ============================================================================

print("✨ Personnalisation du design...\n")

fig.update_layout(
    # Titre
    title={
        'text': (
            '<b>Distribution de la consommation énergétique par tranche d\'altitude</b><br>'
            f'<sub>Mountain Energy Score - Département {NOM_DEPARTEMENT_AVEC_ARTICLE} ({DEPARTEMENT})</sub>'
        ),
        'font': {'size': 22, 'family': 'Arial, sans-serif', 'color': '#2c3e50'},
        'x': 0.5,
        'xanchor': 'center'
    },
    
    # Axes
    xaxis=dict(
        title='<b>Tranche d\'altitude</b>',
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e'),
        showgrid=False
    ),
    yaxis=dict(
        title='<b>Consommation énergétique (kWh/m²/an)</b>',
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#ecf0f1',
        zeroline=False
    ),
    
    # Style
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,  # Pas de légende nécessaire (noms sur l'axe X)
    
    # Dimensions
    width=1200,
    height=700,
    
    # Marges pour l'annotation
    margin=dict(l=80, r=80, t=100, b=160)
)

# Ajout de l'insight en annotation
if len(stats_par_tranche) >= 2:
    fig.add_annotation(
    text=(
        f"<b>📊 Insight clé :</b> La consommation médiane augmente de "
        f"<b>{ecart_vallee_montagne:.0f} kWh/m²/an</b> entre la vallée "
        f"({stats_par_tranche[0]['mediane']:.0f} kWh/m²/an) et la haute montagne "
        f"({stats_par_tranche[-1]['mediane']:.0f} kWh/m²/an), soit une hausse de "
        f"<b>{pct_augmentation:.1f}%</b>.<br>"
        f"La dispersion augmente également avec l'altitude, révélant une plus grande hétérogénéité des situations en montagne."
        ),
        xref="paper", yref="paper",
        x=0.5, y=-0.19,
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

# Export HTML interactif
fichier_html = GRAPHIQUES_PATH / "02_boxplot_altitude_consommation.html"
fig.write_html(fichier_html)
print(f"   ✅ HTML interactif : {fichier_html}")

# Export PNG haute résolution
fichier_png = GRAPHIQUES_PATH / "02_boxplot_altitude_consommation.png"
fig.write_image(fichier_png, width=1200, height=700, scale=2)
print(f"   ✅ Image PNG : {fichier_png}")

# ============================================================================
# EXPORT DES STATISTIQUES
# ============================================================================

# Sauvegarde des statistiques dans un fichier CSV pour référence
df_stats = pd.DataFrame(stats_par_tranche)
fichier_stats = GRAPHIQUES_PATH / "stats_boxplot.csv"
df_stats.to_csv(fichier_stats, index=False)
print(f"   ✅ Statistiques : {fichier_stats}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*80)
print("✅ GRAPHIQUE 2 TERMINÉ")
print("="*80)

if len(stats_par_tranche) >= 2:
    print(f"\n📈 Résultat clé : +{ecart_vallee_montagne:.0f} kWh/m²/an (+{pct_augmentation:.1f}%) vallée → montagne haute")

print(f"📂 Fichiers disponibles dans le dossier '{GRAPHIQUES_PATH}/'")
print(f"🌐 Ouvre {fichier_html.name} dans un navigateur pour voir le graphique interactif\n")