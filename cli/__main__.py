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


from cli.agents.design import DesignAgent

@app.command()
def design(
    context: str = typer.Option("", "--context", "-c", help="Additional context for the agent."),
    project_path: str = typer.Option(
        None, "--project-path", "-p", help="The root path of the project to analyze. Overrides PROJECT_PATH env var."
    ),
    requirement_path: str = typer.Option(
        None, "--requirement-path", "-r", help="The path to the requirement.md file."
    ),
    output: str = typer.Option(None, "--output", "-o", help="The path to the output file."),
):
    """Generate a design.md document."""
    doc_type = DocType.design
    console.print(f"[bold green]Agent 1 – generating {doc_type.value}[/bold green]")

    final_project_path = project_path or Config.PROJECT_PATH
    console.print(f"Using project path: {final_project_path}")

    agent = DesignAgent(console=console)
    bundle = ContextBundle(user_instructions="", context=context) # user_instructions comes from the requirement file
    
    kwargs = {"project_path": final_project_path}
    if requirement_path:
        kwargs["requirement_path"] = requirement_path

    result = agent.generate(bundle, **kwargs)

    if result:
        output_path = output or f"output/{doc_type.value}.md"
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result)

        console.print(f"\n[bold green]Output written to {output_path}[/bold green]")


from cli.agents.task import TaskAgent

@app.command()
def tasks(
    context: str = typer.Option("", "--context", "-c", help="Additional context for the agent."),
    requirement_path: str = typer.Option(
        "output/requirement.md", "--requirement-path", "-r", help="The path to the requirement.md file."
    ),
    design_path: str = typer.Option(
        "output/design.md", "--design-path", "-d", help="The path to the design.md file."
    ),
    output_dir: str = typer.Option("output/tasks", "--output-dir", "-o", help="The directory to save the task files."),
):
    """Generate task files from requirement and design documents."""
    doc_type = DocType.tasks
    console.print(f"[bold green]Agent 2 – generating {doc_type.value}[/bold green]")

    agent = TaskAgent(console=console)
    bundle = ContextBundle(user_instructions="", context=context)

    kwargs = {
        "requirement_path": requirement_path,
        "design_path": design_path,
        "output_dir": output_dir,
    }

    result = agent.generate(bundle, **kwargs)
    console.print(f"\n[bold green]{result}[/bold green]")



if __name__ == "__main__":
    app()
