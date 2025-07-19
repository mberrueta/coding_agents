from langchain_google_genai import ChatGoogleGenerativeAI

from brixmis.config import Config


def get_llm(model: str = Config.LLM_MODEL_NAME, temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=Config.GOOGLE_API_KEY)
