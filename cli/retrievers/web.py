from brixmis.config import Config
from brixmis.retrievers.document import Document
from brixmis.retrievers.web import WebRetriever


def search_in_web(query: str) -> list[Document]:
    web_retriever = WebRetriever(
        search_engine_name=Config.SEARCH_ENGINE_NAME,
        search_engine_api_key=Config.SEARCH_ENGINE_API_KEY,
        search_engine_id=Config.SEARCH_ENGINE_ID,
    )
    return web_retriever.search(query=query)
