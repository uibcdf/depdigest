# DepDigest 1.0.0 preparation checklist

Updated: 2026-10-04, under [#26](https://github.com/uibcdf/depdigest/issues/26).
This preparation checkpoint does not authorize tagging or publishing 1.0.0.
The current public release is 0.12.0.

## Current preparation evidence

- [x] Run current source integration with pinned, clean SMonitor, ArgDigest and
  PyUnitWizard sources in qualified Python 3.14.
- [x] Verify real quantity success, dimensionality failure and composed
  missing-dependency diagnostics with an isolated regression.
- [x] Check declared optional root imports independently of static audits.
- [x] Retain revisions, measurements, outcomes and limitations in
  [the collective evidence pack](collective_evidence_pack.md).
- [x] Keep #6 and #8 deferred without a compelling current consumer requirement.
- [x] Reconcile delivered LazyRegistry diagnostics with the roadmap.

## Decisions before a release candidate

- [ ] Resolve or explicitly accept audit scope in
  [#27](https://github.com/uibcdf/depdigest/issues/27), including module-level
  control flow and separate syntax-error semantics.
- [ ] Record the consumer-owned template decision in
  [PyUnitWizard #93](https://github.com/uibcdf/pyunitwizard/issues/93).
- [ ] Decide whether a numerical startup budget is required; establish and
  validate it if so. Current timings impose no budget.
- [ ] Name the release decision owner and record consumer acceptance and
  remaining compatibility limitations.
- [ ] Finish public contract review, migration notes, changelog, support
  narrative and release version plan.

## Candidate-specific gates

- [ ] Pin candidate source SHA and Conda release route before tagging.
- [ ] Pass the required exact-source matrix and API/CLI/schema contract suite.
- [ ] Validate the exact installed artifact on supported platforms and Python
  minors; retain source, filename and SHA-256 evidence.
- [ ] Re-run relevant consumer integration against the candidate, separating
  source from installed-package evidence.
- [ ] Verify docs, CLI, distribution contents and archive/attribution claims
  required by the chosen release route.
- [ ] Record dated go/no-go evidence and accepted limitations.

Existing 0.12.0 matrices and its public artifact are historical evidence, not
closure of future candidate gates. Follow [the release routes](conda_release_routes.md).
