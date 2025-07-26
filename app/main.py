from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def init_db():
    Base.metadata.create_all(bind=engine)

@app.get("/menu")
def get_menu():
    menu_items = [
        { "name": "Margherita", "description": "Tomato, mozzarella, and fresh basil" },
        { "name": "Pepperoni", "description": "Loaded with pepperoni and mozzarella cheese" },
        { "name": "Veggie", "description": "Bell peppers, onions, olives, and mushrooms" },
        { "name": "BBQ Chicken", "description": "BBQ sauce, grilled chicken, and red onions" },
        { "name": "Hawaiian", "description": "Ham, pineapple, and mozzarella" },
        { "name": "Meat Lovers", "description": "Sausage, pepperoni, ham, and bacon" },
        { "name": "Four Cheese", "description": "Mozzarella, parmesan, gorgonzola, and goat cheese" },
        { "name": "Spicy Italian", "description": "Spicy salami, peppers, and chili oil" },
    ]
    return menu_items

@app.get("/")
def read_root():
    return {"message": "Hello, Dockerized FastAPI!"}

@app.get("/ping")
def ping():
    return {"ping": "pong"}
