---
name: data-anomaly-detector
description: Autonomous structured data scanning skill that evaluates inventory levels, lead times, cost variances, and safety stock buffer depletion.
version: 1.0.0
author: Cortex-SupplyGuard Team
category: Supply Chain Analytics
tags: [anomaly-detection, inventory, forecasting, risk-scoring]
---

# Data Anomaly Detector Skill (`data-anomaly-detector`)

## Overview
The **Data Anomaly Detector** skill acts as the first line of defense in the enterprise supply chain agentic pipeline. It queries enterprise database tables (e.g. `INVENTORY_LEVELS`, `PURCHASE_ORDERS`, `SUPPLIER_METRICS`) to compute anomaly risk scores based on statistical deviations and operational rules.

## Capabilities
- **Stockout Window Calculation**: Identifies items where `Current Stock / Daily Consumption < Reorder Lead Time + Safety Buffer (7 Days)`.
- **Lead-Time Delay Anomaly**: Detects supplier shipments delayed past expected ETA by > 3 days.
- **Price Volatility Detection**: Identifies unit cost increases exceeding baseline by > 15%.
- **Risk Prioritization**: Assigns a unified Risk Score (0–100) and Severity Level (`CRITICAL`, `WARNING`, `STABLE`).
