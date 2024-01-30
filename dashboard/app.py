import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Bibliometrics']

# Retrieve collection names from MongoDB and sort them alphabetically
collection_names = sorted(db.list_collection_names())

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Tableau de bord de la librairie en ligne"),
    
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': 'All Categories', 'value': 'all'}] + [{'label': collection_name, 'value': collection_name} for collection_name in collection_names],
            value=['all'],  # Allow selecting multiple collections
            multi=True  # Enable multi-select
        )
    ]),
    
    html.Div([
        dcc.Graph(id='book-count-graph')
    ])
])

# Define callback to update graph based on category selection
@app.callback(
    Output('book-count-graph', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_collections):
    if 'all' in selected_collections:
        selected_collections = collection_names
    if selected_collections:
        data = []
        for collection_name in selected_collections:
            collection = db[collection_name]
            book_count = collection.count_documents({})
            data.append({'collection': collection_name, 'book_count': book_count})
        
        # Sort the data by book count in descending order
        data = sorted(data, key=lambda x: x['book_count'], reverse=True)
        
        # Create a bar chart
        fig = go.Figure()
        for d in data:
            fig.add_trace(go.Bar(x=[d['collection']], y=[d['book_count']], name=d['collection']))
        
        fig.update_layout(barmode='group', xaxis_title='Collection', yaxis_title='Book Count',
                          title="Nombre de livres par collection")
        
        fig.update_yaxes(range=[0, 25])

        return fig
    else:
        return {}

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)