import os
from dataclasses import asdict
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from prompt_toolkit import prompt as prompt_toolkit_prompt

from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle


class RequirementAgent(BaseAgent):
    def __init__(self, console: Optional[Console] = None):
        super().__init__("cli/templates/requirement/prompt.md.j2", console=console)
        self.clarification_template_path = (
            "cli/templates/requirement/clarification_prompt.md.j2"
        )

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

    def _get_clarifying_questions(
        self, user_instructions: str, project_context: str
    ) -> str | None:
        """Asks the LLM if it has questions, returns them or None."""
        clarification_bundle = ContextBundle(
            user_instructions=user_instructions, context=project_context
        )
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(self.clarification_template_path)
        prompt = template.render(asdict(clarification_bundle))

        with self.console.status(
            "[bold green]Checking for necessary clarifications...[/bold green]"
        ):
            llm_questions = self.llm.invoke(prompt).content.strip()

        if "NO_QUESTIONS" in llm_questions or not llm_questions:
            return None
        return llm_questions

    def generate(self, context: ContextBundle, **kwargs) -> str:
        project_path = kwargs.get("project_path")
        if not project_path:
            raise ValueError("project_path is required for RequirementAgent")

        with self.console.status("[bold green]Gathering project context...[/bold green]"):
            project_context = self._gather_project_context(project_path)

        questions = self._get_clarifying_questions(
            context.user_instructions, project_context
        )

        clarification_conversation = ""
        if questions:
            self.console.print(
                "\n[bold yellow]The AI has some clarifying questions for you:[/bold yellow]"
            )
            self.console.print(questions)
            self.console.print(
                "[dim]You can use SHIFT+ENTER for multiline input. Press ESC then ENTER to submit.[/dim]"
            )
            self.console.print("\n[bold yellow]Your answers[/bold yellow]")
            # Rich's Prompt.ask doesn't support multiline. We use prompt_toolkit directly,
            # which is a dependency of rich for advanced prompt features.
            # The user is instructed to press ESC -> Enter to submit.
            answers = prompt_toolkit_prompt(multiline=True)
            clarification_conversation = (
                f"\n\n### AI's Questions\n{questions}\n\n### User's Answers\n{answers}"
            )

        full_context = f"## Project Context\n\n{project_context}"
        if context.context:
            full_context += f"\n\n## Additional Context from User\n\n{context.context}"

        if clarification_conversation:
            full_context += f"\n\n## Clarification Round\n{clarification_conversation}"

        context.context = full_context

        with self.console.status(
            "[bold green]Generating requirement document...[/bold green]"
        ):
            prompt = self._render_prompt(context)
            response = self.llm.invoke(prompt)

        self._log("Done.")
        return response.content
