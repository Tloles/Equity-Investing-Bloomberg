Execute the implementation plan specified below, step by step with validation at each stage.

$ARGUMENTS

## Execution Process

1. **Load the plan** — Read the plan file specified in the arguments (e.g., `plans/bloomberg-fetcher.md`). If no file specified, ask which plan to execute.

2. **Read CLAUDE.md** — Refresh project rules and patterns before writing any code.

3. **Execute step by step** — For each step in the plan:
   a. Announce which step you're implementing
   b. Read the relevant existing files first
   c. Make the changes
   d. Verify syntax (run `python3 -c "import ast; ast.parse(open('file.py').read())"` for Python files)
   e. Check for import errors
   f. Move to next step

4. **Validation after all steps:**
   - Run `python3 -c "from main import app; print('Import OK')"` to verify the app loads
   - Check that no existing imports are broken
   - Verify all new Pydantic models have proper Optional fields with defaults
   - Ensure graceful degradation — new features failing should never crash existing ones

5. **Test instructions** — After implementation, provide:
   - The exact command to restart the server
   - What ticker to test with and what to look for
   - Expected console output (e.g., `[Bloomberg] NVDA: fetched 25 fields`)

## Rules During Execution

- **Follow the plan exactly** — don't add scope or redesign mid-implementation
- **Keep changes minimal** — don't refactor unrelated code
- **Preserve backward compatibility** — FMP/Finviz fallback must still work
- **Use existing patterns** — match the code style of surrounding code
- **Print debug logs** — every new fetcher should print `[ModuleName] ticker: result` logs
- **Handle errors gracefully** — wrap external calls in try/except, return None/empty on failure
- **Commit message** — suggest an atomic commit message at the end
