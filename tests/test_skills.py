"""
Unit tests for CoCo Agent Skills.
"""
import pytest
from src.skills_registry import SkillsRegistry
from skills.data_anomaly_detector.detector_rules import DataAnomalyDetector
from skills.cortex_reasoner.reasoner_prompts import CortexReasoner
from skills.action_executor.execution_handlers import ActionExecutor

def test_skills_registry_loading():
    registry = SkillsRegistry()
    skills = registry.list_skills()
    skill_names = [s["name"] for s in skills]
    
    assert "data-anomaly-detector" in skill_names
    assert "cortex-reasoner" in skill_names
    assert "action-executor" in skill_names

def test_data_anomaly_detector():
    detector = DataAnomalyDetector(min_risk_threshold=50.0)
    sample_inventory = [
        {
            "item_id": "SKU-TEST-1",
            "item_name": "Test Microchip",
            "current_stock": 50,
            "daily_burn_rate": 20,
            "supplier_lead_time_days": 10,
            "expected_arrival_delay_days": 5,
            "unit_cost": 100,
            "historical_unit_cost": 100
        }
    ]
    anomalies = detector.analyze_inventory_records(sample_inventory)
    assert len(anomalies) == 1
    assert anomalies[0]["item_id"] == "SKU-TEST-1"
    assert anomalies[0]["risk_score"] >= 50.0

def test_cortex_reasoner():
    reasoner = CortexReasoner()
    anomaly = {
        "item_id": "SKU-TEST-1",
        "item_name": "Test Microchip",
        "days_inventory_remaining": 2.5,
        "daily_burn_rate": 20,
        "expected_arrival_delay_days": 5,
        "risk_score": 75.0,
        "severity": "WARNING"
    }
    incident_logs = [
        {"source": "Logistics Email", "content": "Port congestion near freight terminal."}
    ]
    res = reasoner.reason_over_anomaly(anomaly, incident_logs)
    assert res["status"] == "SUCCESS"
    assert "root_cause" in res
    assert len(res["mitigation_options"]) >= 1

def test_action_executor_policy_guardrails():
    executor = ActionExecutor(max_auto_approve_budget=50000.0)
    
    # Under limit
    auth_low = executor.validate_policy_guardrails(25000.0)
    assert auth_low["authorized"] is True
    assert auth_low["auth_code"] == "APPROVED_AUTO"

    # Over limit
    auth_high = executor.validate_policy_guardrails(75000.0)
    assert auth_high["authorized"] is False
    assert auth_high["auth_code"] == "REQUIRES_HUMAN_ESCALATION"
