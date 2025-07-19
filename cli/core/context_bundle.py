from dataclasses import dataclass

"""
# Here, file_context is not provided, so it defaults to None
bundle1 = ContextBundle(user_instructions="some instructions")
# bundle1.file_context is None

# Here, we provide a string for file_context
bundle2 = ContextBundle(user_instructions="some instructions", file_context="this is content from a file")
# bundle2.file_context is "this is content from a file"
"""

@dataclass
class ContextBundle:
    """
    A dataclass to hold the context that will be passed to the agents.
    """

    user_instructions: str
    context: str | None = None
    file_context: str | None = None
    web_context: str | None = None
    rag_context: str | None = None
