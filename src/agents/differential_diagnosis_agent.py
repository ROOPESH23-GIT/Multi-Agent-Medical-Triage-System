class DifferentialDiagnosisAgent:
    """
    Agent responsible for generating probabilistic differential diagnosis candidates
    based on symptom cluster, vital anomalies, and patient medical history.
    """
    def __init__(self):
        self.name = "DifferentialDiagnosis"
        self.disease_profiles = [
            {
                "condition": "Acute Coronary Syndrome (Myocardial Infarction)",
                "keywords": ["chest pain", "radiat", "sweat", "jaw", "arm"],
                "vital_flags": ["tachycardia", "hypertensive"],
                "base_confidence": 0.85
            },
            {
                "condition": "Severe Acute Asthma Exacerbation",
                "keywords": ["wheez", "shortness of breath", "asthma", "sentence"],
                "vital_flags": ["severe hypoxemia", "tachycardia"],
                "base_confidence": 0.90
            },
            {
                "condition": "Viral Upper Respiratory Infection (URI)",
                "keywords": ["sore throat", "runny nose", "cough", "cold"],
                "vital_flags": [],
                "base_confidence": 0.75
            },
            {
                "condition": "Soft Tissue Traumatic Laceration",
                "keywords": ["laceration", "cut", "glass", "bleeding", "oozing"],
                "vital_flags": [],
                "base_confidence": 0.92
            }
        ]

    def evaluate_differential(self, intake_profile: dict) -> list:
        text = (intake_profile["complaint"] + " " + " ".join(intake_profile["history"])).lower()
        anomalies_str = " ".join(intake_profile["anomalies"]).lower()

        differentials = []
        for profile in self.disease_profiles:
            matches = sum(1 for kw in profile["keywords"] if kw in text)
            vital_matches = sum(1 for vf in profile["vital_flags"] if vf in anomalies_str)

            if matches > 0:
                confidence = profile["base_confidence"] * (matches / max(1, len(profile["keywords"])))
                if vital_matches > 0:
                    confidence = min(0.95, confidence + 0.15)
                differentials.append({
                    "condition": profile["condition"],
                    "confidence_percentage": int(confidence * 100),
                    "matched_indicators": matches + vital_matches
                })

        differentials.sort(key=lambda x: x["confidence_percentage"], reverse=True)
        return differentials if differentials else [{
            "condition": "Undifferentiated Acute Malaise",
            "confidence_percentage": 50,
            "matched_indicators": 1
        }]
