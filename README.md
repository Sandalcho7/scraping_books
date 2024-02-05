# BIBLIOMETRICS / DAHSBOARD WITH MONGO DB

Coding in python and link to a scraped data base in Mongo DB.
First steps is scrapping and second steps is the creation of the dashboard linked with mongoDB.

***

# Table of Contents
1. [Overview](#overview)
2. [How to Run](#how-to-run)
3. [Different views](#different-views)
   - [1. CEO](#1-ceo)
   - [2. Real Estate Agent](#2-real-estate-agent)
4. [Notes](#notes)

***

## Overview
As a data analyst we have been asked to create an innovating project with AI and data analysis.
With scrapping tool we had to extract strategic datas on a website : https://books.toscrape.com/ and create a dashboard to get the intersting datas such as :
  Number of books per categoy
  Average rating for each categories
  List of books available (more than 10 instocks)

## How to Run
- run in python 3.11
- Ensure you have to pip install requirements.txt (Scrapy / pymongo 3.12.0)
- download : Mongo DB following this instruction list

INSTALL MONGO DB
********
download mongodb 
with last version for linux
 https://www.mongodb.com/try/download/community
implement download in you linux environment
in your terminal open the repository where the mongodb download is done :
User-PC-PF1MSF5J:~$ tar -zxvf mongodb-linux-x86_64-ubuntu2204-7.0.5.tgz
User-PC-PF1MSF5J:~$ sudo mv mongodb-linux-x86_64-ubuntu2204-7.0.5 /usr/local/mongodb
User-PC-PF1MSF5J:~$ sudo mkdir -p /data/db
User-PC-PF1MSF5J:~$ sudo chown -R $USER /data/db
User-PC-PF1MSF5J:~$ cd /usr/local/mongodb/bin
User-PC-PF1MSF5J:/usr/local/mongodb/bin$ ./mongod
DOWNLOAD MONGODB COMPASS
you can implement it in a Windows Environment to ensure interface with internet.
https://www.mongodb.com/try/download/compass
****** 
/!\ our database name is "bibliometrics" : ensure you have no database with the same name in MongoDB
1. Run mongo db before running your code
2. Open compass_mongoDB and make sure you are connected and with no database named bibliometrics
3. Run the file named : spider.py in 'scraper' with 'python3 spider.py' 
3. Run the file named : app.py in 'dashboard' with 'python3 app.py'

***

## Different views

app = dash.Dash()
app.run_server(debug=True)

You will access to the main dashboard page with
`http://127.0.0.1:8050/`

***
### 1. Number of books in each category
- **URL**: `http://127.0.0.1:8050/`
- **Method**: Dash .find in mongo DB Bibliometrics
- **DropDown** : Values are all categories in bibliometrics. Selections can be multiple default value is 'all' (all catgories in bibliometrics)
- **Params**: 
  - `book.count`
- **Success Response**: graph with number of books per categories selected.

### 2. Average rating for each category
- **URL**: `http://127.0.0.1:8050/`
- **Method**: Dash .find in mongo DB Bibliometrics
- **DropDown** : Values are all categories in bibliometrics. Selections can be multiple default value is 'all' (all catgories in bibliometrics)
- **Params**: 
  - `rating average`
- **Success Response**: graph with number of books per categories selected.

### 3. List of books available (more than 10 in stocks)
- **URL**: `http://127.0.0.1:8050/`
- **Method**: Dash .find in mongo DB Bibliometrics
- **DropDown** : Values are all categories in bibliometrics. Selections can be multiple default value is 'all' (all catgories in bibliometrics)
- **Params**: 
"available_books = list(collection.find({"available_stock": {"$gt": 10}, "category": {'$in': categories_filtered}}, {'_id': 0}))"
- **Success Response**: table with a list of book, category, price and rating.

### 4. List of books rated by more than 3
- **URL**: `http://127.0.0.1:8050/`
- **Method**: Dash .find in mongo DB Bibliometrics
- **DropDown** : Values are all categories in bibliometrics. Selections can be multiple default value is 'all' (all catgories in bibliometrics)
- **Params**: 
"best_rated_books = list(collection.find({"rating": {"$gt": 4}, "category": {'$in': categories_filtered}}, {'_id': 0}))"
- **Success Response**: table with a list of book, category and rating


## Notes

- this is a collaborative work with common work on all the steps of the project.
Merge, commits were made live and in a cooperative environment.

```
## Usage

internal usage only. for training only
```

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
