# Changelog

This file tracks version changes for Xnurta MCP Skills and the accompanying documentation.

## [Unreleased]

### Added

- **Vendor ASIN metric semantics** (`xnurta-query-ads-performance` `1.1.0` → `1.2.0`, ticket BC-9770): `TotalSalesAmount`/`OrderCount`/`UnitCount`/`TACOS` on Vendor rows use the shipped basis (not ordered), unified with Seller rows so they can be summed directly in a mixed query. Documented the availability split for `OrderedRevenue`/`OrderedTACOS` (only under `distributorView_=MANUFACTURING`) vs `ShippedRevenue`/`ShippedTACOS` (both views). Documented Vendor dimension auto-locking: the underlying table has up to 4 rows per `(profileId, date, ASIN)` (`distributorView_` × `sellingProgram_`), and querying without locking them inflates ad metrics and `GlanceViews` by up to 4×; the server defaults to `MANUFACTURING` + `RETAIL` and reports what it defaulted via `meta.appliedDefaults`. Added guidance for mixed Seller+Vendor queries: unified metrics aggregate directly, Vendor-specific metrics need grouping by `storeType_`.

### Fixed

- **Managed-group full-configuration explanation** (`xnurta-query-entity-metadata`, version to be bumped at release time): added a customer-display layer — page-name labels in the user's language, backend field names and rule numbers hidden by default; brand/non-brand/competitor mode presented separately from the AI Action Space; distinguished the objective's UI category from its selected option, with Chinese `targetType=2` rendered as "保持订单稳定" rather than "控制成本" or an English enum label; `aiPersonality` shown as the raw `1`-`5` number, never replaced or appended with a text label such as "激进"; clarified that `aiAutomation.*.status` is a mode discriminator (AI vs Rule), not an enabled/disabled flag; filled in the `isSelf=1/2/3` scope and lookback-window semantics for rules 4/5; folded the performance-based-budget upper/lower bounds back into their parent strategy and grouped "custom settings" vs "frequency settings", explaining that the configured budget takes effect at the store's local midnight the next day; added the conversion from budget dayparting's "reduction percentage" to "effective budget as a percentage of the current day's budget", and stopped mislabeling the budget cap as the actual pacing ratio. Also corrected an incorrect `select` statement in the full-read example.
- **Hourly (AMS) timezone confirmed** (`xnurta-query-ads-performance`, same version range as above): `date`/`hour` confirmed to be in the profile's local IANA timezone (not UTC); data latency is roughly 2 hours (much faster than the daily pipeline's T+2).
- **No verified product-identity join path for hourly queries yet**: adding `productAd.asin_`/`productAd.sku_` to `select` fails with a `business_error` (cannot join the CTE); `factEntity: productAd` itself rejects `timeGranularity: hourly`. Only the `productAd.*` combination was tested — whether `asin.*` or a daily `campaign`+`productAd` combination fails the same way is untested; don't extrapolate.
- **15-month lookback boundary is inclusive**: verified that a `dateStart` exactly at the 15-month-ago cutoff succeeds; only a date strictly earlier than that errors (`start.isBefore(earliest)` semantics). The docs previously said the boundary date itself would fail.

## [1.1.1] - 2026-08-25

Based on the online v1.1.0 release as a single version baseline, this release aligns the Skills with the MCP Server's current `pre` behavior and adds hourly (AMS) data, managed-group schedules, automation-rule reads, and managed-group templates.

### Added

- **Hourly / AMS data** (`xnurta-query-ads-performance` `1.0.0` → `1.1.0`): new `timeGranularity` (`daily` / `hourly`, where **`hourly` requires `factEntity=campaign`**) and a new fact entity `keywordPlacement` (keyword × placement, hourly by nature, SP only). Both are capped at a **7-day span** rather than 90 days, `keywordPlacement` uses bare field names (the second naming exception after `searchTerm`), and its `AISpend`/`AISales` are always `0` with `AIACOS`/`AIROAS` always `null` — placeholders, not real values. New example: `example-hourly-ams.md`.
- **Managed-group schedule reads** (`xnurta-query-entity-metadata` `1.1.3` → `1.2.0`): new entity `aiGroup_schedule`, whose contract differs from every other entity — exactly one `profileId`, `filters` must contain `aiGroupId` and nothing else, pagination and sorting are ignored, and all schedules come back in one call. New example: `example-ai-group-schedule.md`. Weekly schedules (`timeType=2`) inherit `optimizeType`/`acos`/`aiPersonality` from the parent group, so read those from the group.
- **Rule-mode (RBA) rule configuration reads** (same skill): for a rule running in Rule mode, its conditions, actions, condition items, periods and hour matrices are readable under `aiGroup`'s `aiAutomation.{ruleType}` (rules 2/4/5/13/17/19/20/181/182). Confirmed leaves carry a `...Text` companion; unconfirmed leaves pass through raw. **Readable, not writable** — this reverses the previous "RBA config can be neither read nor modified" statement. New `references/automation-rule-reading.md` documents the Help Center semantics for hourly bid multipliers, hourly budget restoration, budget utilization, AND/OR condition groups, strategy priority, lookback exclusion periods, placement calculations, and scheduled campaign start/stop actions.
- **Automation-rule query boundary** (same skill): `entity=automationRule` returns only the rule types enabled for specified campaigns; it does not return template names, conditions, actions, or frequency. `aiGroup.aiAutomation` represents embedded Rule-mode configuration inside a managed group's action space, not the account-level automation template library. Inventory rules are SKU/product-level, and neither current entry point can reliably read their configuration.
- **Managed-group schedule writes** (`xnurta-edit-ai-group` `1.0.4` → `1.1.0`): documented the full contract of `save_sp_sb_ai_group_schedule` (SP/SB only) — omit `id` to create / `id>0` to update, `isActive=false` with an `id` to delete, `timeType=1` carries its own base settings, **`timeType=2` is rejected if it carries them**, word-list settings are stripped server-side, and overlaps come back as `Schedule_Date_Overlap`. This reverses the previous "scheduling is unsupported and rejected by the backend" statement.
- **Managed-group templates** (`xnurta-create-ai-group` `1.0.3` → `1.1.0`, `xnurta-edit-ai-group` `1.1.0`): added `get_ai_group_template` (list / detail — a read that sits behind the write scope) and the `templateId` parameter on the three write tools. Explicit arguments override template values; precedence is `templateId` > `operation` > plain field edit. A template whose rule 4 / rule 5 is bound to specific campaigns and ad groups (`isSelf=2` with the rule enabled) is rejected. **Templates themselves are read-only** — MCP cannot create, edit, or delete one.
- **Hour-of-day structure analysis** (`xnurta-ads-structure-analysis` `1.0.0` → `1.0.1`): new `breakdownBy: hourOfDay`, with its campaign-only and per-request 7-day constraints spelled out. Label the result as a sample only when it covers a subset of the requested window; full chunked coverage must not be described as sampling.

### Fixed (statements that contradicted actual server behavior)

- **`profileIds` is now all-or-nothing**: every requested ID must be authorized across all read and write tools; one unauthorized value fails the entire request (`Requested profileIds contain unauthorized values`). This **reverses** the previous "unauthorized IDs are silently dropped, an empty intersection returns an empty result set" statement, and the zero-result diagnosis sequence was rewritten accordingly.
- **Scope names corrected**: `amazon_sa:performance:read` → `amazon_sa_performance_data:read`, `amazon_sa:ads_configuration:read` → `amazon_sa_ads_configuration:read`, `amazon_sa:ads_logs:read` → `amazon_sa_ads_logs:read`; the write side now names `amazon_sa_managed_group:write` and `amazon_sa_managed_group_delete:write` explicitly.
- **Pagination validation diverges by tool**: on `get_ads_perf` / `get_entity_metadata`, a `pageSize` over 500 or ≤0 and a `page` ≤0 now error instead of being clamped; `get_operation_log` still clamps silently. Derived page sizes need guarding at both ends (`xnurta-product-diagnosis` changed `min(topN, 500)` to `max(1, min(topN, 500))`).
- **`get_operation_log`'s `createdDate` timezone is not fixed** (`xnurta-query-operation-log` `1.1.1` → `1.2.0`): `aiGroup` rows are always UTC; `campaign`/`adGroup`/`target`/`placement` rows are store-local for a single `profileId` and UTC for several (measured: the same record 7 hours apart). This **replaces** the earlier "genuine gap in the spec, do not guess" treatment with the measured behavior, and adds requirements to label the timezone, never merge single- and multi-profile results, and treat mixed-entity responses as unreliable chronologically.
- **`language` default**: `get_ads_perf` defaults to `en`, not `zh` (an unrecognized value falls back to `en` silently).
- **SB-unsupported fields now hard-error**: enabling an SP-only action-space field on an SB group (`bidAmazonBusinessStatus`, `btb*`, `bidDaypartStatus`, `bidPerformanceStrictAcosStatus`, `bidAdPlace*`, `tos`/`pdp`/`ros` bounds, `structPause*` — 16 fields) fails the whole request and lists every offending field, rather than being silently ignored.
- **`aiGroup` reads return a projection of the currently effective config**: first trimmed by `campaignType` (SD has no bid/struct/brand action spaces and no automation rules; SB drops struct plus the placement/B2B families), then reduced by switch and mode (an off switch drops its dependent fields; an AI-mode rule is omitted entirely; a Rule-mode rule drops AI-only parameters). **A missing field is not "unset" and not "the write failed"** — verify a write by checking the switch first, then its dependents.
- **`aiAutomation` semantics and field names**: on the write side it is a flat object (`bidDaypartStatus`, `targetHarvestRuleStatus`, `negativeTargetRuleStatus`, `budgetDaypartRuleStatus` + `budgetDaypartExcuteDays`, `budgetPerformanceRuleStatus`, `placementAdjustmentRuleStatus`, `pauseCampaignRuleStatus`, `bidPerformanceRuleStatus`, `targetPauseSupplementRuleStatus`), and **`0` = AI mode while `1` = Rule mode (unsupported by these tools)** — the opposite of the intuitive "1 = enabled". On the read side it is keyed by rule number. An empty `aiAutomation` object is ambiguous because the effective-config projection may omit AI-mode or inapplicable rules; it must not be interpreted as "all rules are disabled."
- **`edit_sd_ai_managed_group`'s `optimizeType`** accepts `1`/`2`/`3` (`3` = boost volume); the docs previously listed only 1 and 2.
- **`delete_ai_managed_group` routing is fail-fast** (`xnurta-delete-ai-group` `1.0.2` → `1.0.3`): an undeterminable `campaignType` is rejected rather than guessed; the entry point now links the managed-group enum glossary needed for pre-delete confirmation.
- **Two error envelope shapes**: tool-level failures use `errorType`, pipeline-level failures (rate limiting, auth, downstream business errors, timeouts) use `error`; responses now carry `requestId`, which should be quoted to the user when reporting a failure. Actual rate limits are documented (IP 60/min, token prefix 300/min, tenant and user dimensions 120/min for reads and 20/min for writes, and a fail-closed 429 when the limiter is unavailable).
- **`get_operation_log`'s `currency` may be the literal `"mixed"`** on cross-currency results — not a currency code, so never format or sum with it.
- **Batch operation naming and no-go list** (`xnurta-edit-ai-group`): added the server's canonical camelCase operation codes (case- and underscore-insensitive), and marked all four word-list-related operations (`NEGATIVE_TARGET`, `BRAND_TARGET`, `TARGET_PAUSED_ADD`, `TARGET_HARVEST_ACTION`) as unavailable in batch mode.

### Documentation consistency

- `skills/README.md` version table brought up to each `SKILL.md`'s actual version (previously four entries behind), with real scope names in the Scope column.
- `skills/manifest.json`: `release` → `v1.1.1`, `updated_at` → `2026-08-25`; fields normalized to `mcp_tools` (array) and `scopes` (array), now filled in for all 10 skills.
- All Skill versions now live in frontmatter `metadata.version`, and installation/version-check guidance reads that field so every Skill passes the Codex Skill frontmatter validator.
- The four optional skills' Version History gained `1.0.0` and `1.0.1` entries (previously stopping at v0.x), and references to a design draft that doesn't ship with the skills were removed.
- The read-side `platform-notes.md` self-description was made generic; all 7 copies are now byte-identical (it previously claimed only the 3 read skills carried one).
- Self-check fixes clarify effective-config read-back verification, read-only Rule-mode boundaries, schedule response envelopes, complete hourly chunking versus sampling, Vendor inference limits, and delete enum references.
- Release versions use the online `main` manifest as their baseline; multiple local fixes in one unreleased batch are consolidated into one version bump.

### Changed (previously unreleased entries, shipping with 1.1.1)

- **xnurta-query-entity-metadata** `1.1.0` → `1.1.1`.
- **xnurta-query-operation-log** `1.1.0` → `1.1.1`.
- **xnurta-create-ai-group** `1.0.0` → `1.0.1`: added business-term disambiguation, a mandatory clarification gate before writes, and corrected create-time budget and target mappings.
- **xnurta-edit-ai-group** `1.0.0` → `1.0.1`: added business-term disambiguation, clarification separate from write authorization, and path-specific status handling.
- **xnurta-query-entity-metadata** `1.1.1` → `1.1.2`: documented managed-group total-budget rollups and their proportional campaign-budget behavior.
- **xnurta-create-ai-group** `1.0.1` → `1.0.2`: clarified group budget, performance-budget increase caps, budget reallocation scope, and create-time confirmation requirements.
- **xnurta-edit-ai-group** `1.0.1` → `1.0.2`: added the complete fixed/percentage and per-campaign/group budget model, reliable enabled-campaign lookup, impact preview, and ambiguity handling.
- **xnurta-delete-ai-group** `1.0.0` → `1.0.1`: stopped relying on unsupported campaign `aiGroupId` server filtering; campaign membership is now verified after full pagination and local filtering.
- **xnurta-create-ai-group** `1.0.2` → `1.0.3`: added Strict ACOS / ACOS priority mode guidance (`bidPerformanceStrictAcosStatus` — SP only; preconditions `targetType=2` + `bidPerformanceStatus=1` + `aiPersonality>=3`; Auto Pacing precedence; tradeoff must be confirmed) and disambiguation distinguishing it from setting a target ACOS.
- **xnurta-edit-ai-group** `1.0.2` → `1.0.3`: same Strict ACOS guidance plus a disambiguation cross-reference.
- **xnurta-edit-ai-group** `1.0.3` → `1.0.4`: switched the budget-cap preview's enabled-campaign lookup to server-side `aiGroupId` filtering (campaign supports it), replacing the earlier full-pull + local-filter approach.
- **xnurta-delete-ai-group** `1.0.1` → `1.0.2`: switched campaign-list capture to server-side `aiGroupId` filtering — **reverting the 1.0.1 local-filter approach**, since campaign `aiGroupId` filtering is supported per the Xnurta Ads API.
- **xnurta-query-entity-metadata** `1.1.2` → `1.1.3`: clarified that for the campaign entity **every return field is filterable** (all return fields, no exceptions — including `aiGroupId`, `portfolioId`, and the `campaign*Date` fields).
- Added Skill version-check guidance: during installation or updates, AI agents compare local `SKILL.md` versions with the remote `manifest.json` and tell the user when installed Skills are outdated.
- Added an OAuth preflight requirement for AI agents: follow MCP authorization discovery and validate all protocol-required request fields before sending an OAuth request.

## [1.1.0] - 2026-08-18

Adds managed-group write support and aligns the query Skills with the latest MCP Tool documentation.

### Changed

- Added OAuth authorization alongside the existing MCP Token authentication method.
- Kept MCP Token in the Plugin's bundled configuration; OAuth-capable clients can connect through a Custom Connector or manual setup.
- Updated the README, installation guide, connection verification, and 401 troubleshooting to cover both authorization methods.
- **xnurta-query-operation-log** `1.0.0` → `1.1.0` — `get_operation_log` pagination model updated. Two modes decided by `entities`: a single non-`aiGroup` entity now supports **real pagination** (`page` + `pageSize`, loop until `hasNextPage=false`); multi-entity or `aiGroup`-only stays **limit-only** (`limit`/`truncated`). `pageSize` default `50` → `100`, max `200` → `1,000` (`aiGroup`-only `10,000`). Added guidance to steer the user toward a single entity when a limit-only result is truncated.
- **xnurta-query-entity-metadata** `1.0.0` → `1.1.0` — documented the new `select` parameter (top-level field projection, ordered, unknown fields ignored via `meta.hint`, no effect on pagination). Noted that enum `{field}Text` companion fields are **not** auto-appended when `select` is used — the `xxxText` field must be listed explicitly.
- Added three **required Skills at version 1.0.0**: `xnurta-create-ai-group`, `xnurta-edit-ai-group`, and `xnurta-delete-ai-group`, covering SP, SB, and SD AI managed-group creation, editing, and deletion.
- Documented that managed-group writes modify live configuration immediately and require confirmation plus read-back verification.
- Documented current limitations: no scheduling, template-based setup, or word-list settings; RBA configuration cannot be read or edited, RBA → AI is supported, and AI → RBA is not supported.

## [1.0.0] - 2026-07-29

First release (matching MCP Server v1.0.0 · Data Query).

### Added

- 3 **required Skills**:
  - **xnurta-query-ads-performance** `1.0.0` — ad performance queries, mapped to MCP tool `get_ads_perf` (scope: `amazon_sa:performance:read`)
  - **xnurta-query-entity-metadata** `1.0.0` — entity configuration / metadata queries, mapped to MCP tool `get_entity_metadata` (scope: `amazon_sa:ads_configuration:read`)
  - **xnurta-query-operation-log** `1.0.0` — operation log queries, mapped to MCP tool `get_operation_log` (scope: `amazon_sa:ads_logs:read`)
- 4 **optional Skills** (under `skills/optional/`, add as needed after the required ones):
  - **xnurta-weekly-ads-report** `0.9.4` — weekly ads report
  - **xnurta-monthly-ads-report** `0.5.6` — monthly ads report
  - **xnurta-ads-structure-analysis** `0.2.3` — ad structure analysis
  - **xnurta-product-diagnosis** `0.1.11` — product diagnosis
- `skills/manifest.json` machine-readable version list with a `required` flag
- README and installation guide (Claude / ChatGPT Codex / OpenClaw / Hermes / Cursor / Cline / Cherry Studio client setup)
