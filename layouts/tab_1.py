from dash import html, dcc, dash_table, Input, Output, State
import numpy as np

# Layout de la pestaña 1
def render_tab_1():
    return html.Div([
        html.Label("Selecciona el número de escenarios:"),
        dcc.Dropdown(
            id='dropdown-rows',
            options=[{'label': i, 'value': i} for i in range(1, 11)],
            value=1,
            clearable=False
        ),
        
        dash_table.DataTable(
            id='dynamic-table',
            columns=[
                {'name': 'Etiqueta', 'id': 'Etiqueta', 'editable': False},
                {'name': 'LCA', 'id': 'LCA', 'editable': True},
                {'name': 'LCC', 'id': 'LCC', 'editable': True},
                {'name': 'Tech', 'id': 'Tech', 'editable': True},
                {'name': 'SLCA', 'id': 'SLCA', 'editable': True},
                {'name': 'Descripción', 'id': 'Descripcion', 'editable': True}
            ],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            style_header={'fontWeight': 'bold'},
        ),
        
        html.Button("Enviar", id="submit-button", n_clicks=0),
        html.Div(id="output-values"),
    ])

# Callbacks específicos de la pestaña 1
def register_callbacks_tab_1(app):
    @app.callback(
        Output('dynamic-table', 'data'),
        Input('dropdown-rows', 'value')
    )
    def update_table(num_rows):
        alphabet = [chr(65 + i) for i in range(26)]
        return [{'LCA': '', 'LCC': '', 'Tech': '', 'SLCA': '', 'Etiqueta': alphabet[i]} for i in range(num_rows)]

    @app.callback(
        Output('table-data-store', 'data'),  # Guardamos los datos en el dcc.Store
        Input('submit-button', 'n_clicks'),
        State('dynamic-table', 'data')
    )
    def save_data(n_clicks, table_data):
        if n_clicks > 0:
            # Convertimos los datos de la tabla en arreglos de NumPy
            lca = np.array([row['LCA'] for row in table_data])
            lcc = np.array([row['LCC'] for row in table_data])
            tech = np.array([row['Tech'] for row in table_data])
            slca = np.array([row['SLCA'] for row in table_data])
            return {'LCA': lca.tolist(), 'LCC': lcc.tolist(), 'Tech': tech.tolist(), 'SLCA': slca.tolist()}
        return {}  # Si no se presionó el botón, retornamos vacío