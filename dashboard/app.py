import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from dash.dash_table import FormatTemplate
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Initialize Dash app
app = dash.Dash(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['Bibliometrics']
book_collection = db['Books']


# 'Récupérer tous les livres avec du stock supérieur à 10'
def only_book_available(categories_filtered):
    if 'all' in categories_filtered:
        available_books = list(book_collection.find({"available_stock": {"$gt": 10}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    else:
        available_books = list(book_collection.find({"available_stock": {"$gt": 10}, "category": {'$in': categories_filtered}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    return available_books

# print('Récupérer tous les livres sans stock')
# book_wo_stock = book_collection.find({"available_stock": None}, {'title': 1,'_id': 0})
# for books in book_wo_stock:
#     print(books)

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
    ]),
    html.Div([
        html.H2("list of books available : more than 10"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-table',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{'name': 'category', 'id': 'category'},
                         {'name': 'Title', 'id': 'title'}, 
                         {'name': 'Price', 'id': 'price'}, 
                         {'name': 'Rating', 'id': 'rating'}],
                data=[]
              )
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

# Define callback to update dropdown options dynamically for the table update
@app.callback(
    Output('category-dropdown-table', 'options'),
    [Input('category-dropdown-table', 'value')]
)
def update_dropdown_options_table(filtered_categories):
    categories = book_collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

# Define callback to update graph based on category selection
@app.callback(
    Output('table', 'data'),
    [Input('category-dropdown-table', 'value')]
)
def update_table(filtered_categories):
    data = only_book_available(filtered_categories)
    return data


# Run Dash app
if __name__ == '__main__':
    app.run_server(debug=True)