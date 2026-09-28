class PatientIntakeAgent:
    """
    Agent responsible for structured patient intake, parsing vitals,
    identifying physiological vital anomalies (Tachycardia, Hypoxia, Pyrexia, Hypotension).
    """
    def __init__(self):
        self.name = "PatientIntake"

    def process_patient(self, raw_data: dict) -> dict:
        vitals = raw_data.get("vitals", {})
        hr = vitals.get("heart_rate", 75)
        sbp = vitals.get("blood_pressure_sys", 120)
        dbp = vitals.get("blood_pressure_dia", 80)
        spo2 = vitals.get("spo2", 98)
        temp = vitals.get("temp_c", 37.0)

        anomalies = []
        if hr > 100:
            anomalies.append(f"Tachycardia ({hr} bpm)")
        elif hr < 50:
            anomalies.append(f"Bradycardia ({hr} bpm)")

        if spo2 < 92:
            anomalies.append(f"Severe Hypoxemia (SpO2 {spo2}%)")
        elif spo2 < 95:
            anomalies.append(f"Borderline Hypoxia (SpO2 {spo2}%)")

        if sbp >= 160 or dbp >= 100:
            anomalies.append(f"Hypertensive Crisis/Stage 2 ({sbp}/{dbp} mmHg)")
        elif sbp < 90:
            anomalies.append(f"Hypotension/Shock risk ({sbp}/{dbp} mmHg)")

        if temp >= 38.5:
            anomalies.append(f"High Fever ({temp}°C)")

        return {
            "case_id": raw_data.get("case_id", "UNKNOWN"),
            "patient_name": raw_data.get("patient_name", "Anonymous"),
            "age": raw_data.get("age", 30),
            "gender": raw_data.get("gender", "Unspecified"),
            "complaint": raw_data.get("chief_complaint", ""),
            "pain_score": raw_data.get("pain_score", 0),
            "vitals": vitals,
            "anomalies": anomalies,
            "history": raw_data.get("history", [])
        }
