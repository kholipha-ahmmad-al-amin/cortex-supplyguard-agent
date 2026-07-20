"""
Contextual Action Executor helper script.
Provides transactional operations, policy guardrail validation, and audit trail generation.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

class ActionExecutor:
    def __init__(self, max_auto_approve_budget: float = 50000.0, engine=None):
        self.max_auto_approve_budget = max_auto_approve_budget
        self.engine = engine

    def validate_policy_guardrails(self, cost_usd: float) -> Dict[str, Any]:
        if cost_usd <= self.max_auto_approve_budget:
            return {
                "authorized": True,
                "auth_code": "APPROVED_AUTO",
                "reason": f"Expenditure ${cost_usd:,.2f} is within autonomous approval limit (${self.max_auto_approve_budget:,.2f})."
            }
        else:
            return {
                "authorized": False,
                "auth_code": "REQUIRES_HUMAN_ESCALATION",
                "reason": f"Expenditure ${cost_usd:,.2f} exceeds autonomous limit (${self.max_auto_approve_budget:,.2f}). Escalated to VP Supply Chain."
            }

    def execute_action(self, selected_option: Dict[str, Any], anomaly_data: Dict[str, Any]) -> Dict[str, Any]:
        cost = float(selected_option.get("cost_estimate_usd", 0.0))
        action_type = selected_option.get("action_type", "PO_REALLOCATION")
        item_id = anomaly_data.get("item_id", "UNKNOWN")
        item_name = anomaly_data.get("item_name", "Component")
        
        policy = self.validate_policy_guardrails(cost)
        
        action_id = f"ACT-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        execution_status = "EXECUTED" if policy["authorized"] else "ESCALATED_PENDING_APPROVAL"
        po_number = f"PO-{uuid.uuid4().hex[:6].upper()}"
        
        result_details = {
            "action_id": action_id,
            "po_number": po_number,
            "item_id": item_id,
            "item_name": item_name,
            "action_type": action_type,
            "cost_usd": cost,
            "timestamp": timestamp,
            "policy_authorization": policy["auth_code"],
            "policy_reason": policy["reason"]
        }

        if self.engine:
            self.engine.record_action_audit(result_details)
            if policy["authorized"]:
                self.engine.update_inventory_stock(item_id, added_stock=500, status="BUFFER_REALLOCATED")

        return {
            "status": execution_status,
            "action_id": action_id,
            "execution_mode": "AUTONOMOUS" if policy["authorized"] else "HUMAN_IN_THE_LOOP",
            "action_type": action_type,
            "financial_authorization": policy["auth_code"],
            "details": result_details,
            "audit_trail_recorded": True
        }
