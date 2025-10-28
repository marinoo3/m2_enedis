from .plot import Plot

import pandas as pd
import plotly.graph_objects as go



class HeatMap(Plot):

    def __split_tranches(self) -> tuple[list, list, pd.DataFrame, pd.DataFrame]:

        ordre_tranches = [label for label in self.LABELS_ALTITUDE if label in self.df['classe_altitude'].unique()]

        # Ordre chronologique des périodes
        ordre_periodes = ['Avant 1975', '1975-2000', '2001-2012', 'Après 2012']
        ordre_periodes = [p for p in ordre_periodes if p in self.df['periode_categorie'].unique()]

        tableau_conso = pd.DataFrame(index=ordre_periodes, columns=ordre_tranches)
        tableau_effectifs = pd.DataFrame(index=ordre_periodes, columns=ordre_tranches)

        for periode in ordre_periodes:
            for tranche in ordre_tranches:
                mask = (self.df['periode_categorie'] == periode) & (self.df['classe_altitude'] == tranche)
                logements = self.df[mask]
                
                if len(logements) >= 10:  # Seuil minimum
                    conso_moyenne = logements['conso_5_usages_par_m2_ep'].mean()
                    effectif = len(logements)
                    
                    tableau_conso.loc[periode, tranche] = conso_moyenne
                    tableau_effectifs.loc[periode, tranche] = effectif

        return ordre_tranches, ordre_periodes, tableau_conso, tableau_effectifs
    
    def __cross_analysis(self, tableau_conso:pd.DataFrame) -> tuple[pd.DataFrame, float, float, float, float, float]:

        tableau_conso_numeric = tableau_conso.apply(pd.to_numeric, errors='coerce')
        max_conso = tableau_conso_numeric.max().max()
        max_position = tableau_conso_numeric.stack().idxmax()

        pire_periode = max_position[0]
        pire_tranche = max_position[1]

        # Comparaison avec le meilleur
        min_conso = tableau_conso_numeric.min().min()

        ecart = max_conso - min_conso
        pct_ecart = (ecart / max_conso) * 100

        return tableau_conso_numeric, pire_periode, pire_tranche, min_conso, max_conso, pct_ecart

    def _validate_data(self, df):
        df_valide = df[
            (df['altitude_moyenne'].notna()) & 
            (df['classe_altitude'].notna()) &
            (df['conso_5_usages_par_m2_ep'] <= 1000) &
            (df['periode_categorie'].notna())
        ]
        return df_valide
    
    def _create_plot(self):

        ordre_tranches, ordre_periodes, tableau_conso, tableau_effectifs = self.__split_tranches()
        tableau_conso_numeric, pire_periode, pire_tranche, min_conso, max_conso, pct_ecart = self.__cross_analysis(tableau_conso)

        z_data = tableau_conso_numeric.values

        text_data = []
        for i, _ in enumerate(tableau_conso.index):
            row_text = []
            for j, _ in enumerate(tableau_conso.columns):
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

        fig.update_layout(
            # Titre
            title={
                'text': (
                    '<b>Double peine : ancienneté du bâti × altitude</b><br>'
                    '<sub>Département Haute-Savoie (74)</sub>'
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
            height=700,
            
            # Marges
            margin=dict(l=120, r=150, t=120, b=160)
        )

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

        return fig