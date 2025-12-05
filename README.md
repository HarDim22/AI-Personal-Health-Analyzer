🌿 MyLab Insight
AI-Assisted Personal Health Analyzer (React + FastAPI)

MyLab Insight is a full-stack health analysis application that helps users interpret common lab results, track historical trends, and receive AI-style educational explanations.

It combines a modern React frontend, a FastAPI backend, rule-based interpretation engine, and PDF report generation.

🧑‍⚕️ Not medical advice — educational only.

🚀 Demo (Local Development)

Frontend → http://localhost:5174
Backend → http://localhost:8000

📌 Features
🔬 Lab Result Interpretation

Glucose fasting range evaluation

HbA1c classification

LDL / HDL / Total cholesterol analysis

Triglycerides interpretation

Overall risk score

🧠 AI-Style Explanation Engine

Generates human-like summaries

Provides lifestyle suggestions

Highlights key abnormalities

Fully deterministic (rule-based, no ML)

📊 Trend Visualization

Glucose chart over time (Recharts)

Stored lab history (JSON-based)

📄 PDF Report Generation

Clean formatted PDF file

Includes all lab values and interpretation

💻 Modern Frontend (React + Vite)

Responsive UI

Form validation

Light & simple design

Environment-based API URL

🧱 FastAPI Backend

Clean REST architecture

CORS configured for Vercel / local dev

🏗 Architecture Overview
                    ┌──────────────────────────┐
                    │        React UI          │
                    │  (Vite Frontend)         │
                    └───────────┬──────────────┘
                                │ REST API
                                ▼
                    ┌──────────────────────────┐
                    │      FastAPI Backend     │
                    ├──────────────────────────┤
                    │ analyze-labs             │
                    │ save-result              │
                    │ ai-summary               │
                    │ generate-report (PDF)    │
                    └───────────┬──────────────┘
                                │
                                ▼
                    ┌──────────────────────────┐
                    │   history.json storage   │
                    └──────────────────────────┘

📁 Project Structure
AI-Personal-Health-Analyzer/
│
├── backend/
│   ├── main.py
│   ├── health_rules.py
│   ├── history.json
│   ├── requirements.txt
│ │
├── health-analyzer-frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── App.css
│   ├── index.html
│   └── package.json
│
└── README.md           

⚙️ Backend Setup (FastAPI)
1️⃣ Install dependencies
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# ή
source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt

2️⃣ Run server
uvicorn main:app --reload


Backend runs at:

http://localhost:8000

🔌 Backend API Endpoints
POST /analyze-labs

Analyze lab values.

POST /save-result

Analyze + store entry in history.

GET /history

Return sorted history list.

POST /ai-summary

Return AI-style explanation based on lab values.

GET /generate-report

Returns a PDF with analysis.

🖥 Frontend Setup (React + Vite)
1️⃣ Install dependencies
cd health-analyzer-frontend
npm install

2️⃣ Start development server
npm run dev -- --port 5174


Frontend at:

http://localhost:5174

🌍 Environment Variables

Create a .env.local in the frontend:

VITE_API_BASE_URL=http://localhost:8000


For production (Vercel):

VITE_API_BASE_URL=https://your-backend-host.com

📦 Deployment
🔵 Frontend → Vercel

Select the frontend folder

Framework should auto-detect Vite

Add env variable VITE_API_BASE_URL

🔵 Backend → Railway / Fly.io / Deta Space


Start command:

uvicorn main:app --host 0.0.0.0 --port $PORT


Don’t forget to update allowed CORS origins.



🧭 What I Learned (Strong Portfolio Section)

This project allowed me to practice and strengthen:

Full-stack development (React + FastAPI)

REST API design

Rule-based reasoning systems

Generating PDF files in Python

State management in React

Data visualization with Recharts

CORS configuration & environment variables

Clean project structure and GitHub workflow

Building deployable real-world apps


👤 Author
Dimitra Charizani
Applied Informatics — University of Macedonia

🔗 LinkedIn: https://linkedin.com/in/dimitra-charizani
🔗 GitHub: https://github.com/HarDim22