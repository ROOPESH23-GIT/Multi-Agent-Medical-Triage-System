#!/usr/bin/env python3
"""
🏥 Multi-Agent Medical Triage System - Live Emergency Room Simulation
Iterates through 4 emergency cases demonstrating agentic clinical prioritization.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.orchestrator import TriageOrchestrator

def print_banner():
    print("=" * 72)
    print(" 🏥 MULTI-AGENT MEDICAL TRIAGE SYSTEM - EMERGENCY DEPARTMENT SIMULATOR")
    print("=" * 72)
    print(" Agents: Intake Vitals + ESI Classifier + Differential Dx + Safety Guardian")
    print("-" * 72)

def main():
    print_banner()

    cases_file = os.path.join(os.path.dirname(__file__), "data", "sample_cases.json")
    with open(cases_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    orchestrator = TriageOrchestrator()

    for idx, case_data in enumerate(cases, 1):
        print(f"\n--- [PROCESSING CASE {idx}/{len(cases)}]: {case_data['case_id']} ---")
        time.sleep(0.4)

        result = orchestrator.triage_patient(case_data)

        print(f"👤 Patient: {result['patient_name']} ({result['age']}y {result['gender']})")
        print(f"📋 Chief Complaint: \"{result['complaint']}\" (Pain Scale: {result['pain_score']}/10)")
        v = result["vitals"]
        print(f"🩺 Vitals: BP: {v.get('blood_pressure_sys')}/{v.get('blood_pressure_dia')} | HR: {v.get('heart_rate')} bpm | SpO2: {v.get('spo2')}% | Temp: {v.get('temp_c')}°C")

        if result["vital_anomalies"]:
            print(f"  ⚠️  Vitals Warning: {', '.join(result['vital_anomalies'])}")

        # ESI
        esi = result["esi_assessment"]
        print(f"\n[Agent: ESITriage] Assigned: 🚨 {esi['tier']} (Wait Limit: {esi['urgency']})")
        print(f"  Reasoning: {esi['reasoning']}")

        # Differential Diagnosis
        print("\n[Agent: DifferentialDiagnosis] Top Diagnostic Suspicions:")
        for d in result["differential_diagnoses"][:2]:
            print(f"  • {d['condition']} — Confidence: {d['confidence_percentage']}%")

        # Safety & Bay Routing
        safety = result["safety_audit"]
        if safety["red_flags"]:
            for rf in safety["red_flags"]:
                print(f"  🚨 {rf}")

        print(f"\n[Agent: SafetyGuardian] Destination Bay:")
        print(f"  ➡️  {safety['destination_bay']}")
        print("-" * 72)

    print("\n✨ Emergency Department Triage simulation concluded successfully!\n")

if __name__ == "__main__":
    main()
