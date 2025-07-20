import os
import io
import re
import networkx as nx
from typing import Optional

from rich.console import Console

from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle
from cli.core.code_graph import build_graph


class DesignAgent(BaseAgent):
    def __init__(self, console: Optional[Console] = None):
        super().__init__("cli/templates/design/prompt.md.j2", console=console)

    def _get_project_name(self, mix_content: str) -> str:
        match = re.search(r"app: :(\w+)", mix_content)
        if match:
            return match.group(1)
        return "unknown_project"

    def _get_dependencies(self, mix_content: str) -> str:
        try:
            deps_section = mix_content.split("defp deps do", 1)[1].split("end", 1)[0]
            return deps_section.strip()
        except IndexError:
            return "Could not parse dependencies from mix.exs"

    def generate(self, context: ContextBundle, **kwargs) -> str:
        project_path = kwargs.get("project_path")
        requirement_path = kwargs.get("requirement_path", "./output/requirement.md")

        if not project_path:
            raise ValueError("project_path is required for DesignAgent")

        try:
            with open(requirement_path, 'r') as f:
                requirement_content = f.read()
        except FileNotFoundError:
            raise ValueError(f"Requirement file not found at {requirement_path}")

        mix_path = os.path.join(project_path, "mix.exs")
        mix_content = ""
        if os.path.exists(mix_path):
            with open(mix_path, 'r') as f:
                mix_content = f.read()

        project_name = self._get_project_name(mix_content)
        dependencies = self._get_dependencies(mix_content)

        with self.console.status("[bold green]Building code graph...[/bold green]"):
            code_graph = build_graph(project_path)
            graph_gml = io.BytesIO()
            nx.write_gml(code_graph, graph_gml)
            graph_gml_string = graph_gml.getvalue().decode('utf-8')

        context.project_name = project_name
        full_context = f"## Requirement\n\n{requirement_content}\n\n"
        full_context += f"## Project Name\n\n`{project_name}`\n\n"
        full_context += f"## Project Dependencies (from mix.exs)\n\n```elixir\n{dependencies}\n```\n\n"
        full_context += f"## Project Code Graph\n\n```gml\n{graph_gml_string}\n```"
        if context.context:
            full_context += f"\n\n## Additional Context from User\n\n{context.context}"

        context.context = full_context

        with self.console.status(
            "[bold green]Generating design document...[/bold green]"
        ):
            prompt = self._render_prompt(context)
            response = self.llm.invoke(prompt)

        self._log("Done.")
        return response.content
