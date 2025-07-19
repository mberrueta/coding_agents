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
    └── agents/
        ├── __init__.py
        └── requirement_agent.py
```
