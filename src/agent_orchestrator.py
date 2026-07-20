"""
Agent Orchestrator for Enterprise Supply Chain & Operations.
Implements a stateful, multi-step agentic workflow orchestrating CoCo skills:
Skill 1 (data-anomaly-detector) -> Skill 2 (cortex-reasoner) -> Decision Branching -> Skill 3 (action-executor).
"""
import time
from typing import Dict, Any, List
from src.snowflake_engine import SnowflakeEngine
from src.skills_registry import SkillsRegistry
from skills.data_anomaly_detector.detector_rules import DataAnomalyDetector
from skills.cortex_reasoner.reasoner_prompts import CortexReasoner
from skills.action_executor.execution_handlers import ActionExecutor

class AgentOrchestrator:
    def __init__(self, engine: SnowflakeEngine = None, max_budget_usd: float = 50000.0):
        self.engine = engine or SnowflakeEngine()
        self.registry = SkillsRegistry()
        self.detector = DataAnomalyDetector(min_risk_threshold=50.0)
        self.reasoner = CortexReasoner(engine=self.engine)
        self.executor = ActionExecutor(max_auto_approve_budget=max_budget_usd, engine=self.engine)
        self.execution_logs = []

    def log_step(self, step_number: int, skill_name: str, description: str, data: Any):
        """Appends structured trace log for agent execution step."""
        log_entry = {
            "step": step_number,
            "skill": skill_name,
            "timestamp": time.strftime("%H:%M:%S"),
            "description": description,
            "data": data
        }
        self.execution_logs.append(log_entry)
        return log_entry

    def run_autonomous_workflow(self, target_sku: str = None) -> Dict[str, Any]:
        """
        Executes complete multi-step autonomous agent workflow.
        Returns final execution summary report.
        """
        self.execution_logs = []
        workflow_start_time = time.time()
        
        # STEP 1: Data Scanning & Anomaly Detection (Skill 1)
        self.log_step(1, "data-anomaly-detector", "Querying Snowflake warehouse for inventory anomalies", {"target_sku": target_sku or "ALL"})
        
        if target_sku:
            sql = "SELECT * FROM INVENTORY_LEVELS WHERE item_id = ?;"
            params = (target_sku,)
        else:
            sql = "SELECT * FROM INVENTORY_LEVELS;"
            params = ()
            
        inventory_rows = self.engine.query(sql, params)
        anomalies = self.detector.analyze_inventory_records(inventory_rows)
        
        if not anomalies:
            self.log_step(1, "data-anomaly-detector", "Scanning complete. No anomalies exceeding threshold.", {"anomalies_count": 0})
            return {
                "status": "COMPLETED_STABLE",
                "summary": "All inventory levels within safe operational margins.",
                "execution_trace": self.execution_logs
            }

        top_anomaly = anomalies[0]
        self.log_step(1, "data-anomaly-detector", f"Detected {len(anomalies)} anomalies. Selected top priority target.", top_anomaly)
        
        # STEP 2: Cortex Deep Reasoning & Unstructured Log Fusion (Skill 2)
        sku = top_anomaly["item_id"]
        self.log_step(2, "cortex-reasoner", f"Fetching unstructured incident logs for SKU '{sku}'", {"item_id": sku})
        
        incident_logs = self.engine.query(
            "SELECT * FROM OPERATIONAL_INCIDENT_LOGS WHERE item_id = ? OR item_id IS NULL ORDER BY timestamp DESC;",
            (sku,)
        )
        
        self.log_step(2, "cortex-reasoner", "Synthesizing multi-modal reasoning via Snowflake Cortex AI", {"logs_count": len(incident_logs)})
        reasoning_result = self.reasoner.reason_over_anomaly(top_anomaly, incident_logs)
        self.log_step(2, "cortex-reasoner", "Root Cause Analysis & Financial Risk Quantification completed", reasoning_result)
        
        # STEP 3: Decision Branching Engine (Risk & Authorization Evaluation)
        recommended_options = reasoning_result.get("mitigation_options", [])
        if not recommended_options:
            selected_option = {
                "option_id": 1,
                "title": f"Standard Buffer Procurement for {top_anomaly.get('item_name')}",
                "action_type": "PO_REALLOCATION",
                "cost_estimate_usd": 15000.0
            }
        else:
            # Pick first recommended option
            selected_option = next((opt for opt in recommended_options if opt.get("recommended")), recommended_options[0])

        decision_branch = "AUTONOMOUS_EXECUTION"
        cost = selected_option.get("cost_estimate_usd", 0.0)
        if cost > self.executor.max_auto_approve_budget:
            decision_branch = "HUMAN_ESCALATION_BRANCH"
            
        self.log_step(3, "decision-branching", f"Evaluated guardrail policies -> Decision Branch: {decision_branch}", {
            "selected_option": selected_option["title"],
            "cost_usd": cost,
            "max_autonomous_limit": self.executor.max_auto_approve_budget,
            "branch": decision_branch
        })
        
        # STEP 4: Contextual Action Execution & Audit Logging (Skill 3)
        self.log_step(4, "action-executor", "Executing transactional action and registering audit trail", selected_option)
        action_result = self.executor.execute_action(selected_option, top_anomaly)
        self.log_step(4, "action-executor", f"Action Result: {action_result['status']}", action_result)
        
        elapsed_seconds = round(time.time() - workflow_start_time, 3)

        return {
            "status": "WORKFLOW_COMPLETED",
            "execution_time_sec": elapsed_seconds,
            "target_item": top_anomaly["item_name"],
            "anomaly_severity": top_anomaly["severity"],
            "risk_score": top_anomaly["risk_score"],
            "root_cause": reasoning_result["root_cause"],
            "financial_impact": reasoning_result["financial_impact_estimate"],
            "decision_branch": decision_branch,
            "action_executed": action_result,
            "execution_trace": self.execution_logs
        }

if __name__ == "__main__":
    from src.mock_data_generator import seed_enterprise_database
    eng = SnowflakeEngine()
    seed_enterprise_database(eng)
    orchestrator = AgentOrchestrator(engine=eng)
    result = orchestrator.run_autonomous_workflow()
    print("\n--- WORKFLOW SUMMARY ---")
    print(f"Status: {result['status']}")
    print(f"Root Cause: {result['root_cause']}")
    print(f"Action Executed: {result['action_executed']['status']} ({result['action_executed']['details']['action_id']})")
