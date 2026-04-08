# Contributing

Thank you for your interest in contributing to sg-plugins!

## Plugins

Each plugin lives in `plugins/your-plugin-name/` and must contain:

```
your-plugin-name/
├── plugin.json          # Plugin manifest (required)
├── README.md            # Documentation (required)
├── skills/              # Skills (SKILL.md files)
│   └── your-skill/
│       └── SKILL.md
├── agents/              # Agent definitions (optional)
│   └── your-agent.md
└── commands/            # Slash commands (optional)
    └── your-command.md
```

### plugin.json

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Brief description",
  "author": {
    "name": "Your Name"
  },
  "license": "MIT",
  "skills": "./skills/"
}
```

## Standalone Skills

Skills that don't need a full plugin live in `skills/your-skill-name/`:

```
your-skill-name/
├── SKILL.md             # Skill definition with YAML frontmatter (required)
└── references/          # Supporting materials (optional)
    └── topic.md
```

### SKILL.md frontmatter

```yaml
---
name: your-skill-name
description: "Brief description of what the skill does and when to activate it"
allowed-tools: Read, Grep, Glob
---
```

## Guidelines

1. **One plugin per folder** in `plugins/`, one skill per folder in `skills/`
2. **Register plugins** in `.claude-plugin/marketplace.json`
3. **Include a README** for plugins; skills are self-documented via SKILL.md
4. **MIT license** for all contributions
5. **No secrets or API keys** in the repository
6. **English** for code and documentation (skill content may be in other languages)

## Submitting

1. Fork this repository
2. Create your plugin in `plugins/your-plugin-name/` or skill in `skills/your-skill-name/`
3. For plugins: add entry to `.claude-plugin/marketplace.json`
4. Submit a pull request

We review PRs for quality, security, and usefulness.
