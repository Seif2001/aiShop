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

## 📁 Folder Structure
ai-customer-agent/
├── backend/ # Django backend
│ ├── AIshop/ # Django project
│ ├── users/ # Auth & profile management
│ ├── conversations/ # Chat history
│ ├── products/ # Product data
│ ├── orders/ # Order tracking
│ ├── requirements.txt
│ └── Dockerfile
│
├── frontend/ # React frontend
│ ├── src/
│ ├── public/
│ └── package.json
│
├── docker-compose.yml
├── .env.example
└── README.md
