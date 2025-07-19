import os
import sys
import typer
from rich.console import Console
from enum import Enum

# Add project root to sys.path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from cli.agents.requirement import RequirementAgent
from cli.core.config import Config
from cli.core.context_bundle import ContextBundle


class DocType(str, Enum):
    requirement = "requirement"
    design = "design"
    tasks = "tasks"


app = typer.Typer()
console = Console()


@app.command()
def requirement(
    context: str = typer.Option("", "--context", "-c", help="The user's instructions for the agent."),
    project_path: str = typer.Option(
        None, "--project-path", "-p", help="The root path of the project to analyze. Overrides PROJECT_PATH env var."
    ),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file."),
):
    """Generate a requirement.md document."""
    doc_type = DocType.requirement
    console.print(f"[bold green]Agent 0 – generating {doc_type.value}[/bold green]")
    console.print(f"Context: {context or '(none provided)'}")

    # Determine project path with priority: CLI arg > ENV var > default "."
    final_project_path = project_path or Config.PROJECT_PATH
    console.print(f"Using project path: {final_project_path}")

    agent = RequirementAgent(console=console)
    bundle = ContextBundle(user_instructions=context)
    result = agent.generate(bundle, project_path=final_project_path)

    if result:
        output_path = output or f"output/{doc_type.value}.md"
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result)

        console.print(f"\n[bold green]Output written to {output_path}[/bold green]")


@app.command()
def design(
    context: str = typer.Option("", "--context", "-c", help="The user's instructions for the agent."),
    project_path: str = typer.Option(
        None, "--project-path", "-p", help="The root path of the project to analyze. Overrides PROJECT_PATH env var."
    ),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file."),
):
    """Generate a design.md document. (Not implemented yet)"""
    console.print(f"[bold red]Agent for {DocType.design.value} not implemented yet.[/bold red]")
    raise typer.Exit()


@app.command()
def tasks(
    context: str = typer.Option("", "--context", "-c", help="The user's instructions for the agent."),
    project_path: str = typer.Option(
        None, "--project-path", "-p", help="The root path of the project to analyze. Overrides PROJECT_PATH env var."
    ),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file."),
):
    """Generate a tasks.md document. (Not implemented yet)"""
    console.print(f"[bold red]Agent for {DocType.tasks.value} not implemented yet.[/bold red]")
    raise typer.Exit()


if __name__ == "__main__":
    app()
