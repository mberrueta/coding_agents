from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle

class DesignAgent(BaseAgent):
    def __init__(self):
        super().__init__("templates/design/prompt.md.j2")

    def generate(self, context: ContextBundle) -> str:
        return "Dummy design content based on: " + context.user_instructions