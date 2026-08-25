# Xnurta MCP

Bring Xnurta's advertising capabilities into your own AI agent (Claude, ChatGPT, and more) and make your data part of your workflow — query data, run analyses, and calculate true profitability in plain language, combining your own costs, margins, and goals. After authorization, there is no need to repeatedly sign in to the platform, export spreadsheets, or switch between systems.

The current Xnurta MCP v1.2.0 supports data queries and creating, editing, and deleting AI managed groups, including hourly (AMS) data, managed-group schedules, automation-rule reads, and applying platform templates. Direct campaign management is not yet available.

---

## What v1.2.0 can do for you

- **Query your data in natural language** — ask "rank last week's campaigns by ACOS" or "show this product line's TACOS trend over the past 8 weeks" right inside your AI assistant. After authorization, there is no need to repeatedly sign in or export data.
- **Calculate true profitability with your own data** — hand your costs / margins / goals to the AI and let it pull ad spend: "based on real margins, which campaigns are losing money — cut or scale?" Questions that require combining ad data with your own business data are exactly what the platform alone can't answer.
- **Codify your own playbook** — save frequent questions as templates, or even schedule a weekly report routine that runs every Monday.
- **Manage AI managed groups** — create, edit, or delete managed groups after explicit confirmation, then read back the resulting state.

### What you can query and manage

| Category | Contents |
|----------|----------|
| **Performance / report data** | Impressions, clicks, spend, sales, ACOS, ROAS, CTR, CVR, CPC, and more; AI-managed metrics; business metrics such as total sales, TACOS, sessions, and Buy Box share |
| **Entity configuration / metadata** | Campaigns, ad groups, targets, advertised products, ASINs, managed groups, product lines |
| **Operation logs** | Human and AI action history, filterable by operator, action type, entity, and time window |
| **AI managed-group management** | Create, edit, and delete SP, SB, and SD managed groups; update supported optimization targets, budgets, campaign membership, and AI action-space settings |

---

## Supported AI assistants

Xnurta MCP works with any MCP-compatible AI assistant. Recommended and fully tested:

| AI assistant | Recommendation |
|--------------|----------------|
| **Claude Code** | ⭐ Recommended |
| **ChatGPT** | ⭐ Recommended |

Other MCP-compatible clients — Cursor, Cline, Claude Desktop, OpenClaw, Hermes, Cherry Studio, and more — work with the standard configuration in the [Installation Guide](docs/installation.md).

---

## Quick start (4 steps)

1. **Choose an authorization method and connect MCP** — Xnurta MCP supports both OAuth and MCP Token; choose based on client capabilities and usage requirements.
2. **Verify the connection** — call `get_user_authorized_context` and confirm the authorized store scope.
3. **Install Skills** — from this repo's [`skills/`](skills/) directory.
4. **Start querying** — ask in natural language.

### Plugin installation (Claude Code / Codex)

Add the marketplace, then install the plugin. Desktop app users should use the Plugins settings; command-line users can use the CLI commands. See [Plugin installation](#plugin-installation) below or **[Installation Guide · Option 2](docs/installation.md#option-2--plugin-installation)**.

### One-message setup (recommended)

In any client whose AI can configure things itself (Claude, ChatGPT Codex, Cherry Studio, etc.), send:

```text
Please read the following GitHub repository and follow its instructions to configure Xnurta MCP and install the Skills:
https://github.com/Xnurta/MCP

Xnurta MCP supports both OAuth and MCP Token authentication.
Please check which authorization methods the current client supports, briefly explain when each method is appropriate, and ask me to confirm which method to use before starting authorization.
If I choose OAuth, open the sign-in page when authorization is required so I can complete it.
When using OAuth, follow the MCP Authorization specification. Before sending any OAuth request, validate the discovered endpoints and all required fields; do not omit or guess protocol parameters.

After the configuration is complete, call get_user_authorized_context to verify the connection.
```

<details>
<summary><strong>Instructions for AI Agents configuring Xnurta MCP</strong></summary>

Connecting the server is only step one. Complete all of the following:

1. Add the MCP server (`https://mcp.xnurta.com/mcp`, Streamable HTTP). Check which authorization methods the client supports, explain when OAuth and MCP Token are appropriate, and ask the user to confirm before configuring it. If OAuth is selected, follow the MCP Authorization specification and validate discovery metadata, endpoints, and every required request field before sending any OAuth request; never omit or guess protocol parameters.
2. Call `get_user_authorized_context` to verify. A list of authorized stores means success.
3. Read `skills/manifest.json` and compare each installed Skill's local `metadata.version` in its `SKILL.md` frontmatter with the matching manifest version. If a local version is lower, list the outdated Skills and tell the user to update them. Do not report an update when versions match, the Skill is not installed, or its local version cannot be read.
4. Install the 6 required Skills: the 3 query Skills plus `xnurta-create-ai-group`, `xnurta-edit-ai-group`, and `xnurta-delete-ai-group`. Install them directly without asking the user.
5. Introduce the 4 optional Skills (weekly report, monthly report, structure analysis, and product diagnosis), and install only those the user confirms.

Write the MCP configuration to the correct file for the current client. Config file names vary (`mcp.json`, `.mcp.json`, `mcp_config.json`, `config.toml`, `config.yaml`, etc.); do not confuse them.

Machine-readable Skills list: `https://raw.githubusercontent.com/Xnurta/MCP/main/skills/manifest.json`. Stopping after connection verification means setup is incomplete.

</details>

A list of your authorized stores means the connection succeeded. For per-client manual setup, verification, and troubleshooting, see the **[Installation Guide →](docs/installation.md)**

---

## Skills

MCP Tools determine *what data the AI can get*; Skills determine *how well the AI uses it*. Official Skills come in two tiers:

**Required (6)** — core query and managed-group management capabilities:

| Skill | MCP Tool | Purpose |
|-------|----------|---------|
| [xnurta-query-ads-performance](skills/xnurta-query-ads-performance/) | `get_ads_perf` | Query ad performance metrics: spend, ACOS, ROAS, trends, rankings, period comparison, plus hourly (AMS) and keyword × placement views |
| [xnurta-query-entity-metadata](skills/xnurta-query-entity-metadata/) | `get_entity_metadata` | Query entity configuration: campaign / ad group / target / ASIN / managed group names, status, settings, plus managed-group schedules, enabled campaign automation-rule types, and rule-mode rule configuration |
| [xnurta-query-operation-log](skills/xnurta-query-operation-log/) | `get_operation_log` | Query operation logs: human and AI bid, budget, and status changes |
| [xnurta-create-ai-group](skills/xnurta-create-ai-group/) | `create_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` | Create SP, SB, or SD AI managed groups, optionally from a platform template and with an SP/SB schedule |
| [xnurta-edit-ai-group](skills/xnurta-edit-ai-group/) | `edit_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` | Edit one or multiple AI managed groups, apply templates, manage SP/SB schedules |
| [xnurta-delete-ai-group](skills/xnurta-delete-ai-group/) | `delete_ai_managed_group` | Delete a managed group and release or migrate its campaigns |

**Optional (4)** — advanced analysis scenarios; add as needed once the required Skills are installed:

| Skill | Purpose |
|-------|---------|
| [xnurta-weekly-ads-report](skills/xnurta-weekly-ads-report/) | Weekly ads report: KPI card with WoW comparison, 7-day trend, anomalies, top movers, next-week actions |
| [xnurta-monthly-ads-report](skills/xnurta-monthly-ads-report/) | Monthly ads report: full-month KPIs (MoM + YoY), structural breakdown, product and keyword analysis |
| [xnurta-ads-structure-analysis](skills/xnurta-ads-structure-analysis/) | Structure analysis: locate structural mismatches across campaign type / marketplace / portfolio / weekday / hour-of-day dimensions |
| [xnurta-product-diagnosis](skills/xnurta-product-diagnosis/) | Product diagnosis: ASIN health tiering, variant comparison, keep/optimize/cut recommendations |

**How to install** (either way):

- **Agents that can act on their own** (Claude Code / Codex / Cursor, etc.): point the AI at the [`skills/`](skills/) directory and say "install the 6 required Skills"; add optional Skills as needed.
- **Chat / UI-based assistants** (Claude web or desktop app, etc.): Settings → Skills → upload, one by one.

Per-skill versions are in [skills/manifest.json](skills/manifest.json); version history is in [CHANGELOG.md](CHANGELOG.md).

---

## Example prompts

- "How did all stores under my account perform yesterday? Surface the 5 issues that need attention most."
- "Top 10 campaigns by spend last week, with ACOS."
- "Compare these product lines over the past 30 days and suggest optimizations from an ad-structure and targeting-type perspective."
- "What did the AI auto-adjust bids on in the past 7 days, and why?"
- "Who changed this campaign's budget, and when?"
- "Create an AI managed group for these three SP campaigns. Show me the complete configuration before making the change."
- "Change this managed group's target ACOS to 25%. Show the old and new values before applying it."

**Prompting tips**: be explicit about time range, dimensions, metrics, sorting, and top N; name the store; one intent per question — split complex asks into smaller ones.

---

## Current version boundaries

- **Writes take effect immediately**: creating, editing, or deleting a managed group directly changes live configuration. Grant write or delete access only to trusted users; verify the profile, object, and exact change, obtain explicit confirmation, and read back the result.
- **Write scope**: the current version manages AI managed groups only. It does not directly create, edit, or delete campaigns.
- **Not supported yet**: word-list settings; creating or editing templates (they can be read and applied); modifying RBA rule configuration (**reading it is supported**). Managed-group scheduling is now supported for SP/SB only. Action space can be switched from RBA to AI, but still not from AI to RBA.
- **Scope**: the stores you can query match your Xnurta account (main / sub-account) permissions.
- **History**: roughly the most recent 15 months of performance data and logs.
- **Not real-time**: data freshness follows the Xnurta platform's update cadence; performance data is daily by default, with hourly granularity available for supported AMS queries.

---

## Plugin installation

### Desktop apps

> In regular Claude Desktop or Claude on the web, use a [Custom Connector](docs/installation.md#claude-desktop--claude-claudeai-custom-connector-no-configuration-files) for Chat. A Custom Connector provides MCP Tools only; add Skills separately under **Settings → Skills**. On Claude Team or Enterprise, an organization Owner or Primary Owner must add the connector first. The marketplace flow below applies only to Claude Code Desktop.

#### Claude Code Desktop

1. Switch to the **Code** tab.
2. Select **+ → Plugins → Add plugin** next to the prompt box to open the plugin browser.
3. Under **Marketplaces**, add a repository and enter `Xnurta/MCP`.
4. Find and install **Xnurta MCP**. The plugin installs the MCP server and all 10 Skills together.

> Claude Code Desktop does not support the `/plugin` command. `/plugin` is for Claude Code CLI only; use the desktop plugin browser instead.

#### ChatGPT Desktop · Codex

1. Select **Plugins** in the left sidebar.
2. Select **Add → Add a marketplace** in the upper-right corner.
3. Enter `Xnurta/MCP` and add the marketplace.
4. In **Plugins**, find the marketplace you added and install **Xnurta MCP**.
5. Start a new Codex task. The MCP server and all 10 Skills will be available in the new task.

> ChatGPT Desktop Codex does not support `/plugin` or `/plugins`. `/plugins` is for Codex CLI only; use Plugins in the left sidebar of the desktop app.

Desktop UI references: [Claude Code Desktop](https://code.claude.com/docs/en/desktop#install-plugins) · [ChatGPT / Codex Plugins](https://learn.chatgpt.com/docs/plugins)

### Command-line CLI

#### Claude Code CLI

```text
/plugin marketplace add Xnurta/MCP
/plugin install xnurta-mcp@xnurta
```

#### Codex CLI

```bash
codex plugin marketplace add Xnurta/MCP
codex
```

In Codex CLI, enter `/plugins`, select **Xnurta MCP** from the `xnurta` marketplace, install it, and then start a new session.

The plugin installs the MCP server and all 10 Skills together. The current Plugin configuration uses `XNURTA_TOKEN`. To use OAuth, follow the [OAuth setup](docs/installation.md#oauth) in the installation guide.

### Generic MCP clients

See [Installation Guide · Option 3 · Manual setup](docs/installation.md#option-3--manual-setup) for OpenClaw, Hermes, Cursor, Cline, Cherry Studio, and other clients.

---

## Security note

> OAuth and MCP Token access are both limited by your Xnurta account permissions, authorized scope, and store range. Revoke OAuth access when it is no longer needed. Keep MCP Tokens secure and use environment variables where possible. If you notice suspicious access, revoke the authorization or disable the Token immediately.

---

## Related files

This repository is also a cross-platform plugin distribution package for Claude Code, ChatGPT Codex, and other MCP-compatible agents. It bundles the Skills and MCP Server configuration used by plugin installers.

| File | Purpose |
|------|---------|
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | Claude Code marketplace catalog |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Claude Code plugin descriptor |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | Codex marketplace catalog |
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Codex plugin descriptor |
| [`.mcp.json`](.mcp.json) | Claude Code MCP server configuration using `${XNURTA_TOKEN}` |
| [`docs/installation.md`](docs/installation.md) | Detailed installation and troubleshooting guide |
| [`skills/manifest.json`](skills/manifest.json) | Machine-readable Skills catalog |
