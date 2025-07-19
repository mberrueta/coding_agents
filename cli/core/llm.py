from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI

from cli.core.config import Config


"""Initializes and returns a language model client.

This function supports both Google Gemini and Ollama models.
It determines which client to use based on the model name.

Example:
>>> from cli.core.llm import get_llm
>>> llm = get_llm("gemini-pro")
>>> print(llm.invoke("Hello, world!"))
"""
def get_llm(model: str = Config.LLM_MODEL_NAME, temperature: float = 0.2) -> BaseChatModel:
    if "gemini" in model:
        return ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=Config.GEMINI_API_KEY)
    return ChatOllama(model=model, temperature=temperature)
