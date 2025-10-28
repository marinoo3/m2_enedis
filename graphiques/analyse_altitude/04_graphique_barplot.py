"""
Graphique 3 : Barplot - Surcoût énergétique annuel par tranche d'altitude
Mountain Energy Score - Haute-Savoie

Ce graphique traduit les différences de consommation en impact financier concret.
Il montre le surcoût annuel moyen en euros pour un logement selon son altitude,
en prenant la vallée comme référence (surcoût = 0€).

Visualisation : Diagramme en barres avec surcoûts en euros
"""

import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import numpy as np

# Import de la configuration
from config import (
    DEPARTEMENT, NOM_DEPARTEMENT, NOM_DEPARTEMENT_AVEC_ARTICLE,
    DATA_PROCESSED_PATH, GRAPHIQUES_PATH,
    COULEURS_ALTITUDE, LABELS_ALTITUDE,
    PRIX_ELECTRICITE, SURFACE_REFERENCE
)

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("GRAPHIQUE 3 : SURCOÛT FINANCIER PAR TRANCHE D'ALTITUDE")
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
    (df['conso_5_usages_par_m2_ep'] <= 1000)
].copy()

print(f"   ✅ {len(df_valide):,} logements analysés\n")

# ============================================================================
# CALCUL DES CONSOMMATIONS MOYENNES PAR TRANCHE
# ============================================================================

print("📊 Calcul des consommations moyennes par tranche...\n")

# Ordre des tranches (du bas vers le haut)
ordre_tranches = [label for label in LABELS_ALTITUDE if label in df_valide['tranche_altitude'].unique()]

# Calcul de la consommation moyenne par tranche
stats_tranches = []

for tranche in ordre_tranches:
    donnees_tranche = df_valide[df_valide['tranche_altitude'] == tranche]['conso_5_usages_par_m2_ep']
    
    conso_moyenne = donnees_tranche.mean()
    effectif = len(donnees_tranche)
    
    stats_tranches.append({
        'tranche': tranche,
        'conso_moyenne': conso_moyenne,
        'effectif': effectif
    })
    
    print(f"   {tranche:35s} : {conso_moyenne:6.1f} kWh/m²/an (n = {effectif:,})")

print()

# ============================================================================
# CALCUL DES SURCOÛTS FINANCIERS
# ============================================================================

print("💰 Calcul des surcoûts financiers...\n")
print(f"   Paramètres de calcul :")
print(f"   • Prix électricité : {PRIX_ELECTRICITE:.2f} €/kWh")
print(f"   • Surface référence : {SURFACE_REFERENCE} m²\n")

# La vallée sert de référence (surcoût = 0€)
conso_reference = stats_tranches[0]['conso_moyenne']

# Calcul du surcoût pour chaque tranche
for stats in stats_tranches:
    # Différence de consommation par rapport à la vallée (kWh/m²/an)
    ecart_conso = stats['conso_moyenne'] - conso_reference
    
    # Surcoût annuel pour un logement de référence (€/an)
    surcout_annuel = ecart_conso * SURFACE_REFERENCE * PRIX_ELECTRICITE
    
    stats['ecart_conso'] = ecart_conso
    stats['surcout_annuel'] = surcout_annuel
    
    print(f"   {stats['tranche']:35s}")
    print(f"      Écart consommation : {ecart_conso:+7.1f} kWh/m²/an")
    print(f"      Surcoût annuel     : {surcout_annuel:+7.0f} €/an")
    print()

# ============================================================================
# ANALYSE DÉTAILLÉE DES TRANCHES HAUTES
# ============================================================================

print("\n📊 Analyse détaillée des tranches montagneuses...\n")

# Comparaison des deux tranches les plus hautes
if len(stats_tranches) >= 2:
    montagne = stats_tranches[-2]
    haute_montagne = stats_tranches[-1]
    
    print(f"   {montagne['tranche']} :")
    print(f"      Conso moyenne : {montagne['conso_moyenne']:.1f} kWh/m²/an")
    print(f"      Effectif      : {montagne['effectif']:,} logements")
    
    print(f"\n   {haute_montagne['tranche']} :")
    print(f"      Conso moyenne : {haute_montagne['conso_moyenne']:.1f} kWh/m²/an")
    print(f"      Effectif      : {haute_montagne['effectif']:,} logements")
    
    ecart = haute_montagne['conso_moyenne'] - montagne['conso_moyenne']
    print(f"\n   💡 Écart entre les deux : {ecart:+.1f} kWh/m²/an")
    
    if abs(ecart) < 5:
        print(f"      → Pas de différence significative au-delà de 1200m d'altitude")
        print(f"      → Hypothèse : plateau de consommation en haute altitude")

# ============================================================================
# CRÉATION DU GRAPHIQUE
# ============================================================================

print("🎨 Création du graphique barplot...\n")

# Préparation des données pour le graphique
tranches_noms = [s['tranche'] for s in stats_tranches]
surcouts = [s['surcout_annuel'] for s in stats_tranches]
consos = [s['conso_moyenne'] for s in stats_tranches]
effectifs = [s['effectif'] for s in stats_tranches]

# Couleurs pour les barres
couleurs_barres = [COULEURS_ALTITUDE.get(t, '#95a5a6') for t in tranches_noms]

# Création du graphique
fig = go.Figure()

fig.add_trace(go.Bar(
    x=tranches_noms,
    y=surcouts,
    marker_color=couleurs_barres,
    text=[f"<b>{s:.0f} €/an</b><br>({c:.0f} kWh/m²/an)<br>n = {e:,}" 
          for s, c, e in zip(surcouts, consos, effectifs)],
    textposition='inside',  
    textfont=dict(size=12, color='white', family='Arial, sans-serif'),  
    hovertemplate=(
        '<b>%{x}</b><br>' +
        'Surcoût annuel: %{y:.0f} €/an<br>' +
        'Consommation: %{customdata[0]:.0f} kWh/m²/an<br>' +
        'Effectif: %{customdata[1]:,} logements<br>' +
        '<extra></extra>'
    ),
    customdata=[[c, e] for c, e in zip(consos, effectifs)]
))

# ============================================================================
# PERSONNALISATION DU GRAPHIQUE
# ============================================================================

print("✨ Personnalisation du design...\n")

# Calcul du surcoût maximum pour l'annotation
surcout_max = max(surcouts)
tranche_max = tranches_noms[surcouts.index(surcout_max)]
conso_max = consos[surcouts.index(surcout_max)]

fig.update_layout(
    # Titre
    title={
        'text': (
            '<b>Surcoût énergétique annuel par tranche d\'altitude</b><br>'
            f'<sub>Mountain Energy Score - Département {NOM_DEPARTEMENT_AVEC_ARTICLE} ({DEPARTEMENT}) - '
            f'Logement de référence : {SURFACE_REFERENCE}m², prix électricité {PRIX_ELECTRICITE}€/kWh</sub>'
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
        title='<b>Surcoût énergétique annuel (€/an)</b>',
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e'),
        showgrid=True,
        gridwidth=1,
        gridcolor='#ecf0f1',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='#34495e'
    ),
    
    # Style
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    
    # Dimensions
    width=1200,
    height=700,
    
    # Marges
    margin=dict(l=80, r=80, t=120, b=160)
)

# Ajout de l'insight
fig.add_annotation(
    text=(
        f"<b>💰 Insight clé :</b> Vivre en {tranche_max.lower()} coûte <b>+{surcout_max:.0f}€/an</b> "
        f"de plus en énergie par rapport à la vallée pour un logement de {SURFACE_REFERENCE}m².<br>"
        f"Cela représente l'équivalent de <b>{surcout_max/12:.0f}€ par mois</b> de facture énergétique supplémentaire, "
        f"soit un budget non négligeable pour les ménages vivant en altitude."
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
fichier_html = GRAPHIQUES_PATH / "03_barplot_surcout_altitude.html"
fig.write_html(fichier_html)
print(f"   ✅ HTML interactif : {fichier_html}")

# Export PNG haute résolution
fichier_png = GRAPHIQUES_PATH / "03_barplot_surcout_altitude.png"
fig.write_image(fichier_png, width=1200, height=700, scale=2)
print(f"   ✅ Image PNG : {fichier_png}")

# Export CSV des statistiques
df_stats = pd.DataFrame(stats_tranches)
fichier_stats = GRAPHIQUES_PATH / "stats_surcout.csv"
df_stats.to_csv(fichier_stats, index=False)
print(f"   ✅ Statistiques : {fichier_stats}")

# ============================================================================
# RÉSUMÉ
# ============================================================================

print("\n" + "="*80)
print("✅ GRAPHIQUE 3 TERMINÉ")
print("="*80)
print(f"\n💰 Résultat clé : +{surcout_max:.0f}€/an de surcoût maximum en {tranche_max.lower()}")
print(f"📂 Fichiers disponibles dans le dossier '{GRAPHIQUES_PATH}/'")
print(f"🌐 Ouvre {fichier_html.name} dans un navigateur pour voir le graphique interactif\n")