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
