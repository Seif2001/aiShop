# 🤖 AI Customer Service Agent

This project is a full-stack conversational AI agent designed to assist users with customer service tasks such as:

- 📦 Tracking orders
- 👤 Managing user profiles
- 🔍 Searching products

It uses **Django REST Framework** for the backend and **React + Vite + TailwindCSS** for the frontend. Authentication is managed using **JWT tokens**, and AI replies are generated through a custom Python agent.

---

## 🛠️ Tech Stack

| Layer        | Technology                            |
|--------------|----------------------------------------|
| Backend      | Django, Django REST Framework, PostgreSQL |
| Frontend     | React, Vite, TailwindCSS               |
| Auth         | SimpleJWT (access token only)          |
| AI Logic     | Custom Python-based agent              |
| DevOps       | Docker, Docker Compose                 |
| Docs         | drf-spectacular (Swagger/OpenAPI)      |

---

---

## 🚀 Getting Started

### 📦 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
docker-compose up --build
```

