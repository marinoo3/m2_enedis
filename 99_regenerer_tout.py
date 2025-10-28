"""
Script de régénération complète du projet Mountain Energy Score
Haute-Savoie (74)

Ce script exécute séquentiellement tous les scripts de génération
pour recréer l'ensemble des graphiques et la page HTML finale.

Utilisation : python 00_regenerer_tout.py
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

# Liste des scripts à exécuter dans l'ordre
SCRIPTS = [
    "01_preparation_donnees.py",
    "02_graphique_scatter.py",
    "03_graphique_boxplot.py",
    "04_graphique_barplot.py",
    "05_graphique_barres_dpe.py",
    "06_graphique_periode_construction.py",
    "07_page_complete.py",
    "08_generer_html_standalone.py"
]

# ============================================================================
# AFFICHAGE D'EN-TÊTE
# ============================================================================

print("\n" + "="*80)
print("🚀 RÉGÉNÉRATION COMPLÈTE DU PROJET MOUNTAIN ENERGY SCORE")
print("="*80)
print(f"📅 Démarré le : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}")
print(f"📊 Nombre de scripts à exécuter : {len(SCRIPTS)}\n")

# ============================================================================
# EXÉCUTION SÉQUENTIELLE
# ============================================================================

resultats = []
debut_total = datetime.now()

for i, script in enumerate(SCRIPTS, 1):
    print("─" * 80)
    print(f"▶️  [{i}/{len(SCRIPTS)}] Exécution de : {script}")
    print("─" * 80)
    
    # Vérifier que le script existe
    if not Path(script).exists():
        print(f"❌ ERREUR : Le fichier {script} n'existe pas !")
        resultats.append({
            'script': script,
            'statut': 'INTROUVABLE',
            'duree': 0
        })
        continue
    
    # Exécuter le script
    debut = datetime.now()
    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=300  # Timeout de 5 minutes par script
        )
        
        duree = (datetime.now() - debut).total_seconds()
        
        # Afficher la sortie du script
        if result.stdout:
            print(result.stdout)
        
        # Vérifier le code de retour
        if result.returncode == 0:
            print(f"✅ {script} terminé avec succès en {duree:.1f}s\n")
            resultats.append({
                'script': script,
                'statut': 'SUCCÈS',
                'duree': duree
            })
        else:
            print(f"❌ ERREUR dans {script} (code {result.returncode})")
            if result.stderr:
                print(f"Détails de l'erreur :\n{result.stderr}")
            resultats.append({
                'script': script,
                'statut': 'ERREUR',
                'duree': duree
            })
            
    except subprocess.TimeoutExpired:
        duree = (datetime.now() - debut).total_seconds()
        print(f"⏱️  TIMEOUT : {script} a dépassé le temps limite (5 minutes)")
        resultats.append({
            'script': script,
            'statut': 'TIMEOUT',
            'duree': duree
        })
        
    except Exception as e:
        duree = (datetime.now() - debut).total_seconds()
        print(f"❌ EXCEPTION lors de l'exécution de {script} : {e}")
        resultats.append({
            'script': script,
            'statut': 'EXCEPTION',
            'duree': duree
        })

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================

duree_totale = (datetime.now() - debut_total).total_seconds()

print("\n" + "="*80)
print("📊 RÉSUMÉ DE L'EXÉCUTION")
print("="*80 + "\n")

# Comptage des statuts
nb_succes = sum(1 for r in resultats if r['statut'] == 'SUCCÈS')
nb_erreurs = sum(1 for r in resultats if r['statut'] in ['ERREUR', 'EXCEPTION', 'TIMEOUT'])
nb_introuvables = sum(1 for r in resultats if r['statut'] == 'INTROUVABLE')

print(f"✅ Succès      : {nb_succes}/{len(SCRIPTS)}")
print(f"❌ Erreurs     : {nb_erreurs}/{len(SCRIPTS)}")
print(f"❓ Introuvable : {nb_introuvables}/{len(SCRIPTS)}")
print(f"⏱️  Durée totale : {duree_totale:.1f}s ({duree_totale/60:.1f} min)\n")

# Tableau détaillé
print("Détail par script :\n")
print(f"{'Script':<45} {'Statut':<15} {'Durée (s)':<10}")
print("─" * 80)
for r in resultats:
    statut_emoji = {
        'SUCCÈS': '✅',
        'ERREUR': '❌',
        'EXCEPTION': '❌',
        'TIMEOUT': '⏱️ ',
        'INTROUVABLE': '❓'
    }.get(r['statut'], '❓')
    
    print(f"{r['script']:<45} {statut_emoji} {r['statut']:<13} {r['duree']:>8.1f}s")

print("\n" + "="*80)

# ============================================================================
# MESSAGE FINAL
# ============================================================================

if nb_succes == len(SCRIPTS):
    print("🎉 TOUS LES SCRIPTS ONT ÉTÉ EXÉCUTÉS AVEC SUCCÈS !")
    print("\n📂 Résultats disponibles dans le dossier 'graphiques/'")
    print("🌐 Ouvre 'graphiques/mountain_energy_score_rapport_complet.html' dans un navigateur\n")
elif nb_erreurs > 0:
    print(f"⚠️  {nb_erreurs} script(s) ont rencontré des erreurs")
    print("📋 Vérifie les messages d'erreur ci-dessus pour plus de détails\n")
else:
    print("✅ Régénération terminée avec quelques avertissements\n")

print("="*80 + "\n")