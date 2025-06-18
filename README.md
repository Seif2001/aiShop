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

### 📁 Clone the Repository

```bash
git clone https://github.com/Seif2001/aiShop.git
cd aiShop
```

### 📦 Backend Setup

---

## 🔐 Get Your OpenRouter API Key (for Mistral or GPT Models)

This project uses [OpenRouter.ai](https://openrouter.ai) to connect to AI models such as **Mistral**, **Claude**, or **GPT-4** via API.

Follow these steps:

1. Go to [https://openrouter.ai](https://openrouter.ai)
2. Sign up or log in
3. Go to **API Keys**
4. Click **Create new key**
5. Copy the key (starts with `sk-or-...`)

---

## 🔑 Add It to Your `.env` File

Inside your `backend/.env` add:

```env
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxxxxxx
```
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
docker compose up --build
```

---

## 🔗 Live Demo & Documentation Links

| Interface            | Link                                                | Description                                   |
|----------------------|-----------------------------------------------------|-----------------------------------------------|
| 🖥️ Frontend (React)  | [http://localhost:5173](http://localhost:5173)      | Vite dev server for the AI customer UI        |
| 📡 Backend API Docs  | [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) | Swagger UI via drf-spectacular |

---

## 📬 API Examples

### 🔐 Signup User

**POST** `/api/users/signup/`

Creates a new user and returns JWT tokens.

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/users/signup/ \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seif123",
    "email": "seif@example.com",
    "password": "seif1234"
  }'
```
### Response
```bash
{
  "message": "Signup successful",
  "user": {
    "id": 1,
    "username": "seif123",
    "email": "seif@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJh...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhb..."
  }
}
```
---

### 🔑 Login User

**POST** `/api/users/login/`

Authenticates a user and returns a JWT access token.

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seif@example.com",
    "password": "123"
  }'
```
### Response:
```bash
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "seif123",
    "email": "seif@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
  }
}

```
---

### 💬 Chat with AI Agent

**POST** `/api/conversations/chat/`

Sends a user message to the AI agent and receives an intelligent response. Requires authentication via JWT.

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/conversations/chat/ \
  -H "accept: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "List all orders"
  }'
```

### Response:
```bash
{
  "message": "Hello! Here are the orders associated with your user ID 2:\n\n1. Order #1: You have a pending order for Noise Cancelling Headphones x2.\n2. Order #2: You also have a pending order for an Iphone x1.\n\nBoth orders are yet to be processed. We'll keep you updated on their status. If you have any other requests or need assistance with something else, feel free to let me know!"
}
```

