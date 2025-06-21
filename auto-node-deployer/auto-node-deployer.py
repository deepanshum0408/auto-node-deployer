import argparse
import subprocess
import os
import sys
import yaml
import logging
from typing import Dict, Any
from utils.monitor import is_process_running
from rich.console import Console

console = Console()
VERSION = "1.0.0"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'nodes.yaml')

logging.basicConfig(
    filename='logs/deployer.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def load_config() -> Dict[str, Any]:
    """Load node configuration from YAML file."""
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)['nodes']

def deploy_node(node: str, config: Dict[str, Any]) -> None:
    """Deploy the specified node using its config."""
    node_cfg = config[node]
    console.print(f"[cyan]Deploying {node_cfg['display_name']} Node...[/cyan]")
    os.makedirs("logs", exist_ok=True)
    try:
        with open(node_cfg['log_file'], "w") as log_file:
            subprocess.Popen(
                node_cfg['start_command'].split(),
                stdout=log_file,
                stderr=subprocess.STDOUT
            )
        console.print(f"[green]Node started on port {node_cfg['port']}[/green]")
        logging.info(f"Started {node} node on port {node_cfg['port']}")
    except Exception as e:
        console.print(f"[bold red]Failed to start node: {e}[/bold red]")
        logging.error(f"Failed to start {node} node: {e}")

def check_status(node: str, config: Dict[str, Any]) -> None:
    """Check if the node process is running."""
    node_cfg = config[node]
    keyword = node_cfg['start_command'].split()[0]
    if is_process_running(keyword):
        console.print(f"[bold green]{node_cfg['display_name']} node is running![/bold green]")
    else:
        console.print(f"[bold red]{node_cfg['display_name']} node is NOT running![/bold red]")

def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(description="Auto Node Deployer")
    parser.add_argument('--node', choices=['shardeum', 'taiko'], required=False)
    parser.add_argument('--status', action='store_true', help="Check node status")
    parser.add_argument('--version', action='store_true', help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"Auto Node Deployer v{VERSION}")
        sys.exit(0)

    config = load_config()
    if not args.node:
        parser.print_help()
        sys.exit(1)

    if args.status:
        check_status(args.node, config)
    else:
        deploy_node(args.node, config)

if __name__ == "__main__":
    main() 