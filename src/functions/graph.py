import plotly.express as px
import pandas as pd


def create_book_count_graph(df):
    book_count = df["category"].value_counts().reset_index()
    book_count.columns = ["category", "count"]
    colors = px.colors.qualitative.Set3[: len(book_count)]
    fig = px.bar(
        book_count,
        x="category",
        y="count",
        color="category",
        color_discrete_sequence=colors,
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def create_rating_graph(df):
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    avg_rating = df.groupby("category")["rating"].mean().reset_index()
    avg_rating = avg_rating.sort_values(by="rating", ascending=False)
    fig = px.bar(
        avg_rating,
        x="category",
        y="rating",
        color="category",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def create_rating_pie_chart(books):
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for book in books:
        rating = book["rating"]
        rating_counts[rating] += 1
    fig = px.pie(
        names=[f"Rating {rating}" for rating in rating_counts.keys()],
        values=list(rating_counts.values()),
        hole=0.3,
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig
