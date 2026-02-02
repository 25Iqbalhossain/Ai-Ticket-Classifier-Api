## Run (Docker)

 
 1) Create `.env`
Copy the example env file and update values if needed:

```bash
cp .env.example .env

Copy-Item .env.example .env

2) Build & Start

From the project root (where docker-compose.yml exists):

docker compose up --build


Run in background (optional):

docker compose up --build -d

3) Open API Docs (Swagger)

Swagger UI: http://localhost:8000/docs

Useful Commands:

Stop containers
docker compose down

Stop + remove volumes (reset DB/data if any)
docker compose down -v

View logs:
docker compose logs -f

Rebuild only:
docker compose build --no-cache
docker compose up

Check running services
docker compose ps


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

