from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_google_community import GoogleSearchAPIRetriever

from cli.retrievers.document import Document


class WebRetriever:
    def __init__(self, search_engine_name: str, **kwargs):
        self.search_engine_name = search_engine_name
        self.kwargs = kwargs

    def search(self, query: str) -> list[Document]:
        if self.search_engine_name == "tavily":
            retriever = TavilySearchAPIRetriever(**self.kwargs)
        elif self.search_engine_name == "google":
            retriever = GoogleSearchAPIRetriever(**self.kwargs)
        else:
            raise ValueError(f"Unknown search engine: {self.search_engine_name}")

        return retriever.invoke(query)
