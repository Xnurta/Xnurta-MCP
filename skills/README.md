# Xnurta MCP Skills

Official Skills for use with Xnurta MCP, in two tiers:

- **Required (6)**: core query and managed-group management capabilities — always install these.
- **Optional (4)**: advanced analysis playbooks for specific scenarios; install as needed.

## Required Skills

| Skill | Version | MCP Tool | Scope | Purpose |
|-------|---------|----------|-------|---------|
| [xnurta-query-ads-performance](xnurta-query-ads-performance/) | 1.2.0 | `get_ads_perf` | `amazon_sa_performance_data:read` | Query ad performance metrics: spend, ACOS, ROAS, trends, rankings, period comparison, hourly (AMS) and keyword × placement breakdowns, plus Vendor ASIN metric semantics (shipped/ordered, distributorView/sellingProgram) |
| [xnurta-query-entity-metadata](xnurta-query-entity-metadata/) | 1.2.0 | `get_entity_metadata` | `amazon_sa_ads_configuration:read` | Query entity configuration: campaign / ad group / target / ASIN / managed group names, status, settings, plus managed-group schedules, enabled campaign automation-rule types, and rule-mode rule configuration |
| [xnurta-query-operation-log](xnurta-query-operation-log/) | 1.2.0 | `get_operation_log` | `amazon_sa_ads_logs:read` | Query operation logs: human and AI bid, budget, and status changes (including the timestamp timezone rules) |
| [xnurta-create-ai-group](xnurta-create-ai-group/) | 1.1.0 | `create_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` | `amazon_sa_managed_group:write` | Create SP, SB, or SD AI managed groups, optionally from a platform template and with an SP/SB schedule |
| [xnurta-edit-ai-group](xnurta-edit-ai-group/) | 1.1.0 | `edit_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` | `amazon_sa_managed_group:write` | Edit one or multiple AI managed groups, apply templates, manage SP/SB schedules |
| [xnurta-delete-ai-group](xnurta-delete-ai-group/) | 1.0.3 | `delete_ai_managed_group` | `amazon_sa_managed_group_delete:write` | Delete a managed group and release or migrate its campaigns |

## Optional Skills

Advanced analyses built on the required query Skills — add as needed once those are installed:

| Skill | Version | Purpose |
|-------|---------|---------|
| [xnurta-weekly-ads-report](xnurta-weekly-ads-report/) | 1.0.1 | Weekly ads report: KPI card with WoW comparison, 7-day trend, anomaly summary, top movers, next-week actions |
| [xnurta-monthly-ads-report](xnurta-monthly-ads-report/) | 1.0.1 | Monthly ads report: full-month KPIs (MoM + YoY), structural breakdown, product and keyword analysis, next-month recommendations |
| [xnurta-ads-structure-analysis](xnurta-ads-structure-analysis/) | 1.0.1 | Structure analysis: break down spend and efficiency by campaign type / marketplace / portfolio / weekday / hour-of-day and locate structural mismatches |
| [xnurta-product-diagnosis](xnurta-product-diagnosis/) | 1.0.1 | Product diagnosis: ASIN health tiering, variant comparison, diagnostic cards for underperformers, keep/optimize/cut recommendations |

## Versions

- **For programs**: [`manifest.json`](manifest.json) is the machine-readable version list (each entry carries `name`, `version`, `required`, `mcp_tools` (array), `scopes` (array), `path`, `description`), available at a stable address:

  ```
  https://raw.githubusercontent.com/Xnurta/Xnurta-MCP/main/skills/manifest.json
  ```

- **For humans**: each Skill's version is in the `metadata.version` field of its `SKILL.md` frontmatter; overall history is in [CHANGELOG.md](../CHANGELOG.md).
- **For AI agents**: when installing, updating, or configuring Skills from this repository, compare each installed Skill's local `SKILL.md` `metadata.version` with the matching entry in the manifest above. If the local version is lower, list the outdated Skills and tell the user to update them. Do not repeat this check during normal MCP queries.
- **Release baseline**: when preparing a release, use the online `manifest.json` on the `main` branch as the version baseline. Combine multiple local fixes in the same unreleased batch into one version bump instead of incrementing from an unpublished local version.
- On every release, `manifest.json` and the frontmatter are updated together, with a matching git tag / GitHub Release.

## Installation

- **Agents that can act on their own** (Claude Code, ChatGPT Codex, Cursor, etc.): point the AI at a skill directory and say "install this". Install the 6 required Skills first, then add optional ones as needed.
- **Chat / UI-based assistants** (Claude web or desktop app, etc.): add them manually in each client's settings (in Claude, for example: Settings → Skills → upload, one by one).

## Directory layout

```
skills/
├── manifest.json              # machine-readable version list
├── xnurta-query-ads-performance/     # required
├── xnurta-query-entity-metadata/     # required
├── xnurta-query-operation-log/       # required
├── xnurta-create-ai-group/           # required
├── xnurta-edit-ai-group/             # required
├── xnurta-delete-ai-group/           # required
├── xnurta-weekly-ads-report/         # optional
├── xnurta-monthly-ads-report/        # optional
├── xnurta-ads-structure-analysis/    # optional
└── xnurta-product-diagnosis/         # optional
```

Each Skill is a self-contained directory with a `SKILL.md` (name / description / metadata.version and methodology) and `references/` (field references, example queries, etc.).
