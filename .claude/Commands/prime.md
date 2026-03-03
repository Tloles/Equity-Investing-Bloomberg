Perform a comprehensive analysis of this codebase to build full context. This is the Bloomberg Equity Analysis Platform — a FastAPI + vanilla JS equity research tool.

## Steps

1. **Read the PRD** — Start by reading `PRD-Bloomberg.md` for the full product vision, feature specs, and phase plan.

2. **Read CLAUDE.md** — Load the project rules, architecture, and current status.

3. **Scan the backend** — Read these files to understand the data flow:
   - `main.py` (routes, response models, Phase 1/2 gather logic)
   - `backend/analyzer.py` (Claude AI analysis prompt and tool schema)
   - `backend/dcf.py` (DCF model)
   - `backend/comps.py` (Finviz-powered comps)
   - `backend/finviz_fetcher.py` (Finviz data scraping)
   - `backend/sec_fetcher.py` (SEC EDGAR 10-K)
   - `backend/transcript_fetcher.py` (8-K transcripts)
   - `backend/news_fetcher.py` (Google News RSS)

4. **Scan the frontend** — Read these files to understand rendering:
   - `frontend/index.html` (tab structure, valuation banner)
   - `frontend/js/app.js` (main logic, progress steps)
   - `frontend/js/analysis.js` (analysis tab)
   - `frontend/style.css` (first 100 lines for theme/variables)

5. **Identify the current phase** — Check which implementation phase we're in per the PRD and what work remains.

6. **Summarize** — Output a brief status report:
   - What's working
   - What's broken or incomplete
   - What the next logical task is based on the PRD phases
   - Any technical debt or issues you noticed
