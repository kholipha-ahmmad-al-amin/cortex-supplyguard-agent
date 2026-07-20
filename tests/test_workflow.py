"""
Integration tests for End-to-End Agent Workflow Orchestration.
"""
import pytest
from src.snowflake_engine import SnowflakeEngine
from src.mock_data_generator import seed_enterprise_database
from src.agent_orchestrator import AgentOrchestrator

@pytest.fixture
def enterprise_env():
    engine = SnowflakeEngine(db_path=":memory:")
    seed_enterprise_database(engine)
    return engine

def test_end_to_end_autonomous_workflow(enterprise_env):
    orchestrator = AgentOrchestrator(engine=enterprise_env, max_budget_usd=50000.0)
    summary = orchestrator.run_autonomous_workflow()
    
    assert summary["status"] == "WORKFLOW_COMPLETED"
    assert summary["decision_branch"] in ["AUTONOMOUS_EXECUTION", "HUMAN_ESCALATION_BRANCH"]
    assert summary["action_executed"]["audit_trail_recorded"] is True

    # Verify Audit Trail recorded in Snowflake DB
    audit_rows = enterprise_env.query("SELECT * FROM AUDIT_TRAIL;")
    assert len(audit_rows) >= 1

def test_high_severity_human_escalation_branch(enterprise_env):
    # Set max budget low to trigger human escalation policy branch
    orchestrator = AgentOrchestrator(engine=enterprise_env, max_budget_usd=100.0)
    summary = orchestrator.run_autonomous_workflow()
    
    assert summary["status"] == "WORKFLOW_COMPLETED"
    assert summary["decision_branch"] == "HUMAN_ESCALATION_BRANCH"
    assert summary["action_executed"]["financial_authorization"] == "REQUIRES_HUMAN_ESCALATION"
