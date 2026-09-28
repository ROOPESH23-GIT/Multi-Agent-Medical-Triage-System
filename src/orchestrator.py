from .agents.intake_agent import PatientIntakeAgent
from .agents.esi_triage_agent import ESITriageAgent
from .agents.differential_diagnosis_agent import DifferentialDiagnosisAgent
from .agents.safety_guardian_agent import SafetyGuardianAgent

class TriageOrchestrator:
    """
    Central Coordinator managing emergency triage lifecycle:
    Intake -> ESI Classification -> Differential Diagnosis -> Safety Guardian Review.
    """
    def __init__(self):
        self.intake_agent = PatientIntakeAgent()
        self.esi_agent = ESITriageAgent()
        self.diff_agent = DifferentialDiagnosisAgent()
        self.safety_agent = SafetyGuardianAgent()

    def triage_patient(self, raw_patient_data: dict) -> dict:
        # Step 1: Normalize intake and evaluate vital signs
        intake_profile = self.intake_agent.process_patient(raw_data=raw_patient_data)

        # Step 2: Calculate Emergency Severity Index (ESI)
        esi_assessment = self.esi_agent.evaluate_esi(intake_profile)

        # Step 3: Compute candidate differential diagnoses
        differentials = self.diff_agent.evaluate_differential(intake_profile)

        # Step 4: Validate clinical safety guardrails and assign hospital bed
        safety_audit = self.safety_agent.review_and_route(intake_profile, esi_assessment, differentials)

        return {
            "case_id": intake_profile["case_id"],
            "patient_name": intake_profile["patient_name"],
            "age": intake_profile["age"],
            "gender": intake_profile["gender"],
            "complaint": intake_profile["complaint"],
            "pain_score": intake_profile["pain_score"],
            "vitals": intake_profile["vitals"],
            "vital_anomalies": intake_profile["anomalies"],
            "esi_assessment": esi_assessment,
            "differential_diagnoses": differentials,
            "safety_audit": safety_audit
        }
