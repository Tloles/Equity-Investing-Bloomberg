# Bloomberg Equity Analysis Platform

## Project Overview

A one-click equity research workbench that automates fundamental stock analysis — from data gathering through valuation modeling to professional report generation. Built for Georgia Tech's Equity Investing course.

**Stack:** FastAPI backend (Python 3.9+) + vanilla JS frontend (no build step). No React, no npm, no Tailwind.

**Repository:** https://github.com/Tloles/Equity-Investing-Bloomberg

## Architecture

```
main.py                          # FastAPI entry point, all routes, Pydantic response models
backend/
  analyzer.py                    # Claude AI bull/bear analysis (Anthropic API)
  bloomberg_fetcher.py           # Bloomberg blpapi data interface (when connected)
  comps.py                       # Comparable company analysis (Finviz-powered, no FMP)
  config.py                      # Shared constants (PROJECTION_YEARS, etc.)
  dcf.py                         # DCF intrinsic value model
  ddm.py                         # Dividend discount model (GGM + Two-Stage)
  financials.py                  # Historical financial statements
  finviz_fetcher.py              # Finviz scraping for peers, metrics, analyst data
  industry_classifier.py         # Sector/industry classification (FMP profile)
  industry_config.py             # Sector-specific rules and DCF adjustments
  market_data.py                 # FRED API for risk-free rate
  news_fetcher.py                # Google News RSS for headlines
  sec_fetcher.py                 # SEC EDGAR 10-K filing scraper
  transcript_fetcher.py          # SEC EDGAR 8-K earnings transcript scraper
frontend/
  index.html                     # Single page with tab navigation
  style.css                      # All styles (dark professional theme)
  js/
    app.js                       # Main app logic, tab switching, progress steps
    api.js                       # API call helpers
    analysis.js                  # Analysis tab rendering
    dcf.js                       # DCF tab rendering + recalculation
    ddm.js                       # DDM tab rendering + recalculation
    financials.js                # Financials tab rendering (4 sub-tabs)
    comps.js                     # Comps tab rendering (3 sub-views)
    industry.js                  # Industry/Porter's Five Forces tab
```

## Data Source Priority

1. **Bloomberg `blpapi`** — primary when connected to terminal (no rate limits)
2. **SEC EDGAR** — 10-K filings and 8-K transcripts (free, always available)
3. **FRED** — risk-free rate / 10yr Treasury (free)
4. **Finviz** (`finvizfinance`) — peers, 90+ fundamentals, analyst targets (free scraping)
5. **Google News RSS** — recent headlines by ticker (free)
6. **FMP** — financial statements fallback when Bloomberg unavailable (250 calls/day free tier)
7. **Anthropic Claude** — AI analysis and narrative generation

## Key Technical Patterns

### Backend
- All data fetchers run concurrently via `asyncio.gather` + `asyncio.to_thread`
- Every data source is optional — use `return_exceptions=True` and degrade gracefully
- Print `[ModuleName] ticker: ...` debug logs for every fetch (success and failure)
- Pydantic models for all API responses
- Dataclasses for internal data containers
- Functions that call external APIs should accept the ticker as first argument
- Always `.upper()` the ticker at entry point

### Frontend
- Vanilla JS only — no frameworks, no build step, no npm
- All JS files loaded via `<script>` tags in index.html
- CSS in a single `style.css` file
- Tab content rendered by dedicated `render{Tab}(data)` functions
- Helper functions: `show(el)`, `hide(el)`, `escapeHtml(str)` defined in app.js
- Horizontal scrolling tables with `.proj-table-scroll` wrapper
- Numbers formatted with `toFixed()`, market caps with B/T/M suffixes

### Code Style
- Python: 4-space indent, type hints on function signatures, f-string debug logs
- JS: 2-space indent, `const`/`let` (no `var`), template literals for HTML
- Remove dead code proactively — don't comment it out
- Keep modules focused — one data source per file

## Environment Variables (.env)

```
ANTHROPIC_API_KEY=required
FMP_API_KEY=optional
FRED_API_KEY=required
BLOOMBERG_ENABLED=false
```

## Running the App

```bash
cd ~/Equity-Investing-Project/Equity-Investing-Bloomberg
python3 -m uvicorn main:app --reload
# Open http://localhost:8000
```

## Current Status

### Working (no Bloomberg needed)
- Analysis tab (AI bull/bear thesis, rating, metrics, news, catalysts)
- Industry tab (Porter's Five Forces via Claude)
- Comps tab (Finviz peers + fundamentals, no FMP dependency)
- News (Google News RSS)
- SEC EDGAR (10-K filings, 8-K transcripts)
- Step-based progress indicator

### Needs FMP or Bloomberg
- DCF tab (financial statements for projections)
- DDM tab (dividend history, quote price)
- Financials tab (5-year statements)
- Valuation banner (needs current price)

### Planned
- Bloomberg `blpapi` integration (Phase 4)
- Report tab with PDF export (Phase 5)
- Technical analysis tab (Phase 6)
- Landing page, screening, batch analysis (Phase 7)

## Important Rules

1. **Never break existing functionality** — all changes must be backward compatible with the free data tier
2. **Test with `KO` (Coca-Cola)** — it's a dividend payer with stable data, good for testing all tabs
3. **Graceful degradation is mandatory** — if a data source fails, the tab shows "unavailable" message, never a 500 error
4. **Keep the single-file frontend** — don't split into components or add a build step
5. **PRD is the source of truth** — see `PRD-Bloomberg.md` for feature specs and phase planning
6. **Commit after each working feature** — atomic commits with descriptive messages
