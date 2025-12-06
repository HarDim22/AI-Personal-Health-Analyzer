---
title: MyLab Insight – AI Personal Health Analyzer
emoji: 🌿
colorFrom: indigo
colorTo: blue
sdk: fastapi
sdk_version: "0.110.0"
app_file: main.py
pinned: false
---

# 🌿 MyLab Insight  
**AI-Assisted Personal Health Analyzer (React + FastAPI)**

MyLab Insight is a **full-stack health analysis application** that helps users interpret common lab results, track historical trends, and receive AI-style educational explanations.

It combines a modern **React frontend**, a **FastAPI backend**, a **rule-based interpretation engine**, and **PDF report generation**.

🧑‍⚕️ **Not medical advice — educational use only.**

---

## 🚀 Live Demo

- **Backend API (Hugging Face Space):**  
  👉 https://hardim22-ai-personal-health-analyzer.hf.space

- **Frontend (Vercel):**  
  👉 https://ai-personal-health-analyzer.vercel.app/

---

## 📌 Features

### 🔬 Lab Result Interpretation
- Glucose fasting range evaluation  
- HbA1c classification  
- LDL / HDL / Total cholesterol analysis  
- Triglycerides interpretation  
- Overall health risk score  

### 🧠 AI-Style Explanation Engine
- Human-readable summaries  
- Lifestyle suggestions  
- Highlighted abnormalities  
- **Fully deterministic** (rule-based, no ML, no hallucinations)

### 📊 Trend Visualization
- Glucose trends over time (Recharts)  
- Stored lab history (JSON-based)

### 📄 PDF Report Generation
- Clean formatted PDF output  
- Includes values, references & explanations

### 💻 Modern Frontend (React + Vite)
- Responsive UI  
- Form validation  
- Simple, clean design  
- Environment-based API configuration

### 🧱 FastAPI Backend
- Clean REST architecture  
- Deployed on **Hugging Face Spaces**  
- CORS configured for frontend integration

---

## 🏗 Architecture Overview

┌──────────────────────────┐
│ React UI │
│ (Vite + Recharts) │
└───────────┬──────────────┘
│ REST API
▼
┌──────────────────────────┐
│ FastAPI Backend │
├──────────────────────────┤
│ analyze-labs │
│ save-result │
│ ai-summary │
│ generate-report (PDF) │
└───────────┬──────────────┘
│
▼
┌──────────────────────────┐
│ history.json storage │
└──────────────────────────┘


---

## 📁 Project Structure

AI-Personal-Health-Analyzer/
│
├── backend/ # Hugging Face Space
│ ├── main.py
│ ├── health_rules.py
│ ├── history.json
│ ├── requirements.txt
│ └── README.md
│
├── health-analyzer-frontend/ # Vercel deployment
│ ├── src/
│ │ ├── App.jsx
│ │ ├── main.jsx
│ │ └── App.css
│ ├── index.html
│ └── package.json
│
└── README.md


---

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/analyze-labs` | Analyze lab values |
| POST | `/save-result` | Analyze + store entry |
| GET  | `/history` | Retrieve saved analyses |
| POST | `/ai-summary` | AI-style explanation |
| GET  | `/generate-report` | Download PDF report |

---

## 🌍 Environment Variables (Frontend)

Create `.env.local` in the frontend project:

```env
VITE_API_BASE_URL=https://hardim22-ai-personal-health-analyzer.hf.space
Used automatically by Vercel during deployment.

⚠️ Disclaimer

This application does not provide medical advice or diagnosis.
All outputs are educational only and must be interpreted by a qualified healthcare professional.

🧭 What I Learned (Key Portfolio Value)

This project helped me strengthen skills in:

Full-stack development (React + FastAPI)

REST API design & integration

Rule-based reasoning systems

Generating PDF files in Python

State management in React

Data visualization with Recharts

CORS configuration & environment variables

GitHub workflow & clean project structure

Deploying real-world applications (Hugging Face + Vercel)

👤 Author

Dimitra Charizani
Applied Informatics — University of Macedonia

🔗 GitHub: https://github.com/HarDim22

🔗 LinkedIn: https://linkedin.com/in/dimitra-charizani