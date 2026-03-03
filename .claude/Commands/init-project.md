Set up the project for local development and verify everything works.

## Steps

1. **Check Python version** — Run `python3 --version`. Needs 3.9+.

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt --break-system-packages
   ```

3. **Check .env file:**
   - Verify `.env` exists with at least `ANTHROPIC_API_KEY` and `FRED_API_KEY`
   - If missing, copy from `.env.example` and prompt user to fill in keys
   - Check `FMP_API_KEY` is present (optional but needed for DCF/DDM/Financials when Bloomberg unavailable)

4. **Start the server:**
   ```bash
   python3 -m uvicorn main:app --reload
   ```

5. **Verify startup** — Check for any import errors in the console output.

6. **Test a basic analysis** — Open `http://localhost:8000` in browser, enter `KO`, and verify:
   - Progress steps appear and advance
   - Analysis tab populates with bull/bear thesis
   - Comps tab shows Finviz peers (even if FMP is rate-limited)
   - News headlines appear in the analysis

7. **Report status** — List which tabs are working and which show "unavailable" (expected if FMP is rate-limited).
