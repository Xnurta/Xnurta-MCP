# Managed-Group Customer Display

Use this guide whenever presenting an `aiGroup` or `aiGroup_schedule` configuration to a
customer. It defines the product-facing labels and grouping; the response object's nesting is a
transport schema, not the UI information architecture.

## Language and Raw Fields

- Match the user's language. The labels below are the product's English names; if the user
  writes in another language, present the same settings in theirs.
- Do not show backend keys (`bidPerformanceStatus`, `aiActionSettings`, `aiAutomation`), rule
  numbers (`Rule 17`, `ruleType=17`), or raw enum tokens in the main answer.
- Keep a raw key/code only when the user explicitly requests raw API data or technical debugging.
  Put it in a separate technical appendix, never in the customer-facing setting name.
- IDs may be shown when useful, but label them: `aiGroupId` becomes "Managed-group ID", and
  `profileId` becomes "Profile ID".

## Customer-Facing Sections

Use this order for a complete configuration:

1. Basic settings
2. Campaigns
3. Brand, non-brand, and competitor mode
4. AI Action Space
   - Bid optimization
   - Budget optimization
   - Targeting optimization
   - Structure optimization
5. Automation rules

## Managed-Group Objective

The objective has two UI levels: a category heading and the selected option. Present the selected
option as **Objective**; the category may be shown as secondary context but must not replace the
selected option. Map from `targetType` rather than copying a returned enum text into the answer.

| Internal value | Option | UI category |
|---:|---|---|
| `1` | Drive growth | Increase sales |
| `2` | Optimize ROAS | Drive efficiency |
| `3` | Promotion sales boost | Increase sales |
| `4` | *(legacy value, no longer offered in the UI)* | — |

A group read back with `targetType=4` is a **legacy value from before the current objective UI** — not a current option, and not the same thing as the separate "Budget utilization priority (Beta)" toggle (which is an independent switch, not part of `targetType`; see the create/edit skills' enum reference). Don't render a customer-facing objective name for it. Say the group predates the current objective options and, if the user wants to act on it, that changing it requires selecting one of `1`-`3`.

For value `2`, render:

> Objective: Optimize ROAS
>
> Category: Drive efficiency

Do not render `Optimize ROAS (Drive efficiency, targetType=2)` in the main answer. The option,
the category and the backend value are three different concepts; raw codes belong only in a
technical appendix the user asked for.

## AI Personality

Show AI personality as its numeric level only in customer-facing managed-group and schedule
configuration output:

> AI personality: 4

Do not replace the number with a descriptive enum label such as "Aggressive", and do not append
the label in parentheses. The returned `aiPersonalityText` is useful for parsing/debugging only;
the product-facing value for this setting is the integer `1`-`5`.

(On accounts that set personality per action space there is no single number - see the create /
edit skills' `ai-personality.md` for how to present those.)

`brandOptimization` is only a backend container. **It is not an AI Action Space section.** Show
`brandedStatus` / `competitorStatus` and their dependent settings in the separate brand/non-brand/
competitor section. When the mode is off, one concise off row is enough; when on, expand the
returned brand/competitor matching and list settings.

| Backend field | Customer label |
|---|---|
| `brandedStatus` | Brand mode |
| `brandedMatchType` / `brandedList` | Brand matching / word lists |
| `competitorStatus` | Competitor mode |
| `competitorMatchType` / `competitorList` | Competitor matching / word lists |

## Action-Space Labels

Use the product label, not the field name.

| Backend field | Customer label | Section |
|---|---|---|
| `bidPerformanceStatus` | Adjust bids by performance | Bid |
| `bidPerformanceStrictAcosStatus` | ACOS priority mode | Bid, subordinate to performance bidding |
| `bidAdPlaceStatus` | Placement bid adjustment | Bid |
| `bidRangeStatus` | Bid range | Bid |
| `bidRangeType` / `bidRange` | Bid-range type and limits | Bid, subordinate to bid range |
| `bidDaypartStatus` | Bid dayparting | Bid |
| `bidAdPlaceRangeStatus` | Placement-specific bid ranges | Bid |
| `bidAmazonBusinessStatus` | Amazon Business bid adjustment | Bid |
| `btbRangeStatus` / `btbMin` / `btbMax` | B2B bid range | Bid, subordinate to B2B bidding |
| `budgetDynamicStatus` | Adjust budget by performance | Budget |
| `budgetRedistributeStatus` | Budget reallocation | Budget |
| `budgetDaypartStatus` | Budget dayparting | Budget |
| `negativeTargetStatus` | Add negative targets | Targeting |
| `targetHarvestStatus` | Target harvesting | Targeting |
| `targetPausedAddStatus` | Pause targets | Targeting |
| `structPauseProductStatus` | Pause products | Structure |
| `structPauseCampaignStatus` | Pause campaigns and ad groups | Structure |

Show every supported switch separately as on/off for a complete read. Subordinate fields belong
under their parent switch; they are not additional action spaces. Do not infer one switch from a
sibling field.

## Managed-Group Rule Names

The codes below are internal routing keys. Use only the product-facing name in the answer.

| Internal rule type | Customer label |
|---:|---|
| `2` | Bid dayparting |
| `4` | Target harvesting |
| `5` | Add negative targets |
| `13` | Budget dayparting |
| `17` | Adjust budget by performance |
| `19` | Placement bid adjustment |
| `20` | Pause campaigns and ad groups |
| `181` | Adjust bids by performance |
| `182` | Pause targets |

For example, render rule type `17` as:

> Adjust budget by performance: on
>
> Mode: Rule

Do not render "Rule 17", "Budget rule", or "Rule status: enabled (Rule-driven)". The paired
action-space switch supplies on/off; the retained rule entry supplies the Rule operating mode.

## Complete-Read Shape

Prefer column headings such as `Setting / Status / Configuration`, not `Field / Value`. Do not
put backend keys in the setting column. For a compact answer, keep off settings to one line and
expand only enabled settings and retained Rule configurations.
