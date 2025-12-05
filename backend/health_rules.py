# health_rules.py
"""
Basic medical rules for interpreting common blood test results.

This file does NOT use AI.
It only applies fixed medical reference ranges and simple if/else logic.

Goal:
- For each lab marker, return:
  - status: "low" / "normal" / "elevated" / "high" / etc.
  - reference_range: human-readable normal range
  - message: short explanation in English

Later we will plug this into:
- a FastAPI backend
- a React frontend
- optional AI summarization
"""

from typing import Dict, Any, Optional


# -----------------------------
# 1. Reference ranges (simplified)
# -----------------------------

GLUCOSE_RANGE = {
    "low": 70,          # < 70 mg/dL = hypoglycemia
    "normal_max": 99,   # 70–99 = normal fasting glucose
    "prediabetes_max": 125,  # 100–125 = impaired fasting glucose
    # >= 126 = diabetes (fasting)
}

HBA1C_RANGE = {
    "normal_max": 5.6,       # < 5.7% = normal
    "prediabetes_max": 6.4,  # 5.7–6.4% = prediabetes
    # >= 6.5% = diabetes
}

LDL_RANGE = {
    "optimal_max": 100,
    "near_optimal_max": 129,
    "borderline_high_max": 159,
    "high_max": 189,
    # >= 190 = very high
}

HDL_RANGE = {
    # Simplified: in reality depends on sex, etc.
    "low_max": 40,    # < 40 mg/dL = low HDL
    # >= 40 mg/dL = acceptable / protective
}

TRIGLYCERIDES_RANGE = {
    "normal_max": 149,
    "borderline_high_max": 199,
    "high_max": 499,
    # >= 500 = very high
}

TOTAL_CHOLESTEROL_RANGE = {
    "desirable_max": 199,
    "borderline_high_max": 239,
    # >= 240 = high total cholesterol
}


# ---------------------------------
# 2. Helper functions for each marker
# ---------------------------------

def analyze_glucose(value: float) -> Dict[str, Any]:
    """
    Analyze fasting glucose (mg/dL).
    Returns a dict with status, reference range, and explanation.
    """
    if value < GLUCOSE_RANGE["low"]:
        status = "low"
        message = (
            "Fasting glucose is low (possible hypoglycemia). "
            "If there are symptoms like dizziness or confusion, medical evaluation is recommended."
        )
    elif GLUCOSE_RANGE["low"] <= value <= GLUCOSE_RANGE["normal_max"]:
        status = "normal"
        message = "Fasting glucose is within the normal range."
    elif GLUCOSE_RANGE["normal_max"] < value <= GLUCOSE_RANGE["prediabetes_max"]:
        status = "elevated"
        message = (
            "Fasting glucose is elevated (prediabetic range). "
            "Lifestyle changes and follow-up testing are usually recommended."
        )
    else:
        status = "high"
        message = (
            "Fasting glucose is high (range compatible with possible diabetes). "
            "Medical evaluation is strongly recommended."
        )

    return {
        "name": "Fasting Glucose",
        "value": value,
        "unit": "mg/dL",
        "status": status,
        "reference_range": "70–99 mg/dL (fasting)",
        "message": message,
    }


def analyze_hba1c(value: float) -> Dict[str, Any]:
    """
    Analyze HbA1c (%).
    HbA1c reflects average blood glucose over the last ~3 months.
    """
    if value <= HBA1C_RANGE["normal_max"]:
        status = "normal"
        message = "HbA1c is within the normal range."
    elif HBA1C_RANGE["normal_max"] < value <= HBA1C_RANGE["prediabetes_max"]:
        status = "elevated"
        message = (
            "HbA1c is in the prediabetes range. "
            "This suggests an increased risk of developing diabetes."
        )
    else:
        status = "high"
        message = (
            "HbA1c is high (range compatible with diabetes). "
            "Medical evaluation and management are recommended."
        )

    return {
        "name": "HbA1c",
        "value": value,
        "unit": "%",
        "status": status,
        "reference_range": "< 5.7%",
        "message": message,
    }


def analyze_ldl(value: float) -> Dict[str, Any]:
    """
    Analyze LDL cholesterol (mg/dL).
    Often called 'bad' cholesterol.
    """
    if value < LDL_RANGE["optimal_max"]:
        status = "optimal"
        message = "LDL is in the optimal range."
    elif value <= LDL_RANGE["near_optimal_max"]:
        status = "near_optimal"
        message = "LDL is near optimal but could be improved."
    elif value <= LDL_RANGE["borderline_high_max"]:
        status = "borderline_high"
        message = (
            "LDL is borderline high. Lifestyle changes and monitoring are usually recommended."
        )
    elif value <= LDL_RANGE["high_max"]:
        status = "high"
        message = (
            "LDL is high. This is associated with increased cardiovascular risk. "
            "Medical evaluation is recommended."
        )
    else:
        status = "very_high"
        message = (
            "LDL is very high. This is associated with a high risk of cardiovascular disease. "
            "Prompt medical evaluation is important."
        )

    return {
        "name": "LDL Cholesterol",
        "value": value,
        "unit": "mg/dL",
        "status": status,
        "reference_range": "< 100 mg/dL (optimal)",
        "message": message,
    }


def analyze_hdl(value: float) -> Dict[str, Any]:
    """
    Analyze HDL cholesterol (mg/dL).
    Often called 'good' cholesterol.
    """
    if value < HDL_RANGE["low_max"]:
        status = "low"
        message = (
            "HDL is low. This may reduce protection against cardiovascular disease."
        )
    else:
        status = "good"
        message = (
            "HDL is in an acceptable range and may be protective for cardiovascular health."
        )

    return {
        "name": "HDL Cholesterol",
        "value": value,
        "unit": "mg/dL",
        "status": status,
        "reference_range": "≥ 40 mg/dL (simplified general reference)",
        "message": message,
    }


def analyze_triglycerides(value: float) -> Dict[str, Any]:
    """
    Analyze triglycerides (mg/dL).
    """
    if value <= TRIGLYCERIDES_RANGE["normal_max"]:
        status = "normal"
        message = "Triglycerides are within the normal range."
    elif value <= TRIGLYCERIDES_RANGE["borderline_high_max"]:
        status = "borderline_high"
        message = "Triglycerides are borderline high. Diet and lifestyle changes are often recommended."
    elif value <= TRIGLYCERIDES_RANGE["high_max"]:
        status = "high"
        message = (
            "Triglycerides are high. This may increase cardiovascular risk."
        )
    else:
        status = "very_high"
        message = (
            "Triglycerides are very high. There is an increased risk of pancreatitis. "
            "Prompt medical evaluation is important."
        )

    return {
        "name": "Triglycerides",
        "value": value,
        "unit": "mg/dL",
        "status": status,
        "reference_range": "< 150 mg/dL",
        "message": message,
    }


def analyze_total_cholesterol(value: float) -> Dict[str, Any]:
    """
    Analyze total cholesterol (mg/dL).
    """
    if value <= TOTAL_CHOLESTEROL_RANGE["desirable_max"]:
        status = "desirable"
        message = "Total cholesterol is in the desirable range."
    elif value <= TOTAL_CHOLESTEROL_RANGE["borderline_high_max"]:
        status = "borderline_high"
        message = (
            "Total cholesterol is borderline high. "
            "Lifestyle changes and monitoring are often recommended."
        )
    else:
        status = "high"
        message = (
            "Total cholesterol is high and may increase cardiovascular risk."
        )

    return {
        "name": "Total Cholesterol",
        "value": value,
        "unit": "mg/dL",
        "status": status,
        "reference_range": "< 200 mg/dL",
        "message": message,
    }


# ---------------------------------
# 3. Central function: analyze multiple labs together
# ---------------------------------

def analyze_labs(
    glucose: Optional[float] = None,
    hba1c: Optional[float] = None,
    ldl: Optional[float] = None,
    hdl: Optional[float] = None,
    triglycerides: Optional[float] = None,
    total_cholesterol: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Accepts optional lab values and returns a combined interpretation.
    Each parameter can be None if that test is not available.
    """

    results = []

    if glucose is not None:
        results.append(analyze_glucose(glucose))

    if hba1c is not None:
        results.append(analyze_hba1c(hba1c))

    if ldl is not None:
        results.append(analyze_ldl(ldl))

    if hdl is not None:
        results.append(analyze_hdl(hdl))

    if triglycerides is not None:
        results.append(analyze_triglycerides(triglycerides))

    if total_cholesterol is not None:
        results.append(analyze_total_cholesterol(total_cholesterol))

    # Simple overall risk estimation
    overall_risk = "unknown"

    for r in results:
        if r["status"] in ("high", "very_high"):
            overall_risk = "high_risk"
            break
        elif r["status"] in ("borderline_high", "elevated", "near_optimal"):
            if overall_risk != "high_risk":
                overall_risk = "moderate_risk"

    # Build a simple human-readable summary (no AI, just logic)
    if not results:
        summary = "No lab values were provided, so no interpretation can be made."
    else:
        if overall_risk == "high_risk":
            summary = (
                "Some of your lab values are in a high or very high range. "
                "This may be associated with an increased health risk. "
                "You should discuss these results with a healthcare professional."
            )
        elif overall_risk == "moderate_risk":
            summary = (
                "Some of your lab values are slightly outside the optimal range. "
                "Lifestyle changes and periodic follow-up testing are usually recommended."
            )
        else:
            summary = (
                "All available lab values appear to be within acceptable ranges. "
                "Continuing healthy lifestyle habits and routine check-ups is still important."
            )

    return {
        "overall_risk": overall_risk,
        "summary": summary,
        "items": results,
    }



# ---------------------------------
# 4. Small demo for quick testing
# ---------------------------------

if __name__ == "__main__":
    demo = analyze_labs(
        glucose=132,
        hba1c=6.1,
        ldl=154,
        hdl=38,
        triglycerides=210,
        total_cholesterol=245,
    )
    from pprint import pprint
    pprint(demo, width=120)
