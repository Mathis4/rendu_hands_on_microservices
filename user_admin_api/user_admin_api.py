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

# Récupérer tous les utilisateurs (admin only)
@app.get("/admin/users")
async def get_all_users():
    result = await app.state.db.fetch("SELECT * FROM my_table;")
    return [dict(record) for record in result]

# Supprimer un utilisateur (admin only)
@app.delete("/admin/users/delete")
async def delete_user(user_id: int):
    await app.state.db.execute("DELETE FROM my_table WHERE id=$1;", user_id)
    return {"message": "Utilisateur supprimé avec succès"}

# Envoyer (ajouter) une donnée
@app.post("/users/send")
async def send_data(name: str):
    await app.state.db.execute("INSERT INTO my_table (name) VALUES ($1);", name)
    return {"message": "Donnée envoyée avec succès"}