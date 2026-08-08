# Release and Versioning

This page summarizes the practical release flow used in this repository.

## 1. Prepare release content

Before tagging:
- ensure tests pass;
- ensure public API contract tests pass;
- ensure docs build;
- ensure README and docs reflect actual behavior;
- ensure `CHANGELOG.md` has release notes for the target version;
- ensure `devguide/roadmap.md` reflects delivered vs in-progress milestones;
- ensure support/deprecation notes are updated when compatibility changed;
- verify ignored/generated files are not accidentally tracked.

## 2. Commit and push release-ready state

Create coherent commits and push `main`.

## 3. Create and push tag

Use semantic version tags (for example `0.2.0`) when release scope is clear and repository state is stable.

## 4. Post-tag validation

After pushing a tag:
- verify release badge/version links;
- verify docs references to release when applicable;
- confirm no local drift remains.

## 5. Pre-RC and Stabilization Quality Gates (`0.8.0`/`0.9.x`/`0.10.x`)

When preparing release candidates:
- accept only bug fixes and documentation consistency changes;
- avoid feature additions unless they unblock release quality;
- require explicit migration notes for any contract-affecting change;
- keep migration notes centralized in `CHANGELOG.md`;
- keep contract tests green before tagging.
