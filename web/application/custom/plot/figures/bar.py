from .plot import Plot

import plotly.graph_objects as go



class Bar(Plot):

    def __split_tranches(self) -> list[dict]:

        ordre_tranches = [label for label in self.LABELS_ALTITUDE if label in self.df['classe_altitude'].unique()]

        stats_tranches = []
        for tranche in ordre_tranches:
            donnees_tranche = self.df[self.df['classe_altitude'] == tranche]['conso_5_usages_par_m2_ep']
            
            conso_moyenne = donnees_tranche.mean()
            effectif = len(donnees_tranche)
            
            stats_tranches.append({
                'tranche': tranche,
                'conso_moyenne': conso_moyenne,
                'effectif': effectif
            })

        conso_reference = stats_tranches[0]['conso_moyenne']
        for stats in stats_tranches:
            # Différence de consommation par rapport à la vallée (kWh/m²/an)
            ecart_conso = stats['conso_moyenne'] - conso_reference
            
            # Surcoût annuel pour un logement de référence (€/an)
            surcout_annuel = ecart_conso * self.SURFACE_REFERENCE * self.PRIX_ELECTRICITE
            
            stats['ecart_conso'] = ecart_conso
            stats['surcout_annuel'] = surcout_annuel

        return stats_tranches

    def _validate_data(self, df):
        df_valide = df[
            (df['altitude_moyenne'].notna()) & 
            (df['classe_altitude'].notna()) &
            (df['conso_5_usages_par_m2_ep'] <= 1000)
        ]
        return df_valide
    
    def _create_plot(self):

        stats_tranches = self.__split_tranches()
        
        # Préparation des données pour le graphique
        tranches_noms = [s['tranche'] for s in stats_tranches]
        surcouts = [s['surcout_annuel'] for s in stats_tranches]
        consos = [s['conso_moyenne'] for s in stats_tranches]
        effectifs = [s['effectif'] for s in stats_tranches]

        couleurs_barres = [self.COULEURS_ALTITUDE.get(t, '#95a5a6') for t in tranches_noms]

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

        surcout_max = max(surcouts)
        tranche_max = tranches_noms[surcouts.index(surcout_max)]

        fig.update_layout(
            # Titre
            title={
                'text': (
                    '<b>Surcoût énergétique annuel par tranche d\'altitude</b><br>'
                    f'<sub>Département Haute-Savoie (74) - '
                    f'Logement de référence : {self.SURFACE_REFERENCE}m², prix électricité {self.PRIX_ELECTRICITE}€/kWh</sub>'
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
            height=self.HEIGHT,
            
            # Marges
            margin=dict(l=80, r=80, t=180, b=160)
        )

        fig.add_annotation(
            text=(
                f"<b>💰 Insight clé :</b> Vivre en {tranche_max.lower()} coûte <b>+{surcout_max:.0f}€/an</b><br>"
                f"de plus en énergie par rapport à la vallée pour un logement de {self.SURFACE_REFERENCE}m².<br>"
                f"Cela représente l'équivalent de <b>{surcout_max/12:.0f}€ par mois</b> de facture énergétique supplémentaire,<br>"
                "soit un budget non négligeable pour les ménages vivant en altitude."
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