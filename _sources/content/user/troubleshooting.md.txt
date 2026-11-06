# Troubleshooting

Use this page when integration does not behave as expected.

## Symptom: Optional dependency error appears even when not expected

Check:
- `when={...}` keys match actual function argument names.
- Condition values match the runtime values exactly.
- You are not triggering a guarded path indirectly.

## Symptom: Function runs, but later fails with `ModuleNotFoundError`

Likely cause:
- optional import is outside the guarded function.

Fix:
- move optional import inside the function decorated with `@dep_digest(...)`.

## Symptom: Plugin not visible in `LazyRegistry`

Check:
- plugin directory name matches key in `MAPPING`.
- mapped dependency key exists in `LIBRARIES`.
- plugin module defines the expected attribute (`attr_name`).
- capability visibility (`SHOW_ALL_CAPABILITIES`) matches your intention.

## Symptom: `_depdigest.py` seems ignored

Check:
- file is in package root and named exactly `_depdigest.py`.
- decorated function belongs to the expected package root.
- no stale runtime registration overrides are active in tests.

For test environments:
- call `clear_package_configs()`;
- clear cached assumptions before rerunning.

## Symptom: Custom exception class receives wrong arguments

DepDigest tries multiple constructor contracts.
If your exception still fails, simplify constructor signature or accept a
single `message` argument path.

## Symptom: Status output from `get_info(...)` looks wrong

Check:
- `LIBRARIES` keys are importable module names;
- `pypi` and `conda` fields are correct install names;
- environment actually contains expected packages.

## Symptom: Diagnostic noise in development logs

Confirm:
- your integration uses the intended SMonitor profile;
- expected exploratory failures are not treated as fatal application errors.

## Still Stuck?

Create a minimal reproducer with:
- `_depdigest.py`
- one guarded function
- exact call that fails

Then compare against:
- [DEPDIGEST_GUIDE.md](https://github.com/uibcdf/depdigest/blob/main/standards/DEPDIGEST_GUIDE.md)
- [MolSysMT](https://github.com/uibcdf/molsysmt)
