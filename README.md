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

### Requirement Agent
The first step is to generate a `requirement.md` file.

```bash
# Generate requirements for adding OAuth2 login
uv run cli requirement --context "Add OAuth2 login" --project-path "/path/to/your/project" > ./output/requirement.md
```

### Design Agent
Once you have a `requirement.md` file, you can run the `design` agent to generate a technical design.

```bash
# Generate a design document from the requirement
uv run cli design --project-path "/path/to/your/project"
```

### Task Agent
After the design is generated, you can create the specific development tasks.

```bash
# Generate tasks from the design
uv run cli tasks
```

This command will read `./output/requirement.md` and `./output/design.md` and create a set of `taskN.md` files in the `./output/tasks/` directory. You can specify different paths using the `--requirement-path`, `--design-path`, and `--output-dir` options.


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
