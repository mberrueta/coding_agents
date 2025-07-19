from typing import List, Literal
from pydantic import BaseModel, Field

# the Agent’s Input Contract
class ContextBundle(BaseModel):
    # 1.  Mandatory: what is being built / changed
    user_prompt: str = Field(..., description="e.g. 'add OAuth2 login'")

    # 2.  Mandatory: where is the code
    codebase_root: str = Field(..., description="absolute path")

    # 3.  Optional: extra knowledge sources
    rag_chunks: List[str] = Field(default_factory=list)   # from local vector store
    web_snippets: List[str] = Field(default_factory=list) # from web search
    templates: List[str] = Field(default_factory=list)    # markdown templates to follow

    # 4.  Optional: previous outputs (for later agents)
    prev_requirements: str = ""
    prev_design: str = ""
