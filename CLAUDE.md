# CLAUDE.md — sg-plugins

## 1. About
Public open-source plugins and skills for Claude Code, Gemini CLI, and Codex.

## 2. Stack
- Format: Claude Code Plugin System (plugin.json + SKILL.md + agents/*.md)
- Language: English for docs and code; skill content may be in other languages
- Hosting: GitHub (SG-Agentic-Org/sg-plugins, public)
- License: MIT

## 3. Structure
- `plugins/` — full plugins (plugin.json + skills/agents/commands)
- `skills/` — standalone skills (SKILL.md + optional references/)

## 4. Rules
- English for README, CONTRIBUTING, docs
- Skill content may be in the language of its target audience
- No proprietary business context
- No API keys or secrets
- Each plugin registered in `.claude-plugin/marketplace.json`
- README.md required for each plugin; SKILL.md required for each skill
