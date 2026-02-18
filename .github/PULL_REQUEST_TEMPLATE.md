## Scope
Describe the purpose of this PR in 2-4 lines.

## Behavior Changes
- What changes for users or integrators?
- Any compatibility considerations?

## Validation
- [ ] `pytest -q`
- [ ] `pytest --cov=depdigest --cov-report=term-missing` (if behavior changed)
- [ ] `make -C docs html` (if docs changed)

## Documentation Impact
- [ ] User docs updated (if integration behavior changed)
- [ ] Developer docs updated (if contributor workflow/architecture changed)
- [ ] Contract docs updated (`standards/DEPDIGEST_GUIDE.md` / `SMONITOR_GUIDE.md`) when needed

## Checklist
- [ ] Changes are focused and reviewable
- [ ] Added/updated tests for new behavior
- [ ] No generated artifacts accidentally tracked
