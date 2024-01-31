import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Initialize Dash app
app = dash.Dash(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Bibliometrics']
collection = db['Books']

# Define layout
app.layout = html.Div([

    html.H1("Bibliometric's dashboard"),

    html.Hr(),
    
    html.Div([
        html.H2("Number of books in each category"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dcc.Graph(id='book-count-graph')
        ])
    ])
    
])

# Define callback to update dropdown options dynamically
@app.callback(
    Output('category-dropdown', 'options'),
    [Input('category-dropdown', 'value')]
)
def update_dropdown_options(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

# Define callback to update graph based on category selection
@app.callback(
    Output('book-count-graph', 'figure'),
    [Input('category-dropdown', 'value')]
)
def update_graph(selected_categories):
    if 'all' in selected_categories:  # If "All categories" is selected
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    book_count = df['category'].value_counts().reset_index()
    book_count.columns = ['category', 'count']
    
    # Use a ColorBrewer color scale
    fig = px.bar(book_count, x='category', y='count', color='category', color_discrete_sequence=px.colors.qualitative.Set3)

    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)