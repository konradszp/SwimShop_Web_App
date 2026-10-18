# SwimShop Web

Web version of the POS, inventory and orders management system for a swimming gear shop.

Backend: **FastAPI**  (in progess)
Frontend: **React** (in progress)  
Database: **MySQL** (Docker)

## Project Structure

```
├── backend/                 # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── routers/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # React (to be added)
├── docker-compose.yml
├── schema.sql
└── README.md
```

## Requirements

- Docker + Docker Compose
- Python 3.12+ and Node.js for local development

## Getting Started

```bash
# Make sure schema.sql is in the project root
docker compose up --build
```

- API: http://localhost:8000  
- Documentation: http://localhost:8000/docs  
- MySQL: `localhost:3307`

