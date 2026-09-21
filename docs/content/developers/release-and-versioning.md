# Release and Versioning

This page summarizes the practical release flow used in this repository.

## 1. Prepare release content

Before tagging:
- ensure tests pass;
- decide and record the Conda route in `devtools/conda-build/release_plan.toml`;
- run the full Python/platform matrix on the exact candidate commit;
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

Use canonical three-part tags (for example `0.2.0`) without a `v` prefix or
prerelease suffix. The tag must identify the commit that passed the release
gates. Candidate testing takes place in the Conda staging label; it does not
create a public prerelease tag. Follow the two procedures in
`devguide/conda_release_routes.md`: an unstaged release can publish Conda
automatically after its preflight, while a staged release must promote the
exact tested file and SHA-256. Do not re-upload the staged filename.

## 4. Post-tag validation

After pushing a tag:
- verify release badge/version links;
- verify the exact public Conda coordinate and digest independently;
- verify the public Zenodo archival record and file inventory when required;
- verify docs references to release when applicable;
- confirm no local drift remains.

## 5. Pre-RC and Stabilization Quality Gates (`0.8.0`/`0.9.x`/`0.10.x`)

When preparing release candidates:
- accept only bug fixes and documentation consistency changes;
- avoid feature additions unless they unblock release quality;
- require explicit migration notes for any contract-affecting change;
- keep migration notes centralized in `CHANGELOG.md`;
- keep contract tests green before tagging.
