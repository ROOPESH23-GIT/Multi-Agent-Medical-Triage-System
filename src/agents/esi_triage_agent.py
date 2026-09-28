class ESITriageAgent:
    """
    Agent responsible for categorizing patients into the Emergency Severity Index (ESI Levels 1-5).
    Evaluates:
      - Level 1: Immediate life-saving resuscitation needed
      - Level 2: High risk, severe distress, acute confusion
      - Level 3: Multiple hospital resources needed (labs, imaging, IV)
      - Level 4: One hospital resource needed (X-ray or suturing)
      - Level 5: No hospital resources needed (prescription refill, exam)
    """
    def __init__(self):
        self.name = "ESITriage"

    def evaluate_esi(self, intake_profile: dict) -> dict:
        vitals = intake_profile["vitals"]
        complaint = intake_profile["complaint"].lower()
        spo2 = vitals.get("spo2", 98)
        hr = vitals.get("heart_rate", 75)
        pain = intake_profile.get("pain_score", 0)

        # Rule 1: Immediate resuscitation required?
        if "cardiac arrest" in complaint or "unresponsive" in complaint or spo2 < 85:
            return {
                "esi_level": 1,
                "tier": "Level 1 - Resuscitation",
                "urgency": "IMMEDIATE (0 minutes)",
                "reasoning": "Critical failure of vital functions requiring immediate endotracheal or hemodynamic intervention."
            }

        # Rule 2: High risk situation, severe pain, or acute chest pain / severe respiratory distress?
        if ("chest pain" in complaint and ("radiat" in complaint or "sweat" in complaint)) or \
           ("shortness of breath" in complaint and spo2 < 90) or \
           pain >= 8 or hr > 120 or spo2 < 90:
            return {
                "esi_level": 2,
                "tier": "Level 2 - Emergent",
                "urgency": "WITHIN 10 MINUTES",
                "reasoning": "High-risk clinical presentation with potential ischemic or respiratory compromise. Immediate cardiac/respiratory bed needed."
            }

        # Rule 3: Requires multiple diagnostic resources? (Labs + imaging or IV)
        if "laceration" in complaint or "broken" in complaint or "fracture" in complaint:
            return {
                "esi_level": 4,
                "tier": "Level 4 - Less Urgent",
                "urgency": "WITHIN 60 MINUTES",
                "reasoning": "Single resource required (wound suturing or simple plain radiograph). Stable hemodynamics."
            }

        if "fever" in complaint or "abdominal pain" in complaint:
            return {
                "esi_level": 3,
                "tier": "Level 3 - Urgent",
                "urgency": "WITHIN 30-45 MINUTES",
                "reasoning": "Requires multiple hospital resources (Blood work + urinalysis / IV fluids). Vitals stable."
            }

        # Default: Level 5
        return {
            "esi_level": 5,
            "tier": "Level 5 - Non-Urgent",
            "urgency": "WITHIN 120 MINUTES",
            "reasoning": "Low acuity condition manageable in ambulatory fast-track or outpatient clinic."
        }
