# PDF Summary AI Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)

---

## 🚀 Features

* **Smart Parsing:** Uses OpenAI GPT-4o to extract key points, monetary amounts, and dates.
* **Multilingual Support:** Automatically detects the document language and generates the summary in the same language.
* **Audio Summary:** Generates an MP3 voiceover of the summary using OpenAI TTS (`alloy` voice).
* **Cost Transparency:** Calculates and displays the exact USD cost for processing based on tokens.
* **Dockerized:** Fully containerized setup with `docker-compose`.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Interfaced via `ui/demo_ui.py`)
* **Backend:** FastAPI (Entry point `app/api.py`)
* **Database:** SQLite (Stores history and metadata)
* **AI:** OpenAI API (Assistants v2 + TTS-1)
* **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

```text
.
├── app/
│   ├── api.py
│   ├── config.py
│   ├── service.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── Dockerfile
├── ui/
│   ├── demo_ui.py
│   └── Dockerfile
├── .env               
└── docker-compose.yml 
```

## ⚡ Setup & Installation

* Follow these steps to get the application running in minutes using Docker.

### Prerequisites
* **Docker** and **Docker Compose** installed on your machine.
* An active **OpenAI API Key** (you can get it [here](https://platform.openai.com/api-keys)).

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd demo
````

## 2. Configure Environment
* Create a .env file in the root directory of the project. This file will store your sensitive API keys and is excluded from version control.

* Open .env and add your OpenAI API Key:
```text
  OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 3. Build and Run
* Start the application using Docker Compose. This command will build the images for both Backend and Frontend and start the services.
```bash
docker-compose up --build
```

## 4. Access the Application
* Once the logs show that the server is running, you can access the app:

* Frontend (UI): http://localhost:8501 – Upload PDFs here.

* Backend (API Docs): http://localhost:8000/docs – Explore the API endpoints with Swagger.

