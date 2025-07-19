import typer
from rich.console import Console
from enum import Enum


class DocType(str, Enum):
    requirement = "requirement"
    design = "design"
    tasks = "tasks"


app = typer.Typer()
console = Console()

# Example:
#
# ```py
# uv cli requirement -c "Add OAuth2 Login"
# ```
@app.command("generate")
def generate(doc_type: DocType, context: str = typer.Option("", "--context", "-c")):
    """Generate one of: requirement.md | design.md | tasks.md"""
    console.print(f"[bold green]Agent 0 – generating {doc_type.value}[/bold green]")
    console.print(f"Context: {context or '(none provided)'}")

if __name__ == "__main__":
    app()
