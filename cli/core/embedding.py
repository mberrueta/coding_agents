from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embedding_function(model_name: str) -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(model=model_name)
