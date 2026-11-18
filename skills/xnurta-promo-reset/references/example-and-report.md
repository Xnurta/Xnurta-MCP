# Promo Reset - worked example and structured report

## Example

> **Customer**: Reset the changes made for Prime Big Deal Days.
>
> **AI**: Please confirm a few things. 1) Store data suggests the promotion ran Oct 6-7, with many
> changes also on Oct 5 and Oct 8. Should all four days be included? Should everything be restored
> at once, or in batches based on performance (recommended)? 2) Are any deals still running or
> products low on stock? After the promotion, back to normal, or stay profitable at a target
> ACOS - and how much can ads spend per day? 3) Do you have a record of the pre-promo settings
> (a sheet or a bulk export from before Oct 5)?
>
> **Customer**: Include Oct 5-8, restore in performance-based batches. No deals are continuing.
> Back to normal, about $3,000 a day. No record.
>
> **AI**: From Oct 5-8 the log shows budget changes on 88 campaigns, all recorded as made in the
> Amazon Ads console, with no named author. Were these yours?
>
> **Customer**: Yes, my team made them.
>
> **AI**: Then they are treated as yours. Based on performance from Oct 9-11:
> - **Restore now - worse after the promo: 16**. For example, Snacks-SP-Exact-Keyword goes from $100 back to $50. Its
>   post-promo ACOS was 119%, above both its normal 34-41% range and its 41% target. These 16
>   campaigns spent $1,533 over the three post-promo days.
> - **Step down over several days: 13**. For example, Noodles-SP-Exact-Keyword goes from $100 to
>   $78, then $57, then $35. Its post-promo conversion rate was 13.9%, still above its normal
>   8.3-9.7% range.
> - **Restore in one step: 7**. Performance was normal or spend was too low to evaluate.
> - **You decide: 49**. Four were changed again after Oct 8; 45 were reduced during the
>   promotion and will not be increased automatically.
>
> After these restores, spend comes to about $2,700 a day, inside your $3,000.
> Below is the write preview. Which should I execute: (a) everything suggested (recommended) /
> (b) only "Restore now" / (c) none for now? Before the first write I save the plan file, which
> is also your undo file.
>
> {write preview: today's value for every row to be written}

## structured_report

```json
{
  "store": {"profileId": "...", "profileName": "...", "timezone": "..."},
  "window": {"start": "...", "end": "...", "clock": "store-local"},
  "mode": "performanceBased|allAtOnce|recapOnly",
  "postWindow": {"start": "...", "end": "..."},
  "targetSource": "log|file|mixed",
  "file": {"name": null, "rowsRead": 0, "matched": 0, "couldNotMatch": [], "unitsConfirmed": null},
  "sources": ["email", "Manual", "MCP"],
  "amazonSideSources": ["Amazon Console"],
  "groups": [{"aiGroupName": "...", "field": "targetType|acos|aiPersonality|bidRange|totalBudget|<action-space switch>", "now": "...", "restoreTo": "...", "basis": "...", "suggestion": "restoreNow|stepDown|restoreOnce|hold|customerDecides|skip", "steps": [], "decisionReason": null, "holdUntil": null, "holdReason": null}],
  "schedules": [{"aiGroupName": "...", "scheduleId": "...", "phase": "single|warmup|event", "startDate": "...", "endDate": "...", "storeDate": "...", "timeType": 1, "origin": "promo|other", "state": "running|ended|unknown|null", "bidAudit": {"state": "withinRange|outsideRange|notVerifiable|noRange|scheduleStillRunning", "rangeType": "fixed|coefficient|none|null", "outsideCount": 0, "checkedCount": 0, "note": "..."}, "note": "..."}],
  "noAction": [{"objectType": "...", "name": "...", "now": "...", "reason": "atOriginal|archived|..."}],
  "items": [{"objectType": "campaignBudget|keywordBid|targetBid|adGroupBid|placement|portfolioBudget|paused|enabled", "targetSource": "log|file", "name": "...", "amazonId": "...",
             "source": "person|mcpMatched|mcpUnmatched|amazonConsole|amazonConsoleConfirmed", "changedBy": "...",
             "prePromo": 50, "now": 100, "restoreTo": 50, "steps": [75, 50], "suggestion": "restoreNow|stepDown|restoreOnce|hold|customerDecides|skip",
             "decisionReason": null, "holdUntil": null, "holdReason": null,
             "reason": "...", "postDays": 3, "postSpend": 0, "postAcos": null, "normalAcos": [34, 41], "targetAcos": 41,
             "binding": null, "savedPerDay": 0, "salesGivenUpPerDay": 0}],
  "notWritable": [{"objectType": "sbAdGroupBid|...", "name": "...", "prePromo": 0, "now": 0, "reason": "..."}],
  "moneyBothWays": {"savedPerDay": 0, "salesGivenUpPerDay": 0, "givenUpRoas": null, "givenUpAboveTarget": false},
  "budgetCheck": {"userDailyBudget": null, "basis": "savings|sumOfBudgets", "dailyAfterRestore": null, "fits": null, "shortBy": null},
  "searchTermsToKeep": [{"searchTerm": "...", "campaignName": "...", "orders": 0, "clicks": 0, "roas": 0, "suggestedExactBid": 0}],
  "execution": {"planFile": null, "checkedFrom": null, "lastChecked": null,
                "counts": {"planned": 0, "held": 0, "inProgress": 0, "done": 0, "needsReadBack": 0, "failed": 0, "stoppedChangedByOthers": 0, "skipped": 0, "customerDecides": 0, "undoPending": 0, "undone": 0, "ended": 0}},
  "storeContext": {"windows": [{"phase": "pre|promo|post", "start": "...", "end": "...", "days": 0, "dailySpend": 0, "dailySales": 0, "dailyOrders": 0, "cpc": null, "cvr": null, "acos": null, "roas": null}], "attributionNote": "..."}
}
```

Field notes:

- `source` says where the change came from: a person, an MCP write matched to the promo
  change log, an MCP write not matched (it stays in "you decide" until the user says it belongs
  to the promo), Amazon's side (`Amazon Console`, author unknown), or Amazon's side confirmed
  by the user (Step 2a).
- `decisionReason` is set only when `suggestion` is `customerDecides`: `lowered`,
  `changedAfterWindow`, `createdInWindow`, `pausedInWindow`, `enabledInWindow`, `aiSwitched`,
  `aiChangedAfter`, `smallRaise` (under 10%), `amazonSide`, `mcpUnmatched`,
  `historyUnreadable`, `fileMismatch`.
- `holdUntil` (store date) and `holdReason` (`dealRunning`, `holidayHold`, `waitForSchedule`)
  are set only when `suggestion` is `hold`; they become the plan file's `holdUntil` /
  `holdReason`. A running schedule is not an item: it is in `schedules` (`state: running`),
  and its plan-file reminder row uses `holdReason: scheduleRunning` (`execution-safety.md`
  section 1).
- `binding` (`true` / `false` / `null` = cannot tell yet) is set only on lowered budgets
  (`pacing-rules.md` section 7) - in both modes.
- `notWritable` lists items with a pre-promo value but no MCP write route (SB ad group default
  bids); the user changes them in the platform.
- `moneyBothWays`, `savedPerDay`, `salesGivenUpPerDay` and `searchTermsToKeep` are filled only in
  "in batches by performance" mode (`pacing-rules.md` section 8; SKILL Step 4); `null` / empty
  in "all at once" mode. `budgetCheck` is `null` when the user gave no daily budget; its
  `basis` is `sumOfBudgets` in "all at once" mode (SKILL Step 4).
- `execution` mirrors the plan file once it exists (`execution-safety.md`): its name, the
  stale-check start (`staleCheckFrom`), the last check, and how many rows are in each status.
  Before the plan file exists every count is 0 and `planFile` is `null`.
- `schedules[]` lists every schedule read. Only `timeType: 1` + `origin: "promo"` rows count:
  a running one gets a plan-file reminder row, and they carry the group's audit. Weekly
  (`timeType: 2`, `state: null` - no dates) and `origin: "other"` rows are information only,
  with `bidAudit: null`; while in effect they delay the group's audit (its promo rows show
  `scheduleStillRunning`, `note` the date it waits for - `restore-list.md` section 5).
- `schedules[].bidAudit` is the group's one audit (`restore-list.md` section 5), the same on each
  of its promo schedule rows. `rangeType` is `none` with `noRange` (bid range off) and `null`
  when the range was not read (`scheduleStillRunning`). It is evidence only, not approval
  to write a bid. `storeContext.windows` is filled in both restore modes, and in a recap-only run
  (`mode: "recapOnly"`, where `items`, `groups` and the rest stay empty), from three named
  windows; every rate is recomputed from summed metrics. The one exception: restoring from a
  file with no promo dates skips the recap - `storeContext` and `postWindow` are `null`
  (`from-file.md` section 4).

## Customer names for each group

One name per value, used the same way in the chat summary, the markdown template, the HTML
report and the example. Never show the raw value.

| `suggestion` (or section) | Customer name | What it means |
|---|---|---|
| group settings | Managed-group settings | Objective, target ACOS and other group settings go back first |
| `restoreNow` | Restore now - worse after the promo | Clearly worse than its normal range and its target: back to the pre-promo value today |
| `stepDown` | Step down over several days | Raised 1.5x or more, or still converting above normal: one step a day, today's step only |
| `restoreOnce` | Restore in one step | Performing normally, too little spend to judge, worse on ACOS while SB / SD / Vendor sales are still arriving (raised < 1.5x), or "all at once" mode: back to the pre-promo value today |
| `hold` | On hold until {date} | A deal still running, the holiday hold, or a group setting you chose to keep until its schedule ends (a running schedule itself is listed under schedules) |
| `customerDecides` | You decide | Lowered, changed again later, created / paused / enabled in the window, small raises, Amazon-side or unmatched changes |
| `skip` | No action | Already at the pre-promo value, or archived - listed in `noAction[]` only, never also in `items[]` |
| schedules | Schedule still running / Schedule ended / For information only | Checked against the store date; weekly schedules and ones not from this promo are for information only |
| `notWritable` | Change in the platform | No MCP write route (SB ad group default bids) |

"Restore now" and "Restore in one step" both write the pre-promo value today; the names differ
because the reason differs - say the reason on every row.

In every mode `postWindow` is the store-level post window - the dates of `storeContext`'s `post`
entry (the earliest post days - SKILL.md Step 4), `null` when there are no post days yet. With
`mode: "allAtOnce"`: `storeContext` is still filled (the recap shows in both modes, except a
dateless file restore; it is store-level, three daily queries); each item's
`postDays`, `postSpend`, `postAcos`, `normalAcos` and `targetAcos` are `null`, while `steps` keeps its one
step (the pre-promo value, e.g. `[50]`) like any restore-at-once item, so the result feeds the
plan file, resume and read-back directly; `suggestion` is
only `restoreOnce`, `hold`, `customerDecides` or `skip`; the `reason` of a restored item says
the user chose to restore without judging performance.

`postDays` is how many post-promo days the item was judged on: full days after the window, ending
no later than today - 2, at most 3 (`pacing-rules.md` section 1) - so 0-3. `postSpend` and
`postAcos` are summed over those days. With `postDays` under 3 the item follows the thin-data
rule (not the section 5 decision); with `postDays: 0` both are `null`.

In **either** mode, an item whose `changedBy` is `Amazon Console` carries `suggestion` =
`customerDecides` regardless of what its performance would otherwise suggest, and its
`reason` says the change came from Amazon's side with no known author. In the JSON result
those rows' sources are listed under `amazonSideSources`, separate from `sources`. **The one
exception** is a run where the customer confirmed the `Amazon Console` changes as theirs (Step
2a): then those rows are paced like human rows, `Amazon Console` moves into `sources`, and
`amazonSideSources` is empty.
