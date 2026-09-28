class SafetyGuardianAgent:
    """
    Agent responsible for clinical safety guardrails, red-flag overrides,
    and routing patients to specific hospital bays (Trauma Bay, Acute Resuscitation, Fast Track).
    """
    def __init__(self):
        self.name = "SafetyGuardian"

    def review_and_route(self, intake: dict, esi: dict, diffs: list) -> dict:
        vitals = intake["vitals"]
        spo2 = vitals.get("spo2", 98)
        hr = vitals.get("heart_rate", 75)
        sbp = vitals.get("blood_pressure_sys", 120)

        red_flags = []
        override_triggered = False

        if spo2 < 90:
            red_flags.append("CRITICAL: Severe Hypoxia (SpO2 < 90%) - Risk of immediate arrest")
            override_triggered = True

        if hr > 130:
            red_flags.append("CRITICAL: Severe Supraventricular / Ventricular Tachycardia")
            override_triggered = True

        if sbp < 90:
            red_flags.append("CRITICAL: Hemodynamic Collapse / Septic or Cardiogenic Shock")
            override_triggered = True

        # Determine Bay Routing
        esi_level = esi["esi_level"]
        if override_triggered or esi_level == 1:
            destination_bay = "Resuscitation Trauma Bay 1 (Immediate Bed)"
            assigned_esi = min(esi_level, 2)
        elif esi_level == 2:
            destination_bay = "Emergency Acute Monitoring Bay (Continuous ECG & Pulse Ox)"
            assigned_esi = 2
        elif esi_level == 3:
            destination_bay = "Sub-Acute Assessment Area (Urgent Care Wing)"
            assigned_esi = 3
        elif esi_level == 4:
            destination_bay = "Minor Injuries & Procedure Room"
            assigned_esi = 4
        else:
            destination_bay = "Ambulatory Fast Track / Outpatient Waiting Lounge"
            assigned_esi = 5

        return {
            "destination_bay": destination_bay,
            "final_esi_level": assigned_esi,
            "red_flags": red_flags,
            "safety_override": override_triggered,
            "clinical_disclaimer": "Triaged by autonomous clinical support agent. Physical MD sign-off mandatory."
        }
