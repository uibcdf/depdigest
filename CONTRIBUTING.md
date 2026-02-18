# Contributing to DepDigest

Thanks for contributing. This guide is the practical workflow for code and docs contributions.

## 1. Before you start

- Read the user and developer docs:
- `docs/content/user/index.md`
- `docs/content/developers/index.md`
- Review the integration contracts:
- `standards/DEPDIGEST_GUIDE.md`
- `SMONITOR_GUIDE.md`

## 2. Create a focused branch

Work in one branch per topic (feature, fix, docs, or tests). Keep scope tight so reviews are fast and safe.

## 3. Validate locally

Minimum checks before opening a PR:

```bash
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

Use the PR template and include:
- short scope summary;
- behavior change notes;
- test evidence;
- docs impact.

## 6. Diagnostics and contracts

If you touch diagnostics:
- follow `SMONITOR_GUIDE.md`;
- keep catalog-driven messages;
- do not silence emission failures.

If you touch dependency resolution:
- keep runtime resolution behavior stable;
- preserve hard vs soft dependency semantics documented in `standards/DEPDIGEST_GUIDE.md`.
