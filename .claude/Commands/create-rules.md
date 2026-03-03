Analyze the current codebase and regenerate the CLAUDE.md file with up-to-date project rules.

## Process

1. **Scan the full directory structure** — Run `find . -type f -not -path './.git/*' -not -path './__pycache__/*' -not -path './node_modules/*' | head -60` to see all files.

2. **Read key files** to understand current architecture:
   - `main.py` — routes, models, data flow
   - All `backend/*.py` — data sources and processing
   - `frontend/index.html` — tab structure
   - `frontend/js/*.js` — rendering logic
   - `.env.example` — required environment variables
   - `requirements.txt` — Python dependencies

3. **Identify patterns** — Note:
   - How data fetchers are structured (function signatures, error handling)
   - How frontend tabs render (function naming, DOM patterns)
   - What data sources are active vs deprecated
   - Any technical debt or inconsistencies

4. **Regenerate CLAUDE.md** with these sections:
   - Project Overview (1-2 sentences)
   - Stack description
   - Architecture (file tree with descriptions)
   - Data Source Priority (ordered list)
   - Key Technical Patterns (backend + frontend)
   - Environment Variables
   - How to run
   - Current Status (working / broken / planned)
   - Important Rules

5. **Write the file** — Overwrite `CLAUDE.md` with the updated content.

Keep it concise — CLAUDE.md should be under 150 lines. It's a quick reference, not documentation.
