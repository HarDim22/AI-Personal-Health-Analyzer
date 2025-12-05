# 🧪 MyLab Insight – React Frontend  
Modern health dashboard for analyzing lab results, visualizing trends, and receiving AI-style explanations.

This is the frontend of the MyLab Insight system, built with React + Vite and styled with modern responsive UI.  
It communicates with a FastAPI backend through REST APIs.

---

## 🎨 Features

- Clean modern UI (React + Vite)
- Form for entering common lab values
- Result interpretation with risk levels
- AI-style explanation panel
- Lab history tracking
- Glucose trend chart (Recharts)
- PDF report download
- Environment-based API URL (`.env` support)
- Fully ready for Vercel deployment

---

## 📁 Project Structure

ai-health-analyzer-frontend/
│
├── public/
├── src/
│ ├── App.jsx
│ ├── main.jsx
│ ├── components/ (if added later)
│ └── App.css
├── index.html
├── package.json
└── README.md

## 🔧 Environment Variables

Create `.env.local` for development:

VITE_API_BASE_URL=http://localhost:8000

java
Copy code

For production (Vercel):

VITE_API_BASE_URL=https://your-backend.onrender.com

yaml
Copy code

---

## 🛠️ Run Locally

Clone:

```bash
git clone https://github.com/your-username/ai-health-analyzer-frontend
cd ai-health-analyzer-frontend
Install:

bash
Copy code
npm install
Start dev server:

bash
Copy code
npm run dev -- --port 5174
Open:

arduino
Copy code
http://localhost:5174
🌍 Deploy on Vercel
Import GitHub repo

Framework: Vite

Add environment variable:

ini
Copy code
VITE_API_BASE_URL=https://your-backend.onrender.com
Deploy → Done ✔

🧠 API Integration Example
jsx
Copy code
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

const res = await fetch(`${API_BASE_URL}/analyze-labs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formValues),
});
👤 Author
Dimitra Charizani
Applied Informatics | Full-Stack Developer
🔗 LinkedIn: https://linkedin.com/in/dimitra-charizani