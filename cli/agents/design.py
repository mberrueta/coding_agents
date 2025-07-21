import os
import io
import re
import json
import glob
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

    def _find_and_read_package_json(self, project_path: str) -> str:
        # Search for package.json in the project path recursively
        package_json_paths = glob.glob(os.path.join(project_path, '**', 'package.json'), recursive=True)
        
        # Exclude node_modules
        package_json_paths = [p for p in package_json_paths if 'node_modules' not in p]

        if not package_json_paths:
            return "Could not find package.json."

        # Prioritize assets/package.json, then root, then first found
        package_json_path = None
        assets_path = os.path.join(project_path, "assets", "package.json")
        root_path = os.path.join(project_path, "package.json")

        if assets_path in package_json_paths:
            package_json_path = assets_path
        elif root_path in package_json_paths:
            package_json_path = root_path
        else:
            package_json_path = package_json_paths[0]

        if package_json_path and os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                try:
                    package_data = json.load(f)
                    deps = package_data.get("dependencies", {})
                    dev_deps = package_data.get("devDependencies", {})
                    all_js_deps = {**deps, **dev_deps}
                    if all_js_deps:
                        return json.dumps(all_js_deps, indent=2)
                    else:
                        return "No dependencies found in package.json."
                except json.JSONDecodeError:
                    return f"Error parsing {package_json_path}."
        
        return "Could not find package.json."

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
        js_dependencies = self._find_and_read_package_json(project_path)

        with self.console.status("[bold green]Building code graph...[/bold green]"):
            code_graph = build_graph(project_path)
            graph_gml = io.BytesIO()
            nx.write_gml(code_graph, graph_gml)
            graph_gml_string = graph_gml.getvalue().decode('utf-8')

        context.project_name = project_name
        full_context = f"## Requirement\n\n{requirement_content}\n\n"
        full_context += f"## Project Name\n\n`{project_name}`\n\n"
        full_context += f"## Project Dependencies (from mix.exs)\n\n```elixir\n{dependencies}\n```\n\n"
        full_context += f"## Project JS Dependencies (from package.json)\n\n```json\n{js_dependencies}\n```\n\n"
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
