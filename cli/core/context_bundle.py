from dataclasses import dataclass


@dataclass
class ContextBundle:
    """
    A dataclass to hold the context that will be passed to the agents.
    """

    user_instructions: str
    file_context: str | None = None
    web_context: str | None = None
    rag_context: str | None = None