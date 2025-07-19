from cli.agents.base import BaseAgent
from cli.core.context_bundle import ContextBundle

class RequirementAgent(BaseAgent):
    def __init__(self):
        super().__init__("cli/templates/requirement/prompt.md.j2")

    def generate(self, context: ContextBundle) -> str:
        prompt = self._render_prompt(context)
        response = self.llm.invoke(prompt)
        return response.content
