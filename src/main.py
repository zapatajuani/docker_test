from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from databases import Database
import dotenv

dotenv.load_dotenv()
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_NAME")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_HOST = os.getenv("POSTGRES_HOST")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await database.connect()
        query = f"CREATE TABLE IF NOT EXISTS {os.getenv('TABLE_NAME')} (id SERIAL PRIMARY KEY, name VARCHAR(100))"
        await database.execute(query=query)
    except Exception as e:
        print(e)
    
    # This is where the application starts
    yield

    try:
        await database.disconnect()
    except Exception as e:
        print(e)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/users")
async def read_users():
    query = f"SELECT * FROM {os.getenv('TABLE_NAME')}"
    users = await database.fetch_all(query=query)
    return users

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    query = f"SELECT * FROM {os.getenv('TABLE_NAME')} WHERE id = :user_id"
    user = await database.fetch_one(query=query, values={"user_id": user_id})
    return user

@app.post("/users")
async def create_user(name: str):
    query = f"INSERT INTO {os.getenv('TABLE_NAME')} (name) VALUES (:name)"
    await database.execute(query=query, values={"name": name})
    return {"message": "User created successfully"}

@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str):
    query = f"UPDATE {os.getenv('TABLE_NAME')} SET name = :name WHERE id = :user_id"
    await database.execute(query=query, values={"name": name, "user_id": user_id})
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = f"DELETE FROM {os.getenv('TABLE_NAME')} WHERE id = :user_id"
    await database.execute(query=query, values={"user_id": user_id})
    return {"message": "User deleted successfully"}
