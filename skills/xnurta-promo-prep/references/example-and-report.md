# Promo Prep - worked example and structured report

## Example

> **Customer**: Black Friday is coming. Get my ads ready.
>
> **AI**: A normal day here is about $1,800 of ad spend. Four questions first:
> 1. **Dates**: Black Friday is Nov 28 and Cyber Monday Dec 1 (fixed dates); Amazon's sale
>    window around them is set by Amazon - which dates has it announced for your marketplace?
>    Warm-up days before it: (a) 3 days (recommended) / (b) none / (c) other.
> 2. **Ad budget per event day**: (a) $3,600, 2x normal (balanced) / (b) $2,340, 1.3x /
>    (c) your own number. A cap for every day, or a total for the whole window?
> 3. **Goal**: (a) maximum sales / (b) sales but stay profitable. Any hard limit, e.g. "ACOS no
>    more than 35%"?
> 4. **Target and margin**: keep each managed group's own target ACOS (recommended), or one
>    target for the event? Your margin, or a ROAS you will not go below?
>
> **Customer**: Nov 20-Dec 1, warm-up from the 17th. $4,500 a day, a cap. Maximum sales, ACOS
> no more than 35%. Keep the groups' targets. Margin about 40%.
>
> **AI**: Health check first:
> - **Stock**: 2 of 38 advertised ASINs will run out before Dec 1 at event pace (one has 9 days
>   of cover and nothing inbound). I will not raise their campaigns.
> - **Budget ceilings**: the "Dog Food" portfolio has a $3,000 monthly cap and has already used
>   $2,410 - it would stop those campaigns on day one. Raise it?
> - **Managed groups**: 14 SP groups. One already has your "BF_Deal" schedule inside the window
>   and one has no room for another schedule; the other 12 have none. 1 SD group (no schedules
>   for SD).
> - **Reference event** (the most recent: Prime Big Deal Days, Oct 7-8, against Sep 23-Oct 6):
>   spend 2.4x normal, CPC +18%, conversion +31%.
>
> A few more, all optional: any deals or campaigns to leave alone? Your brand names - I found
> "PawPrime" on your ASINs. Any stock you know is low or arriving?
>
> **Customer**: Deals on the dog-food line. Leave the "BF_Deal" campaigns alone. Brand is
> PawPrime. Nothing on stock.
>
> **AI**: From your store's total sales day by day last Black Friday:
>
> | Plan for the day | Dates | Multiple | Day budget |
> |---|---|---|---|
> | Warm-up | Nov 17-19 | 1.3x | $2,340 |
> | Early deals | Nov 20-27 | 1.4x | $2,520 |
> | Black Friday | Nov 28 | 2.4x | $4,320 |
> | Weekend | Nov 29-30 | 1.9x | $3,420 |
> | Cyber Monday | Dec 1 | 2.3x | $4,140 |
>
> Change any of these if you know better - a deal day, for example.
>
> **Customer**: Looks right.
>
> **AI**: Which managed groups should get Promotion sales boost? Only the head groups use it,
> so the whole account does not surge together. Candidates - the 4 groups that make up 80% of
> managed-group spend over the last 30 days:
>
> | Group | 30-day spend | Sales | Orders | ACOS |
> |---|---|---|---|---|
> | Dog Food AI | $9,800 | $41,200 | 610 | 23.8% |
> | Cat Food AI | $6,900 | $25,600 | 402 | 27.0% |
> | Treats AI | $4,100 | $14,900 | 251 | 27.5% |
> | Dog Food - Brand AI | $3,300 | $19,400 | 330 | 17.0% |
>
> "Dog Food - Brand AI" is almost all PawPrime searches - treat it as brand defence (Drive
> growth) instead? (a) the first 3 as head groups, brand group as defence (recommended) / (b) all
> 4 / (c) your own list.
>
> **Customer**: (a).
>
> **AI**: Plan: the peak day is 2.4x a normal day and buys about 46 event clicks per main ASIN -
> **balanced**.
> - **12 event schedules**, Nov 20-Dec 1: the 3 head groups you confirmed use Promotion sales
>   boost; the other 9 use Drive growth. Targets use each group's actual 30-day ACOS, never
>   below its current target: head groups start at 1.5x (Dog Food AI: 23.8% -> 35.7%, cut to
>   your 35% limit), the brand-defence group at 1.0x, the others at 1.2x; groups with fewer than
>   5 orders fall back to their current target and are labelled. For the 3 head groups only,
>   every AI adjustment intensity is set to at least 4 (settings already above 4 stay
>   unchanged) and budget by performance is on at +100%, which lets the AI spend **on top of**
>   the group total on strong days - the 3 head groups' totals are $900 a day, so up to $900
>   more; that is counted against the extra money you allow each day. The other groups keep
>   theirs. Plus a warm-up schedule Nov 17-19 - your warm-up days, drive growth. Every schedule
>   ends with the event on Dec 1.
>   I will write one group first for you to check in the platform, then the other 11.
> - **2 of the 14 groups skipped**: one already has 4 schedules (none ended yet), one overlaps
>   your existing "BF_Deal" schedule.
> - **Outside groups**: 9 campaign budgets by the day plan above, 41 bids on proven keywords
>   (+30%), top of search on 4 campaigns where it converts 1.6x the campaign average (up to +60%). The
>   non-brand campaigns' raises go in on Nov 16, the day before the warm-up; the rest on Nov 19.
>   Later days' budgets are written by the monitor from this plan.
> - **By product line**: dog food 52% of the push (deals, ACOS 24%), cat food 31%, treats 17%.
>
> Below is the write preview - one table per write type, each row with now -> new, when it is
> written and why. Which parts should I apply: (a) all, each on its date (recommended) /
> (b) only the schedules now / (c) not yet? Either way I hand you the change log with every row
> of this plan now.
>
> {write preview: the tables of the output template}

## structured_report

```json
{
  "store": {"profileId": "...", "profileName": "...", "timezone": "...", "storeType": "seller|vendor"},
  "generatedAt": "...", "dataAsOf": {"performance": "...", "stock": "..."},
  "scope": {"type": "store|mainCampaigns|named", "campaigns": 0, "ofCampaigns": 0, "spendShare": null, "named": []},
  "event": {"name": "...", "start": "...", "end": "...", "warmupStart": "...", "source": "user|announcement"},
  "answers": {"budgetMode": "dailyCap|windowTotal|null", "eventBudget": null, "dailyCap": null, "monthBudget": null, "goal": "max|profit|null", "hardLimit": {"acos": null, "roas": null}, "nonBrandLimit": null, "dealAsins": [], "leaveAlone": [], "brandNames": [], "competitorBrands": [], "unanswered": []},
  "dayRoles": [{"role": "warmup|early|peak|between", "dates": [], "multiple": 0, "dayBudget": 0, "source": "user|lastYearSameEvent|flat"}],
  "sizing": {"normalDay": 0, "peakDayBudget": 0, "windowSum": null, "multiple": 0, "eventCpc": 0, "clicksPerAsin": 0, "tier": "conservative|balanced|aggressive", "absorbable": 0, "referenceEvent": {"name": "...", "dates": "...", "comparedWith": "..."}, "referenceEventLift": {"spend": null, "sales": null, "cpc": null, "cvr": null}},
  "ceilingAcos": 0, "ceilingBasis": "hardLimit|targetX1.15|target|store60X1.25|store60X1.00",
  "raiseLine": {"targetAcos": null, "floorAcos": null, "hardLimitAcos": null, "raiseAcos": 0, "holdUpperAcos": null, "perGroup": [{"aiGroupName": "...", "raiseAcos": 0}]},
  "healthCheck": [{"check": "stock|delivery|budgetCeiling|managedGroup|referenceEvent|productLine|brandTraffic|guardrail", "severity": "blocker|warning|info", "object": "...", "finding": "...", "action": "..."}],
  "guardrails": [{"type": "profileBudgetCap|bidRange|placementRange|budgetManagement|brandNegativeProtection", "object": "...", "readState": "verified|warning|notExposed|notVerifiable", "current": "...", "needed": "...", "action": "..."}],
  "schedules": [{"aiGroupName": "...", "groupClass": "head|defensive|other", "groupClassSource": "namedFocus|userConfirmed|spendCandidate", "group30Acos": 25, "group30Orders": 120, "scheduleBase": "group30Actual|currentTargetFallback|userTarget", "scheduleMultiplier": 1.5, "phase": "warmup|event", "startDate": "...", "endDate": "...",
                 "now": {"optimizeType": 1, "acos": 30, "aiPersonality": 3, "budgetByPerformance": false, "budgetIncreasePct": null},
                 "optimizeType": 3, "acos": 37.5, "aiPersonality": 4, "budgetByPerformance": true, "budgetIncreasePct": 100,
                 "cutBy": null, "endedSchedulesToDelete": [{"scheduleId": "...", "startDate": "...", "endDate": "..."}],
                 "overlaps": [], "status": "ready|needsYes|blocked|scheduled|failed|needsReadBack|skipped", "statusReason": null}],
  "changes": [{"objectType": "groupTotalBudget|groupSetting|campaignBudget|keywordBid|targetBid|placement|portfolioBudget", "name": "...", "amazonId": "...", "brandClass": "brand|nonBrand|mixed|null",
               "field": null, "now": 0, "event": 0, "laterDays": [{"targetDate": "...", "budget": 0}], "reason": "...", "writeOn": "now|preWarmup|eve|<date>",
               "status": "ready|needsYes|blocked|written|failed|needsReadBack|skipped", "statusReason": null}],
  "notRaised": [{"objectType": "campaign|keyword|target|aiGroup", "name": "...", "acos": null, "limitAcos": null, "why": "hold|overHardLimit|belowTarget|fastSpending|budgetNotLimiting|stockFlagged|leaveAlone|aiOff|notEligible"}],
  "headroom": [{"date": "...", "extraAllowed": 0, "extraUsed": 0, "left": 0, "why": ["budgetsNotLimiting|bidsAtClickValue|overAbsorbable|scaledDown"]}],
  "atAGlance": {"changeNow": [{"objectType": "...", "count": 0, "addedPerDay": 0, "writeOn": "now|preWarmup|eve|<date>"}], "risks": [{"severity": "blocker|warning|info", "text": "..."}]},
  "productLines": [{"name": "...", "spend": 0, "sales": 0, "acos": 0, "pushShare": 0}],
  "timeline": [{"date": "...", "time": null, "what": "..."}]
}
```

Field notes:

- `dataAsOf.performance` is the last complete day used (`D` in health-check); `dataAsOf.stock`
  the date of the platform's inventory snapshot (or the customer's own source).
- `ceilingBasis` says which row of push-plan section 2 set `ceilingAcos`.
- `schedules[].now` is the group's current setting the phase was built from (push-plan section
  6). `group30Acos`, `group30Orders`, `scheduleBase` and `scheduleMultiplier` make the target
  reproducible (the shape above: max(30, 25 x 1.5) = 37.5). `groupClass` is never `head`
  under "profitable"; `cutBy` is `hardLimit`, `floor` or `ceiling` (no hard limit and no yes to the higher target)
  when that cap lowered the target, else `null`.
  `endedSchedulesToDelete` lists ended dated schedules removed to make room - each becomes a
  `scheduleDelete` change-log row.
- `changes[].objectType: groupSetting` is a direct group edit - an SD group's goal or target, or
  an AI switch the user asked for - with `field` naming the setting (push-plan section 6, SKILL
  Step 3.4).
- `writeOn` follows push-plan section 8: `preWarmup` = the day before warm-up starts, `eve` =
  the day before the event start.
- `notRaised` is every in-scope object the plan deliberately leaves alone, with the reason -
  the "Hold" and "Over the hard limit" lists of push-plan section 2 included, and managed
  groups whose Group-30 ACOS is over the hard limit (`aiGroup`, `overHardLimit`: target kept,
  push-plan section 6).
- `headroom` is one row per event day from "Fit the total" (push-plan section 3).

**Status values and their customer names.** Before writing: `blocked` -> "Cannot proceed",
`needsYes` -> "Needs your decision", `ready` -> "Ready". After writing: `scheduled` (a schedule
written and read back; it starts on its own date) -> "Scheduled", `written` -> "Applied and
verified", `needsReadBack` -> "Awaiting verification", `failed` -> "Failed", `skipped` ->
"Skipped" plus `statusReason`. Never show the raw value.

`schedules[].acos` is a percent number (37.5 = 37.5%) and, on a schedule that can be written,
must be in `(0, 1000]` - the fixed-date schedule write rejects anything else. A group whose
current target ACOS is empty or 0 has no computed value: its row carries `acos: null` and
`status: "blocked"` (push-plan section 6), never `0`, until the user gives a target (then
`scheduleBase: "userTarget"`). `phase` is `event`, plus a `warmup` row when there is a warm-up -
one row per phase.
