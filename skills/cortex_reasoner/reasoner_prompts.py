"""
Cortex Deep Reasoner helper script.
Provides prompt synthesis and reasoning logic connecting structured anomalies with unstructured logs.
"""
import json
from typing import Dict, Any, List

class CortexReasoner:
    def __init__(self, engine=None):
        self.engine = engine

    def construct_cortex_prompt(self, anomaly: Dict[str, Any], incident_logs: List[Dict[str, Any]]) -> str:
        logs_text = ""
        for i, log in enumerate(incident_logs, 1):
            logs_text += f"\nIncident {i} [{log.get('source', 'System')} | {log.get('timestamp', '')}]:\n{log.get('content', '')}\n"
            
        if not logs_text:
            logs_text = "No direct unstructured log entries found for this SKU."

        prompt = f"""
You are Snowflake Cortex AI Supply Chain Analyst. Perform deep reasoning on the following enterprise anomaly and incident logs.

--- STRUCTURED ANOMALY METRICS ---
Item ID: {anomaly.get('item_id')}
Item Name: {anomaly.get('item_name')}
Category: {anomaly.get('category')}
Warehouse Location: {anomaly.get('warehouse_location')}
Current Stock: {anomaly.get('current_stock')} units
Daily Consumption: {anomaly.get('daily_burn_rate')} units/day
Days Inventory Remaining: {anomaly.get('days_inventory_remaining')} days
Supplier Lead Time: {anomaly.get('supplier_lead_time_days')} days
Expected Shipping Delay: {anomaly.get('expected_arrival_delay_days')} days
Risk Score: {anomaly.get('risk_score')}/100 ({anomaly.get('severity')})

--- UNSTRUCTURED OPERATIONAL INCIDENT LOGS ---
{logs_text}
"""
        return prompt

    def reason_over_anomaly(self, anomaly: Dict[str, Any], incident_logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        item_name = anomaly.get("item_name", "Component")
        days_rem = anomaly.get("days_inventory_remaining", 0)
        burn_rate = anomaly.get("daily_burn_rate", 10)
        delay = anomaly.get("expected_arrival_delay_days", 0)
        
        log_keywords = []
        for log in incident_logs:
            content = log.get("content", "").lower()
            if "port" in content or "ship" in content or "canal" in content or "vessel" in content:
                log_keywords.append("Typhoon Sea Conditions & Maritime Vessel Delay")
            if "shortage" in content or "foundry" in content or "silicon" in content:
                log_keywords.append("Raw Material Shortage at Primary Supplier")
            if "customs" in content or "tariff" in content:
                log_keywords.append("LAX Tariff Classification Audit & Customs Hold")

        cause = " / ".join(log_keywords) if log_keywords else "Supplier Lead-Time Spike & Depleted Safety Buffer"
        
        shortage_days = max(1.0, delay - days_rem)
        estimated_loss = round(shortage_days * burn_rate * 850.0, 2)
        
        reallocation_cost = round(estimated_loss * 0.12, 2)
        emergency_po_cost = round(estimated_loss * 0.22, 2)

        result = {
            "status": "SUCCESS",
            "root_cause": f"Critical bottleneck: {cause}. Current stock depleted in {days_rem} days while shipment is delayed by {delay} days.",
            "financial_impact_estimate": f"${estimated_loss:,.2f} potential revenue loss due to assembly line shutdown.",
            "confidence_score": 0.94,
            "mitigation_options": [
                {
                    "option_id": 1,
                    "title": f"Air-Freight Reroute for {item_name}",
                    "action_type": "PO_REALLOCATION",
                    "cost_estimate_usd": reallocation_cost,
                    "eta_days": 2,
                    "recommended": True,
                    "rationale": f"Fastest mitigation; prevents ${estimated_loss:,.2f} loss for a cost of only ${reallocation_cost:,.2f}."
                },
                {
                    "option_id": 2,
                    "title": f"Emergency Spot-Market Purchase (Secondary Vendor)",
                    "action_type": "EMERGENCY_PO",
                    "cost_estimate_usd": emergency_po_cost,
                    "eta_days": 3,
                    "recommended": False,
                    "rationale": f"Secures stock locally, but has higher premium (${emergency_po_cost:,.2f})."
                }
            ]
        }
        return result
