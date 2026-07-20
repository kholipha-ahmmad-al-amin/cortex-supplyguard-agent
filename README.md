# The Silicon Valley Engineering Manifesto: Cortex-SupplyGuard
### Autonomous Enterprise Resilience Infrastructure Powered by Snowflake CoCo CLI

**Engineering Team:** EquiSaaS BD  
**Founder & Systems Lead:** Kholipha Ahmmad Al-Amin (kholifaahmadalamin@gmail.com)  
**Hackathon Challenge:** Snowflake CoCo CLI Hackathon 2026 (Intelligent Workflow Automation Agents)  
**Public Repository:** https://github.com/kholipha-ahmmad-al-amin/cortex-supplyguard-agent  

---

## The Problem

Enterprise supply chains operate on paper-thin margins where unexpected lead-time spikes, maritime port delays, and supplier defaults cause catastrophic production halts. Traditional Enterprise Resource Planning (ERP) and Business Intelligence (BI) platforms are fundamentally passive: they log anomalies long after damage is done, forcing operational teams to manually inspect disparate tables, cross-reference email incident reports, and negotiate emergency procurement over days. 

This latency results in millions of dollars of unmitigated revenue leakage per incident, operational paralysis, and compliance risks. Modern enterprise data infrastructure requires cognitive autonomy rather than static reporting.

---

## The Solution

Cortex-SupplyGuard transforms passive enterprise data infrastructure into an autonomous cognitive operational loop. Built upon Snowflake CoCo CLI Agent Skills (`SKILL.md`), the architecture fuses real-time structured data scanning with multi-modal LLM reasoning using Snowflake Cortex AI (`SNOWFLAKE.CORTEX.COMPLETE`).

The system detects statistical inventory vulnerabilities, cross-references unstructured operational incident logs, quantifies monetary downtime risk, evaluates financial policy guardrails, and executes transactional mitigations autonomously.

### Core Engineering Capabilities
1. **Autonomous Anomaly Detection:** Continuous evaluation of warehouse burn rates, lead times, and safety stock buffer depletion.
2. **Multi-Modal Cortex Reasoning:** Unstructured text intelligence connecting raw metrics with logistics incident logs, shipping alerts, and supplier emails.
3. **Policy-Bounded Execution:** Strict financial guardrails enforcing automatic authorization for expenditures under $50,000 while routing higher-risk actions to human escalation queues.
4. **Immutable Audit Ledger:** Full cryptographic traceability recording every prompt, reasoning path, and issued purchase order.

---

## Live Demo & Tech Stack

Cortex-SupplyGuard is engineered for zero-cost deployment, allowing enterprises to run the full cognitive stack locally or in edge environments without incurring recurring server overhead.

### Tech Stack Breakdown
* **Agentic Framework:** Snowflake CoCo CLI (Cortex Code Agent Skills Architecture)
* **Cognitive AI Engine:** Snowflake Cortex AI (Snowflake Arctic LLM Completion Functions)
* **Database Layer:** Snowflake AI Data Cloud / High-Performance SQLite Enterprise Emulator
* **User Interface:** Rich Terminal CLI (ANSI Traces, Animated Progress Bars) & Glassmorphism Web App (HTML5, Vanilla CSS3, ES6 JavaScript, Flask)
* **Testing & Quality Assurance:** PyTest End-to-End Suite

---

## Local Setup & Run Instructions

Follow these copy-pasteable commands to set up and run the environment locally.

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/kholipha-ahmmad-al-amin/cortex-supplyguard-agent.git
cd cortex-supplyguard-agent
pip install -r requirements.txt
```

### 2. Run Terminal Execution Demo
Execute the full multi-step agent resolution loop in your terminal:
```bash
python main.py --demo
```
*(Or double-click `run_demo.bat` on Windows)*

### 3. Launch Web Dashboard Visualizer
Start the live interactive Web UI server:
```bash
python main.py --web
```
Open **http://127.0.0.1:5000** in your browser. *(Or double-click `run_web_dashboard.bat` on Windows)*

### 4. Interactive CoCo CLI Prompt Shell
Launch the interactive command line shell:
```bash
python main.py --cli
```
*(Or double-click `run_cli.bat` on Windows)*

### 5. Execute Automated Test Suite
Run unit and integration verification tests:
```bash
python main.py --test
```
*(Or double-click `run_tests.bat` on Windows)*

---

## System Documentation (Mermaid.js)

### 1. System Architecture Diagram
```mermaid
graph TD
    subgraph Data Layer
        A[Snowflake Warehouse: INVENTORY_LEVELS]
        B[Snowflake Warehouse: SUPPLIERS]
        C[Snowflake Warehouse: INCIDENT_LOGS]
    end

    subgraph CoCo Agent Skills Layer
        D["Skill 1: data-anomaly-detector"]
        E["Skill 2: cortex-reasoner"]
        F["Skill 3: action-executor"]
    end

    subgraph Decision Engine
        G{Expenditure Policy Check}
        H[Auto-Approve Branch]
        I[Human Escalation Branch]
    end

    subgraph Output & Audit
        J[Transaction PO Ledger]
        K[Terminal CLI Visualizer]
        L[Glassmorphism Web UI]
    end

    A --> D
    D -->|Structured Risk Score| E
    C -->|Unstructured Logs| E
    E -->|Mitigation Plan| G
    G -->|< $50,000 Budget| H
    G -->|>= $50,000 Budget| I
    H --> F
    I --> F
    F --> J
    J --> K
    J --> L
```

### 2. Entity-Relationship Diagram (ERD)
```mermaid
erDiagram
    INVENTORY_LEVELS {
        string item_id PK
        string item_name
        string category
        string warehouse_location
        float current_stock
        float daily_burn_rate
        int supplier_lead_time_days
        int expected_arrival_delay_days
        float unit_cost
        float historical_unit_cost
        string status
    }

    SUPPLIERS {
        string supplier_id PK
        string supplier_name
        float reliability_score
        string country
        string contact_email
    }

    OPERATIONAL_INCIDENT_LOGS {
        string log_id PK
        string item_id FK
        string source
        string timestamp
        string severity
        string content
    }

    AUDIT_TRAIL {
        string action_id PK
        string timestamp
        string po_number
        string item_id FK
        string item_name
        string action_type
        float cost_usd
        string policy_authorization
        string policy_reason
    }

    INVENTORY_LEVELS ||--o{ OPERATIONAL_INCIDENT_LOGS : "monitored_by"
    INVENTORY_LEVELS ||--o{ AUDIT_TRAIL : "triggers"
    SUPPLIERS ||--o{ INVENTORY_LEVELS : "supplies"
```

### 3. Data Flow Diagram (DFD)

#### DFD Level 0 (Context Diagram)
```mermaid
graph LR
    User([Operations Manager]) -->|Query / Trigger| AgentSystem[Cortex-SupplyGuard Agent System]
    DataCloud[(Snowflake AI Data Cloud)] <-->|Warehouse Tables & Cortex LLM| AgentSystem
    AgentSystem -->|Audit Logs & Purchase Orders| EnterpriseLedger[(Audit Ledger)]
    AgentSystem -->|Live Telemetry & Recommendations| User
```

#### DFD Level 1 (Process Decomposition)
```mermaid
graph LR
    Sub1[(Inventory DB)] --> P1[1.0 Anomaly Detection]
    P1 -->|Risk Vector| P2[2.0 Multi-Modal Cortex Reasoning]
    Sub2[(Incident Logs)] --> P2
    P2 -->|Mitigation Plan| P3[3.0 Policy Evaluation]
    P3 -->|Approved Plan| P4[4.0 Transaction Execution]
    P4 --> Sub3[(Audit Ledger)]
    P4 --> Sub4[(Updated Stock DB)]
```

### 4. Use Case Diagram
```mermaid
graph LR
    subgraph Users & Actors
        Manager([Supply Chain Manager])
        System([Autonomous CoCo Agent])
        CortexAI([Snowflake Cortex AI Engine])
    end

    subgraph System Boundary
        UC1(Scan Inventory Anomalies)
        UC2(Synthesize Incident Logs)
        UC3(Quantify Financial Risk)
        UC4(Evaluate Authorization Guardrails)
        UC5(Issue Emergency Purchase Order)
        UC6(View Live Execution Telemetry)
    end

    Manager --> UC1
    Manager --> UC6
    System --> UC1
    System --> UC2
    CortexAI --> UC2
    System --> UC3
    System --> UC4
    System --> UC5
```

### 5. Sequence Diagram (Core User Interaction Loop)
```mermaid
sequenceDiagram
    autonumber
    actor Manager as Operations Manager
    participant CLI as CoCo CLI / Web UI
    participant Orch as Agent Orchestrator
    participant S1 as Skill 1: Anomaly Detector
    participant S2 as Skill 2: Cortex Reasoner
    participant S3 as Skill 3: Action Executor
    participant DB as Snowflake Database

    Manager->>CLI: Execute Workflow (run)
    CLI->>Orch: Initiate Agentic Loop
    Orch->>S1: Analyze Inventory Records
    S1->>DB: Query INVENTORY_LEVELS Table
    DB-->>S1: Return Stock Metrics
    S1-->>Orch: Return Anomaly Vector (SKU-9021, Score: 75.3)

    Orch->>S2: Perform Multi-Modal Reasoning
    S2->>DB: Fetch OPERATIONAL_INCIDENT_LOGS
    DB-->>S2: Return Shipping Delay Log
    S2-->>Orch: Return Root Cause & Mitigation Options

    Orch->>S3: Validate Policy & Execute Action
    S3->>S3: Evaluate Expenditure Limit ($24,464 < $50,000 Limit)
    S3->>DB: Update Stock & Insert AUDIT_TRAIL Record
    DB-->>S3: Confirmation ACK
    S3-->>Orch: Action Executed (PO-F4D23D)

    Orch-->>CLI: Workflow Execution Complete
    CLI-->>Manager: Display Execution Trace & Summary
```

---

## Engineering Team & Contact

Developed by **EquiSaaS BD** for the Snowflake CoCo CLI Hackathon 2026.

* **Engineering Lead:** Kholipha Ahmmad Al-Amin
* **Email:** kholifaahmadalamin@gmail.com
* **GitHub Organization:** https://github.com/kholipha-ahmmad-al-amin
