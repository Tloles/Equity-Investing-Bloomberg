Create an atomic git commit for the current changes.

## Process

1. **Check status** — Run `git status` and `git diff --stat` to see what changed.

2. **Verify before committing:**
   - Run `python3 -c "from main import app; print('OK')"` to make sure the app loads
   - Check there are no `.env` or API key files staged
   - Check there are no `__pycache__` or `.pyc` files staged

3. **Stage and commit:**
   - Stage only the relevant files (not everything blindly)
   - Write a descriptive commit message following this format:
     ```
     [module] Brief description of what changed

     - Detail 1
     - Detail 2
     ```
   - Examples:
     - `[comps] Migrate from FMP to Finviz for peer data`
     - `[bloomberg] Add bloomberg_fetcher.py with BDP/BDH support`
     - `[report] Add Report tab with AI narrative generation`
     - `[frontend] Add valuation banner with DCF/DDM/Comps cards`

4. **Push** — Run `git push origin main` after committing.

5. **Confirm** — Show the commit hash and summary.
