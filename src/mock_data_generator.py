"""
Mock Data Generator for Enterprise Supply Chain & Operations.
Seeds realistic inventory, supplier, and unstructured incident log tables.
"""
from src.snowflake_engine import SnowflakeEngine

def seed_enterprise_database(engine: SnowflakeEngine):
    """Populates database tables with realistic supply chain scenarios."""
    # Clear existing data
    engine.execute("DELETE FROM INVENTORY_LEVELS;")
    engine.execute("DELETE FROM SUPPLIERS;")
    engine.execute("DELETE FROM OPERATIONAL_INCIDENT_LOGS;")
    engine.execute("DELETE FROM AUDIT_TRAIL;")

    # 1. Seed Inventory
    inventory_items = [
        ("SKU-9021", "Ultra-Core Microprocessor X7", "Semiconductors", "US-West Main Depot", 120.0, 45.0, 14, 8, 450.0, 380.0),
        ("SKU-8840", "High-Density Lithium Battery Cell B2", "Energy Storage", "EU-Central Hub", 450.0, 80.0, 10, 5, 210.0, 205.0),
        ("SKU-7712", "Precision Aluminum Alloy Frame A4", "Structural Components", "Asia-Pacific Warehouse", 1800.0, 60.0, 7, 0, 85.0, 85.0),
        ("SKU-6530", "Optic Sensor Array Pro-V", "Sensors", "US-East Distribution Center", 85.0, 25.0, 12, 9, 310.0, 290.0),
        ("SKU-5011", "Fiber Optic Connectivity Module", "Networking", "US-West Main Depot", 2200.0, 100.0, 5, 0, 45.0, 45.0)
    ]

    for item in inventory_items:
        engine.execute("""
        INSERT INTO INVENTORY_LEVELS 
        (item_id, item_name, category, warehouse_location, current_stock, daily_burn_rate, supplier_lead_time_days, expected_arrival_delay_days, unit_cost, historical_unit_cost)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, item)

    # 2. Seed Suppliers
    suppliers = [
        ("SUP-101", "Global Microchip Foundry Corp", 94.5, "Taiwan", "dispatch@globalmicrochip.com"),
        ("SUP-102", "VoltTech Energy Solutions", 88.0, "South Korea", "support@volttech.kr"),
        ("SUP-103", "AeroAlloy Heavy Industries", 97.2, "Germany", "orders@aeroalloy.de"),
        ("SUP-104", "Apex Photonics Ltd", 79.5, "Japan", "contact@apexphotonics.jp")
    ]

    for supplier in suppliers:
        engine.execute("""
        INSERT INTO SUPPLIERS (supplier_id, supplier_name, reliability_score, country, contact_email)
        VALUES (?, ?, ?, ?, ?);
        """, supplier)

    # 3. Seed Unstructured Operational Incident Logs
    logs = [
        ("INC-8042", "SKU-9021", "Logistics Dispatch Email", "2026-07-19T14:30:00Z", "HIGH",
         "Container vessel MV Horizon carrying SKU-9021 Microprocessor batch stranded near port due to severe Typhoon sea conditions. Port clearance delayed by 7 to 10 days."),
        
        ("INC-8043", "SKU-6530", "Customs Advisory Notice", "2026-07-19T16:45:00Z", "CRITICAL",
         "Customs Hold: Tariff classification audit initiated at LAX freight terminal for SKU-6530 Optic Sensor shipments. Clearance on hold pending updated compliance filing."),

        ("INC-8044", "SKU-8840", "Supplier Operational Update", "2026-07-18T09:15:00Z", "MEDIUM",
         "VoltTech lithium refining facility undergoing scheduled maintenance. Daily shipment throughput reduced by 20% for next 5 days.")
    ]

    for log in logs:
        engine.execute("""
        INSERT INTO OPERATIONAL_INCIDENT_LOGS (log_id, item_id, source, timestamp, severity, content)
        VALUES (?, ?, ?, ?, ?, ?);
        """, log)

    print(f"Successfully seeded enterprise tables: {len(inventory_items)} inventory items, {len(suppliers)} suppliers, {len(logs)} incident logs.")

if __name__ == "__main__":
    eng = SnowflakeEngine()
    seed_enterprise_database(eng)
    eng.close()
