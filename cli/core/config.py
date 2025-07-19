"""
Configuration management for the CLI application.

This module provides a centralized way to manage settings and configurations
for the application.
"""

import os


class Config:
    """
    A configuration class that loads settings from environment variables.

    This class dynamically retrieves all environment variables from the current
    environment and sets them as class attributes. This provides a flexible
    and centralized way to manage application settings without hardcoding them.

    If an environment variable is not set, the corresponding attribute will be
    None, so it's important to handle this case in the application logic,
    for example by providing a default value.
    """

    # Define default values for configurations that may not be set
    LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gemini-1.5-flash")
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    EMBEDDING_MODEL_NAME = os.environ.get(
        "EMBEDDING_MODEL_NAME", "text-embedding-004"
    )
    CHROMA_PATH = os.environ.get("CHROMA_PATH", ".chroma")
    SEARCH_ENGINE_NAME = os.environ.get("SEARCH_ENGINE_NAME", "google")
    SEARCH_ENGINE_API_KEY = os.environ.get("SEARCH_ENGINE_API_KEY")
    SEARCH_ENGINE_ID = os.environ.get("SEARCH_ENGINE_ID")

