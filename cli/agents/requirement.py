from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle

class RequirementAgent(BaseAgent):
    def __init__(self):
        super().__init__("templates/requirement/prompt.md.j2")

    def generate(self, context: ContextBundle) -> str:
        return "Dummy requirement content based on: " + context.user_instructions