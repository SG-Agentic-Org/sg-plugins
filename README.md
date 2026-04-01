# sg-plugins

Open-source plugin marketplace for AI coding assistants.

Plugins work with **Claude Code**, **Gemini CLI**, and **Codex**.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting plugins.

## License

MIT License. See [LICENSE](LICENSE) for details.
