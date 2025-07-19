import os
from typing import Optional

from rich.console import Console

from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle


class RequirementAgent(BaseAgent):
    def __init__(self, console: Optional[Console] = None):
        super().__init__("cli/templates/requirement/prompt.md.j2", console=console)

    def _gather_project_context(self, project_path: str) -> str:
        """Gathers context from a hardcoded set of files for a Phoenix project."""
        context_parts = []

        # File structure
        self._log("Analyzing project file structure...")
        context_parts.append("### Project file structure (up to 3 levels deep)")
        tree_output = self._run_command(["tree", "-L", "3"], cwd=project_path)
        context_parts.append(f"```\n{tree_output}\n```")

        # mix.exs for dependencies
        mix_path = os.path.join(project_path, "mix.exs")
        if os.path.exists(mix_path):
            self._log("Reading mix.exs...")
            context_parts.append("\n### mix.exs (Dependencies and project info)")
            mix_content = self._read_file(mix_path)
            context_parts.append(f"```elixir\n{mix_content}\n```")

        # Find router.ex
        self._log("Searching for router file...")
        router_path = None
        lib_dir = os.path.join(project_path, "lib")
        if os.path.isdir(lib_dir):
            for root, _, files in os.walk(lib_dir):
                if "router.ex" in files:
                    router_path = os.path.join(root, "router.ex")
                    break
        if router_path:
            self._log(f"Reading router file at {router_path}...")
            context_parts.append("\n### Router (lib/.../router.ex)")
            router_content = self._read_file(router_path)
            context_parts.append(f"```elixir\n{router_content}\n```")

        # config/config.exs
        config_path = os.path.join(project_path, "config", "config.exs")
        if os.path.exists(config_path):
            self._log("Reading main configuration file...")
            context_parts.append("\n### Main Configuration (config/config.exs)")
            config_content = self._read_file(config_path)
            context_parts.append(f"```elixir\n{config_content}\n```")

        return "\n".join(context_parts)

    def generate(self, context: ContextBundle, project_path: str) -> str:
        self._log("Gathering project context...")
        project_context = self._gather_project_context(project_path)

        full_context = f"## Project Context\n\n{project_context}"
        if context.context:
            full_context += f"\n\n## Additional Context from User\n\n{context.context}"

        context.context = full_context

        self._log("Generating requirement document...")
        prompt = self._render_prompt(context)
        response = self.llm.invoke(prompt)
        self._log("Done.")
        return response.content
