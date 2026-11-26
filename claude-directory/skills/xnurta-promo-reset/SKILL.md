---
name: xnurta-promo-reset
description: >-
  After a promotion (Prime Day, Prime Big Deal Days, Black Friday / Cyber Monday, holidays),
  find every bid, budget, placement and AI managed-group setting a person changed for it,
  recover each pre-promo value from the operation log (or the customer's own sheet, export or
  screenshot) and restore them - all at once or paced by post-promo performance (now, over 2-3
  days, or held) - with reasons, a preview, an undo file and read-back; also audits bids after a
  promo schedule ends and recaps the promo. Use for "reset my promo changes", "revert Black
  Friday bids", "what did I change during the promotion?", "recap how Black Friday went" (recap
  only), "are my bids back to normal after the schedule?", "restore from my sheet". Not for before or during a promo (use
  xnurta-promo-prep / xnurta-promo-monitor), undoing AI's own adjustments (except a bid edit the
  user asks for after the bid audit), or edits with no promo behind them (use xnurta-edit-ads /
  xnurta-edit-ai-group).
metadata:
  version: 1.1.0
---

# Promo Reset

## Scope: an orchestration skill

This skill has no MCP tool of its own. It reads with three tools and writes with two
existing skills:

| Step | Tool | Owning skill |
|---|---|---|
| What changed, and what it was before | `get_operation_log` | [xnurta-query-operation-log](../xnurta-query-operation-log/SKILL.md) |
| Post-promo performance and the normal range | `get_ads_perf` | [xnurta-query-ads-performance](../xnurta-query-ads-performance/SKILL.md) |
| Internal ids, current values, groups, inventory | `get_entity_metadata` | [xnurta-query-entity-metadata](../xnurta-query-entity-metadata/SKILL.md) |
| Restore budgets, bids, placements, portfolio caps | `batch_update_ads` | [xnurta-edit-ads](../xnurta-edit-ads/SKILL.md) |
| Restore managed-group settings | `save_sp_sb_ai_managed_group` / `edit_sd_ai_managed_group` | [xnurta-edit-ai-group](../xnurta-edit-ai-group/SKILL.md) |
| End a promo schedule early (only when the user asks for that schedule) | `save_sp_sb_ai_group_schedule` (`operation: "delete"`) | [xnurta-edit-ai-group](../xnurta-edit-ai-group/SKILL.md) |

> **Dependency - install all five skills above alongside this one.** Skills install as
> sibling directories under your agent's skills root (`.claude/skills/<name>/` for Claude
> Code; see the installation notes in [README](../README.md)); the `../xnurta-.../` links in
> this file resolve against it. Every write in this skill goes through the owning write
> skill's rules - its confirmation protocol, its discriminator fields, its read-back. This
> file does not repeat them and does not relax them.
>
> **Read each owning skill when its step comes, not all up front**: a query skill (only the
> sections for the query at hand) when you pull that data; the write skills only when you reach
> the preview and the writes.

Auth, error envelopes, pagination, date limits and currency rules are in the base skills'
`references/platform-notes.md` - read it once from any of the three query skills (they ship the
same file). The cross-tool points that matter for this skill:

- **Ids differ by tool.** `get_ads_perf` returns Amazon ids; `get_operation_log` returns both
  (`entityId` internal, `amazonCampaignId` / `amazonEntityId` Amazon); writes need the internal
  id plus discriminator fields from `get_entity_metadata`. Join performance to the log on the
  Amazon id; write with the internal id.
- **Clocks differ by entity.** Ad-entity log rows are store-local for one `profileId`;
  SP/SB managed-group rows are UTC; **SD managed-group rows use an undocumented server clock**
  (see the operation-log skill). Performance dates are store days.
- **Amounts are local currency** on every tool here; a store's run never mixes currencies.

| Reference | Read it when |
|---|---|
| [`references/restore-list.md`](references/restore-list.md) | Building the restore list: which log queries, which rows count, how to get the pre-promo value, how a log row maps to a write |
| [`references/pacing-rules.md`](references/pacing-rules.md) | Deciding each item's suggestion: normal range, target ACOS, "clearly worse", step-down days, held items |
| [`references/execution-safety.md`](references/execution-safety.md) | Step 5, before the first write, and before continuing or undoing a reset: the plan file's columns, the stale check, row states, undo |
| [`references/from-file.md`](references/from-file.md) | The customer uploads their own record: reading the file, matching rows to objects, comparing with the account and the log |
| [`references/example-and-report.md`](references/example-and-report.md) | A full worked conversation; the `structured_report` JSON shape |
| [`references/html-report.md`](references/html-report.md) | Optional customer-facing HTML report; read only when a downloadable, shareable or print-ready report is needed |
| [`references/error-handling.md`](references/error-handling.md) | A write is refused, data is missing, or an answer does not fit the normal flow |

## Output language

The skill documentation and examples are written in English. Answer in the user's language and
pass the matching `language` value to `get_ads_perf` so returned display text is consistent.

Default to the Markdown report in chat. If the user asks for a report to download, share, print
or send to a customer, or the detailed tables are too long to scan comfortably in chat, also
create the static HTML report in [`references/html-report.md`](references/html-report.md). The
chat summary, preview and confirmation remain in chat; an HTML file never counts as approval
and never replaces the plan / undo file used to resume or undo a reset.

### Trial and demo documents

When the user asks for a trial run, demo, CSM handoff or example customer deliverable, run this
current workflow again against the data available now and render the resulting
`structured_report`. Do not relabel, restyle or carry forward result tables from an older trial.
An older document may provide the scenario only; re-query every displayed account value and
recompute every recommendation under the current rules. Mark simulated customer answers and
assumptions separately from queried facts, and include the run time, store, scope and data
windows. Trial mode is read-only unless the user separately confirms writes. If the current
workflow stops because required answers, operation-log history or comparison data are missing,
show that real stop and next step; never invent restore targets or later-stage results. Markdown,
HTML and any external document must all come from the same current-run `structured_report`.

## What it does, in one paragraph

A promo is set up by hand: budgets raised, bids raised, placement multipliers raised, managed
groups switched to Promotion sales boost with a looser target ACOS. After the
promo all of that has to come back, and people forget what they changed, forget to change it
back, or cut everything at once and lose traffic that was still converting. This skill
recovers every human promo change and its **pre-promo value** from the operation log and,
as the user chooses, either restores everything at once or looks at how each item did in the
days after the promo and proposes **restore now / step down over a few days / hold / you
decide** - each with the numbers behind it. If the customer kept their own record, they can
upload it and the restore targets come from the file instead. Nothing is written
until the user confirms, and an undo file is produced before the first write.

## Principles

1. **Ask before suggesting.** The window, how to restore and any follow-on deals change
   the answer (Step 1).
2. **Only restore what a person changed for the promo.** AI and rules keep doing their job;
   undoing their moves fights the AI (see [`restore-list.md`](references/restore-list.md)).
3. **Every suggestion carries its numbers.** "ACOS 119%, normal 34-41%, target 41%" - never
   a bare verdict.
4. **Never overwrite a later decision.** Anything changed again after the promo - by a person, Amazon's side, a rule, AI or a tool - is
   the customer's call.
5. **Undoable.** Undo file before the first write, read-back after every write.

## Workflow

### Step 1 - Fix the window, then ask in three groups

Resolve `profileIds` the usual way (`get_user_authorized_context`; one store unless the user
asks for several). **Run this skill one store at a time**: log timestamps are store-local
only when one `profileId` is passed (see the operation-log skill's "createdDate Timezone"),
and the window boundaries depend on it.

**The window comes first, and how depends on what the user already said:**

- **Dates given** (in the message, or the promo change log - below): before asking anything,
  pull the store's daily spend around those dates (`get_ads_perf`, `factEntity: campaign`,
  `select: ["date"]`) and propose the full window from the data: "spend was about 2x normal on
  10/6-10/7, and there were many changes on 10/5 and 10/8 - include those four days?" Promo
  adjustments routinely start a day or two before the event and end a day after.
- **No dates**: ask only which promo and roughly when it ran, in the same message as the
  groups below. Pull the data once they answer and propose the full window then. Never guess
  the dates.

Also say now if the managed groups are still in Promotion sales boost - that is often the
biggest single item (Step 2c).

**Then ask in one message, three groups** - skip anything the user already answered:

| Group | Ask | What it decides |
|---|---|---|
| 1. The promo and how to restore | The window above (confirm, or give it); restore **all at once, regardless of performance**, or **in batches by performance** (recommended) | The log window; whether Step 3 judges each item |
| 2. What is different now | Anything still running - a deal not ended, a product low on stock? After the promo: back to normal, or stay profitable at a target ACOS, and how much can ads spend per day? | Items to hold or restore first; the target the pacing uses (`references/pacing-rules.md` section 3); the budget check in Step 4 |
| 3. Your own record | A record of the pre-promo values - a sheet, a bulk export taken before the promo, a screenshot? | Whether the targets come from a file (below) |

**Follow-ups, only when they apply** - ask after the answers above, once each:

- **The window ended more than ~14 days ago** (either restore mode): the values have stayed
  that long, which may be deliberate. Say how long it has been and ask whether they kept them
  on purpose; restore only what they want back, and judge pacing on the most recent days
  ([`references/pacing-rules.md`](references/pacing-rules.md) section 1).
- **Black Friday / Cyber Monday**: December holiday demand usually stays above November's.
  Keep raises that are still converting until a date the user names (for example Dec 26),
  instead of stepping them down now? The answer feeds the "holiday hold" override in Step 3.
  Never assume it; with no answer, pace as usual.

**Their own record (group 3).** If they upload one - now or at any point - the restore targets
come from the file: follow [`references/from-file.md`](references/from-file.md) instead of
building targets from the log (Step 2 then only supplies the log's view for the comparison, the
"changed again later" check and the binding-budget note).

**If the user has the promo change log** from `xnurta-promo-prep` / `xnurta-promo-monitor`
(see that skill's `references/change-log.md`), its window is the **minimum**: from the earlier
of the warm-up start and the file's earliest `writtenAt` (prep writes group budgets and portfolio
caps before the warm-up) to the event end, plus the days the monitor wrote on. The data check
under "Dates given" still runs and may only widen it (people often adjust things a day before or
after the skills wrote anything): propose the wider of the two in one question, never a narrower
window than the file's. Use the file's pre-promo
value per object (the earliest confirmed write's `valueBefore`, with `needsReadBack` rows settled
first against the operation log - `references/restore-list.md` section 2) as a cross-check of the log's pre-promo value: a mismatch goes to "you
decide". The operation log stays the
source of the list - the file only covers what was written through those skills.

**Recap only.** When the user asks for a recap of the promotion ("how did Black Friday go?")
and not for a restore, ask only which promo and roughly when (if not given) - not the three
groups or the follow-ups; fix the window from the data as above, show the Promo Recap table
(pre-promo / promo / post-promo daily averages; Step 4 describes it) with the store-level reading of it, and stop:
no restore list, no plan file, no writes. Offer the reset afterwards ("want me to list what was
changed for it and restore it?").

### Step 2 - Build the restore list

**Look a few days before the window the user gave.** Prep often starts earlier than people
remember. Pull the 3-5 days before the start too; if changes there look like the same promo
(the same campaigns or groups, the same direction, a burst of them), show the counts and ask
whether to include them before building the list.

Full procedure, queries and edge cases: [`references/restore-list.md`](references/restore-list.md).
The rules that decide the result:

a. **Pull the log without a `changeBy` filter and classify `changedBy` yourself.** A row is a
   human change when `changedBy` is an email address or `Manual`; a row with
   `operationSource` = `MCP` was made through MCP, which is not always the promo skills. **With
   the promo change log**, include only the MCP rows that match a confirmed-write row in it
   (`written`, or `needsReadBack` settled against the log; object, `logField`, value and time -
   `references/restore-list.md` section 2, "Matching a log row to the change log"). Rows the
   log marks `planned`, `fulfilled`, `failed`, `skipped` or `changedByOthers` do not count as
   promo changes;
   other MCP rows go to "you decide". **Without it**, show the MCP rows' count and
   ask once whether they belong to the promo; until the user says yes they stay in "you
   decide". Rows this reset run wrote itself are removed by the stale check (Step 5). **Never
   filter with `changeBy: manual`** - the server rejects it (`references/restore-list.md`
   section 2).

   **`Amazon Console` is a source, not an operator** - the change came from Amazon's side, author
   unknown. **It is not in the default restore set**: list those rows in their own section as
   source-unknown, force `suggestion` to `customerDecides`, and restore only the ones the user
   confirms one by one - never via `restoreNow` or `stepDown`. Two cases change how you ask
   (`references/restore-list.md` section 2, "Amazon Console"):
   - **(Nearly) every setting change is `Amazon Console`**: say so with the counts and ask
     **once** whether those changes were theirs; only on a clear yes do they count like human
     rows, named "Amazon Console - confirmed by you" in the header.
   - **An object type changes at a pace no person works at** (an automated tool): recommend
     leaving that type out and let the customer decide - even after the yes above.

   The user may widen the sources (for example, "include API changes") - then say in the list header which sources
   are included.

b. **Pre-promo value = the `previousValue` of the first human change to that field inside the
   window.** Later changes inside the window do not matter, including a blanket "set
   everything to $100" the customer did on the last day. Skip creation rows - an empty
   `previousValue`, or `0` on budgets, bids, target ACOS and objective - those are not pre-promo
   values. **Except placement adjustments: `0` there is a real pre-promo value** (no uplift), so a
   top-of-search change `0 -> 100` is restored to `0`, never skipped
   (`references/restore-list.md` section 3).

c. **Managed-group settings go on the list too, and go first.** Objective (`optimizeType` in
   the log, `targetType` on SP/SB write), target ACOS (`acos`), AI personality, bid range
   (`bidRangeMin` / `bidRangeMax`), action-space switches and the group's **total budget**
   changed directly on a group do not revert by themselves. A **dated schedule** reverts
   automatically, but only after its end date: compare each schedule's `endDate` with the store's
   current date. Ended ones go under "ended with the schedule" for the schedule settings, then
   get the post-schedule bid audit (once per group, when none of its schedules is in effect - `references/restore-list.md` section 5); ones still
   running (a promo schedule that runs past the window, or one a person extended) go under
   "schedule still running, ends {date}", not as
   expired - see `references/restore-list.md` section 3. Judge each schedule, not the group: a
   group total budget changed directly in the same window still needs its own restore row.
   Weekly schedules (`timeType=2`) and schedules not from the promo are information only - no
   reminder row or audit of their own (`references/restore-list.md` section 3), but while in
   effect they delay the group's audit (section 5).
   Restore group settings before budgets: the objective and target decide how AI
   bids; the budget is only a ceiling.

   **Zero managed-group rows is not proof of zero changes** (the query can fail silently): with
   groups still on Promotion sales boost (`targetType: 3`) and no dated schedule in effect that carries goal `3`, say the history could not be read
   and treat those groups as "you decide" (`references/restore-list.md` section 1).

d. **Budgets: only `dailyBudget` counts.** In managed groups AI rewrites the day's spendable
   budget every hour (`changeField: currentBudget`, hundreds of rows per store in a few days).
   Those are not promo adjustments and must not be restored.

e. **Split the list:**
   - raised during the promo -> candidates for restore (Step 3 decides how)
   - a budget or bid raised by less than 10% -> **customer decides**; probably a routine
     adjustment, not a promo change - give the count and their daily spend
     (`references/restore-list.md` section 3)
   - lowered during the promo -> **customer decides**; often a deliberate cut (Step 3 notes
     whether the lower budget is actually binding)
   - changed again after the window - by anyone or anything (a person, Amazon's side, a rule,
     AI, a tool), except this run's own writes -> **customer decides**
   - a managed group's AI switched on or off in the window -> **customer decides**
   - created during the promo -> **customer decides** (pause or keep; there is no "before")
   - paused during the promo (campaign, ad group, product ad, keyword / target) -> **customer
     decides**; never re-enabled automatically
   - enabled during the promo (the same object types) -> **customer decides**, with its
     post-promo spend; never paused automatically - it keeps spending after the promo
   - current value already equals the pre-promo value -> skip, but count it

f. **Also on the list**: ad group default bids (SP / SD can be restored; SB has no write route)
   and portfolio budget caps - see [`references/restore-list.md`](references/restore-list.md).

### Step 3 - Decide each item's pace

**If the user chose "all at once"**, skip only the performance judgement: no per-item
post-promo `get_ads_perf` pull and no per-item pacing (the three store-level daily pulls for the
recap in Step 4 still run, unless the recap is skipped there). Everything that protects later decisions still
runs - the operation log is still queried through today (Step 2; that is how items changed
again after the window are found), and current values are still read and the stale check
still runs before every write (Step 5).

Every restorable item then goes back at once: **all managed-group settings on the list**
(objective, target ACOS, AI personality, bid range, action-space switches, total budget) and
every bid, budget, placement and portfolio cap raised during the promo. Unchanged: lowered,
changed again after the window, created, paused and enabled during the promo, and budgets and bids
raised by less than 10% still go to the customer, and a deal still
running is still held - restoring those would overwrite a decision rather than undo a promo
adjustment. The "is the lower budget binding" note still works: it comes from the
out-of-budget events in the operation log, not from performance data.

The rest of this step applies to "in batches by performance".

Read each item's **post-promo days**: full days after the window ends, no later than today - 2,
at most the latest 3 (`references/pacing-rules.md` section 1). A day inside the window is never
one of them - right after the promo there may be fewer than 3, or none. Compare them with the
item's own normal range and its target. Exact calculations: [`references/pacing-rules.md`](references/pacing-rules.md).

With 3 post-promo days, checked in this order - the first that applies wins
(`references/pacing-rules.md` section 5 is the rule; this is its summary):

| After the promo | Suggestion |
|---|---|
| Barely spent: under 10x the store's average CPC, whatever the clicks | Restore at once - nothing to judge |
| Clearly worse: ACOS **both** above its own normal range **and** above its target, on 20+ clicks and at least 2x the store's clicks per order (fewer clicks: "Otherwise") | Restore now |
| Above target, but in line with its own normal range | Restore as in "Otherwise"; note it runs above target anyway - not caused by the promo |
| Conversion rate still above its normal range | Step down: over 3 days if raised >= 2x, else 2 days |
| Otherwise | Restore at once if raised < 1.5x, else over 2 days |

An item with fewer than 5 orders in its normal period has no own range: it is compared with the
target only - "clearly worse" means ACOS above target (on the same clicks), and the two rows that
need an own range do not apply (`references/pacing-rules.md` section 2).

On SB, SD and Vendor, attribution lag turns an ACOS-based "restore now" into the "Otherwise"
row's pace (`references/pacing-rules.md` section 4).

Overrides, in this order: a product low on stock -> restore now; a deal still running -> hold
the items that advertise the deal ASINs until it ends; **holiday hold** (only if the user said
yes to it in Step 1) -> every item is held until the user's date except the clearly worse ones,
which are restored now (`references/pacing-rules.md` section 5). After a hold, items are judged
on the days after it ended.
Lowered during the promo -> customer decides, with a note on whether the lower budget is
binding (`references/pacing-rules.md` section 7) - if not, adding it back changes nothing;
point to stock / buy box / listing instead.

Too few post-promo days to judge (0, 1 or 2 - under 3, `references/pacing-rules.md` section 1):
the table above is not used - restore at once if raised < 1.5x, otherwise step down over 2
days, and say the data was too thin. The overrides still apply.

### Step 4 - Present the list, then preview

Show the customer, in this order:

1. **Header**: window, store, sources included, how many items in each group. When restoring
   from the customer's file: name the file and give matched / could not match / skipped
   counts.
2. **Managed-group settings** to restore (old -> new per field).
3. **Restore now - worse after the promo**, **step down over several days** (with each day's
   value), **restore in one step**, **on hold** (with the date) - each row: name, now -> target
   (or the daily steps), post-promo spend, reason with numbers. In "all at once" mode there is
   only **restore in one step** (and on hold): name, now -> target, reason "restored without
   performance evaluation, as requested", no performance columns. Use the customer names in
   `references/example-and-report.md` "Customer names for each group" everywhere - chat,
   template, HTML.
4. **You decide**: lowered, changed again later, created / paused / enabled during the promo,
   raised under 10%, Amazon-side and unmatched MCP changes.
5. **Money both ways**: per item and in total, what the restores save per day and the sales
   they are likely to give up (`references/pacing-rules.md` section 8). **Budget check**, when
   the user gave a daily budget in Step 1: post-promo daily spend minus those savings must fit
   it. If it does not, say by how much and which items would have to go further, lowest ROAS
   first - never cut on your own. In "all at once" mode there is no per-item performance pull, so no
   savings figure: compare the sum of the restored daily budgets with the user's budget instead
   and say that actual spend is usually lower.
6. **Search terms worth keeping** - listed for the customer, never written by this skill: search
   terms from the window with 3+ orders, 10+ clicks, ROAS at the target or better, not an ASIN,
   not already an exact keyword in that campaign; suggested exact bid = their promo CPC, capped
   at value per click x target ACOS. Adding them is `xnurta-edit-ads`, on the customer's word.
7. **Schedules**, checked against the store's date: still running (with the end date - not
   restored; a reminder row in the plan file until that date, when "continue the reset"
   confirms it ended and runs the bid audit - no schedule restore steps) and ended (settings reverted automatically,
   but run the bid audit once none of the group's schedules is in effect); weekly and non-promo
   schedules for information only. The group's direct settings are separate rows, judged now
   (`execution-safety.md` section 1).
8. **Change in the platform**: items with no MCP write route (SB ad group default bids), with
   their pre-promo value.
9. **No action**: already at the pre-promo value; archived.

Store-level recap in one compact table, **in both restore modes** (skipped only when restoring
from a file with no promo dates - `references/from-file.md` section 4): **pre-promo,
promo and post-promo** daily averages for spend, sales, orders, CPC, CVR, ACOS and ROAS. The
pre period is the 14 days before the window (the normal window of `pacing-rules.md` section 1,
pulled at store level here, so it exists in "all at once" mode too); the promo period is the
confirmed reset window; the post period is the **earliest** full days after the window, up to 3,
ending no later than today - 2 - so a recap asked weeks later still shows the days right after
the promo (per-item pacing keeps its own latest days, `references/pacing-rules.md` section 1). In
"all at once" mode there is no per-item pull, but this store-level one is cheap: three
store-level daily queries. With 1-2 post days, say how many; with 0, the post row reads "not available yet - from {window
end + 3 days}" and no change is computed against it. Rates
are recomputed from sums and the report names all three windows. Say when sales are still being
attributed (`references/pacing-rules.md` section 4, "Attribution lag"). If the store's
sales fell sharply after the promo and the drop sits in campaigns that are **not** spending
their budget, say plainly that budget is not the cause and suggest checking stock, buy box and
listing status - do not suggest raising budgets into it.

Then show the write preview and ask which rows to execute. The suggestion is a suggestion: the
customer can drop items, change a suggested pace, or stop at the list. Do not write from the
restore list alone; the customer's confirmation must identify the approved scope.

### Step 5 - Undo file, then write

**Read [`references/execution-safety.md`](references/execution-safety.md) before the first
write** of the run, and again before continuing or undoing a reset - it holds the full column
meanings, the stale-check procedure (clocks, matching this run's own rows), the row states and
undo. The rules below may never be skipped.

1. **Plan file first - it is both the undo file and the resume state.** Before the first
   write, re-read the current value of every item about to change (`get_entity_metadata`) and
   give the user a file (CSV / Excel), one row per object + field, with these columns:
   `runId`, `profileId`, `timezone`, `staleCheckFrom`, `objectType`, `writeRoute`,
   `internalId` + discriminators, `amazonId`, `name`, `field`, `prePromoValue`, `targetSource`,
   `valueBeforeRun` (**the undo value**), `steps`, `lastCompletedStep` (`0`),
   `expectedCurrentValue` (= `valueBeforeRun` at creation), `writtenAt`, `writeResult`,
   `readBackValue`, `rebasedAt`, `holdUntil`, `holdReason`, `bidAudit` (schedule reminder rows
   only), `status` (`planned`, or `held`).
   - **`staleCheckFrom` is recorded immediately before the first restore-list log query
     starts** - one value for every row of the run, never the time the plan file was made.
   - **Update the file after every write and read-back and hand it back to the user.** MCP keeps
     no state between conversations; without the file the run cannot be resumed reliably -
     say so and rebuild a fresh restore list instead.
2. **Stale check - before every write, including resumed steps and undo.** Both conditions:
   - **The value matches**: the current value equals `expectedCurrentValue`, compared as
     numbers at the field's precision.
   - **Nobody else wrote since**: the log for this object and field, from `writtenAt` (or
     `staleCheckFrom` for a row never written) to now, has no row except this run's own MCP
     writes. **Any other row, from any source, -> stop** (`stoppedChangedByOthers`; `customerDecides` for a row never written) and ask,
     even if the value has since been set back.

   A row not yet written whose current value differs from the log's last value goes to "you
   decide" (`customerDecides`). **Check per write batch, not per object**: one current-value read and one log query
   covering every object in the batch; an object that fails is dropped from the batch and the
   rest go ahead. **An empty log result can be a wrong filter**: a wrong id space returns 0
   rows with no error, so prove each write type's filter once - against the known window rows of
   its `targetSource: log` items. A file-only batch with no proven shape runs the check without
   `resourceIds` and must read it completely, or is not written. Query shapes and the proof:
   `execution-safety.md` section 2.
3. **Write in this order**, each through its owning skill and its confirmation rules:
   managed-group settings (`xnurta-edit-ai-group`; a group **total budget** rescales its
   campaigns, so re-read and re-base that group's campaign rows before writing them -
   `references/restore-list.md` section 4) -> portfolio caps -> budgets -> bids
   (keyword / target, then ad group default bids) -> placements (`xnurta-edit-ads`). Split
   batches by `campaignType` (budget and ad-group bid batches must be one type) and keep each
   under the write skills' caps.
4. **Today's step only.** For stepped items, write today's value; the later steps are a plan.
   MCP cannot schedule writes - the customer asks to continue the reset on each following day. On that
   day **drive the work from the plan file, not from a fresh restore list**: handle every row
   by its `status` (`execution-safety.md` section 3), running the stale check before each write.
   Do not write a step twice on the same store day.
5. **Read back** every written object and update its row (`execution-safety.md` section 3). An
   `ambiguous` result sets `needsReadBack`, never a completed step. Report what moved, what did
   not, and why.

**Undo the reset** = settle `needsReadBack` rows, mark every row whose step applied
`undoPending` (no restore step is written for it again), then write `valueBeforeRun` back -
group totals first, then the re-based campaign rows, then bids and placements - through the same
stale check, preview and confirmation; confirmed rows become `undone` and are never written
again; an ambiguous or failed undo stays `undoPending`. Schedule reminder rows stay `held`, so the
bid audit still runs. A later "continue the reset" says the reset was undone and only finishes the undo,
bid audit and reminders; resetting again is a new run with this plan file, which recognises the
earlier restore and undo writes (`execution-safety.md` section 4).

**Held items and schedules that end later** stay in the same plan file (`status: held`,
`holdUntil`); come back with "continue the reset" and that file - not a new run, which would not
recognise this reset's earlier writes (`execution-safety.md` section 3). A held item is judged
again then; a held schedule row is never written - once it has ended, its group gets the bid
audit (`references/restore-list.md` section 5), the result goes in `bidAudit`, and the row becomes
`ended` - or, while another schedule of the group is in effect, `scheduleStillRunning` and the
row stays `held` to the date section 5 gives.

A waiver such as "execute this batch without another confirmation" follows the owning write
skill's waiver rules exactly - the scope is
what the user said, and the verification still runs.

## Example

A full worked conversation is in [`references/example-and-report.md`](references/example-and-report.md).

## Output templates

### markdown

```markdown
# Promo Reset - {store}
**Promotion window**: {start} ~ {end} ({timezone})  **Restore mode**: {performance-based batches / restore all at once}
{Performance-based mode only: **Performance window**: {post start} ~ {post end}}
**Changes included in this run**: changes made by people in Xnurta{ + changes the promo assistant made and that match your promo change record - only when you shared that record}{ + other sources you approved}
{Without the promo change record and with assistant-made changes in the window: **Changes made by the AI assistant**: {n} - listed under "You decide" until you say they belong to this promotion}
{If any Amazon-side rows exist: **Amazon-side changes (source unknown, not restored by default)**: {n} items — listed below for your decision}
{If the customer confirmed them as theirs: add "Amazon Ads console changes (confirmed by you)" to **Changes included in this run** and omit the line above}
{Notes about insufficient data, partial coverage, UTC timestamps, or other limits}

## Summary
| Group | Count | Handling |
|---|---|---|
| Managed-group settings | {n} groups | Restore objective, target ACOS, and other changed settings |
| Restore now - worse after the promo | {n} | ... |
| Step down over several days | {n} | ... |
| Restore in one step | {n} | ... |
| On hold | {n} | Deal still running / holiday hold until {date}. Kept in the plan file |
| You decide | {n} | Reduced during promo / changed again later / created, paused or enabled during promo / raised under 10% / Amazon-side |
| Schedule still running | {n} | Not restored; ends {date}. Kept in the plan file - after that date, say "continue the reset" with the same file |
| Schedule ended | {n} | Schedule settings reverted automatically; audit current bids against the normal range |
| Schedules for information only | {n} | Weekly or not from this promo; not handled - while in effect they delay the group's bid audit |
| Change in the platform | {n} | No MCP write route (SB ad group default bids) |
| No action | {n} | Already at original value / archived |

{In all-at-once mode, keep only Managed-group settings, Restore in one step, On hold, You decide, Schedule still running, Schedule ended, Schedules for information only, Change in the platform and No action. Keep the Promo Recap (omitted for a file restore with no dates); omit money both ways, search terms and the post-promo spend column; use the reason "restored to the pre-promo setting without performance evaluation, as requested".}

Store context (both modes; omitted for a file restore with no dates): pre-promo / promo / post-promo daily averages are shown below.
{Budget check, when a daily budget was given: after the restores about {x} a day against your {budget} - fits / {n} over}

## Managed-Group Settings
| Managed group | Objective | Target ACOS | Other settings |
## Restore Now - Worse After the Promo
| Object | Current | Restore to | Post-promo spend ({n} days) | Reason |
## Step Down Over Several Days
| Object | Current | Daily steps | Post-promo spend ({n} days) | Reason |
## Restore in One Step
| Object | Current | Restore to | Post-promo spend ({n} days) | Reason |
## On Hold
| Object | Pre-promo | Current | Held until | Why |
## You Decide
| Object | Pre-promo | Current | Situation |
## Money Both Ways (performance-based mode only)
| | Per day |
|---|---|
| Spend the restores save | {x} |
| Sales likely given up | {y} (ROAS {r}{, above your target - these settings were working}) |
## Search Terms Worth Keeping (performance-based mode only; not written by this skill)
| Search term | Campaign | Orders | Clicks | ROAS | Suggested exact bid |
## Schedules and post-schedule bids (checked against the store date {today})
| Managed group | Phase | Window | Goal / target ACOS | State: running (ends {date}) / ended / weekly or not from this promo (information only) | Bid audit (once per group) | What happens |
## Promo Recap (both modes, omitted for a file restore with no dates; daily averages)
| Phase | Dates | Spend | Sales | Orders | CPC | CVR | ACOS | ROAS |
{When sales are still being attributed: say which days will still fill in, and until when}
## Change in the Platform
| Object | Pre-promo | Current | Why |
## No Action
| Object | Current | Reason (already at original value / archived / ...) |

---
_Generated: {timestamp} - Data source: Xnurta MCP - Skill: xnurta-promo-reset v{version}_
```

Name every object by its name (`campaignName`, `aiGroupName`, keyword text), never by an
internal id; an export adds the **Amazon** id column (see the base skills' platform-notes ->
"Naming things in your answer").

### structured_report

The JSON shape is in [`references/example-and-report.md`](references/example-and-report.md).

### optional HTML report

Build it only from the finalized `structured_report`; do not recalculate or reinterpret the
restore list while rendering. Show plan-file delivery and stale-check status, but keep the plan
/ undo file as a separate machine-readable attachment. Follow
[`references/html-report.md`](references/html-report.md).

## Data boundaries

- **Only what the log recorded** - unless the customer uploads their own record. A change made
  where the log does not see it, or before the log's 15-month lookback, can only be restored
  from such a file.
- **A customer file is the customer's record, not Amazon's.** Rows are matched to live objects
  and compared with the log; the values themselves are taken as given, and where they differ
  from the log both are shown.
- **SB placement writes switch the campaign to custom bidding** (`bidOptimization=false`) as a
  side effect - say so before writing an SB placement (see `xnurta-edit-ads`
  `references/write-campaign.md`). Where AI placement bid optimization is on, a restored
  placement value may not be what ends up live.
- **Bids under AI management may not stick.** A human bid change on a keyword in a running
  managed group can be re-optimised by AI after it is restored; say so for those rows.
- **Inventory is refreshed once a day** (Seller profiles with SP-API only); FBA `0` is not a
  stock-out when a merchant-fulfilled offer exists - report it as a lead.
- **Some cut-offs are adjustable defaults**, not store facts - listed in
  [`pacing-rules.md`](references/pacing-rules.md); show the numbers so the customer can override.
- **No scheduling.** Stepped restores need the customer to come back each day.

## Error handling

Situation-by-situation handling (a write refused, data missing, an answer that does not fit) is in [`references/error-handling.md`](references/error-handling.md).

## Not covered

- Preparing a promo - use `xnurta-promo-prep`; adjusting during it - use
  `xnurta-promo-monitor`.
- Undoing AI or automation-rule changes - except a bid edit the user asks for after the
  post-schedule bid audit (`references/restore-list.md` section 5).
- Restoring on-off states automatically: pauses made during the promo are listed for the
  customer to decide, and re-enabled only item by item on request.
- SB ad group default bids: listed with their pre-promo value, but there is no MCP write route
  for them - the user changes them in the platform. SP / SD default bids are restored.
- Adding keywords. Step 4 only lists the window's search terms worth keeping (a short list with
  fixed thresholds, `references/pacing-rules.md` section 1); a full harvest with negatives and
  per-term rules is `xnurta-search-term-diagnosis`, and adding the keywords is
  `xnurta-edit-ads`.
