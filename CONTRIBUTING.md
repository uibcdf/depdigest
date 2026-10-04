# Contributing to DepDigest

Thanks for contributing. This guide is the practical workflow for code and docs contributions.

## 1. Before you start

- Read the user and developer docs:
- `docs/content/user/index.md`
- `docs/content/developers/index.md`
- Review the integration contracts:
- `standards/DEPDIGEST_GUIDE.md`
- `SMONITOR_GUIDE.md`

## 2. Choose the contribution route

External contributions use one branch and PR per topic. Authorized internal
maintainers `dprada` and `LMMV` may commit on `main` and push directly, following
the checkpoints in `MOLSYSSUITE_GUIDE.md`. Keep focused commits local and batch
pushes at useful checkpoints; do not open a PR solely for internal CI execution.
Use a PR when an owner review is requested.

## 3. Validate locally

Baseline checks for a completed change (select interim checks by affected scope):

```bash
ruff check .
ruff format --check .
pytest -q
```

If behavior changed, run coverage:

```bash
pytest --cov=depdigest --cov-report=term-missing
```

If docs changed, build docs:

```bash
make -C docs html
```

## 4. Keep commits intentional

- One coherent change per commit.
- Use clear commit messages describing behavior impact.
- Update docs when contracts or user-facing behavior change.

## 5. Open the PR

For the PR route, use the template and include:
- short scope summary;
- behavior change notes;
- test evidence;
- docs impact.

For authorized internal direct pushes, record the outcome in the owning issue,
finish with an unskipped head and inspect its applicable CI. A skip is conditional,
not the default after local checks. Full recovery and release/publication gates
retain their own requirements.

## 6. Diagnostics and contracts

If you touch diagnostics:
- follow `SMONITOR_GUIDE.md`;
- keep catalog-driven messages;
- do not silence emission failures.

If you touch dependency resolution:
- keep runtime resolution behavior stable;
- preserve hard vs soft dependency semantics documented in `standards/DEPDIGEST_GUIDE.md`.
