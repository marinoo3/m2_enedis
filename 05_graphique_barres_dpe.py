"""
Graphique 4 : Concentration des passoires thermiques par altitude
Mountain Energy Score - Haute-Savoie

Ce graphique visualise la proportion de passoires thermiques (F et G) 
ainsi que des bons DPE (A et B) selon les tranches d'altitude.
Le contraste visuel met en évidence l'augmentation des passoires en montagne.

Visualisation : Barres empilées à 100% avec focus F/G
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Import de la configuration
from config import (
    DEPARTEMENT, NOM_DEPARTEMENT, NOM_DEPARTEMENT_AVEC_ARTICLE,
    DATA_PROCESSED_PATH, GRAPHIQUES_PATH,
    LABELS_ALTITUDE
)

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("GRAPHIQUE 4 : CONCENTRATION DES PASSOIRES THERMIQUES PAR ALTITUDE")
print("="*80 + "\n")

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================

print("📂 Chargement des données préparées...\n")

fichier_donnees = DATA_PROCESSED_PATH / f"logements_{DEPARTEMENT}_cleaned.csv"
df = pd.read_csv(fichier_donnees, low_memory=False)

# Filtrage des données valides
df_valide = df[
    (df['altitude_moyenne'].notna()) & 
    (df['tranche_altitude'] != 'Non renseigné') &
    (df['etiquette_dpe'].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G']))
].copy()

print(f"   ✅ {len(df_valide):,} logements avec DPE et altitude valides\n")

# ============================================================================
# CALCUL DES CATÉGORIES PAR TRANCHE
# ============================================================================

print("📊 Calcul de la répartition par catégories...\n")

# Ordre des tranches
ordre_tranches = [label for label in LABELS_ALTITUDE if label in df_valide['tranche_altitude'].unique()]

# Création des catégories simplifiées
def categoriser_dpe(etiquette):
    if etiquette in ['A', 'B']:
        return 'Bons (A-B)'
    elif etiquette in ['C', 'D']:
        return 'Moyens (C-D)'
    elif etiquette == 'E':
        return 'Médiocres (E)'
    else:  # F ou G
        return 'Passoires (F-G)'

df_valide['categorie_dpe'] = df_valide['etiquette_dpe'].apply(categoriser_dpe)

# Calcul des proportions par tranche
stats_par_tranche = []

for tranche in ordre_tranches:
    donnees_tranche = df_valide[df_valide['tranche_altitude'] == tranche]
    total = len(donnees_tranche)
    
    # Comptage par catégorie
    categories = donnees_tranche['categorie_dpe'].value_counts()
    
    stats = {
        'tranche': tranche,
        'total': total,
        'pct_bons': (categories.get('Bons (A-B)', 0) / total * 100),
        'pct_moyens': (categories.get('Moyens (C-D)', 0) / total * 100),
        'pct_mediocres': (categories.get('Médiocres (E)', 0) / total * 100),
        'pct_passoires': (categories.get('Passoires (F-G)', 0) / total * 100),
        'nb_passoires': categories.get('Passoires (F-G)', 0)
    }
    
    stats_par_tranche.append(stats)
    
    print(f"   {tranche:35s}")
    print(f"      Bons (A-B)      : {stats['pct_bons']:5.1f}%")
    print(f"      Moyens (C-D)    : {stats['pct_moyens']:5.1f}%")
    print(f"      Médiocres (E)   : {stats['pct_mediocres']:5.1f}%")
    print(f"      Passoires (F-G) : {stats['pct_passoires']:5.1f}% ({stats['nb_passoires']:,})")
    print()

# Calcul du ratio
pct_vallee = stats_par_tranche[0]['pct_passoires']
pct_montagne_max = max([s['pct_passoires'] for s in stats_par_tranche])
ratio = pct_montagne_max / pct_vallee if pct_vallee > 0 else 0

print(f"   💡 Ratio passoires montagne/vallée : ×{ratio:.1f}\n")

# ============================================================================
# CRÉATION DU GRAPHIQUE BARRES EMPILÉES
# ============================================================================

print("🎨 Création du graphique...\n")

tranches_noms = [s['tranche'] for s in stats_par_tranche]

fig = go.Figure()

# Ordre d'empilement : du meilleur au pire (A-B en bas, F-G en haut)
fig.add_trace(go.Bar(
    name='Bons DPE (A-B)',
    x=tranches_noms,
    y=[s['pct_bons'] for s in stats_par_tranche],
    marker_color='#27ae60',
    text=[f"{s['pct_bons']:.1f}%" for s in stats_par_tranche],
    textposition='inside',
    textfont=dict(color='white', size=11),
    hovertemplate='<b>%{x}</b><br>Bons DPE (A-B): %{y:.1f}%<extra></extra>'
))

fig.add_trace(go.Bar(
    name='DPE moyens (C-D)',
    x=tranches_noms,
    y=[s['pct_moyens'] for s in stats_par_tranche],
    marker_color='#f39c12',
    text=[f"{s['pct_moyens']:.1f}%" for s in stats_par_tranche],
    textposition='inside',
    textfont=dict(color='white', size=11),
    hovertemplate='<b>%{x}</b><br>DPE moyens (C-D): %{y:.1f}%<extra></extra>'
))

fig.add_trace(go.Bar(
    name='DPE médiocres (E)',
    x=tranches_noms,
    y=[s['pct_mediocres'] for s in stats_par_tranche],
    marker_color='#e67e22',
    text=[f"{s['pct_mediocres']:.1f}%" for s in stats_par_tranche],
    textposition='inside',
    textfont=dict(color='white', size=11),
    hovertemplate='<b>%{x}</b><br>DPE médiocres (E): %{y:.1f}%<extra></extra>'
))

fig.add_trace(go.Bar(
    name='PASSOIRES THERMIQUES (F-G)',
    x=tranches_noms,
    y=[s['pct_passoires'] for s in stats_par_tranche],
    marker_color='#e74c3c',
    text=[f"<b>{s['pct_passoires']:.1f}%</b><br>({s['nb_passoires']:,})" for s in stats_par_tranche],
    textposition='inside',
    textfont=dict(color='white', size=12, family='Arial, sans-serif'),
    hovertemplate='<b>%{x}</b><br>Passoires (F-G): %{y:.1f}%<extra></extra>'
))

# ============================================================================
# PERSONNALISATION
# ============================================================================

print("✨ Personnalisation du design...\n")

fig.update_layout(
    # Empilement à 100%
    barmode='stack',
    
    # Titre
    title={
        'text': (
            '<b>Concentration des passoires thermiques selon l\'altitude</b><br>'
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
        tickfont=dict(size=11, color='#34495e')
    ),
    yaxis=dict(
        title='<b>Répartition des DPE (%)</b>',
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e'),
        range=[0, 100],
        ticksuffix='%'
    ),
    
    # Style
    plot_bgcolor='white',
    paper_bgcolor='white',
    
    # Légende
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
        font=dict(size=11)
    ),
    
    # Dimensions
    width=1200,
    height=700,
    
    # Marges
    margin=dict(l=80, r=80, t=140, b=160)
)

# Annotation
fig.add_annotation(
    text=(
        f"<b>🔥 Insight clé :</b> Les passoires thermiques (F/G) représentent "
        f"<b>{pct_vallee:.1f}%</b> des logements en vallée contre <b>{pct_montagne_max:.1f}%</b> en montagne,<br>"
        f"soit <b>×{ratio:.1f}</b> plus de risque d'avoir un logement énergivore en altitude. "
        f"Cette concentration révèle un enjeu majeur de rénovation énergétique en zone de montagne."
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
# EXPORT
# ============================================================================

print("💾 Sauvegarde des fichiers...\n")

fichier_html = GRAPHIQUES_PATH / "04_graphiques_barres_dpe.html"
fig.write_html(fichier_html)
print(f"   ✅ HTML interactif : {fichier_html}")

fichier_png = GRAPHIQUES_PATH / "04_graphiques_barres_dpe.png"
fig.write_image(fichier_png, width=1200, height=700, scale=2)
print(f"   ✅ Image PNG : {fichier_png}")

# Export stats
df_stats = pd.DataFrame(stats_par_tranche)
fichier_stats = GRAPHIQUES_PATH / "stats_dpe_altitude.csv"
df_stats.to_csv(fichier_stats, index=False)
print(f"   ✅ Statistiques : {fichier_stats}")

print("\n" + "="*80)
print("✅ GRAPHIQUE 4 TERMINÉ")
print("="*80)
print(f"\n🔥 Résultat clé : ×{ratio:.1f} plus de passoires thermiques en montagne")
print(f"📂 Fichiers disponibles dans le dossier '{GRAPHIQUES_PATH}/'")
print(f"🌐 Ouvre {fichier_html.name} dans un navigateur\n")