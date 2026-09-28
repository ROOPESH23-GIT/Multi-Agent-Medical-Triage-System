#!/usr/bin/env python3
"""
CLI entry point for Multi-Agent Medical Triage System.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.orchestrator import TriageOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Medical Triage CLI")
    parser.add_argument("--case-index", type=int, default=0, help="Index of case in sample_cases.json (0-3)")
    parser.add_argument("--cases-file", type=str, default="data/sample_cases.json", help="Path to cases JSON file")
    args = parser.parse_args()

    if not os.path.exists(args.cases_file):
        print(f"Error: Cases file not found at {args.cases_file}")
        sys.exit(1)

    with open(args.cases_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    if args.case_index < 0 or args.case_index >= len(cases):
        print(f"Error: case-index must be between 0 and {len(cases)-1}")
        sys.exit(1)

    case_data = cases[args.case_index]
    orchestrator = TriageOrchestrator()
    res = orchestrator.triage_patient(case_data)

    print("\n" + "=" * 60)
    print(f"TRIAGE SUMMARY - {res['case_id']}: {res['patient_name']}")
    print("=" * 60)
    print(f"ESI Level: {res['esi_assessment']['tier']}")
    print(f"Assigned Bay: {res['safety_audit']['destination_bay']}")
    print(f"Primary Differential: {res['differential_diagnoses'][0]['condition']} ({res['differential_diagnoses'][0]['confidence_percentage']}%)")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
