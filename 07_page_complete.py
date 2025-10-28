"""
Page HTML complète : Mountain Energy Score
Haute-Savoie (74)

Page de présentation simple avec succession des graphiques
et un bloc narratif pour raconter la data story.
"""

from pathlib import Path
from config import DEPARTEMENT, NOM_DEPARTEMENT, GRAPHIQUES_PATH

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("GÉNÉRATION DE LA PAGE HTML COMPLÈTE")
print("="*80 + "\n")

# ============================================================================
# CONTENU HTML
# ============================================================================

html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mountain Energy Score - Haute-Savoie (74)</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background-color: #f8f9fa;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 60px;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .story {{
            background: white;
            padding: 40px;
            margin-bottom: 60px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }}
        
        .story h2 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .story p {{
            margin-bottom: 15px;
            font-size: 1.1em;
            text-align: justify;
        }}
        
        .story strong {{
            color: #e74c3c;
        }}
        
        .graphique {{
            background: white;
            padding: 20px;
            margin-bottom: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .graphique img {{
            width: 100%;
            height: auto;
            display: block;
            border-radius: 5px;
        }}
        
        footer {{
            text-align: center;
            padding: 30px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏔️ Mountain Energy Score</h1>
            <p>Impact de l'altitude sur la consommation énergétique des logements</p>
            <p>Département de la Haute-Savoie (74)</p>
        </header>
        
        <div class="story">
            <h2>📊 Analyse en 5 dimensions</h2>
            
            <p>
                Cette étude analyse la consommation énergétique de 207,603 logements en Haute-Savoie selon leur altitude, 
                en exploitant les données DPE de l'ADEME enrichies avec les données d'élévation de l'IGN. L'objectif est 
                de quantifier précisément l'impact de l'altitude sur la performance énergétique des bâtiments.
            </p>
            
            <p>
                <strong>1. Corrélation altitude-consommation :</strong> L'analyse de régression linéaire établit une relation 
                significative entre altitude et consommation énergétique. Le coefficient mesuré est de <strong>+9.1 kWh/m²/an 
                par tranche de 100 mètres d'altitude</strong> (R² = 0.31, p < 0.001). Cette corrélation positive confirme 
                l'hypothèse selon laquelle l'altitude constitue un facteur explicatif majeur de la consommation énergétique, 
                indépendamment des autres variables.
            </p>
            
            <p>
                <strong>2. Distribution par tranche d'altitude :</strong> La segmentation en quatre tranches révèle une 
                progression marquée de la consommation médiane : <strong>175 kWh/m²/an en vallée (0-600m) contre 
                277 kWh/m²/an en montagne (1200-1800m)</strong>, soit une augmentation de <strong>102 kWh/m²/an (+58%)</strong>. 
                La dispersion des valeurs augmente également avec l'altitude, indiquant une hétérogénéité croissante des 
                situations énergétiques en zone de montagne.
            </p>

            <p>
                <strong>Observation du pallier à 1200m :</strong> L'analyse révèle un phénomène remarquable : 
                <strong>au-delà de 1200m d'altitude, la consommation se stabilise</strong>. Les logements situés 
                entre 1200-1800m (montagne) et 1800-2500m (haute montagne) affichent des consommations quasi-identiques 
                (respectivement 294 et 293.7 kWh/m²/an, soit une différence négligeable de 0.3 kWh/m²/an). 
                Ce plateau suggère que <strong>les contraintes climatiques atteignent leur maximum d'impact autour de 1200m</strong>, 
                possiblement en raison d'une optimisation du bâti en très haute altitude (isolation renforcée, adaptation 
                architecturale) ou d'un effet plafond des besoins en chauffage. Cette observation indique que 
                <strong>la zone critique se situe dans la transition 600-1200m</strong>, où la consommation augmente 
                de 76.7 kWh/m²/an, soit l'essentiel du surcoût observé en altitude.
            </p>
            
            <p>
                <strong>3. Quantification du surcoût énergétique :</strong> La conversion en impact financier, basée sur 
                un logement de référence de 70m² et un prix de l'électricité de 0.20€/kWh, établit un surcoût annuel de 
                <strong>290€ en colline et 1,363€ en montagne</strong> par rapport à la vallée. Ce surcoût de 1,363€/an 
                représente un budget mensuel supplémentaire de 114€, soit un différentiel non négligeable dans le budget 
                énergétique des ménages résidant en altitude.
            </p>
            
            <p>
                <strong>4. Répartition des classes DPE :</strong> L'analyse de la distribution des étiquettes énergétiques 
                montre une concentration significativement plus élevée de passoires thermiques (F et G) en altitude. 
                La proportion passe de <strong>11.1% en vallée à 26.9% en montagne</strong>, soit un <strong>ratio de 2.4</strong>. 
                Cette surreprésentation des classes énergétiques défavorables en montagne traduit un décalage structurel 
                de la performance énergétique du parc immobilier selon l'altitude.
            </p>
            
            <p>
                <strong>5. Analyse croisée période de construction × altitude :</strong> La matrice croisant les périodes 
                de construction et les tranches d'altitude identifie les segments les plus critiques. Les logements 
                <strong>construits avant 1975 en montagne (1200-1800m) affichent une consommation moyenne de 364 kWh/m²/an</strong>, 
                soit <strong>3.3 fois supérieure</strong> aux logements récents (après 2012) en vallée (109 kWh/m²/an). 
                Cette catégorie représente <strong>13,432 logements</strong>, constituant un segment prioritaire pour 
                les actions de rénovation énergétique ciblées.
            </p>
            
            <p>
                <strong>Synthèse :</strong> L'altitude apparaît comme un déterminant majeur de la consommation énergétique 
                en Haute-Savoie, avec un effet mesurable (+9.1 kWh/m²/an par 100m), un impact financier substantiel 
                (+1,363€/an en montagne) et une concentration de logements énergivores en altitude. L'analyse croisée 
                avec la période de construction permet d'identifier précisément les 13,432 logements anciens en montagne 
                comme cible optimale pour maximiser l'efficacité des politiques de rénovation énergétique dans le département.
            </p>
        </div>
        
        <div class="graphique">
            <img src="01_scatter_altitude_consommation.png" alt="Graphique 1 : Corrélation altitude et consommation">
        </div>
        
        <div class="graphique">
            <img src="02_boxplot_altitude_consommation.png" alt="Graphique 2 : Distribution par tranche d'altitude">
        </div>
        
        <div class="graphique">
            <img src="03_barplot_surcout_altitude.png" alt="Graphique 3 : Surcoût financier par altitude">
        </div>
        
        <div class="graphique">
            <img src="04_graphiques_barres_dpe.png" alt="Graphique 4 : Concentration des passoires thermiques">
        </div>
        
        <div class="graphique">
            <img src="05_heatmap_periode_altitude.png" alt="Graphique 5 : Double peine ancienneté et altitude">
        </div>
        
        <footer>
            <p>Mountain Energy Score - Analyse des données DPE de l'ADEME</p>
            <p>Département de la Haute-Savoie (74) - 2025</p>
        </footer>
    </div>
</body>
</html>
"""

# ============================================================================
# SAUVEGARDE DU FICHIER HTML
# ============================================================================

print("💾 Génération de la page HTML...\n")

fichier_html = GRAPHIQUES_PATH / "mountain_energy_score_rapport_complet.html"

with open(fichier_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"   ✅ Page HTML créée : {fichier_html}\n")

# ============================================================================
# INSTRUCTIONS
# ============================================================================

print("="*80)
print("✅ PAGE HTML COMPLÈTE GÉNÉRÉE")
print("="*80)
print(f"\n📄 Ouvre le fichier dans un navigateur :")
print(f"   {fichier_html}")
print(f"\n💡 Tous tes graphiques PNG doivent être dans le même dossier")
print(f"   ({GRAPHIQUES_PATH}/)")