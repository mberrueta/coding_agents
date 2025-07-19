from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle

class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__("templates/task/prompt.md.j2")

    def generate(self, context: ContextBundle) -> str:
        return "Dummy task content based on: " + context.user_instructions