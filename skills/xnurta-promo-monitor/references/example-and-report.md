# Promo Monitor - worked example and structured report

## Example

> **Customer**: Black Friday day 1 - how is it going? Should I add budget?
>
> **AI**: (Plan from your prep log: Nov 20-Dec 1, $4,500 a day, ACOS no more than 35%.) It is
> 13:20 in Los Angeles. What do you want right now: push harder, slow down, push specific ASINs,
> or stay inside 35%? Has the $4,500 changed? Anything selling out?
>
> **Customer**: Push harder. Same budget. Nothing new.
>
> **AI**: By 11:00 (the latest hourly data) the store spent $1,640 - 2.6x a normal day by that
> hour. At this pace the day ends near $4,300, inside your $4,500.
> - **Changed today**: someone paused 2 product ads for B0xxxxx at 08:12 (your account). That
>   ASIN sold 11 units through ads yesterday. Was it deliberate?
> - **Winners running out (3)**: e.g. "Dog Food - Exact" ACOS 22% today on 14 orders, $38 of
>   $250 left, runs out around 14:00 at this pace. Suggest $250 -> $325 (+30%).
> - **Managed groups (2 short of budget)**: "Dog Food AI" is converting at 24% against its
>   schedule target of 30% and its campaigns ran out of budget at 12:05. Suggest group total
>   $900 -> $1,170.
> - **Spending, not converting (4 targets)**: 20-46 clicks today, no order. With "push", I leave
>   them for now; they are on the watch list for 18:00.
> - **Too few clicks to judge**: 31 campaigns.
>
> Together the raises add $410 to the day, still inside $4,500. Below is the write preview, in
> batches. Which should I write: (a) all of them (recommended) / (b) only the campaign budgets /
> (c) none for now?
>
> {write preview: the Moves table of the output template, by batch}

## structured_report

```json
{
  "store": {"profileId": "...", "timezone": "...", "storeType": "seller|vendor"},
  "now": {"date": "...", "hour": 13, "latestDataHour": 10, "settledThroughHour": 9},
  "generatedAt": "...",
  "scope": {"type": "store|mainCampaigns|named", "campaigns": 0, "ofCampaigns": 0, "named": []},
  "event": {"name": "...", "start": "...", "end": "...", "day": 1, "days": 12, "dayType": "warmup|sale"},
  "goal": ["push", "slow", "asins", "limit"],
  "budget": {"mode": "dailyCap|windowTotal", "eventBudget": 0, "dailyCap": null, "todayBudget": 0, "windowSpent": null, "windowRemaining": null},
  "limitAcos": null, "limitBasis": "hardLimit|nonBrandLimit|ceiling|storeFallback|null",
  "raiseAcos": null, "holdUpperAcos": null,
  "brandCheck": {"brandCpcChange": null, "brandClickShare": null, "brandClickShareNormal": null, "topOfSearchCpcChange": null, "verdict": "steady|possibleAttack|unknown", "note": "..."},
  "yesterdayReview": {"generated": true, "date": "...", "baselineStart": "...", "baselineEnd": "...", "metrics": [{"name": "spend|sales|orders|cpc|cvr|acos|budgetUsage", "yesterday": null, "baselineDailyAvg": null, "changePct": null}], "anomalies": [{"campaignName": "...", "change": "...", "evidence": "...", "todayAction": "..."}], "todayPriorities": ["..."]},
  "groups": [{"aiGroupName": "...", "state": "shortOfBudget|overTarget|onTrack", "targetInEffect": 0, "targetFrom": "schedule|group", "acosSettled": null, "settledClicks": 0, "totalBudget": 0, "effectiveTotalBudget": null, "effectiveTotalKnown": true, "budgetRedistributeStatus": null, "enabledCampaignCount": null, "ranOutAt": null}],
  "plannedBudgets": [{"campaignName": "...", "targetDate": "...", "role": "warmup|early|peak|between", "multiple": 0, "current": 0, "planned": 0, "status": "planned|fulfilled|skipped|missed", "note": null}],
  "pace": {"spendSoFar": 0, "normalByThisHour": 0, "ratio": 0, "projectedDay": 0},
  "changedToday": [{"time": "...", "who": "person|amazonSide|ai|rule", "entity": "...", "name": "...", "from": "...", "to": "..."}],
  "campaigns": [{"name": "...", "amazonId": "...", "state": "winnerRunningOut|burning|notConverting|clearlyOverLimit|overLimitWatching|held|onPace|underSpending|mixed|tooFewClicks|leftAlone|managed",
                 "watchReason": "overLimit|overFloor|null", "spendToday": 0, "ordersSettled": 0, "acosSettled": null, "budget": 0, "remaining": null, "usageUpdatedTime": "...", "runOutHour": null}],
  "moves": [{"objectType": "scheduleTarget|groupTotalBudget|campaignBudget|keywordBid|targetBid|placement|status", "name": "...", "now": 0, "proposed": 0, "reason": "...", "status": "ready|needsYes|needsReview"}],
  "executed": [{"objectType": "...", "name": "...", "before": 0, "after": 0, "result": "written|failed|needsReadBack|needsReview|notWritten", "reason": "waitingForYes|guard|declined|changedByOthers|null"}],
  "watch": [{"name": "...", "state": "...", "why": "..."}],
  "stock": [{"asin": "...", "coverDaysAtTodayPace": null, "eventDaysLeft": 0, "restockSellableInDays": null, "inbound": null, "protection": {"budgetCut": null, "bidCuts": [], "requiresConfirmation": true}}],
  "nextCheck": "..."
}
```

Field notes:

- `latestDataHour` is the last hour used for spend and pace; `settledThroughHour` the last
  hour used for orders and ACOS (`pace-and-states.md` section 1). At 13:20 they are 10 and 9.
- `limitBasis` says which rung of `pace-and-states.md` section 6 set `limitAcos`.
- `brandCheck` is the first-regular-check-of-the-day line (`pace-and-states.md` section 2); `null`
  values when the brand names are not known.
- `yesterdayReview.generated` is true only at the first regular check of the store day (at or
  after 08:00, never the day-switch check). Later checks in the same conversation reuse it; a
  new conversation the same day regenerates it only if the user asks (`pace-and-states.md`
  section 2). `baselineStart` / `baselineEnd` are the seven days before yesterday, or the seven
  normal days before the warm-up when yesterday was an event day; orders, sales and ACOS for
  yesterday are provisional.
- `groups` holds the managed-group states (`pace-and-states.md` section 7), with
  `effectiveTotalBudget` the total with budget by performance (`moves.md` section 4; `null` when
  it is off or unknown) and `effectiveTotalKnown` `false` only when budget by performance is on
  but its size cannot be read (no group-total raise is proposed); `budgetRedistributeStatus` and
  `enabledCampaignCount` are what the amount-mode size used (`null` in percentage mode or when off); `plannedBudgets`
  the prep `planned` rows for today and tomorrow and what happened to them (`missed` = a
  `planned` row whose day has come and no check wrote it - `moves.md` section 1).

**Customer names.** Campaign states use the names in `pace-and-states.md` section 6
(`burning` is shown as "Spending, no orders yet"); group states: "Short of budget", "Over its
target", "On track". Moves: `ready` -> "Ready", `needsYes` -> "Needs your confirmation".
Moves and executed: `needsReview` -> "Needs review - change it in the platform". Executed: `written` -> "Applied and verified", `failed` -> "Failed", `needsReadBack` ->
"Awaiting verification", `notWritten` with `reason` `waitingForYes` -> "Waiting for your
confirmation", `guard` -> "Blocked by a safety rule", `declined` -> "Not applied, as you chose",
`changedByOthers` -> "Changed by someone else - not overwritten". Watch list: "Watch".
`effectiveTotalKnown: false` -> "Cap with budget by performance: unknown, may be higher". Never
show a raw value.
