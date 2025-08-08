# 🍕 Pizza Grill - Backend

This is the FastAPI backend for the Pizza Grill web application. It manages user authentication and serves menu data via a RESTful API.

## 🔧 Tech Stack

- Python 3.11  
- FastAPI  
- SQLite (for development)  
- SQLAlchemy  
- Docker  

---

## 🧪 Run Locally (No Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

🐳 Run with Docker
docker compose up --build
The API will be available at:
http://localhost:8000

Running Tests in Docker
We use pytest for automated testing.
To run the full test suite inside the backend container:
docker compose exec backend pytest -v app/tests

📂 Project Structure
app/
  ├── main.py           # FastAPI entry point
  ├── database.py       # DB connection & Base class
  ├── models/           # SQLAlchemy models
  ├── routes/           # API endpoints
  ├── deps.py           # Dependencies (get_db, get_current_user, etc.)
  ├── auth.py           # Password hashing & JWT token logic
  ├── schemas.py        # Pydantic schemas
  └── tests/            # Automated tests