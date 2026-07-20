"""
Data Anomaly Detector helper script.
Provides statistical outlier detection and inventory vulnerability scoring logic.
"""
from typing import List, Dict, Any

class DataAnomalyDetector:
    def __init__(self, min_risk_threshold: float = 50.0):
        self.min_risk_threshold = min_risk_threshold

    def analyze_inventory_records(self, inventory_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculates risk score for each inventory record based on stock levels, burn rates, and lead times.
        """
        anomalies = []
        for row in inventory_rows:
            stock = float(row.get("current_stock", 0))
            burn_rate = float(row.get("daily_burn_rate", 1.0))
            lead_time = float(row.get("supplier_lead_time_days", 7))
            delay_days = float(row.get("expected_arrival_delay_days", 0))
            unit_cost = float(row.get("unit_cost", 100))
            historical_cost = float(row.get("historical_unit_cost", unit_cost))
            
            days_remaining = stock / max(burn_rate, 0.1)
            effective_lead_time = lead_time + delay_days
            
            # Risk Scoring Formula
            stockout_risk = max(0.0, min(100.0, (1.0 - (days_remaining / max(effective_lead_time, 1.0))) * 100.0))
            if days_remaining <= effective_lead_time:
                stockout_risk = max(stockout_risk, 85.0)
                
            delay_risk = max(0.0, min(100.0, (delay_days / 10.0) * 100.0))
            
            cost_increase_pct = max(0.0, ((unit_cost - historical_cost) / max(historical_cost, 1.0)) * 100.0)
            cost_risk = max(0.0, min(100.0, cost_increase_pct * 2.0))
            
            composite_score = round(0.50 * stockout_risk + 0.30 * delay_risk + 0.20 * cost_risk, 1)
            
            severity = "STABLE"
            if composite_score >= 80.0:
                severity = "CRITICAL"
            elif composite_score >= 55.0:
                severity = "WARNING"
                
            if composite_score >= self.min_risk_threshold:
                anomalies.append({
                    "item_id": row.get("item_id"),
                    "item_name": row.get("item_name"),
                    "category": row.get("category", "General"),
                    "warehouse_location": row.get("warehouse_location"),
                    "current_stock": stock,
                    "daily_burn_rate": burn_rate,
                    "days_inventory_remaining": round(days_remaining, 2),
                    "supplier_lead_time_days": lead_time,
                    "expected_arrival_delay_days": delay_days,
                    "unit_cost": unit_cost,
                    "risk_score": composite_score,
                    "severity": severity,
                    "metrics": {
                        "stockout_risk": round(stockout_risk, 1),
                        "delay_risk": round(delay_risk, 1),
                        "cost_risk": round(cost_risk, 1)
                    }
                })
                
        anomalies.sort(key=lambda x: x["risk_score"], reverse=True)
        return anomalies
