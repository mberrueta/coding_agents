from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document

from brixmis.config import Config
from brixmis.core.embedding import get_embedding_function


def search_in_rag(
    query: str,
    collection_name: str = "default",
    embedding_model_name: str = Config.EMBEDDING_MODEL_NAME,
) -> list[Document]:
    embedding_function = get_embedding_function(embedding_model_name)
    db = Chroma(persist_directory=Config.CHROMA_PATH, embedding_function=embedding_function)
    retriever = db.as_retriever()
    return retriever.invoke(query)
