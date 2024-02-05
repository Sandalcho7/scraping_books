import dash
from dash import dcc, html, dash_table
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


def only_book_available(categories_filtered):
    if 'all' in categories_filtered:
        available_books = list(collection.find({"available_stock": {"$gt": 10}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    else:
        available_books = list(collection.find({"available_stock": {"$gt": 10}, "category": {'$in': categories_filtered}}, {'category':1,'title': 1, 'price': 1, 'rating': 1, '_id': 0}))
    return available_books


# Define layout
app.layout = html.Div([

    html.H1("BIBLIOMETRIC'S DASHBOARD"),

    html.Hr(),
    
    html.Div([
        html.H2("Number of books in each category"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-count',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dcc.Graph(id='book-count-graph')
        ])
    ], className='request-div'),

    html.Div([
        html.H2("Average rating for each category"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-rating',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dcc.Graph(id='book-rating-graph')
        ])
    ], className='request-div'),

    html.Div([
        html.H2("List of books with more than 10 available"),
        html.Div([
            dcc.Dropdown(
                id='category-dropdown-table',
                className='dropdown',
                options=[{'label': 'All categories', 'value': 'all'}],
                value='all',
                multi=True
            )
        ]),
        html.Div([
            dash_table.DataTable(
                id='table',
                columns=[
                    {'name': 'Title', 'id': 'title'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Price', 'id': 'price'}, 
                    {'name': 'Rating', 'id': 'rating'}
                ],
                data=[],
                page_size=20,
                style_cell={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'text-align': 'center',
                },
                style_header={'font-weight': 'bold'},
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'title'},  # Targeting the 'Title' column
                        'minWidth': '300px',
                        'maxWidth': '600px',
                        'text-align': 'left',
                        'padding-left': '10px',
                    },
                ],
            ),
        ])
    ], className='request-div'),
    
])


# Dropdown for books count
@app.callback(
    Output('category-dropdown-count', 'options'),
    [Input('category-dropdown-count', 'value')]
)
def update_dropdown_options_count(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

# Update graph based on category selection for book count
@app.callback(
    Output('book-count-graph', 'figure'),
    [Input('category-dropdown-count', 'value')]
)
def update_count_graph(selected_categories):
    if 'all' in selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    book_count = df['category'].value_counts().reset_index()
    book_count.columns = ['category', 'count']
    
    # Define color scheme with a color per category
    colors = px.colors.qualitative.Set3[:len(book_count)]
    
    # Use a ColorBrewer color scale
    fig = px.bar(book_count, x='category', y='count', color='category', color_discrete_sequence=colors)

    # Change background color
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


# Dropdown for books rating
@app.callback(
    Output('category-dropdown-rating', 'options'),
    [Input('category-dropdown-rating', 'value')]
)
def update_dropdown_options_rating(selected_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

# Update graph based on category selection for book count
@app.callback(
    Output('book-rating-graph', 'figure'),
    [Input('category-dropdown-rating', 'value')]
)
def update_rating_graph(selected_categories):
    if 'all' in selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({'category': {'$in': selected_categories}})
    
    df = pd.DataFrame(list(filtered_data))
    
    # Ensure rating column is numeric
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    avg_rating = df.groupby('category')['rating'].mean().reset_index()
    
    # Sort by descending ratings
    avg_rating = avg_rating.sort_values(by='rating', ascending=False)
    
    # Use a ColorBrewer color scale
    fig = px.bar(avg_rating, x='category', y='rating', color='category', color_discrete_sequence=px.colors.qualitative.Set3)

    # Change background color
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return fig


# Dropdown for table
@app.callback(
    Output('category-dropdown-table', 'options'),
    [Input('category-dropdown-table', 'value')]
)
def update_dropdown_options_table(filtered_categories):
    categories = collection.distinct('category')
    options = [{'label': 'All categories', 'value': 'all'}]
    options.extend({'label': category, 'value': category} for category in categories)
    return options

# Update table based on category selection
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