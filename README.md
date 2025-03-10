# Madonna Project

## 📌 Project Overview
This project is designed to **ingest, structure, and analyze Madonna-related data**, spanning nearly 60 years.  
The goal is to **build an AI-powered database** that can be explored via a web interface.

## 🛠️ Tech Stack
- **MariaDB** (Relational database for structured metadata)
- **ChromaDB** (Vector database for AI-powered search)
- **FastAPI** (Backend API for serving data)
- **Next.js** (Frontend for browsing & visualization)
- **Docker** (To containerize everything)

## 📂 Project Structure
📂 madonna_project/
│── 📂 data/             # Raw & processed data files
│── 📂 docker/           # Docker setup (MariaDB, ChromaDB)
│── 📂 database/         # Schema & DB setup scripts
│── 📂 backend/          # API backend (FastAPI)
│── 📂 frontend/         # Web UI (Next.js)
│── 📂 scripts/          # Data ingestion & processing
│── 📂 docs/             # Documentation
│── .gitignore
│── README.md

## 🚀 Setup Instructions

### 1️⃣ Install Dependencies
Ensure you have **Docker** installed. Then, run:
```zsh
cd docker
docker-compose up -d

This will start MariaDB & ChromaDB.

2️⃣ Clone & Run This Project

git clone https://github.com/billy3785/madonna_project.git
cd madonna_project

3️⃣ Next Steps
	•	[ ] Ingest first batch of Madonna data
	•	[ ] Set up database schema
	•	[ ] Develop API endpoints for search
	•	[ ] Build interactive web UI
