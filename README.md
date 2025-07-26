# 🍕 Pizza Grill - Backend

This is the FastAPI backend for the Pizza Grill web application. It manages user authentication and serves menu data via a RESTful API.

## 🔧 Tech Stack

- Python 3.11
- FastAPI
- SQLite (for development)
- SQLAlchemy
- Docker

## 🧪 Run Locally (No Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

Run with Docker

docker build -t pizza-backend .
docker run -p 8000:8000 pizza-backend