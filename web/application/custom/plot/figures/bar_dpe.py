from .plot import Plot

import plotly.graph_objects as go



class BarDPE(Plot):

    def __split_tranches(self) -> tuple[list[dict], float, float, float]:

        ordre_tranches = [label for label in self.LABELS_ALTITUDE if label in self.df['classe_altitude'].unique()]

        stats_par_tranche = []

        for tranche in ordre_tranches:
            donnees_tranche = self.df[self.df['classe_altitude'] == tranche]
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

        pct_vallee = stats_par_tranche[0]['pct_passoires']
        pct_montagne_max = max([s['pct_passoires'] for s in stats_par_tranche])
        ratio = pct_montagne_max / pct_vallee if pct_vallee > 0 else 0

        return stats_par_tranche, pct_vallee, pct_montagne_max, ratio

    def _validate_data(self, df):
        df_valide = df[
            (df['altitude_moyenne'].notna()) & 
            (df['classe_altitude'].notna()) &
            (df['etiquette_dpe'].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G']))
        ]
        return df_valide
    
    def _create_plot(self):

        stats_par_tranche, pct_vallee, pct_montagne_max, ratio = self.__split_tranches()
        
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

        fig.update_layout(
            # Empilement à 100%
            barmode='stack',
            
            # Titre
            title={
                'text': (
                    '<b>Concentration des passoires thermiques selon l\'altitude</b><br>'
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
            height=self.HEIGHT,
            
            # Marges
            margin=dict(l=80, r=80, t=180, b=160)
        )

        fig.add_annotation(
            text=(
                "<b>🔥 Insight clé :</b> Les passoires thermiques (F/G) représentent <br>"
                f"<b>{pct_vallee:.1f}%</b> des logements en vallée contre <b>{pct_montagne_max:.1f}%</b> en montagne,<br>"
                f"soit <b>×{ratio:.1f}</b> plus de risque d'avoir un logement énergivore en altitude.<br>"
                "Cette concentration révèle un enjeu majeur de rénovation énergétique en zone de montagne."
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