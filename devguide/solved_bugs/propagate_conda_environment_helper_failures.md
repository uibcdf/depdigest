---
summary: Conda environment helpers discard manager failures and split literal paths.
issue: uibcdf/depdigest#32
status: resolved
opened: 2026-10-08
closed: 2026-10-08
severity: medium
verification: reproduced
area: [devtools, resource-lifecycle]
guard: tests/test_conda_env_helpers.py
normative:
blocked_by: []
supersedes: []
---

# Propagate Conda environment helper failures

## What

At d5a7ac0ae66beaff1ba080e7114bcdd55398c21c, both local create/update
helpers return zero when the selected manager exits 23. Their shell command
strings also split executable/input paths containing spaces. Create already
cleans its temporary manifest; no cleanup leak was reproduced.

## How

An owned fake Conda executable exiting 23 reproduces zero from both CLIs.
The durable guard exercises real child processes for create/update, exit zero/23
and ordinary/spaced paths: six fail before repair and two successful ordinary-path
controls pass. It checks exact argv, live generated YAML at child execution,
removed private directory afterwards, unchanged input and caller-owned sentinel.
No real solver, environment create/update or package publication occurs.

## Why

This owner-local defect was found during uibcdf/molsyssuite#104. A successful
wrapper must not certify a failed or partial environment operation. The runtime
package, provider APIs, recipes, dependency versions and consumer contracts are
unaffected. Conda owns any partially-created environment; the wrapper must not
remove caller environments or guess rollback/retry.

## Existing operations and scope

Reviewed the central `conda_environment_tools.apply_environment` operation and
`uibcdf/molsyssuite#108`: that opt-in route requires dependency-routes@3 and an
owner profile. DepDigest still uses its qualified dependency-routes@2 inventory.
This repair changes the two existing calls to standard-library argument-vector
execution and propagates the existing child result. It adds no copied generator,
new helper/framework or implicit shared-tool migration. A future opt-in adoption
remains owner-reviewed distribution work under uibcdf/molsyssuite#45.

## Acceptance criteria

- Return the selected manager result; preserve executable/file arguments literally.
- Keep create YAML until the child completes and clean the private directory after
  success/failure; preserve caller files/environments.
- Run both CLI helps and the real-child guard in qualified Python 3.14.
- Inspect applicable native source/policy/publication-control jobs before closeout.
- Record focused resource review separately from installed artifacts and historical
  owner cleanup.

## Resolution — 2026-10-08

The existing subprocess calls now receive literal argument lists and their result
becomes the CLI exit status through SystemExit. Create unwinds its existing
managed context after the completed child, cleaning the private manifest and
restoring the working directory. Update keeps the original --prune choice and
active-target semantics. Neither wrapper deletes the environment or input.

Qualified Python 3.14.7: all eight real-child cases pass after six reproduced
failures and two controls before. Both helps pass. With the unchanged central
SDK 1f753e318d8dfa43c5bae1fa127e30ea86fa93b6, all 201 ordinary source tests pass;
five sibling integration cases remain explicitly skipped because this isolated
workspace does not supply the three sibling clones. The initial run had 196
passes and ten skips before providing the SDK; that is superseded for the five
shared-input negative guards. Default distribution checking verifies twenty
routes with declared-and-installed public bounds. No real solver, release,
installed artifact/matrix or scientific compatibility claim is made.

Guard relevance: subprocess-backed manager failure must reach the wrapper's exit;
exact child argv must retain spaced paths; private YAML must exist during manager
execution and be absent after return. Caller input and sentinel remain identical.
This fails on the original discarded result/string invocation and is independent
of the provider runtime package. Applicable native gates are inspected and linked
in the owning issue before its board closure; those are separate from local proof.
