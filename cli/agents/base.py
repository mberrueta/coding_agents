# *   `from abc import ABC, abstractmethod`:
#    Used to define an abstract base class (`BaseAgent`) and abstract methods (`generate`).
#    This ensures that any class inheriting from `BaseAgent` must implement its
#    own `generate` method.
# *   `from jinja2 import Environment, FileSystemLoader`:
#     These are from the Jinja2 templating library.
#     They are used in the `_render_prompt` method to load a template file
#     from the filesystem and fill it with data.
# *   `from cli.core.context_bundle import ContextBundle`:
#     Imports a custom `ContextBundle` data class, which is used to pass structured context data
#     to the agent's methods.
# *   `from cli.core.llm import get_llm`:  Large Language Model (LLM) client,
#     which is then used by the agent.
# *   `from cli.retrievers.rag import search_in_rag`:
#     search over a local knowledge base using Retrieval-Augmented Generation (RAG).
# *   `from cli.retrievers.web import search_in_web`:
#     web search to gather external information.

from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader

from cli.core.context_bundle import ContextBundle
from cli.core.llm import get_llm
from cli.retrievers.rag import search_in_rag
from cli.retrievers.web import search_in_web


class BaseAgent(ABC):
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.llm = get_llm()

    def _render_prompt(self, context: ContextBundle) -> str:
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(self.template_path)
        return template.render(context.model_dump())

    def _search_in_web(self, query: str) -> str:
        return "\n".join([doc.page_content for doc in search_in_web(query)])

    def _search_in_rag(self, query: str) -> str:
        return "\n".join([doc.page_content for doc in search_in_rag(query)])

    @abstractmethod
    def generate(self, context: ContextBundle) -> str:
        pass
