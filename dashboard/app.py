import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
collection = db['books']

# Retrieve data from MongoDB
data = list(collection.find({}, {'_id': 0}))

# Convert MongoDB data to DataFrame
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Tableau de bord de la librairie en ligne"),
    
    html.Div([
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in df['category'].unique()],
            value=df['category'].unique()[0]
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
def update_graph(selected_category):
    filtered_df = df[df['category'] == selected_category]
    book_count = filtered_df['category'].value_counts().reset_index()
    book_count.columns = ['category', 'count']
    fig = px.bar(book_count, x='category', y='count', title=f"Nombre de livres par catégorie ({selected_category})")
    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

print(df.head())
