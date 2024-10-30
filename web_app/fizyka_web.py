import dash
from dash import dcc, html, Input, Output, State
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

np.set_printoptions(suppress=True)

class Czastka:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.points = np.empty((0, 2), dtype=float)
        
    def append_points(self, x, y):
        self.points = np.append(self.points, [[x, y]], axis=0)
        
    def return_max_abs_y_value(self):
        return max(abs(self.points[:, 1])) 
    
    def return_max_abs_x_value(self):
        return max(abs(self.points[:, 0]))

def calculate_points(czastki, points_limit, step):
    for czastka in czastki:
        calc = 0
        while calc <= points_limit:
            x = eval(czastka.A, {'t': calc})
            y = eval(czastka.B, {'t': calc})
            czastka.append_points(x, y)
            calc += step

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Form([
                        dbc.Label('Ilość równań:'),
                        dbc.Input(id='rownania', type='number', value=1),
                    ]),
                    dbc.Form([
                        dbc.Label('Ostatna wartosc "t" do obliczenia:'),
                        dbc.Input(id='points-limit', type='number', value=10),
                    ]),
                    dbc.Form([
                        dbc.Label('Co ile ma obliczac:'),
                        dbc.Input(id='step', type='number', value=0.1,),
                    ],  style={"margin-bottom": "10px"}),
                    html.Hr(style={'width': '100%', 'borderTop': '3px solid #000', 'margin-top': '10px '}),
                    dbc.Form([html.Div(id='czastki-inputs')]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Pokaż wykres', id='submit-button', color='primary', n_clicks=0, className='mt-3'),
                        ], width={"size": 6, "offset": 3})
                    ])
                ])
            ], className='mb-4')
        ], width=4),
        dbc.Col([
            dcc.Graph(id='graph', style={'border': '1px solid #ddd', 'border-radius': '5px'}),
        ], width=8)
    ])
], fluid=True, className='p-4')

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .dbc-card:hover {
                transform: scale(1.05);
            }
            @media (max-width: 768px) {
                .dbc-card {
                    margin-bottom: 20px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

@app.callback(
    Output('czastki-inputs', 'children'),
    Input('rownania', 'value')
)
def update_czastki_inputs(rownania):
    return [
        dbc.Row([
            dbc.Label(f'Podaj wartość A dla czastki {i+1}:'),
            dbc.Input(id={'type': 'czastka-input', 'index': f'A-{i}'}, type='text', value='t'),
            dbc.Label(f'Podaj wartość B dla czastki {i+1}:'),
            dbc.Input(id={'type': 'czastka-input', 'index': f'B-{i}'}, type='text', value='t'),
            html.Hr(style={'width': '100%', 'borderTop': '3px solid #000', 'margin-top': '10px '})
        ], style={'margin_bottom':'10px','padding-left':'10px','padding-right':'10px'}) for i in range(rownania)
    ]

@app.callback(
    Output('graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('rownania', 'value'),
    State('points-limit', 'value'),
    State('step', 'value'),
    State({'type': 'czastka-input', 'index': dash.ALL}, 'value')
)
def update_graph(n_clicks, rownania, points_limit, step, czastki_values):
    if n_clicks == 0:
        return go.Figure()

    czastki = [Czastka(czastki_values[i*2], czastki_values[i*2+1]) for i in range(rownania)]
    calculate_points(czastki, points_limit, step)

    max_x = max(czastka.return_max_abs_x_value() for czastka in czastki)
    max_y = max(czastka.return_max_abs_y_value() for czastka in czastki)

    fig = go.Figure()
    for i, czastka in enumerate(czastki):
        fig.add_trace(go.Scatter(x=czastka.points[:, 0], y=czastka.points[:, 1], mode='markers', name=f'Czastka {i+1}'))

    fig.update_layout(xaxis=dict(range=[0, max_x]), yaxis=dict(range=[-max_y, max_y]), xaxis_title='x[m]', yaxis_title='y[m]')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    # Create a new file named vercel.json in the root directory of your project with the following content:
    {
        "builds": [
            {
                "src": "fizyka_web.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "fizyka_web.py"
            }
        ]
    }

    # Ensure you have a requirements.txt file with all the dependencies listed:
    dash
    dash-bootstrap-components
    numpy
    plotly

    # Push your project to a GitHub repository.

    # Go to Vercel's website and sign up or log in.

    # Create a new project and import your GitHub repository.

    # Vercel will automatically detect the vercel.json file and deploy your Dash app.