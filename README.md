# sg-plugins

Open-source plugins and skills for AI coding assistants.

Works with **Claude Code**, **Gemini CLI**, and **Codex**.

## Installation

### Claude Code

Add this marketplace to your `~/.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "sg-plugins": {
      "source": {
        "source": "github",
        "repo": "SG-Agentic-Org/sg-plugins"
      },
      "autoUpdate": true
    }
  }
}
```

Then enable individual plugins:

```json
{
  "enabledPlugins": {
    "plugin-name@sg-plugins": true
  }
}
```

### Gemini CLI

See [docs/README.gemini.md](docs/README.gemini.md) for Gemini CLI integration.

### Codex

See [docs/README.codex.md](docs/README.codex.md) for OpenAI Codex integration.

## Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| *Coming soon* | — | — |

## Skills

Standalone skills that can be installed directly without a full plugin.

| Skill | Language | Description |
|-------|----------|-------------|
| [clear-writing](skills/clear-writing/) | RU | Business writing following Ilyakhov & Sarycheva methodology |
| [autonomous-loop-onboarding](skills/autonomous-loop-onboarding/) | EN | Interview-driven setup that turns any task manager + LLM host into a personalized autonomous task loop (queue → agent works → self-review → approve). Model-agnostic core + adapters. |
| [mnemaos](skills/mnemaos/) | EN | Interview-driven setup that gives your AI a personal, local Markdown memory — a "vault" it reads at session start and writes back to at the end. Greenfield or adopt an existing folder (read-only audit → approval → backup → migration report). Model-agnostic core + adapters. Full docs: [docs/mnemaos/](docs/mnemaos/). |

### Installing a skill

Copy the skill folder to your Claude Code skills directory:

```bash
cp -r skills/clear-writing ~/.claude/skills/clear-writing
```

Or clone and symlink:

```bash
git clone https://github.com/SG-Agentic-Org/sg-plugins.git
ln -s "$(pwd)/sg-plugins/skills/clear-writing" ~/.claude/skills/clear-writing
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting plugins and skills.

## License

MIT License. See [LICENSE](LICENSE) for details.
