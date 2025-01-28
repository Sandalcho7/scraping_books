def get_books_available(collection, categories_filtered):
    if "all" in categories_filtered:
        books_list = list(
            collection.find(
                {"available_stock": {"$gt": 10}},
                {"category": 1, "title": 1, "price": 1, "rating": 1, "_id": 0},
            )
        )
    else:
        books_list = list(
            collection.find(
                {
                    "available_stock": {"$gt": 10},
                    "category": {"$in": categories_filtered},
                },
                {"category": 1, "title": 1, "price": 1, "rating": 1, "_id": 0},
            )
        )
    return books_list


def get_best_rated_books(collection, categories_filtered):
    if "all" in categories_filtered:
        books_list = list(
            collection.find(
                {"rating": {"$gt": 4}},
                {"category": 1, "title": 1, "rating": 1, "_id": 0},
            )
        )
    else:
        books_list = list(
            collection.find(
                {"rating": {"$gt": 4}, "category": {"$in": categories_filtered}},
                {"category": 1, "title": 1, "rating": 1, "_id": 0},
            )
        )
    return books_list


def search_books_by_title(collection, search_input):
    import re

    search_words = search_input.split()
    regex_pattern = r"(?=.*{})".format(")(?=.*".join(map(re.escape, search_words)))
    books_list = list(
        collection.find(
            {"title": {"$regex": regex_pattern, "$options": "i"}},
            {"category": 1, "title": 1, "rating": 1, "price": 1, "_id": 0},
        )
    )
    return books_list


def get_random_book(collection):
    random_book = collection.aggregate([{"$sample": {"size": 1}}])
    return list(random_book)[0]
