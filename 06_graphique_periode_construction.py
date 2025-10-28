"""
Graphique 5 : Impact de la période de construction selon l'altitude
Mountain Energy Score - Haute-Savoie

Ce graphique visualise la double peine : ancien bâti + altitude.
Il montre comment les logements construits avant les normes thermiques
sont particulièrement énergivores en zone de montagne.

Visualisation : Heatmap période de construction × altitude
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
print("GRAPHIQUE 5 : PÉRIODE DE CONSTRUCTION × ALTITUDE")
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
    (df['conso_5_usages_par_m2_ep'] <= 1000) &
    (df['periode_construction'].notna())
].copy()

print(f"   ✅ {len(df_valide):,} logements avec période de construction valide\n")

# ============================================================================
# CATÉGORISATION DES PÉRIODES
# ============================================================================

print("📅 Catégorisation des périodes de construction...\n")

def categoriser_periode(periode):
    """Regroupe les périodes de construction en grandes époques"""
    if pd.isna(periode):
        return 'Non renseigné'
    
    periode_str = str(periode).lower()
    
    # Avant 1975 (première réglementation thermique)
    if any(x in periode_str for x in ['avant', '1948', '1919', '1945', 'ancien']):
        return 'Avant 1975'
    # 1975-2000 (RT 1974, 1988, 2000)
    elif any(x in periode_str for x in ['1975', '1980', '1985', '1990', '1995', '2000']):
        return '1975-2000'
    # 2001-2012 (RT 2005, 2012)
    elif any(x in periode_str for x in ['2001', '2005', '2010', '2012']):
        return '2001-2012'
    # Après 2012 (RT 2012, RE 2020)
    elif any(x in periode_str for x in ['2013', '2015', '2020', '2021', 'récent']):
        return 'Après 2012'
    else:
        # Par défaut, essayer d'extraire une année
        import re
        annees = re.findall(r'\b(19|20)\d{2}\b', periode_str)
        if annees:
            annee = int(annees[0])
            if annee < 1975:
                return 'Avant 1975'
            elif annee < 2001:
                return '1975-2000'
            elif annee < 2013:
                return '2001-2012'
            else:
                return 'Après 2012'
        return 'Non renseigné'

df_valide['periode_categorie'] = df_valide['periode_construction'].apply(categoriser_periode)

# Filtrer les non renseignés
df_valide = df_valide[df_valide['periode_categorie'] != 'Non renseigné'].copy()

print("   Répartition par période :\n")
repartition = df_valide['periode_categorie'].value_counts().sort_index()
for periode, count in repartition.items():
    pct = (count / len(df_valide)) * 100
    print(f"      {periode:15s} : {count:8,} logements ({pct:5.1f}%)")
print()

# ============================================================================
# CALCUL DE LA HEATMAP PÉRIODE × ALTITUDE
# ============================================================================

print("🔥 Calcul de la heatmap période × altitude...\n")

# Ordre des tranches d'altitude
ordre_tranches = [label for label in LABELS_ALTITUDE if label in df_valide['tranche_altitude'].unique()]

# Ordre chronologique des périodes
ordre_periodes = ['Avant 1975', '1975-2000', '2001-2012', 'Après 2012']
ordre_periodes = [p for p in ordre_periodes if p in df_valide['periode_categorie'].unique()]

# Création du tableau période × altitude avec consommation moyenne
tableau_conso = pd.DataFrame(index=ordre_periodes, columns=ordre_tranches)
tableau_effectifs = pd.DataFrame(index=ordre_periodes, columns=ordre_tranches)

for periode in ordre_periodes:
    for tranche in ordre_tranches:
        mask = (df_valide['periode_categorie'] == periode) & (df_valide['tranche_altitude'] == tranche)
        logements = df_valide[mask]
        
        if len(logements) >= 10:  # Seuil minimum
            conso_moyenne = logements['conso_5_usages_par_m2_ep'].mean()
            effectif = len(logements)
            
            tableau_conso.loc[periode, tranche] = conso_moyenne
            tableau_effectifs.loc[periode, tranche] = effectif
            
            print(f"   {periode:15s} × {tranche:35s} : {conso_moyenne:6.0f} kWh/m²/an (n={effectif:,})")

print()

# ============================================================================
# ANALYSE DU PIRE CROISEMENT
# ============================================================================

print("🔍 Identification du pire croisement...\n")

# Convertir en numérique pour trouver le max
tableau_conso_numeric = tableau_conso.apply(pd.to_numeric, errors='coerce')
max_conso = tableau_conso_numeric.max().max()
max_position = tableau_conso_numeric.stack().idxmax()

pire_periode = max_position[0]
pire_tranche = max_position[1]

print(f"   🚨 Pire combinaison : {pire_periode} × {pire_tranche}")
print(f"      Consommation : {max_conso:.0f} kWh/m²/an")
print(f"      Effectif     : {int(tableau_effectifs.loc[pire_periode, pire_tranche]):,} logements\n")

# Comparaison avec le meilleur
min_conso = tableau_conso_numeric.min().min()
min_position = tableau_conso_numeric.stack().idxmin()

meilleur_periode = min_position[0]
meilleur_tranche = min_position[1]

ecart = max_conso - min_conso
pct_ecart = (ecart / max_conso) * 100

print(f"   ✅ Meilleure combinaison : {meilleur_periode} × {meilleur_tranche}")
print(f"      Consommation : {min_conso:.0f} kWh/m²/an")
print(f"   💡 Écart : {ecart:.0f} kWh/m²/an ({pct_ecart:.0f}%)\n")

# ============================================================================
# CRÉATION DE LA HEATMAP
# ============================================================================

print("🎨 Création de la heatmap...\n")

# Préparation des données
z_data = tableau_conso_numeric.values

# Texte dans chaque cellule avec couleur adaptative
text_data = []
for i, periode in enumerate(tableau_conso.index):
    row_text = []
    for j, tranche in enumerate(tableau_conso.columns):
        conso = tableau_conso.iloc[i, j]
        effectif = tableau_effectifs.iloc[i, j]
        if pd.notna(conso):
            # Choix de la couleur de texte selon le fond de la cellule pour garantir la lisibilité
            # Seuil 220 kWh/m²/an : correspond approximativement à la limite entre fonds clairs et foncés
            couleur = "black" if conso > 220 else "white"
            row_text.append(
                f"<span style='color:{couleur}'><b>{conso:.0f}</b> kWh/m²/an<br>({int(effectif):,})</span>"
            )
        else:
            row_text.append("")
    text_data.append(row_text)

# Création de la heatmap
fig = go.Figure(data=go.Heatmap(
    z=z_data,
    x=ordre_tranches,
    y=ordre_periodes,
    text=text_data,
    texttemplate='%{text}',
    textfont={"size": 10, "family": "Arial, sans-serif"},
    colorscale='RdYlGn_r',  # Rouge (mauvais) → Jaune → Vert (bon), inversé
    colorbar=dict(
        title=dict(
            text="Consommation<br>(kWh/m²/an)",
            side="right"
        ),
        thickness=15,
        len=0.7
    ),
    hovertemplate=(
        '<b>%{y}</b><br>' +
        '%{x}<br>' +
        'Consommation: <b>%{z:.0f} kWh/m²/an</b><br>' +
        '<extra></extra>'
    )
))

# ============================================================================
# PERSONNALISATION
# ============================================================================

print("✨ Personnalisation du design...\n")

fig.update_layout(
    # Titre
    title={
        'text': (
            '<b>Double peine : ancienneté du bâti × altitude</b><br>'
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
        tickfont=dict(size=10, color='#34495e'),
        side='bottom',
        tickangle=0
    ),
    yaxis=dict(
        title='<b>Période de construction</b>',
        title_font=dict(size=13, color='#34495e'),
        tickfont=dict(size=11, color='#34495e')
    ),
    
    # Style
    plot_bgcolor='white',
    paper_bgcolor='white',
    
    # Dimensions
    width=1200,
    height=700,
    
    # Marges
    margin=dict(l=120, r=150, t=120, b=160)
)

# Annotation avec insight clé
fig.add_annotation(
    text=(
        f"<b>🔥 Insight clé :</b> Les logements <b>{pire_periode}</b> en <b>{pire_tranche.lower()}</b> "
        f"consomment jusqu'à <b>{max_conso:.0f} kWh/m²/an</b>, soit <b>{pct_ecart:.0f}% de plus</b> "
        f"que les logements récents en vallée ({min_conso:.0f} kWh/m²/an).<br>"
        f"Cette double peine (ancien bâti + altitude) révèle une priorité absolue pour les politiques "
        f"de rénovation énergétique : <b>{int(tableau_effectifs.loc[pire_periode, pire_tranche]):,} logements</b> "
        f"sont concernés dans cette seule catégorie."
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

fichier_html = GRAPHIQUES_PATH / "05_heatmap_periode_altitude.html"
fig.write_html(fichier_html)
print(f"   ✅ HTML interactif : {fichier_html}")

fichier_png = GRAPHIQUES_PATH / "05_heatmap_periode_altitude.png"
fig.write_image(fichier_png, width=1200, height=700, scale=2)
print(f"   ✅ Image PNG : {fichier_png}")

# Export du tableau
fichier_tableau = GRAPHIQUES_PATH / "tableau_periode_altitude.csv"
tableau_conso.to_csv(fichier_tableau)
print(f"   ✅ Tableau : {fichier_tableau}")

print("\n" + "="*80)
print("✅ GRAPHIQUE 5 TERMINÉ")
print("="*80)
print(f"\n🔥 Double peine : {pire_periode} × {pire_tranche} = {max_conso:.0f} kWh/m²/an")
print(f"📂 Fichiers disponibles dans le dossier '{GRAPHIQUES_PATH}/'")
print(f"🌐 Ouvre {fichier_html.name} dans un navigateur\n")