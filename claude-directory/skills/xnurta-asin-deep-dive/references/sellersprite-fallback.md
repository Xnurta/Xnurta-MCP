# When SellerSprite Is Not Connected

Use the platform's SQP / ABA, eligible brand peer benchmark and current competitorProduct report
first. When SellerSprite is absent, use this reference only for questions those sources cannot
answer. **Leaving a section empty is unacceptable** when account data supports a narrower answer.

Every substituted section must carry two labels: **which path produced it**, and **what that path
cannot answer**. A reader who is not told will take the fallback for the full version.

## The probe

Detect by calling, not by reading a tool list — a tool name can be present while the account has no
entitlement. One cheap SellerSprite call against the target ASIN and marketplace. Data back means
connected. An error, an empty body or no such tool means not connected.

Offer once, in one sentence, and move on. Do not re-ask mid-report.

## 1. Market position

| | |
|---|---|
| **Full path** | Category price bands, rating and review distribution, listing quality, same-brand cannibalisation |
| **Substitute** | `asinPrice`, `asinBsr`, `asinBrand` from `get_entity_metadata` (`entity=asin`) |
| **Reframed question** | Not "how does this price compare to the category" but **"where does this product sit on price and rank among the products this account sells"** |

Rank this ASIN's price and BSR against the account's own catalogue, and against its siblings under
the same parent. A product priced at the top of its own brand's range with a BSR behind its
siblings is a finding you can make without any external data.

**This substitute alone cannot answer** category price distribution, rating, review count or
listing quality. The separate `competitorProduct` read may supply price, stars and review count
for up to 60 recommended competitors per report type, if the report and permission are available.
Do not turn that limited list into a category distribution. BSR is a rank within a category whose
size is unknown here, so treat it as direction over time, not as market share.

## 2. Competitors

| | |
|---|---|
| **Full path** | Head-to-head comparison against same-tier competitors, interception and defence opportunities |
| **Substitute** | `get_ads_perf` at `factEntity=target` with **`queryType: product`** (that parameter is what selects product targeting — `targetType` is not a selectable dimension), over this ASIN's ad groups |
| **Reframed question** | Not "how do competitors compare to us" but **"which competitor ASINs is this account paying to target, and does that spend pay back"** |

This is the substitution with the most value in it, because it is about money already spent. For
each competitor ASIN being targeted: spend, clicks, conversions, sales and ACOS, over both windows.
Three findings come out of it directly:

- Competitor targets taking spend with no conversions — a candidate list for the customer to review
- Competitor targets that convert well — where interception is working, and worth more budget
- The account's **own** ASINs appearing as product targets — self-competition, and almost always
  unintentional

**This product-target path cannot answer** the competitor's price, stars, review count, sales
volume or ranking. The separate `competitorProduct` report can add price, stars and review count
for its returned products, but not sales volume or a complete ranking. Label each source.

## 3. Traffic structure

| | |
|---|---|
| **Full path** | Organic vs ad share, core keyword organic rank, entrance concentration, traffic-collapse attribution |
| **Substitute** | `TACOS`, `TotalSalesAmount`, `Sessions` at `factEntity=asin`, plus `searchTerm` rows for concentration |
| **Reframed question** | Mostly the same question. **`TACOS` is ad spend over total sales, so ad dependence falls straight out of it** — no external data needed |

- **Ad dependence**: `TACOS` across both windows. Rising TACOS with flat total sales means the
  business is buying the same revenue at a higher cost
- **Ad share of sales**: ad-attributed sales over `TotalSalesAmount`. A rising share shows greater
  reliance on ad-attributed sales; attribution differences mean it does not prove organic sales fell
- **Entrance concentration**: Top1 / Top2 / Top5 search terms' share of orders, sales and spend.
  Concentration is not itself a problem — it is a *risk measure*, and it matters most when the top
  entrance is also the one whose efficiency is falling
- **Sessions vs clicks**: a drop in `Sessions` with steady ad clicks points outside advertising

**Cannot answer**: organic keyword rank itself — say it plainly, because "the organic rank dropped"
is the most common explanation offered for a traffic decline and this path cannot confirm it.

### A traffic collapse still gets a checklist, not a shrug

Work the steps in order, recording the source and the verdict for each. Two of them run on SparkX data alone, so the substitute path narrows the answer even when it cannot close it.

| Step | Needs | Verdict it can reach |
|---|---|---|
| **Stock-out** | SparkX `entity=asin` quantities and cover | Main variants healthy → ruled out. An edge variant out of stock needs its share of sales stated |
| **Ad masking** | Xnurta spend, ad-attributed sales share and total sales across both windows | If spend and ad-attributed share rose before total sales weakened, ads may have covered a decline; this pattern alone does not prove an organic drop |
| Price | Buy Box price across both windows | Same price → ruled out |
| Listing suppression | Buy Box ownership and promotion state | Normal → ruled out |
| Search-term demand shift | Weekly SQP market volume for named **head and niche terms** | A fall in head-term demand with stable niche terms suggests a term-level demand shift; it does not establish category-wide seasonality |
| Rank spiral | Organic share and rank decline vs category demand | Organic fell materially faster than the category → share loss |

Without SellerSprite, use the platform's weekly SQP market volume where covered to test category
seasonality for named terms. The other steps depend on their listed data and availability; leave
unverified mechanisms open rather than treating them as ruled out.

### One trap in the business numbers

`TotalSalesAmount ÷ OrderCount` is **amount per order**, not price per unit. It carries multi-unit orders and the price mix across variants. Label it as per-order wherever it appears; a per-unit figure needs the actual selling price, and deriving one by division is a proxy that must be flagged as such.

## What the fallback report should say about itself

One block, near the top, not buried at the end:

> The market and competitor sections use the available platform SQP / ABA and competitorProduct
> results where covered, plus account price, BSR and product-target data for the remaining gaps.
> The competitor report is a limited current list, not a category distribution. Organic keyword
> rank and broader category comparisons remain unverified without SellerSprite.

Say it once. Repeating it in every section turns a caveat into noise.
