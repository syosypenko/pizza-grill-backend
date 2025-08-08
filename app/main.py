from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import engine, Base
from app.models.user import User
from app import models, database, auth, schemas
from app.deps import get_db
from app.routes import protected

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(protected.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = auth.get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/logout")
def logout():
    # Just a confirmation, since JWT is stateless
    return {"message": "Logged out successfully"}

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
