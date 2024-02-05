from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime

# Se connecter à MongoDB (assurez-vous que MongoDB est en cours d'exécution)
client = MongoClient('localhost', 27017)

# Sélectionner la base de données
db = client['media_db']

# Sélectionner la collection
media_collection = db['media']

fake = Faker()

def print_line():
    print('')
    print('*******************************************************')
    print('')


# Fonction pour générer une date aléatoire pour la publication
def random_publication_date(start_year, end_year):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)

# Générer des documents de médias (au moins 10 par type)
media_documents = []

for _ in range(10):
    media_documents.append({
        "type": "book",
        "title": fake.text(max_nb_chars=30),
        "publication_date": datetime.combine(random_publication_date(1900, 2022), datetime.min.time()),
        "authors": [{"name": fake.name(), "birth_year": random.randint(1900, 2022), "birth_city": fake.city()} for _ in range(random.randint(1, 3))],
        "description": fake.sentence()
    })

    media_documents.append({
        "type": "dvd",
        "title": fake.text(max_nb_chars=30),
        "publication_date": datetime.combine(random_publication_date(1990, 2022), datetime.min.time()),
        "directors": [{"name": fake.name(), "birth_year": random.randint(1900, 2022), "birth_city": fake.city()} for _ in range(random.randint(1, 3))],
        "actors": [{"name": fake.name(), "birth_year": random.randint(1900, 2022), "birth_city": fake.city(), "astrological_sign": fake.word()} for _ in range(random.randint(1, 5))],
        "description": fake.sentence()
    })

    media_documents.append({
        "type": "cd",
        "title": fake.text(max_nb_chars=30),
        "publication_date": datetime.combine(random_publication_date(1980, 2022), datetime.min.time()),
        "artists": [{"name": fake.name(), "birth_year": random.randint(1900, 2022), "birth_city": fake.city()} for _ in range(random.randint(1, 3))],
        "description": fake.sentence()
    })

# Insérer les documents dans la collection
resultat_insertion = media_collection.insert_many(media_documents)

# Imprimer les IDs des documents insérés
print(f"IDs des documents insérés : {resultat_insertion.inserted_ids}")

print_line()
# Requêtes

print("1. Récupérer tous les documents")
tous_les_medias = media_collection.find({})
for media in tous_les_medias:
    print(media)

print_line()

print("2. Récupérer les DVDs sortis après 2005")
dvds_apres_2005 = media_collection.find({"type": "dvd", "publication_date": {"$gt": datetime(2005, 1, 1)}})
for dvd in dvds_apres_2005:
    print(dvd)

print_line()

print('3. Récupérer les livres de l\'auteur "Chad Diaz"')
livres_fitzgerald = media_collection.find({"type": "book", "authors.name": "Chad Diaz"}, {'title': 1, '_id': 0})
for livre in livres_fitzgerald:
    print(livre)

print_line()

print('Récupérer tous les livres publiés après 2000')
livres_apres_2000 = media_collection.find({"type": "book", "publication_date": {"$gt": datetime(2000, 1, 1)}})
for livre in livres_apres_2000:
    print(livre)

print_line()

print('5. Récupérer les DVDs réalisés par un dont le prénom est James')
dvds_realisateur_specifique = media_collection.find({"type": "dvd", "directors.name": {"$regex": ".*James.*"}})
for dvd in dvds_realisateur_specifique:
    print(dvd)

print_line()

print('6. Récupérer les CDs publiés dans les années 2000')
cds_annees_2000 = media_collection.find({"type": "cd", "publication_date": {"$gte": datetime(2000, 1, 1), "$lt": datetime(2010, 1, 1)}})
for cd in cds_annees_2000:
    print(cd)

print_line()

print('7. Mettre à jour la description d un DVD spécifique')
update_dvd_query = {"type": "dvd", "title": "Act them training together."}
update_dvd_operation = {"$set": {"description": "Nouvelle description"}}
print(f'Description du DVD avant mise à jour : {media_collection.find_one(update_dvd_query, {"description": 1})}')
media_collection.update_one(update_dvd_query, update_dvd_operation)
print(f'Description du DVD mis à jour : {media_collection.find_one(update_dvd_query, {"description": 1})}')

print_line()

print('8. Agréger le nombre de médias par type')
aggregate_type_count = media_collection.aggregate([
    {"$group": {"_id": "$type", "count": {"$sum": 1}}}
])
for result in aggregate_type_count:
    print(f"Nombre de médias de type {result['_id']}: {result['count']}")

print_line()

print('9. Regrouper les DVDs par acteur et compter le nombre de DVDs pour chaque groupe d acteur qui ont la même première lettre, en filtrant les acteurs nés après 1990.')
# Agrégation avec Filtrage
aggregate_group_by_actor = media_collection.aggregate([
    {"$match": {"type": "dvd", "actors.birth_year": {"$gt": 1990}}},
    {"$unwind": "$actors"},
    {"$group": {"_id": {"$substr": ["$actors.name", 0, 1]}, "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])
for result in aggregate_group_by_actor:
    print(result)
