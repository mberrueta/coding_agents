# Coding Agents

Sequential AI agents that create:
1. requirement.md
2. design.md
3. tasks.md

## Scaffolding

``` sh
uv init
```


## Quick start

```bash
uv run cli generate requirement.md -c "Add OAuth2 login"
```

## Structure

``` sh
coding_agents/              ← root of the repo
├── pyproject.toml          ← uv project file + deps
└── cli/
    ├── __init__.py
    ├── __main__.py
    ├── agents/
    │   ├── base.py           # ABC Agent
    │   ├── requirement.py    # RequirementAgent(BaseAgent)
    │   ├── design.py
    │   └── task.py
    ├── retrievers/
    │   ├── rag.py            # FAISS / Chroma
    │   └── web.py            # SerpAPI or Tavily
    ├── templates/
    │   ├── requirement/*.md.j2
    │   ├── design/*.md.j2
    │   └── task/*.md.j2
    └── core/
        ├── context_bundle.py # pydantic model above
        └── llm.py            # Gemini / Ollama init

```

## Testing

```bash
uv run pytest
```
