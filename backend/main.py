from typing import Optional, List, Dict
import io

import json
import os
import uuid
from uuid import uuid4
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse,FileResponse
from pydantic import BaseModel
from pathlib import Path
from health_rules import analyze_labs  # health_rules.py must be in same folder

# === Paths
BASE_DIR = Path(__file__).parent
HISTORY_FILE = BASE_DIR / "history.json"

app = FastAPI(
    title="AI Personal Health Analyzer",
    description="Simple API that interprets basic blood test results using rule-based logic.",
    version="0.2.1",
)

origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "https://ai-personal-health-analyzer.vercel.app/",
]
# DEV: allow all origins so React on any localhost port can access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LabInput(BaseModel):
    glucose: Optional[float] = None
    hba1c: Optional[float] = None
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    triglycerides: Optional[float] = None
    total_cholesterol: Optional[float] = None

class SaveRequest(LabInput):
    label: Optional[str] = None  


def load_history():
    """Load saved lab analyses from a JSON file."""
    if not HISTORY_FILE.exists:
        return []
    try:
         return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_history(entries):
    """Save the list of analyses to the JSON file."""
    HISTORY_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

def build_ai_like_summary(analysis: Dict) -> Dict:
    """
    Build a pseudo-AI style explanation based on the analysis
    returned by analyze_labs.
    This does NOT provide medical diagnosis, only general education.
    """
    overall_risk = analysis.get("overall_risk", "unknown")
    items = analysis.get("items", [])

    general_overview_parts: List[str] = []
    detailed_points: List[str] = []
    lifestyle_tips: List[str] = []

    # General overview based on overall risk
    if overall_risk == "high_risk":
        general_overview_parts.append(
            "Several of your lab values are outside the recommended ranges. "
            "This pattern may be associated with an increased long-term health risk."
        )
    elif overall_risk == "moderate_risk":
        general_overview_parts.append(
            "Some of your lab values are slightly outside the optimal range. "
            "This suggests areas where lifestyle adjustments and follow-up testing "
            "could be helpful."
        )
    else:
        general_overview_parts.append(
            "The available lab values appear to be within acceptable ranges. "
            "Maintaining healthy habits and regular check-ups remains important."
        )

    # Go through each item to add more context & lifestyle ideas
    for item in items:
        name = item.get("name", "")
        status = item.get("status", "")
        value = item.get("value", None)
        unit = item.get("unit", "")

        # Glucose
        if "Glucose" in name:
            if status in ("high", "very_high"):
                detailed_points.append(
                    f"Your fasting glucose ({value} {unit}) is above the usual fasting range, "
                    "which can be associated with higher blood sugar over time."
                )
                lifestyle_tips.append(
                    "Consider limiting sugary drinks and refined carbohydrates, "
                    "choosing more whole grains and vegetables, and discussing your "
                    "blood sugar with a healthcare professional."
                )
            elif status in ("borderline_high", "elevated"):
                detailed_points.append(
                    f"Your fasting glucose ({value} {unit}) is slightly above the optimal range."
                )
                lifestyle_tips.append(
                    "Regular physical activity, balanced meals with fiber and protein, "
                    "and maintaining a healthy body weight can help keep blood sugar stable."
                )

        # HbA1c
        if "HbA1c" in name:
            if status in ("elevated", "high", "very_high"):
                detailed_points.append(
                    f"HbA1c ({value}{unit}) is above the typical non-diabetic range, "
                    "which can reflect higher average blood sugar over the past few months."
                )
                lifestyle_tips.append(
                    "It may be helpful to monitor carbohydrate intake, stay active most days "
                    "of the week, and discuss possible follow-up testing with a clinician."
                )

        # LDL
        if "LDL" in name:
            if status in ("high", "very_high"):
                detailed_points.append(
                    f"LDL cholesterol ({value} {unit}) is in a high range, which is often "
                    "associated with an increased cardiovascular risk over time."
                )
                lifestyle_tips.append(
                    "General recommendations often include reducing foods rich in saturated fat, "
                    "avoiding trans fats, and increasing sources of unsaturated fats such as "
                    "olive oil, nuts, and fish."
                )
            elif status in ("borderline_high", "elevated"):
                detailed_points.append(
                    f"LDL cholesterol ({value} {unit}) is borderline high."
                )
                lifestyle_tips.append(
                    "Paying attention to diet quality and regular exercise can support more "
                    "favorable cholesterol levels."
                )

        # HDL
        if "HDL" in name:
            if status == "low":
                detailed_points.append(
                    f"HDL cholesterol ({value} {unit}) is on the lower side. HDL is often "
                    "described as 'protective' cholesterol."
                )
                lifestyle_tips.append(
                    "Aerobic activity (such as brisk walking), avoiding smoking, and "
                    "choosing healthier fats may help support HDL levels."
                )

        # Triglycerides
        if "Triglycerides" in name:
            if status in ("high", "very_high"):
                detailed_points.append(
                    f"Triglycerides ({value} {unit}) are elevated, which can be linked to "
                    "diet, weight, and metabolic health."
                )
                lifestyle_tips.append(
                    "Limiting added sugars and alcohol, managing body weight, and increasing "
                    "physical activity are commonly suggested strategies."
                )

        # Total cholesterol
        if "Total Cholesterol" in name:
            if status in ("high", "very_high"):
                detailed_points.append(
                    f"Total cholesterol ({value} {unit}) is higher than the general "
                    "recommended range."
                )
                lifestyle_tips.append(
                    "A heart-friendly pattern often includes plenty of vegetables, fruits, "
                    "whole grains, and moderate portions of healthy fats."
                )

    # If we have no specific detailed points, add a generic one
    if not detailed_points:
        detailed_points.append(
            "No major individual abnormalities were highlighted based on the available values."
        )

    # Avoid repeating identical tips
    unique_tips = []
    for tip in lifestyle_tips:
        if tip not in unique_tips:
            unique_tips.append(tip)

    disclaimer = (
        "This explanation is for general educational purposes only and is not medical advice. "
        "Lab results should always be interpreted in the full context of your health history "
        "by a qualified healthcare professional."
    )

    return {
        "overall_risk": overall_risk,
        "general_overview": " ".join(general_overview_parts),
        "detailed_points": detailed_points,
        "lifestyle_tips": unique_tips,
        "disclaimer": disclaimer,
    }

@app.get("/")
def read_root():
    return {"message": "AI Personal Health Analyzer API is running"}


@app.post("/analyze-labs")
def analyze_labs_endpoint(labs: LabInput):
    labs_dict = labs.dict(exclude_none=True)

    result = analyze_labs(
        glucose=labs_dict.get("glucose"),
        hba1c=labs_dict.get("hba1c"),
        ldl=labs_dict.get("ldl"),
        hdl=labs_dict.get("hdl"),
        triglycerides=labs_dict.get("triglycerides"),
        total_cholesterol=labs_dict.get("total_cholesterol"),
    )

    return result


@app.post("/save-result")
def save_result(req: SaveRequest):
    """
    Analyze labs AND store the result in a simple JSON history file.
    Returns the saved entry including analysis.
    """

    labs_dict = req.dict(exclude_none=True, exclude={"label"})

    analysis = analyze_labs(
        glucose=labs_dict.get("glucose"),
        hba1c=labs_dict.get("hba1c"),
        ldl=labs_dict.get("ldl"),
        hdl=labs_dict.get("hdl"),
        triglycerides=labs_dict.get("triglycerides"),
        total_cholesterol=labs_dict.get("total_cholesterol"),
    )

    entry = {
        "id": str(uuid4()),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "label": req.label,
        "input": labs_dict,
        "analysis": analysis,
    }

    history = load_history()
    history.append(entry)
    save_history(history)

    return entry


@app.get("/history")
def get_history():
    """
    Returns the list of saved lab analyses (most recent first).
    """
    history = load_history()
    # sort by created_at descending
    history_sorted = sorted(
        history,
        key=lambda x: x.get("created_at", ""),
        reverse=True,
    )
    return history_sorted


@app.get("/generate-report")
def generate_report(
    glucose: Optional[float] = None,
    hba1c: Optional[float] = None,
    ldl: Optional[float] = None,
    hdl: Optional[float] = None,
    triglycerides: Optional[float] = None,
    total_cholesterol: Optional[float] = None,
):
    """
    Generates a simple PDF report based on the provided lab values.
    Example:
    /generate-report?glucose=132&hba1c=6.1&ldl=154&hdl=38&triglycerides=210&total_cholesterol=245
    """

    result = analyze_labs(
        glucose=glucose,
        hba1c=hba1c,
        ldl=ldl,
        hdl=hdl,
        triglycerides=triglycerides,
        total_cholesterol=total_cholesterol,
    )

    # Import reportlab lazily
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "AI Personal Health Analyzer - Report")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Overall risk: {result['overall_risk']}")
    y -= 20

    # Summary
    if "summary" in result:
        c.setFont("Helvetica", 10)
        summary = result["summary"]
        for line in wrap_text(summary, 90):
            c.drawString(50, y, line)
            y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Lab results:")
    y -= 20

    c.setFont("Helvetica", 10)
    for item in result["items"]:
        if y < 80:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        line1 = f"{item['name']}: {item['value']} {item['unit']} (status: {item['status']})"
        c.drawString(50, y, line1)
        y -= 14

        line2 = f"Reference: {item['reference_range']}"
        c.drawString(50, y, line2)
        y -= 14

        for msg_line in wrap_text(item["message"], 90):
            c.drawString(50, y, msg_line)
            y -= 14

        y -= 8

    c.showPage()
    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="health_report.pdf"'
        },
    )


def wrap_text(text: str, max_chars: int):
    """
    Simple helper to wrap text into lines of max length max_chars (by words).
    """
    words = text.split()
    lines = []
    current = []

    for w in words:
        tentative = " ".join(current + [w])
        if len(tentative) <= max_chars:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]

    if current:
        lines.append(" ".join(current))

    return lines

@app.post("/ai-summary")
def ai_summary_endpoint(labs: LabInput):
    """
    Build a pseudo-AI style explanation and general lifestyle guidance
    based on the lab values, using deterministic logic.
    """
    labs_dict = labs.dict(exclude_none=True)

    analysis = analyze_labs(
        glucose=labs_dict.get("glucose"),
        hba1c=labs_dict.get("hba1c"),
        ldl=labs_dict.get("ldl"),
        hdl=labs_dict.get("hdl"),
        triglycerides=labs_dict.get("triglycerides"),
        total_cholesterol=labs_dict.get("total_cholesterol"),
    )

    ai_summary = build_ai_like_summary(analysis)

    return {
        "analysis": analysis,
        "ai_summary": ai_summary,
    }
