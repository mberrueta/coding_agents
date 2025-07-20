import os
import io
import networkx as nx
from typing import Optional

from rich.console import Console

from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle
from cli.core.code_graph import build_graph


class DesignAgent(BaseAgent):
    def __init__(self, console: Optional[Console] = None):
        super().__init__("cli/templates/design/prompt.md.j2", console=console)

    def generate(self, context: ContextBundle, **kwargs) -> str:
        project_path = kwargs.get("project_path")
        if not project_path:
            raise ValueError("project_path is required for DesignAgent")

        with self.console.status("[bold green]Building code graph...[/bold green]"):
            code_graph = build_graph(project_path)
            graph_gml = io.BytesIO()
            nx.write_gml(code_graph, graph_gml)
            graph_gml_string = graph_gml.getvalue().decode('utf-8')

        full_context = f"## Project Code Graph\n\n```gml\n{graph_gml_string}\n```"
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
