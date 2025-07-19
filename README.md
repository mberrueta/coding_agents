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
# Generate requirements for adding OAuth2 login
uv run cli requirement -c "Add OAuth2 login"

# Generate requirements and save to a custom file
uv run cli requirement -c "Add OAuth2 login" -o my_requirements.md

# To provide project context, use the --project-path argument (-p)
# or set the PROJECT_PATH environment variable. The CLI argument takes precedence.
#
# Example analyzing a specific project path:
uv run cli requirement \
  -c "Add a new dashboard to view monthly reports" \
  -p "/mnt/data4/matt/code/doctor_smart/doctor_smart"
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
