import dash
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Define areas and coordinates
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

# Create a Heatmap Figure Function
def create_heatmap_figure(matrix, title):
    heatmap = go.Heatmap(
        z=matrix,
        x=areas,
        y=areas,
        colorscale='Viridis'
    )
    layout = go.Layout(
        title=title,
        xaxis=dict(title='Areas'),
        yaxis=dict(title='Areas'),
        showlegend=False,
        autosize=False,
        width=600,
        height=600,
        margin=dict(l=100, r=100, t=100, b=100)
    )
    return go.Figure(data=[heatmap], layout=layout)

# Function to create the route figure
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

# Function to create the fitness evolution figure
def create_fitness_evolution_figure(iterations, fitness_scores):
    trace = go.Scatter(
        x=iterations,
        y=fitness_scores,
        mode='lines+markers',
        name='Fitness Score'
    )
    layout = go.Layout(
        title='Fitness Score Evolution',
        xaxis=dict(title='Generation'),
        yaxis=dict(title='Fitness Score'),
        showlegend=True
    )
    return go.Figure(data=[trace], layout=layout)

# Function to run the Dash dashboard
def run_dashboard(routes, fitnesses, best_route, matrix):
    # Initialize Dash app
    app = dash.Dash(__name__)

    # Generate slider marks without text
    slider_marks = {i: '' for i in range(len(routes))}

    # App layout
    app.layout = html.Div(children=[
        html.H1(
            children='Hallow Knight Route Optimization',
            style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}
        ),

        html.H4(
            children='Francisco Batista; Vicente Miranda; Lourenço Mourão Martins; Cícero Dias dos Santos',
            style={'textAlign': 'center', 'paddingBottom': '20px', 'fontFamily': 'Arial, sans-serif'}
        ),

        html.Div([
            dcc.Slider(
                id='generation-slider',
                min=0,
                max=len(routes) - 1,
                value=0,
                marks=slider_marks,
                step=1,
                updatemode='drag'
            ),
            html.Div(id='slider-output', style={'paddingTop': '10px'})
        ], style={'width': '80%', 'padding': '0px 20px 20px 20px', 'margin': 'auto'}),
        html.Div([
            dcc.Graph(id='route-graph'),
            dcc.Graph(id='best-route-graph')
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'}),
        html.Div([
            dcc.Graph(
                id='heatmap-graph',
                figure=create_heatmap_figure(matrix, 'Geo Earnings/Loss Matrix')
            ),
            dcc.Graph(
                id='fitness-evolution-graph',
                figure=create_fitness_evolution_figure(list(range(len(fitnesses))), fitnesses)
            )
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center'})
    ], style={'textAlign': 'center', 'maxWidth': '1200px', 'margin': 'auto', 'fontFamily': 'Arial, sans-serif'})

    # Callback to update the route graph based on the selected generation
    @app.callback(
        [Output('route-graph', 'figure'), Output('best-route-graph', 'figure'), Output('slider-output', 'children')],
        [Input('generation-slider', 'value')]
    )
    def update_route_graph(selected_generation):
        route_figure = create_route_figure(routes[selected_generation], f'Generation {selected_generation + 1}')
        best_route_figure = create_route_figure(best_route, 'Best Route', color='limegreen')
        best_fitness_score = max(fitnesses)
        return route_figure, best_route_figure, f'Current Generation: {selected_generation + 1}, Best Fitness Score: {best_fitness_score}'

    # Run the app
    app.run_server(debug=False)

# Example usage:
# if __name__ == '__main__':
#     run_dashboard(routes, fitnesses, best_route, matrix)
