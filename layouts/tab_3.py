from dash import html, dcc, Input, Output
import numpy as np

import plotly.graph_objects as go

# Layout de la pestaña 3
def render_tab_3():
    return html.Div([
    html.H1("Página 3: Escenario con Radar Plot"),
    
    html.Div([
        html.Label("Porcentaje LCA:"),
        dcc.Input(id='input-lca', type='number', value=25, min=0, max=100, step=1),
        html.Label("Porcentaje LCC:"),
        dcc.Input(id='input-lcc', type='number', value=25, min=0, max=100, step=1),
        html.Label("Porcentaje Tech:"),
        dcc.Input(id='input-tech', type='number', value=25, min=0, max=100, step=1),
        html.Label("Porcentaje Social:"),
        dcc.Input(id='input-soc', type='number', value=25, min=0, max=100, step=1),
    ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '10px'}),
    
    html.Button("Actualizar Gráfico", id='update-button', n_clicks=0),
    
    dcc.Graph(id='radar-plot', style={'margin-top': '20px'}),
])



# Callbacks específicos de la pestaña 3
def register_callbacks_tab_3(app):
    @app.callback(
        Output('radar-plot', 'figure'),
        Input('update-button', 'n_clicks'),
        Input('input-lca', 'value'),
        Input('input-lcc', 'value'),
        Input('input-tech', 'value'),
        Input('input-soc', 'value'),
        Input('table-data-store', 'data')
    )
    def update_radar_plot(n_clicks, porc1, porc2, porc3, porc4,data):
        if porc1 + porc2 + porc3 + porc4 != 100:
            return go.Figure().update_layout(
                title="La suma de los porcentajes debe ser igual a 100",
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            )
        
        # Datos de entrada
        Val_LCA = np.array(data['LCA'],dtype=np.float64)
        Val_LCC = np.array(data['LCC'],dtype=np.float64)
        Val_Tech = np.array(data['Tech'],dtype=np.float64)
        Val_Social = np.array(data['SLCA'],dtype=np.float64)

        # Máximos y mínimos
        minVal_LCA = np.amin(Val_LCA)
        minVal_LCC = np.amin(Val_LCC)
        maxVal_Tech = np.amax(Val_Tech)
        maxVal_Soc = np.amax(Val_Social)

        # Adimensionalizados
        Vaadim_LCA = minVal_LCA / Val_LCA
        Vaadim_LCC = minVal_LCC / Val_LCC
        Vaadim_Tech = Val_Tech / maxVal_Tech
        Vaadim_Soc = Val_Social / maxVal_Soc

        # Calcular valores
        valores = []
        for j in range(len(Vaadim_LCA)):
            ValA_t = porc1 / 100 * Vaadim_LCA[j]
            ValB_t = porc2 / 100 * Vaadim_LCC[j]
            ValC_t = porc3 / 100 * Vaadim_Tech[j]
            ValD_t = porc4 / 100 * Vaadim_Soc[j]
            suma = ValA_t + ValB_t + ValC_t + ValD_t
            valores.append(suma)

        categories = ['A', 'B', 'C', 'D', 'E', 'F']

        # Generar el radar plot
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=valores,
            theta=categories,
            fill='toself',
            name='Escenario'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False
        )
        return fig