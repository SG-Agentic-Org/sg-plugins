# sg-plugins for Codex

## Overview

Plugins in this marketplace use SKILL.md files — plain markdown with YAML frontmatter.
Codex can read these files directly as context via AGENTS.md references.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/SG-Agentic-Org/sg-plugins.git
   ```

2. Reference skills in your AGENTS.md or project configuration.

3. Skills are located at: `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`

## Compatibility

| Feature | Compatible | Notes |
|---------|-----------|-------|
| Skills (SKILL.md) | Yes | Plain markdown, universally readable |
| Agents (.md) | Partial | May reference Claude-specific tools |
| Commands | No | Claude Code specific |
| Hooks | No | Claude Code specific |

## Usage

Add to your AGENTS.md or pass as context:

```
Follow the instructions in plugins/<plugin>/skills/<skill>/SKILL.md
```
