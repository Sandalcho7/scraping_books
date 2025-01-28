# Introduction au scraping et création d'une interface

## Contexte
Dans le cadre de ma formation de développeur en IA, exercice de scraping d'un site internet et l'exposition des données récoltées via un tableau de bord.

## Outils
- `Scrapy` pour le scraping des données
- `MongoDB` pour le stockage des données
- `Dash` pour le développement de l'interface

## Prérequis
Avant de démarrer le développement le projet, il est nécessaire d'installer certaines dépendances sur l'environnement de travail. Pour effectuer ces installations, vous pouvez éxécuter la commande suivante :
```bash
pip install -r requirements.txt
```
L'installation de MongoDB fait aussi partie des prérequis pour le bon fonctionnement du projet. Vous trouverez ci-dessous la procédure d'installation sur WSL.

### Installation de MongoDB
1 / Mise à jour du système
```bash
sudo apt update
sudo apt upgrade -y
```
2 / Import de la clé GPG MongoDB
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
```
3 / Création du repo MongoDB
```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
Dans cette ligne de commande, remplacez `focal` par :
- `bionic` si vous utilisez Ubuntu 18.04
- `focal` pour Ubuntu 20.04
- `jammy` pour Ubuntu 22.04<br>

La commande ci-dessous vous permettra de connaître version Ubuntu que vous utilisez.
 ```bash
 lsb_release -a
```
4 / Mise à jour de la liste de packages
```bash
sudo apt update
```
5 / Installation de MongoDB
```bash
sudo apt install -y mongodb-org
```
6 / Démarrage de MongoDB
```bash
sudo systemctl start mongod
```

### Installation de MongoDB Compass (GUI)
Si vous souhaitez visualiser graphiquement votre base MongoDB, vous pouvez utiliser Compass. L'outil est téléchargeable [ici](https://www.mongodb.com/try/download/compass).

## Structure du projet
```bash
project/
│
├── src/
│   ├── assets/
│   │   └── style.css         # Feuille de style pour l'interface Dash
│   │
│   ├── functions/
│   │   ├── database.py       # Fonctions de recherche dans la base MongoDB
│   │   └── graph.py          # Fonctions de créations de graphiques
│   │
│   ├── scripts/
│   │   └── scraping.py       # Script de scraping du site internet
│   │
│   └── app.py                # Script du dashboard
│
├── .gitignore
├── README.md
└── requirements.txt          # Dépendances à installer
```

## Procédure
Après l'installation des dépendances et de MongoDB, il reste à scraper les données du site https://books.toscrape.com/. Depuis la racine du projet :
```bash
python src/scripts/scraping.py
```
On peut alors vérifier que les données ont bien été scrapées et sont présentes dans la base MongoDB. Pour lancer l'interface, on exécute la commande suivante :
```bash
python src/app.py
```
