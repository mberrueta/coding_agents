import os
import re
from typing import Optional, List

from rich.console import Console

from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle


class TaskAgent(BaseAgent):
    def __init__(self, console: Optional[Console] = None):
        super().__init__("cli/templates/task/prompt.md.j2", console=console)

    def generate(self, context: ContextBundle, **kwargs) -> str:
        requirement_path = kwargs.get("requirement_path", "./output/requirement.md")
        design_path = kwargs.get("design_path", "./output/design.md")
        output_dir = kwargs.get("output_dir", "./output/tasks")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            with open(requirement_path, 'r') as f:
                requirement_content = f.read()
        except FileNotFoundError:
            raise ValueError(f"Requirement file not found at {requirement_path}")

        try:
            with open(design_path, 'r') as f:
                design_content = f.read()
        except FileNotFoundError:
            raise ValueError(f"Design file not found at {design_path}")

        full_context = f"## Requirement\n\n{requirement_content}\n\n"
        full_context += f"## Design\n\n{design_content}\n\n"
        if context.context:
            full_context += f"\n\n## Additional Context from User\n\n{context.context}"

        context.context = full_context

        with self.console.status(
            "[bold green]Generating tasks...[/bold green]"
        ):
            prompt = self._render_prompt(context)
            response = self.llm.invoke(prompt)

        self._save_tasks(response.content, output_dir)
        
        self._log(f"Tasks saved to {output_dir}")
        return f"Tasks saved to {output_dir}"

    def _save_tasks(self, content: str, output_dir: str) -> List[str]:
        tasks = re.split(r'---\[TASK\]---', content)
        task_files = []
        for i, task_content in enumerate(tasks):
            task_content = task_content.strip()
            if not task_content:
                continue

            task_filename = os.path.join(output_dir, f"task{i+1}.md")
            with open(task_filename, "w") as f:
                f.write(task_content)
            task_files.append(task_filename)
        
        return task_files
