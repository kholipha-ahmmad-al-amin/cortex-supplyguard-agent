"""
Main Entry Point for Snowflake CoCo CLI Enterprise Agent.
Usage:
  python main.py --demo    : Run non-interactive terminal execution demo
  python main.py --cli     : Launch interactive CoCo CLI prompt session
  python main.py --web     : Start live Web Dashboard visualizer server
  python main.py --test    : Run automated unit & integration test suite
"""
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from cli.coco_runner import CoCoCLIRunner
from web.server import start_web_server

def main():
    args = sys.argv[1:]
    
    if not args or "--demo" in args:
        runner = CoCoCLIRunner()
        runner.print_banner()
        runner.display_registered_skills()
        runner.execute_workflow()
    elif "--cli" in args:
        runner = CoCoCLIRunner()
        runner.run_interactive()
    elif "--web" in args:
        start_web_server(port=5000)
    elif "--test" in args:
        import pytest
        sys.exit(pytest.main(["tests"]))
    else:
        print("Unknown argument. Usage: python main.py [--demo | --cli | --web | --test]")

if __name__ == "__main__":
    main()
