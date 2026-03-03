Create a detailed implementation plan for the following feature or task:

$ARGUMENTS

## Planning Process

1. **Read the PRD** — Check `PRD-Bloomberg.md` for relevant feature specs, data sources, and acceptance criteria.

2. **Understand current state** — Read the files that will be affected. Map out:
   - Which backend modules need changes
   - Which frontend files need changes
   - Which data sources are involved
   - What Pydantic/dataclass models need updating

3. **Check for patterns** — Look at how similar features were implemented:
   - How other tabs render data (e.g., `renderComps()` in `comps.js`)
   - How other fetchers are structured (e.g., `finviz_fetcher.py`)
   - How data flows from `asyncio.gather` → response model → frontend

4. **Create the plan** — Write a step-by-step implementation plan with:

### Plan Structure

```
## Feature: [name]

### Overview
[1-2 sentence description of what we're building]

### Files to Create
- [new file path] — [purpose]

### Files to Modify
- [file path] — [what changes and why]

### Backend Changes
1. [Step with specific code changes needed]
2. [Step...]

### Frontend Changes
1. [Step with specific code changes needed]
2. [Step...]

### Data Flow
[How data moves from source → backend → API response → frontend render]

### Testing
- [How to verify this works]
- [Edge cases to check]

### Acceptance Criteria
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
```

5. **Save the plan** — Write the plan to `plans/[feature-name].md`

Do NOT implement anything yet. This is planning only. The plan will be executed separately with `/execute`.
