from langchain_core.documents import Document as LangchainDocument


class Document(LangchainDocument):
    """A document with a score."""

    score: float
