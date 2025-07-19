from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_google_community.search import GoogleSearchAPIWrapper

from cli.retrievers.document import Document


class WebRetriever:
    def __init__(self, search_engine_name: str, **kwargs):
        self.search_engine_name = search_engine_name
        self.kwargs = kwargs

    def search(self, query: str) -> list[Document]:
        if self.search_engine_name == "tavily":
            retriever = TavilySearchAPIRetriever(**self.kwargs)
            return retriever.invoke(query)
        elif self.search_engine_name == "google":
            retriever = GoogleSearchAPIWrapper(**self.kwargs)
            return [Document(page_content=retriever.run(query))]
        else:
            raise ValueError(f"Unknown search engine: {self.search_engine_name}")

def search_in_web(query: str) -> list[Document]:
    retriever = WebRetriever(search_engine_name="google")
    return retriever.search(query)
