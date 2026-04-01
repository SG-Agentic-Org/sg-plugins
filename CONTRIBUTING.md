# Contributing

Thank you for your interest in contributing to sg-plugins!

## Plugin Structure

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

## plugin.json

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

## Guidelines

1. **One plugin per folder** in `plugins/`
2. **Register your plugin** in `.claude-plugin/marketplace.json`
3. **Include a README** with usage examples
4. **MIT license** for all contributions
5. **No secrets or API keys** in the repository
6. **English** for code, comments, and documentation

## Submitting

1. Fork this repository
2. Create your plugin in `plugins/your-plugin-name/`
3. Add entry to `.claude-plugin/marketplace.json`
4. Submit a pull request

We review PRs for quality, security, and usefulness.
