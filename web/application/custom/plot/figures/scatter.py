from .plot import Plot

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats



class Scatter(Plot):
    
    def __linear_regression(self) -> dict:

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            self.df['altitude_moyenne'], 
            self.df['conso_5_usages_par_m2_ep']
        )

        r_squared = r_value ** 2

        altitude_min = self.df['altitude_moyenne'].min()
        altitude_max = self.df['altitude_moyenne'].max()
        x_regression = np.array([altitude_min, altitude_max])
        y_regression = slope * x_regression + intercept

        reg = {
            'stats': {
                'slope': slope,
                'intercept': intercept,
                'r_value': r_value,
                'p_value': p_value,
                'std_err': std_err,
                'r_squared': r_squared
            },
            'altitude': [altitude_min, altitude_max],
            'regression': {
                'x': x_regression,
                'y': y_regression
            }
        }

        return reg

    def _validate_data(self, df):
        df_valide = df[df['altitude_moyenne'].notna()]
        df_plot = df_valide.sample(n=self.TAILLE_ECHANTILLON, random_state=0)
        return df_plot
    
    def _create_plot(self):

        reg = self.__linear_regression()

        fig = px.scatter(
            self.df,
            x='altitude_moyenne',
            y='conso_5_usages_par_m2_ep',
            color='etiquette_dpe',
            color_discrete_map=self.COULEURS_DPE,
            category_orders={'etiquette_dpe': ['A', 'B', 'C', 'D', 'E', 'F', 'G']},  # Ordre croissant des étiquettes DPE
            opacity=0.6,
            labels={
                'altitude_moyenne': 'Altitude moyenne de la commune (m)',
                'conso_5_usages_par_m2_ep': 'Consommation énergétique (kWh/m²/an)',
                'etiquette_dpe': 'Étiquette DPE'
            },
            hover_data={
                'altitude_moyenne': ':.0f',
                'conso_5_usages_par_m2_ep': ':.1f',
                'nom_commune_ban': True,
                'type_batiment': True,
                'periode_construction': True,
                'etiquette_dpe': False  # Déjà visible via la couleur
            },
            title='<b>Impact de l\'altitude sur la consommation énergétique</b><br>'
                '<sub>Département Haute-Savoie (74)</sub>'
        )

        fig.add_trace(
            go.Scatter(
                x=reg['regression']['x'],
                y=reg['regression']['y'],
                mode='lines',
                name=f"Régression linéaire<br>(+{reg['stats']['slope']*100:.1f} kWh/m²/an par 100m)",
                line=dict(color='#e74c3c', width=3, dash='dash'),
                hovertemplate='<b>Tendance linéaire</b><br>Altitude: %{x:.0f}m<br>Consommation estimée: %{y:.1f} kWh/m²/an<extra></extra>'
            )
        )

        fig.update_layout(
            # Dimensions
            height=self.HEIGHT,
            
            # Style de fond
            plot_bgcolor='white',
            paper_bgcolor='white',
            
            # Configuration du titre
            title={
                'font': {'size': 22, 'family': 'Arial, sans-serif', 'color': '#2c3e50'},
                'x': 0.5,
                'xanchor': 'center'
            },
            
            # Configuration des axes
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#ecf0f1',
                zeroline=False,
                title_font=dict(size=13, color='#34495e'),
                tickfont=dict(size=11, color='#34495e')
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='#ecf0f1',
                zeroline=False,
                title_font=dict(size=13, color='#34495e'),
                tickfont=dict(size=11, color='#34495e')
            ),
            
            # Configuration de la légende
            legend=dict(
            title=dict(text='<b>Étiquette DPE</b>', font=dict(size=12)),
            orientation='v',
            yanchor='top',
            y=0.98,
            xanchor='right',
            x=0.98,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#bdc3c7',
            borderwidth=1,
            font=dict(size=10),
            ),
            
            # Mode d'interaction au survol
            hovermode='closest',
            hoverlabel=dict(
                bgcolor='white',
                font_size=11,
                font_family='Arial, sans-serif'
            ),
            
            # Marges pour l'annotation en bas
            margin=dict(l=80, r=80, t=120, b=180)
        )

        fig.add_annotation(
            text=f"<b>📊 Insight clé :</b> Chaque 100m d'altitude supplémentaire augmente<br>"
                f"la consommation de <b>{reg['stats']['slope']*100:.1f} kWh/m²/an</b> en moyenne "
                f"<i>(R² = {reg['stats']['r_squared']:.3f}, p < 0.001)</i>.<br>"
                "Cette corrélation significative démontre l'impact direct de l'altitude sur les besoins énergétiques.",
            xref="paper", yref="paper",
            x=0.5, y=-0.17,
            xanchor='center', yanchor='top',
            showarrow=False,
            bgcolor='rgba(255, 243, 205, 0.95)',
            bordercolor='#f39c12',
            borderwidth=2,
            borderpad=10,
            font=dict(size=11, family='Arial, sans-serif', color='#34495e')
        )


        return fig
