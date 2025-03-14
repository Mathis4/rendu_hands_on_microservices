import asyncpg
from fastapi import FastAPI

app = FastAPI()

# Fonction pour créer la table et insérer des données si elle n'existe pas
async def create_table_if_not_exists():
    # Créer la table si elle n'existe pas déjà
    await app.state.db.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100)
        );
    """)

    # Vérifier si la table est vide
    result = await app.state.db.fetch("SELECT COUNT(*) FROM my_table;")
    count = result[0]["count"]

    # Si la table est vide, insérer des données fictives pour tester
    if count == 0:
        await app.state.db.execute("""
            INSERT INTO my_table (name) VALUES
            ('John Doe'),
            ('Jane Smith'),
            ('Alice Johnson');
        """)

@app.on_event("startup")
async def startup():
    # Connexion à la base de données
    app.state.db = await asyncpg.connect(
        user="user", password="password", database="mydatabase", host="db"
    )
    # Création de la table si elle n'existe pas
    await create_table_if_not_exists()

@app.on_event("shutdown")
async def shutdown():
    # Fermeture de la connexion à la base de données
    await app.state.db.close()

@app.get("/get-data")
async def get_data():
    # Récupération des données de la table
    result = await app.state.db.fetch("SELECT * FROM my_table;")
    return [dict(record) for record in result]  # Convertir les résultats en dictionnaire
