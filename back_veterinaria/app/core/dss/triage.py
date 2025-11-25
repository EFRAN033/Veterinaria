from typing import Dict, Any, List

def calculate_shock_index(hr: int, sbp: int) -> float:
    """
    Calculates Shock Index (SI) = Heart Rate / Systolic Blood Pressure.
    Normal Dog: 0.6 - 0.9
    Shock: > 1.0
    """
    if not sbp or sbp == 0:
        return 0.0
    return round(hr / sbp, 2)

def assess_vitals(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes vital signs and returns a triage score and alerts.
    """
    alerts: List[str] = []
    score = 0
    
    hr = int(data.get('heart_rate', 0))
    sbp = int(data.get('systolic_bp', 0))
    temp = float(data.get('temperature', 0.0))
    rr = int(data.get('respiratory_rate', 0))
    crt = float(data.get('capillary_refill', 0.0))
    
    si = 0.0
    if hr > 0 and sbp > 0:
        si = calculate_shock_index(hr, sbp)
        if si > 1.0:
            alerts.append(f"🔴 CRITICAL: Shock Index {si} (>1.0). Potential Hypovolemic Shock.")
            score += 3
        elif si > 0.9:
            alerts.append(f"🟡 WARNING: Shock Index {si} (0.9-1.0). Monitor closely.")
            score += 1
            
    if temp > 0:
        if temp > 39.5:
            alerts.append(f"🔴 CRITICAL: Hyperthermia ({temp}°C).")
            score += 2
        elif temp > 39.0:
            alerts.append(f"🟡 WARNING: Pyrexia ({temp}°C).")
            score += 1
        elif temp < 37.0:
            alerts.append(f"🔴 CRITICAL: Hypothermia ({temp}°C).")
            score += 2
            
    if rr > 0:
        if rr > 60:
            alerts.append(f"🔴 CRITICAL: Severe Tachypnea ({rr} bpm).")
            score += 2
        elif rr > 40:
            alerts.append(f"🟡 WARNING: Tachypnea ({rr} bpm).")
            score += 1
            
    if crt > 0:
        if crt >= 3.0:
            alerts.append(f"🔴 CRITICAL: CRT {crt}s (Poor Perfusion).")
            score += 3
        elif crt > 2.0:
            alerts.append(f"🟡 WARNING: CRT {crt}s (Delayed).")
            score += 1

    triage_level = "GREEN"
    if score >= 4:
        triage_level = "RED (Immediate Resuscitation)"
    elif score >= 2:
        triage_level = "YELLOW (Urgent)"
    
    return {
        "triage_score": score,
        "triage_level": triage_level,
        "alerts": alerts,
        "calculated_metrics": {
            "shock_index": si
        }
    }
