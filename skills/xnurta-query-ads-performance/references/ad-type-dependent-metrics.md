# Metrics that don't apply to every ad type

## The rule

When one request mixes metrics that apply to every ad type with metrics that apply to only
some, **split it into separate queries** along those lines. The split applies to the base
metrics too: when a restricted metric uses `Clicks` / `Impressions` / `Orders` / `Sales` /
`Conversions` as a numerator or denominator, those base values must be restricted to the same
ad-type range, or the ratio is computed over a wider population than its numerator.

---

## Restricted by campaign type

### New-to-brand (NTB) - not available for SP (`sponsoredProducts`)

| Metric | Meaning |
|------|------|
| NTBOrders / NTB Orders | New-to-brand orders |
| NTBUnits / NTB Units | New-to-brand units |
| NTBSales / NTB Sales | New-to-brand sales |
| NTBOrdersRate / % of NTB Orders | NTB share of orders |
| NTBUnitsRate / % of NTB Units | NTB share of units |
| NTBSalesRate / % of NTB Sales | NTB share of sales |

⚠️ For the three rate metrics, **both** the numerator and the denominator must be restricted to
non-SP (`sponsoredBrands` and `sponsoredDisplay` only). Dividing NTB orders by all-campaign
orders understates the share.

---

### Video - not available for SP (`sponsoredProducts`)

| Metric | Meaning |
|------|------|
| VideoUnmutes | Unmutes |
| VideoFirstQuartileViews | Played to 25% |
| VideoMidpointViews | Played to 50% |
| VideoThirdQuartileViews | Played to 75% |
| VideoCompleteViews | Played to 100% |
| Video5SecondViews | Played 5 seconds or completed |
| Video5SecondViewRate | Share of 5-second-or-complete views |
| VTR | View-through rate |
| vCTR | View-through click rate |

---

### Display - not available for SP (`sponsoredProducts`)

| Metric | Meaning |
|------|------|
| DPV | Detail-page views (= DPVClick + DPVvCPM) |
| DPVR | Detail-page view rate, computed as `sum(DPV) / sum(nsp_impression)` - restrict `campaignType` to non-SP when querying or computing it |
| ViewableImpressions | Impressions that entered the viewport. **Available for every ad type** |
| ViewableImpressionsRate | Share of impressions that were viewable |
| vCPM | Cost per thousand viewable impressions |
| ViewImpressions | vCPM impressions. ⚠️ **SD vCPM campaigns only**, used for `vCPM = Spend / ViewImpressions × 1000` |

⚠️ **`ViewableImpressions` and `ViewImpressions` are different metrics**, one letter apart:

- **ViewableImpressions** - viewable impressions, every ad type
- **ViewImpressions** - vCPM impressions, SD vCPM campaigns only

---

### vCPM / click attribution - not available for SP (`sponsoredProducts`)

Supported fact entities: `campaign` / `adGroup` / `target` / `searchTerm` / `productAd`.
Not supported: `placement`, `asin`.

| Metric | Meaning |
|------|------|
| DPVClick / DPV(Click) | Detail-page views, click-attributed |
| DPVvCPM / DPV(vCPM) | Detail-page views, vCPM-attributed |
| OrdersClick / Orders(Click) | Orders, click-attributed |
| UnitsClick / Units(Click) | Units, click-attributed |
| SalesClick / Sales(Click) | Sales, click-attributed |
| OrdersvCPM / Orders(vCPM) | Orders, vCPM-attributed |
| UnitsvCPM / Units(vCPM) | Units, vCPM-attributed |
| SalesvCPM / Sales(vCPM) | Sales, vCPM-attributed |

---

## Restricted by fact entity

### AI metrics - `campaign` only

| Metric | Meaning |
|------|------|
| AISpend | Spend attributed to AI |
| AISales | Sales attributed to AI (counted where AI spend > 0) |
| AIACOS | AI ACOS |
| AIROAS | AI ROAS |

---

### Top-of-search impression share - `campaign` and `target` only

| Metric | Meaning |
|------|------|
| TopOfSearchIS | Top-of-search impression share. **Take the max, never the sum** - it is a share, so adding rows together is meaningless |

---

### ASIN business metrics - `asin` only

`TotalSalesAmount`, `OrderCount`, `Sessions`, `PageViews`, `TACOS`,
`UnitSessionPercentage`, `BuyBoxPercentage`, `ShippedRevenue`, `ShippedUnits`,
`GlanceViews`, `OrganicSales`, `OrganicOrders` and the rest of the business set belong to the
ASIN fact table alone. They cannot be mixed with `productAd` or any advertising entity.

⚠️ **Never join ASIN's own metrics to `campaign` / `adGroup` / `aiGroup` - for grouping or for
filtering.** The join is not one-to-one, so rows are duplicated and the totals come back
inflated. See the cross-entity join rules in `SKILL.md`.

---

## Dimension-level restriction

### `productAd` - SP (`sponsoredProducts`) only

The promoted-product dimension exists for Sponsored Products alone. When selecting or filtering
on a `productAd.*` field, filter `campaignType` to `sponsoredProducts` as well, or the query
spans ad types where the dimension has no meaning.

---

## How to split a mixed request

| Metrics | Constraint |
|---|---|
| Base advertising metrics (`Impressions`, `Clicks`, `Spend`, `Sales`, `ACOS` …) | every ad type - no `campaignType` filter needed |
| NTB / video / display / vCPM-attribution | restrict `campaignType` to non-SP (`sponsoredBrands`, `sponsoredDisplay`) |
| AI metrics | `factEntity: "campaign"` only |
| `TopOfSearchIS` | `factEntity: "campaign"` or `"target"` only |
| ASIN business metrics | `factEntity: "asin"` only, and never joined to an advertising level |

Report each split as what it is. A table whose NTB column covers only SB and SD while its spend
column covers everything is two different populations side by side, and reads as if SP simply
had no new-to-brand orders.
