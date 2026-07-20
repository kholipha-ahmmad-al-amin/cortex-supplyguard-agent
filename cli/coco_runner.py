"""
Snowflake CoCo CLI Runner & Terminal Interface.
Simulates Snowflake Cortex Code CLI (`coco run`) with step-by-step reasoning traces, ANSI tables, and interactive query mode.
"""
import os
import sys
import time

# Reconfigure stdout/stderr encoding for UTF-8 compatibility on Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure project root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

from src.snowflake_engine import SnowflakeEngine
from src.mock_data_generator import seed_enterprise_database
from src.agent_orchestrator import AgentOrchestrator
from src.skills_registry import SkillsRegistry

console = Console()

class CoCoCLIRunner:
    def __init__(self, budget_usd: float = 50000.0):
        self.engine = SnowflakeEngine()
        seed_enterprise_database(self.engine)
        self.orchestrator = AgentOrchestrator(engine=self.engine, max_budget_usd=budget_usd)
        self.registry = SkillsRegistry()

    def print_banner(self):
        banner_text = """
 [bold cyan]================================================================================[/bold cyan]
 [bold white]  SNOWFLAKE CoCo CLI [/bold white]| [bold green]Enterprise Autonomous SupplyGuard Agent[/bold green]
 [bold cyan]================================================================================[/bold cyan]
 [dim]  Powered by Snowflake Cortex AI Data Cloud & Multi-Step Agent Skills[/dim]
"""
        console.print(banner_text)

    def display_registered_skills(self):
        """Displays table of available CoCo Agent Skills."""
        table = Table(title="[bold yellow]Registered CoCo Agent Skills[/bold yellow]", header_style="bold magenta", border_style="cyan")
        table.add_column("Skill Name", style="bold green", width=24)
        table.add_column("Category", style="cyan", width=22)
        table.add_column("Description", style="white")
        table.add_column("Version", style="dim", width=8)

        for skill in self.registry.list_skills():
            table.add_row(
                skill["name"],
                skill["category"],
                skill["description"],
                skill["version"]
            )
        console.print(table)
        console.print()

    def execute_workflow(self, target_sku: str = None):
        """Executes multi-step workflow with rich visual feedback."""
        console.print(Panel(f"[bold yellow]Executing Autonomous Workflow[/bold yellow] | Target: [bold white]{target_sku or 'ALL INVENTORY'}[/bold white]", border_style="yellow"))

        with Progress(
            SpinnerColumn(spinner_name="dots"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console
        ) as progress:

            t1 = progress.add_task("[bold cyan]Step 1: Data Anomaly Scanning...", total=100)
            time.sleep(0.3)
            progress.update(t1, completed=100)

            t2 = progress.add_task("[bold magenta]Step 2: Cortex LLM Multi-Modal Reasoning...", total=100)
            time.sleep(0.4)
            progress.update(t2, completed=100)

            t3 = progress.add_task("[bold yellow]Step 3: Policy Authorization Guardrails...", total=100)
            time.sleep(0.3)
            progress.update(t3, completed=100)

            t4 = progress.add_task("[bold green]Step 4: Contextual Transaction Execution...", total=100)
            time.sleep(0.3)
            progress.update(t4, completed=100)

        summary = self.orchestrator.run_autonomous_workflow(target_sku=target_sku)
        
        console.print()
        console.print("[bold green][OK] Workflow Execution Completed Successfully![/bold green]")
        console.print()

        trace_table = Table(title="[bold cyan]Agent Execution Trace Log[/bold cyan]", border_style="blue")
        trace_table.add_column("Step", style="bold yellow", width=6)
        trace_table.add_column("CoCo Skill", style="bold green", width=22)
        trace_table.add_column("Action Description", style="white")
        trace_table.add_column("Time", style="dim", width=10)

        for log in summary["execution_trace"]:
            trace_table.add_row(
                f"#{log['step']}",
                log["skill"],
                log["description"],
                log["timestamp"]
            )
        console.print(trace_table)
        console.print()

        summary_markdown = f"""
[bold white]Target Component:[/bold white] [green]{summary['target_item']}[/green]
[bold white]Anomaly Severity:[/bold white] [bold red]{summary['anomaly_severity']}[/bold red] (Risk Score: [bold yellow]{summary['risk_score']}/100[/bold yellow])
[bold white]Synthesized Root Cause:[/bold white] {summary['root_cause']}
[bold white]Financial Risk Quantified:[/bold white] [bold gold1]{summary['financial_impact']}[/bold gold1]
[bold white]Decision Branch:[/bold white] [bold cyan]{summary['decision_branch']}[/bold cyan]
[bold white]Executed Action Status:[/bold white] [bold green]{summary['action_executed']['status']}[/bold green] (Ref ID: [bold white]{summary['action_executed']['details']['action_id']}[/bold white])
[bold white]PO Issued:[/bold white] [bold white]{summary['action_executed']['details']['po_number']}[/bold white] | Cost: [bold green]${summary['action_executed']['details']['cost_usd']:,.2f}[/bold green]
"""
        console.print(Panel(summary_markdown, title="[bold yellow]Cortex Agent Resolution Summary[/bold yellow]", border_style="green"))

    def run_interactive(self):
        """Runs interactive CLI prompt session."""
        self.print_banner()
        self.display_registered_skills()

        while True:
            console.print("[bold cyan]coco>[/bold cyan] Enter command ([bold green]run[/bold green], [bold green]skills[/bold green], [bold green]inventory[/bold green], [bold green]audit[/bold green], [bold red]exit[/bold red]): ", end="")
            cmd = input().strip().lower()

            if cmd in ["exit", "quit", "q"]:
                console.print("[yellow]Exiting CoCo CLI Agent. Goodbye![/yellow]")
                break
            elif cmd == "skills":
                self.display_registered_skills()
            elif cmd == "inventory":
                rows = self.engine.query("SELECT item_id, item_name, current_stock, daily_burn_rate, supplier_lead_time_days, expected_arrival_delay_days, unit_cost FROM INVENTORY_LEVELS;")
                table = Table(title="[bold yellow]Snowflake Warehouse Inventory[/bold yellow]", border_style="cyan")
                table.add_column("SKU", style="green")
                table.add_column("Name", style="white")
                table.add_column("Stock", style="yellow")
                table.add_column("Daily Burn", style="magenta")
                table.add_column("Lead Time", style="blue")
                table.add_column("Delay", style="red")
                table.add_column("Cost", style="cyan")

                for r in rows:
                    table.add_row(r["item_id"], r["item_name"], str(r["current_stock"]), str(r["daily_burn_rate"]), f"{r['supplier_lead_time_days']}d", f"{r['expected_arrival_delay_days']}d", f"${r['unit_cost']}")
                console.print(table)
            elif cmd == "audit":
                rows = self.engine.query("SELECT * FROM AUDIT_TRAIL ORDER BY timestamp DESC;")
                table = Table(title="[bold yellow]Agent Action Audit Trail[/bold yellow]", border_style="magenta")
                table.add_column("Action ID", style="bold green")
                table.add_column("Timestamp", style="dim")
                table.add_column("PO #", style="white")
                table.add_column("SKU", style="yellow")
                table.add_column("Type", style="cyan")
                table.add_column("Cost", style="green")
                table.add_column("Auth", style="bold red")

                for r in rows:
                    table.add_row(r["action_id"], r["timestamp"][:19], r["po_number"], r["item_id"], r["action_type"], f"${r['cost_usd']:,.2f}", r["policy_authorization"])
                console.print(table)
            elif cmd.startswith("run"):
                parts = cmd.split()
                sku = parts[1] if len(parts) > 1 else None
                self.execute_workflow(target_sku=sku)
            else:
                console.print("[dim]Unknown command. Options: run, run <SKU-ID>, skills, inventory, audit, exit[/dim]")

if __name__ == "__main__":
    runner = CoCoCLIRunner()
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        runner.print_banner()
        runner.display_registered_skills()
        runner.execute_workflow()
    else:
        runner.run_interactive()
