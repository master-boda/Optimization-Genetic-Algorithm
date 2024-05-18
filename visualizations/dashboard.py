import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Dados fictícios para visualização
iterations = list(range(10))
fitness_scores = [10, 15, 20, 18, 25, 30, 28, 35, 40, 45]

areas = ["D", "FC", "G", "QS", "QG", "CS", "KS", "RG", "DV", "SN"]
coordinates = {
    "D": (0, 0),
    "FC": (1, 2),
    "G": (3, 3),
    "QS": (4, 1),
    "QG": (6, 2),
    "CS": (7, 4),
    "KS": (9, 0),
    "RG": (5, 6),
    "DV": (2, 7),
    "SN": (8, 5)
}

# Função para gerar dados de rotas fictícias
def generate_routes(num_routes):
    import random
    routes = []
    for _ in range(num_routes):
        route = areas.copy()
        random.shuffle(route)
        route = ["D"] + route + ["D"]
        routes.append(route)
    return routes

# Dados de exemplo
routes = generate_routes(10)
best_route = routes[-1]

# Função para criar o gráfico de uma rota
def create_route_figure(route, title, color='skyblue'):
    x = [coordinates[area][0] for area in route]
    y = [coordinates[area][1] for area in route]
    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers+text',
        marker=dict(size=8, color='blue'),
        line=dict(color=color, width=2),
        text=route,
        textposition='top right'
    )
    layout = go.Layout(
        title=title,
        xaxis=dict(title='X Coordinate', range=[-1, 10]),
        yaxis=dict(title='Y Coordinate', range=[-1, 8]),
        showlegend=False
    )
    return go.Figure(data=[trace], layout=layout)

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Dashboard de Visualização de Otimização'),

    dcc.Graph(
        id='fitness-graph',
        figure={
            'data': [
                go.Scatter(
                    x=iterations,
                    y=fitness_scores,
                    mode='lines+markers',
                    name='Fitness Score'
                )
            ],
            'layout': {
                'title': 'Progresso da Otimização'
            }
        }
    ),
    html.Div([
        dcc.Slider(
            id='generation-slider',
            min=0,
            max=len(routes) - 1,
            value=0,
            marks={i: f'Gen {i+1}' for i in range(len(routes))},
            step=None
        )
    ], style={'width': '80%', 'padding': '0px 20px 20px 20px'}),
    dcc.Graph(id='route-graph'),
    dcc.Graph(id='best-route-graph')
])

@app.callback(
    [Output('route-graph', 'figure'), Output('best-route-graph', 'figure')],
    [Input('generation-slider', 'value')]
)
def update_route_graph(selected_generation):
    route_figure = create_route_figure(routes[selected_generation], f'Generation {selected_generation + 1}')
    best_route_figure = create_route_figure(best_route, 'Best Route', color='limegreen')
    return route_figure, best_route_figure

if __name__ == '__main__':
    app.run_server(debug=True)
