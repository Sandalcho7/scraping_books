import pandas as pd
import dash

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from pymongo import MongoClient

from functions.database import (
    get_books_available,
    get_best_rated_books,
    search_books_by_title,
    get_random_book,
)
from functions.graph import (
    create_book_count_graph,
    create_rating_graph,
    create_rating_pie_chart,
)


app = dash.Dash(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["Bibliometrics"]
collection = db["Books"]

# Layout
app.layout = html.Div(
    [
        html.Div([html.H1("BIBLIOMETRIC'S DASHBOARD")], className="header"),
        html.Div(
            [
                html.H2("📚 Number of books in each category"),
                dcc.Dropdown(
                    id="category-dropdown-count",
                    className="dropdown",
                    options=[{"label": "All categories", "value": "all"}],
                    value="all",
                    multi=True,
                ),
                dcc.Graph(id="book-count-graph"),
            ],
            className="request-div",
        ),
        html.Div(
            [
                html.H2("⭐️ Average rating for each category"),
                dcc.Dropdown(
                    id="category-dropdown-rating",
                    className="dropdown",
                    options=[{"label": "All categories", "value": "all"}],
                    value="all",
                    multi=True,
                ),
                dcc.Graph(id="book-rating-graph"),
            ],
            className="request-div",
        ),
        html.Div(
            [
                html.H2("💹 List of books with more than 10 available"),
                dcc.Dropdown(
                    id="category-dropdown-table",
                    className="dropdown",
                    options=[{"label": "All categories", "value": "all"}],
                    value="all",
                    multi=True,
                ),
                dash_table.DataTable(
                    id="table",
                    columns=[
                        {"name": "Title", "id": "title"},
                        {"name": "Category", "id": "category"},
                        {"name": "Price", "id": "price"},
                        {"name": "Rating", "id": "rating"},
                    ],
                    data=[],
                    page_size=20,
                    style_cell={
                        "whiteSpace": "nowrap",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "text-align": "center",
                    },
                    style_header={"font-weight": "bold"},
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "title"},
                            "minWidth": "300px",
                            "maxWidth": "600px",
                            "text-align": "left",
                            "padding-left": "10px",
                        }
                    ],
                ),
            ],
            className="request-div",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("🎲 Random Book Generator"),
                        html.Button("Generate Random Book", id="random-book-button"),
                    ],
                    className="generate-title",
                ),
                html.Div(id="random-book-output", className="random-book-generator"),
            ],
            className="request-div",
        ),
        html.Div(
            [
                html.H2("🥇 List of books with a 5 stars rating"),
                dcc.Dropdown(
                    id="category-dropdown-table-rating",
                    className="dropdown",
                    options=[{"label": "All categories", "value": "all"}],
                    value="all",
                    multi=True,
                ),
                dash_table.DataTable(
                    id="table-rating",
                    columns=[
                        {"name": "Title", "id": "title"},
                        {"name": "Category", "id": "category"},
                        {"name": "Rating", "id": "rating"},
                    ],
                    data=[],
                    page_size=20,
                    style_cell={
                        "whiteSpace": "nowrap",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "text-align": "center",
                    },
                    style_header={"font-weight": "bold"},
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "title"},
                            "minWidth": "300px",
                            "maxWidth": "600px",
                            "text-align": "left",
                            "padding-left": "10px",
                        }
                    ],
                ),
            ],
            className="request-div",
        ),
        html.Div(
            [
                html.H2("🏆 10 best priced books with 5 stars rating"),
                dash_table.DataTable(
                    id="table-rating-price",
                    columns=[
                        {
                            "name": "Cover",
                            "id": "cover_book",
                            "type": "text",
                            "presentation": "markdown",
                        },
                        {"name": "Title", "id": "title"},
                        {"name": "Category", "id": "category"},
                        {"name": "Price", "id": "price"},
                        {"name": "Rating", "id": "rating"},
                    ],
                    data=[],
                    page_size=20,
                    style_cell={
                        "whiteSpace": "nowrap",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "text-align": "center",
                    },
                    style_header={"font-weight": "bold"},
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "title"},
                            "minWidth": "300px",
                            "maxWidth": "600px",
                            "text-align": "left",
                            "padding-left": "10px",
                        }
                    ],
                ),
            ],
            className="request-div",
        ),
        html.Div(
            [html.H2("🥧 Books count per rating"), dcc.Graph(id="rating-pie-chart")],
            className="request-div",
        ),
        html.Div(
            [
                html.H2("🔍 Search in title"),
                dcc.Input(id="search-text", type="text", placeholder="Enter text..."),
                dash_table.DataTable(
                    id="table-description-found-text",
                    columns=[
                        {"name": "Title", "id": "title"},
                        {"name": "Category", "id": "category"},
                        {"name": "Price", "id": "price"},
                        {"name": "Rating", "id": "rating"},
                    ],
                    data=[],
                    page_size=20,
                    style_cell={
                        "whiteSpace": "nowrap",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "text-align": "center",
                    },
                    style_header={"font-weight": "bold"},
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "title"},
                            "minWidth": "300px",
                            "maxWidth": "600px",
                            "text-align": "left",
                            "padding-left": "10px",
                        }
                    ],
                ),
            ],
            className="request-div",
        ),
        dcc.Interval(id="interval-component", interval=60000, n_intervals=0),
    ]
)


# Callbacks
@app.callback(
    Output("category-dropdown-count", "options"),
    [Input("category-dropdown-count", "value")],
)
def update_dropdown_options_count(selected_categories):
    categories = collection.distinct("category")
    options = [{"label": "All categories", "value": "all"}]
    options.extend({"label": category, "value": category} for category in categories)
    return options


@app.callback(
    Output("book-count-graph", "figure"), [Input("category-dropdown-count", "value")]
)
def update_count_graph(selected_categories):
    if "all" in selected_categories or not selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({"category": {"$in": selected_categories}})
    df = pd.DataFrame(list(filtered_data))
    return create_book_count_graph(df)


@app.callback(
    Output("category-dropdown-rating", "options"),
    [Input("category-dropdown-rating", "value")],
)
def update_dropdown_options_rating(selected_categories):
    categories = collection.distinct("category")
    options = [{"label": "All categories", "value": "all"}]
    options.extend({"label": category, "value": category} for category in categories)
    return options


@app.callback(
    Output("book-rating-graph", "figure"), [Input("category-dropdown-rating", "value")]
)
def update_rating_graph(selected_categories):
    if "all" in selected_categories or not selected_categories:
        filtered_data = collection.find({})
    else:
        filtered_data = collection.find({"category": {"$in": selected_categories}})
    df = pd.DataFrame(list(filtered_data))
    return create_rating_graph(df)


@app.callback(
    Output("category-dropdown-table", "options"),
    [Input("category-dropdown-table", "value")],
)
def update_dropdown_options_table(filtered_categories):
    categories = collection.distinct("category")
    options = [{"label": "All categories", "value": "all"}]
    options.extend({"label": category, "value": category} for category in categories)
    return options


@app.callback(Output("table", "data"), [Input("category-dropdown-table", "value")])
def update_table(filtered_categories):
    return get_books_available(collection, filtered_categories)


@app.callback(
    Output("category-dropdown-table-rating", "options"),
    [Input("category-dropdown-table-rating", "value")],
)
def update_dropdown_options_table_rating(selected_categories):
    categories = collection.distinct("category")
    options = [{"label": "All categories", "value": "all"}]
    options.extend({"label": category, "value": category} for category in categories)
    return options


@app.callback(
    Output("table-rating", "data"), [Input("category-dropdown-table-rating", "value")]
)
def update_table_rating(filtered_categories):
    return get_best_rated_books(collection, filtered_categories)


@app.callback(
    Output("rating-pie-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_pie_chart(n_intervals):
    books = list(collection.find({}, {"title": 1, "rating": 1}))
    return create_rating_pie_chart(books)


@app.callback(
    Output("table-rating-price", "data"), [Input("interval-component", "n_intervals")]
)
def update_table_best_price(n_intervals):
    best_price_and_rating = list(
        collection.find(
            {"rating": {"$gt": 4}},
            {
                "category": 1,
                "title": 1,
                "rating": 1,
                "price": 1,
                "cover_book": 1,
                "_id": 0,
            },
        )
        .sort("price", 1)
        .limit(10)
    )
    for e in best_price_and_rating:
        e["cover_book"] = f"![image]({e['cover_book']})"
    return best_price_and_rating


@app.callback(
    Output("table-description-found-text", "data"), [Input("search-text", "value")]
)
def update_table_found_text(search_text):
    if search_text:
        return search_books_by_title(collection, search_text)
    else:
        return []


@app.callback(
    Output("random-book-output", "children"), [Input("random-book-button", "n_clicks")]
)
def update_random_book_info(n_clicks):
    if n_clicks:
        book = get_random_book(collection)
        return html.Div(
            [
                html.H3(book["title"]),
                html.Div(
                    [
                        html.Div(
                            [html.Img(src=book["cover_book"], alt=book["title"])],
                            className="random-book-image",
                        ),
                        html.Div(
                            [
                                html.P([html.Strong("Category: "), book["category"]]),
                                html.P([html.Strong("Rating: "), str(book["rating"])]),
                                html.P([html.Strong("Price: "), f"£{book['price']}"]),
                                html.P(
                                    [html.Strong("Description: "), book["description"]],
                                    className="random-book-desc",
                                ),
                            ],
                            className="random-book-info",
                        ),
                    ],
                    className="random-book-container",
                ),
            ]
        )


if __name__ == "__main__":
    app.run_server(debug=True)
