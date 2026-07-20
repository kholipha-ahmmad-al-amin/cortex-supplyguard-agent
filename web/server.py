"""
Flask Web Dashboard Server for Snowflake CoCo CLI Enterprise Agent.
Serves web visualizer and provides REST API endpoints for live workflow execution and telemetry.
"""
import os
import sys
from flask import Flask, jsonify, send_from_directory

# Ensure project root in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.snowflake_engine import SnowflakeEngine
from src.mock_data_generator import seed_enterprise_database
from src.agent_orchestrator import AgentOrchestrator

WEB_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")

# Use in-memory SQLite DB for serverless deployment compatibility
engine = SnowflakeEngine(db_path=":memory:")
seed_enterprise_database(engine)

@app.route("/")
def index():
    return send_from_directory(WEB_DIR, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(WEB_DIR, filename)

@app.route("/api/inventory")
def get_inventory():
    rows = engine.query("SELECT * FROM INVENTORY_LEVELS;")
    return jsonify(rows)

@app.route("/api/audit")
def get_audit():
    rows = engine.query("SELECT * FROM AUDIT_TRAIL ORDER BY timestamp DESC;")
    return jsonify(rows)

@app.route("/api/run-agent", methods=["POST"])
def run_agent():
    orchestrator = AgentOrchestrator(engine=engine)
    summary = orchestrator.run_autonomous_workflow()
    return jsonify(summary)

@app.route("/api/reset-data", methods=["POST"])
def reset_data():
    seed_enterprise_database(engine)
    return jsonify({"status": "SUCCESS", "message": "Enterprise database reset & re-seeded."})

def start_web_server(port: int = 5000):
    print(f"\n🚀 Enterprise CoCo Web Dashboard running live at http://127.0.0.1:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    start_web_server(port=port)
