# Xnurta MCP Skills

Official Skills for use with Xnurta MCP, in two tiers:

- **Required (8)**: core query, managed-group management, and ad-editing capabilities — always install these.
- **Optional (13)**: two tool-specific skills plus analysis playbooks for reports, product diagnosis, search terms, market data and promotions; install as needed.

## Required Skills

| Skill | Version | MCP Tool | Scope | Purpose |
|-------|---------|----------|-------|---------|
| [xnurta-query-ads-performance](xnurta-query-ads-performance/) | 1.4.11 | `get_ads_perf` | `amazon_sa_performance_data:read` | Query ad performance metrics: spend, ACOS, ROAS, trends, rankings, period comparison, hourly (AMS) and keyword × placement breakdowns, plus Vendor ASIN metric semantics (shipped/ordered, distributorView/sellingProgram) |
| [xnurta-query-entity-metadata](xnurta-query-entity-metadata/) | 1.4.12 | `get_entity_metadata` | `amazon_sa_ads_configuration:read` | Query entity configuration and delivery status, campaign budget usage (remaining budget / budget status / capped time), category and brand targeting IDs, SB and SD creation entities, managed-group schedules, enabled campaign automation-rule types, and rule-mode rule configuration |
| [xnurta-query-operation-log](xnurta-query-operation-log/) | 1.3.9 | `get_operation_log` | `amazon_sa_ads_logs:read` | Query operation logs: human and AI bid, budget, and status changes (including the timestamp timezone rules) |
| [xnurta-create-ai-group](xnurta-create-ai-group/) | 1.2.7 | `create_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` / `get_sp_sb_ai_personality_recommendation` | `amazon_sa_managed_group:write` | Create SP, SB, or SD AI managed groups, optionally from a platform template recommended by campaign purpose, and with an SP/SB schedule |
| [xnurta-edit-ai-group](xnurta-edit-ai-group/) | 1.2.7 | `edit_sd_ai_managed_group` / `save_sp_sb_ai_managed_group` / `save_sp_sb_ai_group_schedule` / `get_ai_group_template` / `get_sp_sb_ai_personality_recommendation` | `amazon_sa_managed_group:write` | Edit one or multiple AI managed groups, apply templates (recommended by campaign purpose), manage SP/SB schedules |
| [xnurta-delete-ai-group](xnurta-delete-ai-group/) | 1.0.12 | `delete_ai_managed_group` | `amazon_sa_managed_group_delete:write` | Delete a managed group and release or migrate its campaigns |
| [xnurta-edit-ads](xnurta-edit-ads/) | 1.3.0 | `batch_update_ads` | `amazon_sa_campaign_edit:write` | Edit campaign budget / state / bidding / portfolio membership, portfolio budgets and dates, campaign name / end date, ad group state / name / default bid, keywords, targets, promoted products and negatives, including keyword-list expansion (31 routes, 15 may need two-phase confirmation) |
| [xnurta-create-campaign](xnurta-create-campaign/) | 1.2.0 | `create_sp_sb_campaign` / `create_sd_campaign` / `create_sp_ad_group` / `create_sb_ad_group` / `create_sd_ad_group` / `create_portfolio` | `amazon_sa_campaign_create:write` | Create new SP / SB / SD campaigns, add ad groups to existing campaigns, create portfolios |

## Optional Tool Skills

| Skill | Version | MCP Tool | Scope | Purpose |
|-------|---------|----------|-------|---------|
| [xnurta-manage-keyword-list](xnurta-manage-keyword-list/) | 1.0.0 | `get_keyword_list` / `create_keyword_list` / `update_keyword_list` / `delete_keyword_list` | `amazon_sa_keywords_list:write` | Manage keyword lists: search, create, edit, share and delete; referenced by ID from campaigns, ad groups and managed groups |
| [xnurta-query-market-data](xnurta-query-market-data/) | 1.0.1 | `get_market_search_perf` / `get_peer_benchmark` | `sqp:read` (SQP / ABA) + `benchmark:read` (peer benchmark) - **two separate scopes**, each with its own menu permission | Weekly SQP / ABA demand, own share and top-3; weekly or monthly brand peer benchmarks. Single store per call |

## Optional Skills

Advanced analyses built on the required query Skills — add as needed once those are installed:

| Skill | Version | Purpose |
|-------|---------|---------|
| [xnurta-weekly-ads-report](xnurta-weekly-ads-report/) | 1.1.6 | Weekly ads report: KPI card with WoW comparison, 7-day trend, anomaly summary, top movers, next-week actions |
| [xnurta-monthly-ads-report](xnurta-monthly-ads-report/) | 1.2.4 | Monthly ads report: full-month KPIs (MoM + YoY), structural breakdown, product and keyword analysis, next-month recommendations |
| [xnurta-ads-structure-analysis](xnurta-ads-structure-analysis/) | 1.1.7 | Structure analysis: break down spend and efficiency by campaign type / marketplace / portfolio / weekday / hour-of-day and locate structural mismatches |
| [xnurta-product-diagnosis](xnurta-product-diagnosis/) | 1.2.5 | Product diagnosis: portfolio tiering plus a separate lifecycle stage (SP advertising age + 12-week total-sales trend), variant comparison, diagnostic cards for underperformers, keep/optimize/cut recommendations |
| [xnurta-asin-deep-dive](xnurta-asin-deep-dive/) | 1.0.0 | **Install `xnurta-query-market-data` alongside it** (`sqp:read` + `benchmark:read`); each missing scope only switches off its own tool (no `sqp:read` -> substitute path for the SQP / ABA modules; no `benchmark:read` -> no peer background). Single-ASIN deep dive: traffic and ad structure, variants, stock and ACOS mechanism; use platform SQP / ABA and available competitorProduct data first, brand peer benchmarks only as context, SellerSprite for broader comparisons |
| [xnurta-search-term-diagnosis](xnurta-search-term-diagnosis/) | 1.1.0 | Search-term diagnosis: tag search terms by orders, brand / non-brand and keyword / ASIN; report spend distribution, negative and harvest candidates and fragmented exact keywords, with thresholds from the store's order value and target ACOS |
| [xnurta-sqp-insight](xnurta-sqp-insight/) | 1.0.1 | SQP market diagnosis and one-category growth or efficiency plan; diagnose is read-only, plan writes only confirmed rows through edit skills. Needs `xnurta-query-market-data` and Python 3 |
| [xnurta-category-scorecard](xnurta-category-scorecard/) | 1.0.1 | Compare every category with SQP and brand peer benchmarks; produce category plays, peer goal ranges and a budget plan. Read-only; execution goes to edit-ads after confirmation. Needs `xnurta-query-market-data` and Python 3 |
| [xnurta-promo-prep](xnurta-promo-prep/) | 1.0.1 | Promo prep: check stock against event demand, portfolio caps, campaigns already out of budget and managed-group schedules; size the push to the user's event budget; prepare role-matched dated schedules for eligible SP/SB managed groups (Promotion sales boost only for head groups the user confirms; others on Drive growth or kept on Optimize ROAS) and budget / bid / top-of-search raises for the rest, with a product-line summary, preview and change log |
| [xnurta-promo-monitor](xnurta-promo-monitor/) | 1.0.0 | Promo monitor: on event days, read today's hourly pace and budget usage against a normal day, flag winners about to run out of budget, spend without orders, campaigns over the limit, low stock and today's pauses, and propose small capped moves for the user's current goal; answers "can I pause these targets" and "restocks next week - keep spending?" |
| [xnurta-promo-reset](xnurta-promo-reset/) | 1.1.0 | Promo reset: find every bid, budget, placement and managed-group setting a person changed for a promotion and its pre-promo value from the operation log, restore all at once or, as the user chooses, suggest restore now / step down over days / customer decides from post-promo performance; or restore from the customer's own uploaded record; then apply with preview and read-back |

## Versions

- **For programs**: [`manifest.json`](manifest.json) is the machine-readable version list (each entry carries `name`, `version`, `required`, `mcp_tools` (array), `scopes` (array), `path`, `description`), available at a stable address:

  ```
  https://raw.githubusercontent.com/Xnurta/Xnurta-MCP/main/skills/manifest.json
  ```

- **For humans**: each Skill's version is in the `metadata.version` field of its `SKILL.md` frontmatter; overall history is in [CHANGELOG.md](../CHANGELOG.md) — that path resolves in the published layout (`skills/README.md` next to the repository root `CHANGELOG.md`), not when browsing this folder in the source repository.
- **For AI agents**: when installing, updating, or configuring Skills from this repository, compare each installed Skill's local `SKILL.md` `metadata.version` with the matching entry in the manifest above. If the local version is lower, list the outdated Skills and tell the user to update them. Do not repeat this check during normal MCP queries.
- **Release baseline**: when preparing a release, use the online `manifest.json` on the `main` branch as the version baseline. Combine multiple local fixes in the same unreleased batch into one version bump instead of incrementing from an unpublished local version.
- On every release, `manifest.json` and the frontmatter are updated together, with a matching git tag / GitHub Release.

## Installation

- **Agents that can act on their own** (Claude Code, ChatGPT Codex, Cursor, etc.): point the AI at a skill directory and say "install this". Install the 8 required Skills first, then add optional ones as needed.
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
├── xnurta-edit-ads/                  # required
├── xnurta-create-campaign/           # required
├── xnurta-manage-keyword-list/       # optional
├── xnurta-query-market-data/         # optional
├── xnurta-weekly-ads-report/         # optional
├── xnurta-monthly-ads-report/        # optional
├── xnurta-ads-structure-analysis/    # optional
├── xnurta-product-diagnosis/         # optional
├── xnurta-asin-deep-dive/            # optional
├── xnurta-search-term-diagnosis/     # optional
├── xnurta-sqp-insight/               # optional
├── xnurta-category-scorecard/        # optional
├── xnurta-promo-prep/                # optional
├── xnurta-promo-monitor/             # optional
└── xnurta-promo-reset/               # optional
```

Each Skill is a self-contained directory with a `SKILL.md` (name / description / metadata.version and methodology) and `references/` (field references, example queries, etc.).
