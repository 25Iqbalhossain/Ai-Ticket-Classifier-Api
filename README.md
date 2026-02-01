## Run (Docker)

1) Copy env:
   cp .env.example .env

2) Start:
   docker compose up --build

Open:
- Swagger: http://localhost:8000/docs


# Project 
ai_ticket_api/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  ├─ config.py
│  │  └─ db.py
│  ├─ models/
│  │  └─ ticket.py
│  ├─ schemas/
│  │  └─ ticket.py
│  ├─ repositories/
│  │  └─ ticket_repo.py
│  ├─ services/
│  │  ├─ ml_model.py
│  │  └─ ticket_service.py
│  └─ api/
│     └─ routes_ticket.py
├─ scripts/
│  └─ train_model.py
├─ .env.example
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
