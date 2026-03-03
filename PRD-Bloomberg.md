# Bloomberg Equity Analysis Platform — Product Requirements Document

## 1. Executive Summary

The Bloomberg Equity Analysis Platform is a **one-click equity research workbench** that automates the full stack of fundamental stock analysis — from data gathering through valuation modeling to professional report generation. An analyst enters a ticker, and the tool produces a comprehensive equity research package: AI-driven bull/bear thesis, multi-method valuation (DCF, DDM, Comps), industry competitive analysis, and a Bloomberg-style equity research report — work that traditionally takes days of manual research and modeling.

Built for Georgia Tech's Equity Investing course, the platform is organized into three layers that mirror how analysts actually work:

1. **Data Engine** — Automatically pulls financial statements, market data, peer comparisons, earnings transcripts, and news from Bloomberg Terminal (`blpapi`), SEC EDGAR, FRED, Finviz, and Google News RSS. This is where the tool saves the most time — replacing hours of manual data gathering with a single API call.

2. **Analysis & Valuation** — AI-powered fundamental analysis (bull/bear cases, risk assessment, Porter's Five Forces) combined with quantitative valuation models (DCF with sensitivity analysis, Gordon Growth & Two-Stage DDM, comparable company multiples with implied pricing). Interactive tables let analysts override assumptions and instantly see valuation impact.

3. **Report Generation** — Assembles all analysis into a professional equity research report matching Bloomberg/sell-side formatting: narrative write-up, financial model tables with historical actuals and projections, peer comparison matrix, and valuation summary. Available as on-screen preview and downloadable PDF.

Underlying everything is a **modular data architecture** — Bloomberg serves as the primary data source (when connected to a terminal), with automatic fallback to FMP, Finviz, and free public APIs when Bloomberg is unavailable. This dual-mode design means the tool works at school on the terminal and at home with free data.

**Goal:** An analyst enters a ticker and receives a complete, presentation-ready equity research package — the same output that would take a junior analyst 2-3 days of manual work — in under 2 minutes.

---

## 2. Mission

**Mission Statement:** Compress days of equity research into minutes by connecting institutional-grade Bloomberg data, AI-powered analysis, and automated report generation into a single, continuously updating platform.

### Core Principles

1. **Bloomberg First, Free Fallback** — Use Bloomberg `blpapi` for maximum data quality when connected; degrade gracefully to FMP/Finviz/public APIs when offline. The tool always works, just at different quality levels.
2. **Everything Computes** — A change in any assumption (growth rate, discount rate, exit multiple) cascades through every valuation model and updates the report in real-time.
3. **AI Augments, Doesn't Replace** — Claude generates narrative analysis and identifies patterns in filings, but all quantitative models use deterministic formulas the analyst can inspect and override.
4. **Professional Output** — Every screen should look like it belongs on a Bloomberg terminal or in a sell-side research report. No toy UI.
5. **Modular & Extensible** — New data sources, valuation methods, and analysis modules can be added without restructuring existing code. The architecture anticipates growth.
6. **One Click, Full Stack** — The core experience is: enter ticker → get everything. No multi-step wizards, no configuration screens. Advanced users can drill into any tab to customize.

---

## 3. Target Users

### Primary: Graduate Finance Student
- Students in equity investing, security analysis, or portfolio management courses
- Comfortable with Excel-based models; familiar with Bloomberg Terminal basics
- Need to produce defensible equity research reports for course projects and stock pitch competitions
- Pain: gathering data across Bloomberg, SEC filings, and news is slow; building models from scratch for each stock is repetitive; report formatting takes hours

### Secondary: Junior Equity Analyst / Associate
- Buy-side or sell-side analysts performing initial coverage or updating models
- Need to rapidly screen stocks and produce first-pass analysis before deep-dive research
- Pain: consensus data scattered across Bloomberg screens, filings, and broker reports; no single tool connects data → model → report

### Tertiary: Individual Investor / Hobbyist
- Self-directed investors performing fundamental analysis
- May not have Bloomberg access — relies on free data tier
- Pain: free data sources are fragmented and unreliable; building valuation models requires finance expertise

---

## 4. Application Structure

The app has a **single-page layout** with a ticker input bar and **8 horizontal tabs** that populate after analysis:

| Tab | Name | Purpose |
|-----|------|---------|
| **Analysis** | Bull/Bear Analysis | AI-generated investment thesis, rating, key metrics, catalysts, news, sentiment |
| **DCF** | DCF Model | Discounted cash flow with editable projections, sensitivity analysis, intrinsic value |
| **DDM** | Dividend Discount | Gordon Growth + Two-Stage DDM with editable assumptions |
| **Comps** | Comparable Companies | Peer valuation multiples, profitability, growth — with implied pricing |
| **Financials** | Financial Statements | 5-year historical income statement, balance sheet, cash flow, ratios |
| **Industry** | Industry Analysis | Porter's Five Forces, competitive position, KPIs, tailwinds/headwinds |
| **Technical** | Technical Analysis | Price charts, moving averages, RSI, volume analysis, support/resistance *(planned)* |
| **Report** | Equity Research Report | Professional formatted report with narrative, model, comps — preview + PDF export |

### Persistent Elements

- **Ticker Input Bar** — always visible at top; drives all tabs
- **Valuation Banner** — below ticker bar; shows current price + DCF / DDM / Comps valuations side-by-side with upside/downside
- **Step Indicator** — progress steps during analysis (sector classification → fetching filings → running AI → complete)
- **Source Links** — filing URLs, transcript links, data timestamps always accessible

### Navigation

```
[ Analysis ] [ DCF ] [ DDM ] [ Comps ] [ Financials ] [ Industry ] [ Technical ] [ Report ]
```

All tabs populate from a single API call. Users can navigate freely between tabs without re-fetching.

---

## 5. Data Architecture

### Tier 1: Bloomberg Terminal (`blpapi`) — Primary Source

Requires active Bloomberg Terminal session. Provides institutional-grade data with no rate limits.

| Function | Bloomberg Fields | Used In |
|----------|-----------------|---------|
| Company profile | `NAME`, `GICS_SECTOR_NAME`, `GICS_INDUSTRY_NAME`, `GICS_SUB_INDUSTRY_NAME`, `CUR_MKT_CAP`, `BETA_RAW_OVERRIDABLE` | All tabs |
| Financial statements (5yr) | `SALES_REV_TURN`, `GROSS_PROFIT`, `IS_OPER_INC`, `NET_INCOME`, `IS_DILUTED_EPS`, `EBITDA`, `CAPITAL_EXPEND`, `CF_FREE_CASH_FLOW`, `BS_CASH_NEAR_CASH_ITEM`, `BS_LT_BORROW`, `BS_ST_BORROW`, `TOTAL_EQUITY`, `BS_TOT_ASSET` + 15 more via BDH | DCF, DDM, Financials |
| Current quote | `PX_LAST`, `CUR_MKT_CAP`, `EQY_DVD_YLD_IND` | Valuation banner |
| Peer companies | `PEER_RANKED_LIST` via BDS | Comps |
| Peer multiples | `PE_RATIO`, `BEST_PE_RATIO`, `BEST_CUR_EV_TO_EBITDA`, `PX_TO_SALES_RATIO`, `PX_TO_BOOK_RATIO`, `BEST_PEG_RATIO` | Comps |
| Analyst consensus | `BEST_TARGET_PRICE`, `BEST_ANALYST_RATING`, `BEST_EPS`, `BEST_DPS`, `BEST_DVD_GROW` | Analysis, DDM, Report |
| Pre-computed ratios | `GROSS_MARGIN`, `OPER_MARGIN`, `RETURN_COM_EQY`, `RETURN_ON_INV_CAPITAL`, `CUR_RATIO`, `TOT_DEBT_TO_TOT_EQY`, `WACC` | Financials, DCF |
| Dividend history | `DVD_HIST_ALL` via BDH | DDM |
| Institutional ownership | `INSTITUTIONAL_OWNERSHIP_PCT` | Report |
| Short interest | `SHORT_INT_RATIO` | Analysis, Report |
| Segment revenue | `PRODUCT_SEGMENT_REVENUE` via BDS | Analysis, Report |
| Historical prices | `PX_LAST` via BDH (daily) | Technical |

### Tier 2: Free Public APIs — Fallback & Supplement

Always available regardless of Bloomberg connectivity.

| API | Data | Used In | Key Required |
|-----|------|---------|-------------|
| **SEC EDGAR** | 10-K filings (MD&A, Risk Factors), 8-K earnings releases | Analysis, Industry | No |
| **FRED** | 10yr Treasury (risk-free rate), market indicators | DCF, DDM | Yes (free) |
| **Finviz** (`finvizfinance`) | 90+ fundamentals, peer lists, analyst targets, P/E, PEG, beta | Comps, Analysis | No |
| **Google News RSS** | Recent news headlines by ticker | Analysis | No |
| **FMP** | Financial statements, quotes, dividends (when Bloomberg unavailable) | DCF, DDM, Financials | Yes (free tier) |

### Tier 3: AI Analysis (Anthropic Claude API)

| Function | Model | Used In |
|----------|-------|---------|
| Bull/bear thesis generation | Claude (Sonnet) | Analysis tab |
| Porter's Five Forces | Claude (Sonnet) | Industry tab |
| Equity research narrative | Claude (Sonnet) | Report tab |
| Key metrics extraction | Claude (Sonnet) | Analysis tab |

### Data Source Priority Logic

```
For each data point:
  1. If Bloomberg session active → use blpapi
  2. Else if Finviz has it → use finvizfinance
  3. Else if FMP available and not rate-limited → use FMP
  4. Else → show "unavailable" gracefully
```

### Environment Variables (`.env`)

```
# Required
ANTHROPIC_API_KEY=required_for_ai_analysis

# Bloomberg (only when running on terminal machine)
BLOOMBERG_ENABLED=true/false

# Fallback data sources
FMP_API_KEY=optional_free_tier
FRED_API_KEY=required_for_risk_free_rate
```

---

## 6. Feature Specifications

### 6.1 Analysis Tab — AI-Powered Investment Thesis

**Purpose:** Generate a structured investment thesis with rating, bull/bear arguments, risk assessment, and market sentiment — all from 10-K filings, earnings transcripts, and news.

**Components:**
- **Rating Badge** — Overall rating (Strong Buy / Buy / Bullish / Neutral / Bearish / Sell) with color coding
- **Thesis Statement** — One-sentence investment thesis
- **Key Metrics Strip** — 4-5 most relevant financial metrics with trend arrows (revenue growth, margins, EPS, FCF yield, etc.) selected by AI based on sector
- **Bull Case** — 3-5 structured arguments with headline + supporting detail, always visible
- **Bear Case** — 3-5 structured arguments, same format
- **Downplayed Risks** — Risks management is underemphasizing in filings
- **Top News** — 5 most relevant recent headlines (clickable links) selected by AI from Google News RSS feed
- **Recent Catalysts** — Key events extracted from news and filings
- **Market Sentiment** — Narrative summary of current investor sentiment
- **Analyst Summary** — Overall assessment synthesizing all inputs

**Data Sources:** SEC EDGAR (10-K, 8-K transcripts), Google News RSS, Finviz (analyst target/recom), Bloomberg (consensus estimates, short interest when available)

### 6.2 DCF Tab — Discounted Cash Flow Model

**Purpose:** Project 5-year free cash flows and terminal value to compute intrinsic value per share.

**Components:**
- **CAPM Assumptions** — Risk-free rate (FRED/Bloomberg), ERP (Damodaran/Bloomberg), beta, cost of equity. All editable.
- **Historical Actuals Table** — 5 years of revenue, operating income, interest expense, pretax income, tax, net income, EPS, capex, D&A, FCF, balance sheet items. Horizontal scrolling.
- **Projection Table** — 5 years of editable assumptions: revenue growth, operating margin, tax rate, capex %, D&A %, share growth, exit P/E multiple. Each cell is an input that recalculates on change.
- **Valuation Bridge** — PV of FCFs + PV of terminal value = equity value → intrinsic value per share
- **Sensitivity Analysis** — Matrix showing IV at different growth rate × exit multiple combinations
- **Upside/Downside Badge** — Prominent display of IV vs current price

**Methodology:** Net Income + D&A − Capex for FCF; P/E exit multiple for terminal value (not perpetuity growth); equity-basis discounting (cost of equity, not WACC). Bloomberg upgrade path: use `WACC` field for discount rate.

### 6.3 DDM Tab — Dividend Discount Model

**Purpose:** Value dividend-paying stocks using Gordon Growth and Two-Stage models.

**Components:**
- **Dividend History Table** — Annual DPS, payout ratio, DPS growth for all available years
- **Assumptions Panel** — Latest DPS, cost of equity, GGM growth rate, two-stage growth rates/periods. All editable with instant recalculation.
- **Gordon Growth Model** — D₁ / (Ke − g) with intrinsic value and upside badge
- **Two-Stage DDM** — High-growth period + terminal growth, with PV breakdown
- **Projected Dividends Chart** — Visual projection of future dividend stream

**Bloomberg Upgrade:** `BEST_DPS` and `BEST_DVD_GROW` provide forward consensus estimates, replacing backward-looking extrapolation.

### 6.4 Comps Tab — Comparable Company Analysis

**Purpose:** Compare target stock against peers across valuation, profitability, and growth metrics.

**Components:**
- **Sub-tabs** — Valuation / Profitability / Growth views
- **Peer Table** — Target highlighted, 8 peers with full metrics. Horizontal scrolling for many columns.
- **Median Row** — Peer medians for key multiples (P/E, EV/EBITDA, P/S, P/B)
- **Implied Value Cards** — Target price implied by applying peer median multiples to target's financials (e.g., median P/E × target EPS)
- **Peer Source** — Finviz peers (free), Bloomberg `PEER_RANKED_LIST` (when available)

**Data Source:** Finviz `finvizfinance` for peer list and all fundamental metrics (no FMP dependency). Bloomberg overlay adds forward consensus multiples (`BEST_PE_RATIO`, `BEST_CUR_EV_TO_EBITDA`).

### 6.5 Financials Tab — Historical Financial Statements

**Purpose:** Display 5 years of standardized financial statements with computed ratios.

**Components:**
- **4 Sub-tabs** — Income Statement / Balance Sheet / Cash Flow / Ratios
- **Each sub-tab** — Horizontal table with years as columns, line items as rows
- **Ratios sub-tab** — Margins, returns, leverage, efficiency, per-share metrics — computed from raw data or pulled directly from Bloomberg

**Data Source:** FMP (free tier) or Bloomberg BDH historical. Bloomberg provides pre-computed ratios as a bonus.

### 6.6 Industry Tab — Competitive Analysis

**Purpose:** AI-generated Porter's Five Forces analysis and competitive positioning.

**Components:**
- **Five Force Cards** — Each with rating (Low/Medium/High) and detailed explanation
- **Industry Structure** — Narrative assessment of market dynamics
- **Competitive Position** — Company's moats, advantages, vulnerabilities
- **Key KPIs** — Industry-specific metrics that matter most
- **Tailwinds / Headwinds** — Macro factors favoring or threatening the industry

**Data Source:** Claude AI analyzing 10-K text and transcripts. No Bloomberg dependency.

### 6.7 Technical Tab — Technical Analysis *(Planned)*

**Purpose:** Price-based analysis with charts, indicators, and pattern recognition.

**Components:**
- **Price Chart** — Interactive candlestick/line chart with adjustable timeframes (1M, 3M, 6M, 1Y, 5Y)
- **Moving Averages** — 50-day and 200-day SMA/EMA overlays
- **Volume Analysis** — Volume bars with average volume line
- **Momentum Indicators** — RSI (14-day), MACD
- **Support/Resistance** — Key price levels identified algorithmically
- **AI Pattern Recognition** — Claude identifies chart patterns and technical signals *(stretch goal)*

**Data Source:** Bloomberg BDH daily prices (primary), or Yahoo Finance/Alpha Vantage (fallback).

### 6.8 Report Tab — Equity Research Report

**Purpose:** Generate a professional, presentation-ready equity research report combining all analysis.

**Components:**

**Page 1-2: Investment Narrative**
- Key Statistics header box (price, target, market cap, P/E, revenue, margins, dividend)
- Company overview paragraph
- Recent performance and earnings analysis
- Forward outlook and growth drivers
- Acquisition/strategic initiatives discussion (if applicable)
- Balance sheet and capital allocation assessment
- Target price derivation and recommendation

**Page 3: Financial Model**
- Income statement (historical actuals + 5-year projections)
- FCF build (capex, D&A, FCF, dividends, buybacks)
- Balance sheet summary (cash, debt, net debt)
- Margin/growth assumptions strip
- Valuation block (DCF methodology with IV)

**Page 4: Peer Comparison Matrix**
- Price statistics (last, 52-week range, market cap, enterprise value)
- Balance sheet comparison (cash, debt, equity)
- Income statement comparison (revenue, margins, earnings)
- Valuation ratios (P/E, EV/EBITDA, P/S, FCF yield)
- Operating statistics (quarterly revenue growth, quarterly margins)

**Output Formats:**
- On-screen HTML preview within the Report tab
- Downloadable PDF via backend rendering (`weasyprint`)
- All data sourced from the same API response — no additional calls

**AI Component:** Claude generates the 2-page narrative using analysis data, key metrics, bull/bear arguments, catalysts, and financials as context. Formatted in professional sell-side research style.

---

## 7. Persistent Valuation Banner

The valuation banner sits below the ticker input and above the tabs. It updates whenever data is available and persists across all tab views.

**Always displayed:**
- Current stock price with daily change
- Three valuation cards side-by-side:
  - **DCF** — Intrinsic value + upside/downside %
  - **DDM** — GGM intrinsic value + upside/downside % (hidden if no dividends)
  - **Comps** — Implied price range (min–max of PE/EV-EBITDA/PS/PB implied) + upside to midpoint
- Color coding: green background for upside, red for downside

**Expandable (planned):**
- Analyst consensus target price (Bloomberg `BEST_TARGET_PRICE` or Finviz)
- Valuation disconnect assessment (business quality vs. price — Morningstar style)

---

## 8. Technology Stack

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI (Python) |
| Bloomberg Data | `blpapi` Python SDK |
| AI Analysis | Anthropic Claude API |
| Market Data (fallback) | FMP REST API, Finviz (`finvizfinance`), FRED API |
| SEC Filings | SEC EDGAR (direct HTTP, no key) |
| News | Google News RSS (XML parsing) |
| PDF Generation | `weasyprint` |

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | Vanilla JS (no build step) |
| Styling | Custom CSS (dark/professional theme) |
| Tables | Custom horizontal-scroll table components |
| Charts | Planned: Chart.js or Lightweight Charts |
| Icons | Unicode / CSS |

### Data Sources — Priority Order
| Priority | Source | Data | Cost |
|----------|--------|------|------|
| 1 | Bloomberg `blpapi` | Everything (financials, quotes, peers, consensus, ratios) | School terminal (free to student) |
| 2 | SEC EDGAR | 10-K filings, 8-K earnings transcripts | Free |
| 3 | FRED | Risk-free rate (10yr Treasury) | Free |
| 4 | Finviz | Peers, 90+ fundamentals, analyst targets | Free (scraping) |
| 5 | Google News RSS | Recent headlines by ticker | Free |
| 6 | FMP | Financial statements, quotes, dividends (fallback) | Free tier (250 calls/day) |
| 7 | Anthropic Claude | AI analysis, narrative generation | ~$0.01-0.05 per analysis |

### Environment Variables (`.env`)
```
ANTHROPIC_API_KEY=required
BLOOMBERG_ENABLED=false
FMP_API_KEY=optional
FRED_API_KEY=required
```

---

## 9. Implementation Phases

### Phase 1: Foundation ✅
- FastAPI + vanilla JS scaffold
- SEC EDGAR 10-K fetching (4 years)
- SEC EDGAR 8-K transcript fetching (4 quarters)
- Claude AI bull/bear analysis with structured output
- Basic tab navigation (Analysis, DCF)
- FMP integration for financial data

### Phase 2: Valuation Models ✅
- DCF model with editable projection tables and sensitivity analysis
- DDM with Gordon Growth and Two-Stage models
- Comparable company analysis (Comps tab with sub-views)
- Financials tab with 4 sub-tabs (IS, BS, CF, Ratios)
- Industry analysis (Porter's Five Forces via Claude)
- Valuation banner (DCF + DDM + Comps range)

### Phase 3: Data Source Hardening ✅
- Finviz integration for peers and supplementary metrics
- Google News RSS replacing broken FMP news endpoint
- Comps tab migrated to Finviz (FMP-free)
- Graceful degradation when data sources fail
- Step-based progress indicator with queued transitions

### Phase 4: Bloomberg Migration (Current)
- `backend/bloomberg_fetcher.py` — unified Bloomberg data interface via `blpapi`
- Data source router: Bloomberg → Finviz → FMP fallback chain
- Bloomberg pre-export script for offline use (JSON dump from terminal)
- Migrate industry classifier to GICS codes
- Migrate DCF/DDM to Bloomberg financial statements
- Migrate Comps to Bloomberg `PEER_RANKED_LIST` + forward consensus multiples
- Add consensus estimates to Analysis tab (target price, EPS estimates)

### Phase 5: Report Generation
- Report tab with on-screen HTML preview
- AI-generated equity research narrative (2-page write-up)
- Financial model table (actuals + projections)
- Peer comparison matrix (Bloomberg-style formatting)
- PDF export via `weasyprint` backend endpoint
- Key Statistics header box matching sell-side format

### Phase 6: Technical Analysis
- Historical price data integration (Bloomberg BDH or Yahoo Finance)
- Interactive price chart with candlestick/line toggle
- Moving average overlays (50/200 SMA)
- RSI and MACD indicators
- Volume analysis
- Support/resistance level identification

### Phase 7: Platform Polish & Advanced Features
- Landing page with sector cards, popular tickers, market news
- Multi-ticker comparison mode (side-by-side analysis)
- Excel export (multi-tab workbook with model + comps)
- Watchlist / portfolio tracker
- Screening tool (filter universe by Finviz metrics)
- Monte Carlo simulation for DCF assumptions
- Earnings surprise tracking and estimate revision charts
- ESG scoring integration (Bloomberg `ESG_DISCLOSURE_SCORE`)

---

## 10. Success Criteria

The platform is successful when an analyst can:
1. Enter any US-listed ticker and receive a complete analysis in under 2 minutes
2. Read an AI-generated investment thesis with structured bull/bear arguments backed by filing data
3. View and customize a DCF model with editable assumptions and sensitivity analysis
4. See comparable company valuations with real peer multiples and implied pricing
5. Review 5 years of financial statements with computed ratios
6. Understand industry dynamics through Porter's Five Forces analysis
7. See three valuation methods (DCF, DDM, Comps) side-by-side with upside/downside
8. Generate a professional equity research report matching sell-side formatting
9. Download the report as a PDF ready for course submission or presentation
10. Switch seamlessly between Bloomberg (at school) and free data (at home) with no configuration

---

## 11. Key Financial Formulas

| Formula | Calculation |
|---------|-------------|
| Free Cash Flow | Net Income + D&A − Capex |
| Terminal Value | Year-5 Net Income × Exit P/E Multiple |
| Intrinsic Value (DCF) | (PV of FCFs + PV of Terminal Value) ÷ Diluted Shares |
| Cost of Equity (CAPM) | Risk-Free Rate + β × Equity Risk Premium |
| Gordon Growth IV | D₁ ÷ (Ke − g) where D₁ = DPS × (1 + g) |
| Two-Stage DDM IV | PV(Stage 1 Dividends) + PV(Terminal Value at Stage 2 growth) |
| Implied Price (Comps) | Peer Median Multiple × Target's Corresponding Metric |
| Upside/Downside | (Intrinsic Value − Current Price) ÷ Current Price × 100 |
| FCF Yield | Free Cash Flow ÷ Enterprise Value |
| EV/EBITDA | (Market Cap + Net Debt) ÷ EBITDA |
| PEG Ratio | P/E ÷ EPS Growth Rate |
| Dividend Payout Ratio | DPS ÷ EPS |

---

## 12. Bloomberg Field Reference

### BDP (Reference Data — Current Snapshot)
| Category | Fields |
|----------|--------|
| Profile | `NAME`, `GICS_SECTOR_NAME`, `GICS_INDUSTRY_NAME`, `GICS_SUB_INDUSTRY_NAME`, `CUR_MKT_CAP`, `BETA_RAW_OVERRIDABLE` |
| Quote | `PX_LAST`, `CHG_PCT_1D`, `EQY_DVD_YLD_IND` |
| Valuation | `PE_RATIO`, `BEST_PE_RATIO`, `BEST_CUR_EV_TO_EBITDA`, `PX_TO_SALES_RATIO`, `PX_TO_BOOK_RATIO`, `BEST_PEG_RATIO` |
| Consensus | `BEST_TARGET_PRICE`, `BEST_ANALYST_RATING`, `BEST_EPS`, `BEST_DPS`, `BEST_DVD_GROW` |
| Ratios | `GROSS_MARGIN`, `OPER_MARGIN`, `NET_INCOME_MARGIN`, `RETURN_COM_EQY`, `RETURN_ON_ASSET`, `RETURN_ON_INV_CAPITAL`, `CUR_RATIO`, `TOT_DEBT_TO_TOT_EQY`, `WACC` |
| Dividends | `TRAIL_12M_DVD_PER_SH`, `DVD_PAYOUT_RATIO`, `DVD_GROW_5Y` |
| Other | `INSTITUTIONAL_OWNERSHIP_PCT`, `SHORT_INT_RATIO` |

### BDH (Historical Data — Time Series)
| Category | Fields | Override |
|----------|--------|----------|
| Income Statement | `SALES_REV_TURN`, `GROSS_PROFIT`, `IS_OPER_INC`, `IS_INT_EXPENSE`, `PRETAX_INC`, `INCOME_TAX_EXPENSE`, `NET_INCOME`, `IS_DILUTED_EPS`, `EBITDA`, `IS_SH_FOR_DILUTED_EPS`, `IS_RD_EXPEND`, `IS_SGA_EXPEND` | `FUND_PER=FY` |
| Balance Sheet | `BS_CASH_NEAR_CASH_ITEM`, `BS_CUR_ASSET_REPORT`, `BS_TOT_ASSET`, `BS_CUR_LIAB`, `BS_LT_BORROW`, `BS_ST_BORROW`, `TOT_LIAB`, `TOTAL_EQUITY` | `FUND_PER=FY` |
| Cash Flow | `CF_CASH_FROM_OPER`, `CAPITAL_EXPEND`, `CF_FREE_CASH_FLOW`, `CF_DEPR_AMORT`, `CF_DVD_PAID`, `CF_SHARE_REPURCHASE` | `FUND_PER=FY` |
| Prices | `PX_LAST`, `PX_VOLUME` | Daily |
| Dividends | `DVD_HIST_ALL` | `DVD_PERIOD=A` |

### BDS (Bulk Data — Lists)
| Data | Field |
|------|-------|
| Peer companies | `PEER_RANKED_LIST` |
| Segment revenue | `PRODUCT_SEGMENT_REVENUE` |

---

## 13. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Bloomberg `blpapi` only works on terminal machine | Pre-export script dumps data to JSON; free tier fallback always available |
| Bloomberg license prohibits redistribution | Tool runs locally for personal/academic use only; never serves Bloomberg data to third parties |
| FMP rate limiting (250 calls/day) | Finviz handles Comps/peers with no limits; FMP only needed for financial statements when Bloomberg unavailable |
| Finviz web scraping could break | `finvizfinance` library actively maintained; Finviz HTML changes infrequently; FMP as fallback |
| Claude API costs | Each analysis costs ~$0.01-0.05; AI calls are explicit (never background); student budget of $5-10/month covers ~100+ analyses |
| Report generation quality | Template-based structure ensures consistency; AI generates narrative within guardrails; analyst can edit before export |
| Data staleness (pre-export mode) | Timestamps displayed on all data; tool flags when data is >24h old |
| Scope creep | Strict phase boundaries; new features queue to Phase 7; core experience (enter ticker → get analysis) is always priority |

---

## 14. Future Considerations

- Real-time price streaming via Bloomberg `MKTDATA` subscription
- Options analysis tab (Greeks, implied volatility surface, unusual activity)
- Earnings estimate revision tracking and surprise history
- ESG scoring and controversy screening
- Multi-company comparison mode (side-by-side analysis for stock pitches)
- Portfolio-level analytics (correlation, beta, sector exposure)
- Screening tool with custom filters (Finviz screener integration)
- Monte Carlo simulation on DCF assumptions
- Slack/email integration for daily watchlist alerts
- Excel model export (multi-tab .xlsx matching sell-side format)
- CoStar-style data import for cross-asset analysis
- Custom universe creation and batch analysis
- API endpoint for programmatic access (power users)
- Mobile-responsive layout for on-the-go review

---

## 15. Course Integration

| Course Concept | Tool Integration |
|---------------|-----------------|
| Fundamental analysis | Analysis tab: AI extracts key themes from 10-K filings |
| Valuation methods (DCF, DDM, Comps) | Three dedicated tabs with interactive, editable models |
| Financial statement analysis | Financials tab: 5-year statements with 15+ computed ratios |
| Industry analysis (Porter's Five Forces) | Industry tab: AI-generated with sector-specific guidance |
| Equity research report writing | Report tab: auto-generated sell-side-style PDF |
| Comparable company analysis | Comps tab: peer multiples with median benchmarking and implied pricing |
| Risk assessment | Analysis tab: bear case, downplayed risks, catalysts |
| Market efficiency and pricing | Valuation banner: three methods vs. market price — lets students assess mispricing |
