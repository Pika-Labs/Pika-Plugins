# Security policy

## Reporting a vulnerability

If you discover a security issue in the Pika Claude Code plugin (this repo), please email **support@pika.art** rather than opening a public issue or PR.

We aim to:
- Acknowledge within 2 business days
- Provide a fix or mitigation timeline within 7 days for high-severity issues
- Coordinate public disclosure once a fix is shipped

## What this repo's security boundary is

This repo ships **prose** (`skills/*/SKILL.md` files) and the **plugin manifest** (`.claude-plugin/`, `.mcp.json`). There is **no application code** here — no Python, TypeScript, or runtime hooks. All generation happens in:

- **Claude Code itself** (when a user invokes a `/pika:*` slash command)
- **`https://mcp.pika.me/api/mcp`** (the upstream MCP server — runtime issues there should be reported to **support@pika.art** with subject "MCP server: ...")
- **Per-user credentials** (OAuth tokens stored locally by Claude Code; or `MCP_AUTH_TOKEN` / `dk_*` developer keys set in the user's shell environment)

## What's in scope

Issues we want to know about:
- Plugin manifest issues (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.mcp.json`) that would cause unintended MCP server registration
- A SKILL.md prose payload that could be coerced into instructing the agent to call tools or exfiltrate data via adversarial user input

## What's out of scope (forwarded upstream)

- OAuth / token / identity issues → `pika-mcp-server`
- Provider-side issues → upstream provider
- Cost / quota issues → `pika-mcp-server` rate limiting and quotas
- Bugs in Claude Code itself → [`anthropics/claude-code` issues](https://github.com/anthropics/claude-code/issues)

## Cost confirmation

This plugin does **not** ship a client-side cost-confirmation gate. Spending is bounded by your Pika account credit balance and the upstream `pika-mcp-server`'s quota / rate limiting. There is no inline `--yes` / approval prompt to bypass.

Last updated: 2026-05-01.
