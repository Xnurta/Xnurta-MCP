---
name: xnurta-search-term-diagnosis
description: >-
  Diagnose where ad spend goes at the search-term level: tag every search term (keyword vs
  ASIN, branded vs non-branded, order tier), then report spend distribution, brand vs
  non-brand, zero-order waste with negative candidates, harvest candidates for exact match,
  and fragmented exact keywords - with fixed, reproducible rules and thresholds derived from
  the store's own order value and target ACOS. Read-only; execution goes to xnurta-edit-ads.
  Use when the user asks where search-term spend went last month, requests negative candidates, or wants to know which automatic-targeting terms deserve dedicated targeting,
  "search term analysis", "negative keyword candidates", "harvest keywords". Not for
  trend recaps (xnurta-weekly-ads-report / xnurta-monthly-ads-report), campaign-type /
  marketplace structure (xnurta-ads-structure-analysis) or ASIN health
  (xnurta-product-diagnosis).
metadata:
  version: 1.0.3
---

# Search Term Diagnosis

## Scope: a read-only orchestration skill

No MCP tool of its own. It reads with two tools and hands execution to one skill:

| What | Tool | Owning skill - read it first |
|---|---|---|
| Search terms, keyword performance, totals | `get_ads_perf` | [xnurta-query-ads-performance](../xnurta-query-ads-performance/SKILL.md) |
| Exact keywords in use, campaigns, managed groups, brand names | `get_entity_metadata` | [xnurta-query-entity-metadata](../xnurta-query-entity-metadata/SKILL.md) |
| Adding negatives / exact keywords, pausing a keyword | `batch_update_ads` | [xnurta-edit-ads](../xnurta-edit-ads/SKILL.md) |

> **Dependency - install the three skills above alongside this one.** Skills install as
> sibling directories under your agent's skills root (see the
> the installation notes in [README](../README.md)); the `../xnurta-.../` links resolve against it.
> Auth, errors, pagination, date limits and currency rules are in the query skills'
> `references/platform-notes.md` - read it once.

| Reference | Read it when |
|---|---|
| [`references/data-retrieval.md`](references/data-retrieval.md) | Pulling data: which calls, in what order, and the gotchas (filter semantics, field names, paging) |
| [`references/classification.md`](references/classification.md) | Tagging and the five views: exact rules, thresholds, tie-breaks, the reference script |

## Output language

The skill documentation and examples are written in English. Answer in the user's language and
pass the matching `language` value to `get_ads_perf` so returned display text is consistent.

## Principles

1. **Classification is computation, not judgement.** Labels and thresholds are fixed rules
   (see `classification.md`). Run them as code when you can; never re-label a term by feel.
   The same data must produce the same lists and totals every time.
2. **Thresholds come from the customer's own numbers** - average order value and one
   store-wide target ACOS - never a fixed dollar amount.
3. **Describe, then prescribe.** Spend distribution and brand share are descriptions. Only
   the zero-order list, harvest list and fragments carry actions.
4. **Brand terms are an input.** Pre-fill them, never decide them: a brand name can be a
   common word.
5. **Don't fight the AI, don't hide from it.** Terms in managed groups that already run
   automatic negation or harvesting are still listed - labelled, not skipped.
6. **Read-only.** Every change goes through `xnurta-edit-ads` with its own preview and
   confirmation.

## Workflow

### Step 1 - Scope and three inputs

Resolve the store with `get_user_authorized_context`. **One store per run** - thresholds
are in the store's currency and order value.

- **Period**: default the 30 days ending **3 days before today** (e.g. asked on 10/12 ->
  9/10-10/9). The last few days' orders may not be attributed yet, which would make
  zero-order judgements too harsh. Say so in the answer. Other periods are fine; order
  thresholds are scaled to 30 days (`classification.md`).
- **Scope**: whole store by default; named campaigns, or a product (ASIN / parent ASIN) -
  for a product the result is the search terms of the ad groups that contain it, not traffic
  attributed to the ASIN (`data-retrieval.md` -> Narrowing the scope).

Pull data-retrieval calls 1, 3 and 9 first - the pre-fills below come from them. Then confirm
three inputs, the first two **pre-filled by you**:

1. **Brand terms.** Pre-fill the brand from `get_entity_metadata(entity='asin')` ->
   `asinBrand`, then list candidates found in the period's search terms: sub-brands and
   product-line names that appear in the store's own `asinTitle`s, other spellings of the
   brand (spacing, other scripts), and close misspellings. Let the customer tick them and
   add more, including competitor brand terms if they want. Never treat an unconfirmed
   candidate as a brand term.
2. **Target ACOS** - one number for the whole store: ask what ACOS the store should target. If the
   customer has none, use the store's ACOS for the period and say in the first line of the
   answer that the thresholds use it and can be recomputed. **Do not use managed-group
   target ACOS as the threshold** - stores have dozens of groups with targets that vary
   widely and are often set high on purpose; managed groups are only used to label switches.

3. **Product stage** - mature, or new / in launch. It sets the harvest threshold (4 vs 2
   orders in 30 days). Ask; do not infer it from listing dates.

Optional: a **negative whitelist** of word roots that must never be proposed as negatives
(e.g. brand / model / year roots for compatibility products). Ask once; reuse the inputs in
later runs in the same conversation.

### Step 2 - Pull the data

Full call plan and gotchas: [`references/data-retrieval.md`](references/data-retrieval.md).
In short: totals; search terms with orders; zero-order terms above the threshold; source match
types; exact keywords in use and their performance; brand data; managed-group switches for
the listed terms only. **Do not page through every search term** - the zero-order small
terms are derived from totals.

### Step 3 - Classify and save

Apply [`references/classification.md`](references/classification.md) and **save the result to
a file first** (one row per search term with its labels and numbers, plus the totals). The
answer and any export are built from that file, never from a fresh query or a recomputation,
so the conversation and the file always agree.

### Step 4 - Answer

Lead with the scope line, then five short parts:

1. **Spend distribution (V1)**: a small table - core (≥3 orders), potential (1-2), zero-order above the
   one-order target spend, zero-order small terms - with spend, share and ACOS; keyword and
   ASIN traffic shown separately where it matters. Zero-order small terms are one line with
   their amount; never list them term by term. Then add **where small unconverted spend comes
   from**, measured at search term x match type (`data-retrieval.md`) and named as such -
   for example, "48% of low-spend, zero-order traffic by search term and match type came from broad automatic targeting" - plus the top
   campaigns when search-term x campaign detail was pulled. Point to where to look (harvest the
   good terms there, check its negatives, split it out to watch it); don't recommend pausing a
   match type on this number alone.
2. **Branded / non-branded (V2)**: brand share of the listed keyword spend, brand
   ACOS, non-brand ACOS and the ratio,
   and the direction (`classification.md` -> V2). Skip V2 with a reason if the customer
   declined to give brand terms.
3. **Zero-order waste (V3)**, in three groups (`classification.md` -> V3):
   - **zero-order exact keywords** - your own exact keywords with no orders and spend above
     the threshold: pause them (no bid advice);
   - **negative candidates** - count, spend, top 10, each with its action (negative exact for
     keywords, negative product targeting for ASINs) and a label when the managed group
     already has automatic negative targeting on;
   - **zero-order terms you also target as exact keywords** - not proposed as negatives;
     say where the spend came from and leave it to the customer.

   Brand terms, the store's own ASINs and whitelisted roots are held back and counted at the
   end.
4. **Harvest candidates (V4)**: count, orders, top 10 with source match type. Mention managed groups whose
   harvesting is off.
5. **Targeting fragmentation (V5)**: enabled exact keywords with ≤3 orders in 30 days - count, zero-order
   count, spend - and the suggestion to fold them back into auto / broad for mature products.

End by offering the complete list and asking which candidates the user wants to act on.

### Step 5 - Export and hand-off

- **Export** (only if asked): four sheets from the saved file - all tagged search terms,
  negative candidates, harvest candidates, fragmented keywords. Counts and spend must match the
  answer exactly.
- **Execution**: this skill writes nothing. For requests to negate terms, add exact keywords, or pause a keyword,
  hand the rows - with campaign type, campaign and ad group from data-retrieval call 10 - to
  `xnurta-edit-ads` and follow its resolution, preview and confirmation rules. Its route
  limits decide what is possible:
  - SP keyword negatives: `negativeKeyword + create` (campaign level, SP only);
  - SB keyword negatives: `negativeKeyword + copy` to the ad group (SB accepts ad-group level
    only);
  - ASIN negatives: `negativeTarget + create` at ad-group level, and only into a
    product-targeting ad group - edit-ads refuses others;
  - harvest: `keyword + create` (SP / SB); pause: `keyword + updateStatus`.

  Suggest re-running in about 30 days.

## Example

> **Customer**: Review last month's search terms and show where the spend went.
>
> **AI**: Before calculating, please confirm three inputs. The product brand is Acme; the search
> terms also contain "acme pro" and "akme". Should both count as brand terms? What store-wide
> target ACOS should I use? If none is set, I can use the store's actual 30-day ACOS of 32%.
> Finally, is the product mature or in launch?
>
> **Customer**: Count both, use a 35% target, and treat it as mature.
>
> **AI**: Sep 10-Oct 9 search-term spend was $18,420. The most recent three days are excluded
> because orders may not be fully attributed.
> - **Spend distribution**: Core terms with at least three orders accounted for 41% of spend at
>   22% ACOS. Zero-order terms above the $14 one-order target-spend threshold accounted for 13%.
>   Another 24% went to many small zero-order terms; 52% of that traffic came from broad automatic
>   targeting.
> - **Branded / non-branded**: Brand terms accounted for 12% of keyword spend at 9% ACOS.
>   Non-brand ACOS was 3.4 times brand ACOS, so the account relies mainly on non-brand traffic.
> - **Zero-order waste**: Seven active exact keywords had no orders and spent $260 in total. For
>   example, "water jug" spent $41 and is a pause candidate. There were 63 negative candidates
>   with $2,410 spend; "replacement filter cartridge" spent $96 with no orders and is a negative
>   exact candidate. Twenty-one candidates belong to managed groups with Add negative targets on.
>   Four zero-order terms are also active exact keywords and were withheld from the negative list.
> - **Harvest candidates**: 18 terms. For example, "water filter pitcher" generated six orders
>   in 30 days at 24% ACOS from automatic targeting and has no dedicated exact keyword.
> - **Targeting fragmentation**: Of 310 enabled exact keywords, 190 generated at most three orders
>   in 30 days and spent only $640 in total.
>
> Would you like the complete list, and which candidates should be handed off for execution?

## Data boundaries

- **Search-term report only covers what it covers.** SP and SB search terms are both in it
  (verified 2026-10 on a store with SB: 99.8% of SB spend). SD has no search terms.
- **Attribution lag.** The default period stops 3 days before today; if the user insists on
  including recent days, warn that zero-order counts will be overstated.
- **Totals vs listed rows.** Zero-order small terms are derived as total minus listed parts,
  so they have an amount and a source split but no term list.
- **No bids.** This skill never suggests bid values or bid changes, including "lower the bid";
  a zero-order exact keyword gets "pause", not "bid down".
- **Not covered**: keyword-ranking feasibility, cannibalisation between variants, listing /
  stock / price attribution.

## Error handling

| Situation | Handling |
|---|---|
| A metric filter returns `unknown field` | The metric must also be in `metrics` (see `data-retrieval.md`) |
| A grouped query with a metric filter returns nothing | Metric filters apply after grouping - see `data-retrieval.md` |
| `hasNextPage` stays true | Keep paging; never classify on a partial page set |
| Very little spend in the period (a few hundred in store currency) | Say the sample is thin and the lists are indicative |
| Customer declines brand terms | Skip V2 and say why; keep the other views |
