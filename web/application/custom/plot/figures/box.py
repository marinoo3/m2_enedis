from .plot import Plot

import plotly.graph_objects as go



class Box(Plot):

    def __split_tranches(self) -> tuple[list, list[dict], float, float]:

        ordre_tranches = [label for label in self.LABELS_ALTITUDE if label in self.df['classe_altitude'].unique()]

        stats_par_tranche = []
        for tranche in ordre_tranches:
            donnees_tranche = self.df[self.df['classe_altitude'] == tranche]['conso_5_usages_par_m2_ep']
            
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

        ecart_vallee_montagne = stats_par_tranche[-1]['mediane'] - stats_par_tranche[0]['mediane']
        pct_augmentation = (ecart_vallee_montagne / stats_par_tranche[0]['mediane']) * 100

        return ordre_tranches, stats_par_tranche, ecart_vallee_montagne, pct_augmentation

    def _validate_data(self, df):
        df_valide = df[
            (df['altitude_moyenne'].notna()) & 
            (df['classe_altitude'].notna()) &
            (df['conso_5_usages_par_m2_ep'] <= 1000)  # Limite supérieure réaliste
        ]
        return df_valide
    
    def _create_plot(self):
        
        ordre_tranches, stats_par_tranche, ecart_vallee_montagne, pct_augmentation = self.__split_tranches()

        fig = go.Figure()

        # Ajout d'un boxplot pour chaque tranche d'altitude
        for tranche in ordre_tranches:
            donnees_tranche = self.df[self.df['classe_altitude'] == tranche]['conso_5_usages_par_m2_ep']
            
            fig.add_trace(go.Box(
                y=donnees_tranche,
                name=tranche,
                marker_color=self.COULEURS_ALTITUDE.get(tranche, '#95a5a6'),
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

        fig.update_layout(
            # Titre
            title={
                'text': (
                    '<b>Distribution de la consommation énergétique<br>par tranche d\'altitude</b><br>'
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

            # Dimension
            height=self.HEIGHT,
            
            # Style
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,  # Pas de légende nécessaire (noms sur l'axe X)
            
            # Marges pour l'annotation
            margin=dict(l=80, r=80, t=120, b=180)
        )

        fig.add_annotation(
            text=(
                f"<b>📊 Insight clé :</b> La consommation médiane augmente de <b>{ecart_vallee_montagne:.0f} kWh/m²/an</b> <br>"
                f"entre la vallée ({stats_par_tranche[0]['mediane']:.0f} kWh/m²/an) "
                f"et la haute montagne ({stats_par_tranche[-1]['mediane']:.0f} kWh/m²/an), soit une hausse de <b>{pct_augmentation:.1f}%</b>.<br>"
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
        
        return fig