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
book_collection = db['Books']


print('Récupérer tous les livres avec du stock supérieur à 10')
only_book_available = book_collection.find({"available_stock": {"$gt": 10}}, {'title': 1, 'price': 1, '_id': 0})
for books in only_book_available:
    print(books)

print('Récupérer tous les livres sans stock')
book_wo_stock = book_collection.find({"available_stock": None}, {'title': 1,'_id': 0})
for books in book_wo_stock:
    print(books)

# print("1. Récupérer tous les livres")
# all_books = book_collection.find({},{'description':0})
# for zz in all_books:
#     print(zz)

# for livre in livres_apres_2000:
#     print(livre)
# dvds_apres_2005 = book_collection.find({"type": "dvd", "publication_date": {"$gt": datetime(2005, 1, 1)}})
# livres_fitzgerald = book_collection.find({"type": "book", "authors.name": "Chad Diaz"}, {'title': 1, '_id': 0})
# 

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
    categories = book_collection.distinct('category')
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
        filtered_data = book_collection.find({})
    else:
        filtered_data = book_collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    book_count = df['category'].value_counts().reset_index()
    book_count.columns = ['category', 'count']
    
    # Use a ColorBrewer color scale
    fig = px.bar(book_count, x='category', y='count', color='category', color_discrete_sequence=px.colors.qualitative.Set3)

    return fig

# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)