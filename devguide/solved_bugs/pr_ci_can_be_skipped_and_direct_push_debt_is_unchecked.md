---
summary: PR CI can be skipped and direct-push debt is unchecked
issue: uibcdf/depdigest#21
status: resolved
opened: 2026-09-29
closed: 2026-10-03
severity: high
verification: measured
area: [ci, governance]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# PR CI can be skipped and direct-push debt is unchecked

**Detector correction on 2026-09-29:** the review in
`uibcdf/pyunitwizard#91` reproduced an old workflow-run listing from GitHub's
`branch=main` API filter, and the same behavior was observed in SMonitor.
This detector now lists runs without that API filter and checks
`head_branch=main` locally, together with commit ancestry and executed
Linux test steps. A focused regression rejects an otherwise green run from
a feature branch.

At `166e9c9`, routine CI `36640883666` and policy `36640884216`
passed. The [corrected probe](https://github.com/uibcdf/depdigest/actions/runs/36640913043)
recognized `80e021e` as the executed full-matrix watermark and found zero
pending skipped commits. The matrix jobs were omitted. Actual daily schedule,
hosted PR execution and platform claims still need review.

## What

At `0353087`, the primary `CI.yaml` PR test ignored documentation paths and
allowed `[skip ci]` in PR titles or `skip-ci` in branch names to skip its test
job. `main` had no effective branch rules. Direct-push skip markers had no
daily full-suite recovery. The
[weekly twelve-cell matrix](https://github.com/uibcdf/depdigest/actions/runs/36455844421)
passed at that exact commit, including executed `Run tests` steps in all four
Linux cells. This is a routing and enforcement gap, not a failed test suite.

## How

Run the complete Linux 3.13 PR test without workflow path or title/branch
skip conditions. Require its stable check on PRs, while administrators retain
direct pushes. Preserve the existing weekly and manual full matrix. Add a
conditional daily full matrix at 00:47 America/Mexico_City that detects
skipped commits since the last executed, green Linux matrix. If run history
or API evidence is unavailable, run it. A probe input checks the backlog
without dispatching test jobs.

## Why

DepDigest is a shared support library. A green weekly matrix does not guard
a PR whose test job never ran, and repeated skipped direct pushes can leave
regressions unseen. The conditional daily route implements the suite policy
in `uibcdf/molsyssuite#39` without requiring a full matrix after each commit.

## Acceptance criteria

- The required PR test cannot be omitted by local filters or skip conditions.
- Skipped direct pushes stay due until an executed full Linux matrix passes.
- Hosted routine, full-matrix and probe evidence are recorded.
- Branch protection preserves direct pushes for the named internal maintainers.
- The first real nightly and PR route are observed before calling this adopted.

## Resolution

Commit `e6dfa7c` implements the workflow and detector. At that exact commit,
[routine CI](https://github.com/uibcdf/depdigest/actions/runs/36533588363)
and [MolSysSuite policy](https://github.com/uibcdf/depdigest/actions/runs/36533589077)
passed. The [probe-only dispatch](https://github.com/uibcdf/depdigest/actions/runs/36534534264)
recognized the executed weekly matrix `36455844421` at `0353087` as its
watermark, found zero later skipped commits, and omitted all matrix jobs.

The `main` branch now requires the strict `Test on ubuntu-latest, Python 3.13`
check. Administrators are exempt from the PR gate; the only current
collaborators with push permission are `dprada` and `LMMV`, both
administrators. Keep this issue open until the first actual nightly, hosted
PR route, and platform-claim review.

The direct push of `d779cfa` with `[skip ci]` exercised that bypass. A
[second probe-only dispatch](https://github.com/uibcdf/depdigest/actions/runs/36534652166)
found exactly that skipped commit after the `0353087` full-matrix watermark
and reported that full recovery is due. It omitted all matrix jobs because
the dispatch was diagnostic. A
[manual full-matrix dispatch](https://github.com/uibcdf/depdigest/actions/runs/36534834729)
then passed all twelve jobs at `80e021e`, including the four Linux `Run tests`
steps. The [post-matrix probe](https://github.com/uibcdf/depdigest/actions/runs/36534985790)
recognized `80e021e` as the new executed watermark and found zero pending
skipped commits; its matrix jobs were omitted. The actual daily schedule and
hosted PR execution remain to be observed. Keep the issue open until those
outcomes and the platform-claim review are recorded centrally.

## Routine policy 1.5.4 adoption — 2026-10-03

The maintainer authorized publication and adoption of policy-v1.5.4 under
uibcdf/molsyssuite#39. The immutable tag points to central e459ea0; the
component now calls that published gate and receives the byte-identical
canonical guide through the suite synchronizer. Routine development uses
Python 3.14. The existing full Python 3.11–3.14 matrices and skipped-commit
recovery semantics are preserved; no public package is published here.
Local conformance and changed-workflow Actionlint checks pass. Hosted
policy and applicable routine checks are dispatched separately from skipped
direct pushes; their exact commits and outcomes remain to be measured.

The single Linux routine package suite moves to Python 3.14; the required
PR check must use its new name while preserving strict checks and administrator
direct-push bypass. The complete weekly matrix still includes every older minor.

The development interpreter is changed in devtools/requirements.yaml and
regenerated through the existing broadcaster. No generated dependency file
is edited by hand.

## Hosted evidence review — 2026-10-03

The live classic branch protection API now requires the strict
`Test on ubuntu-latest, Python 3.14` check from GitHub Actions (app 15368).
Administrator enforcement remains disabled. The current push-capable
collaborators are `dprada` and `LMMV`, both administrators. The absence of a
repository ruleset does not mean the classic branch protection is absent.
This supersedes the historical Python 3.13 check name above.

The scheduled [run 37121680648](https://github.com/uibcdf/depdigest/actions/runs/37121680648)
at `104661a0f4aff894420107cb9d0ccb15bbf8fd4f` exercised actual recovery:
the detector found one skipped commit after the executed full-matrix anchor
`2d56ef4330e36ddba421c344acf5dab0f0221c7a`, requested the matrix, and all
twelve Linux/macOS/Windows Python 3.11–3.14 jobs passed their `Run tests`
steps. This is scheduled execution evidence, not a probe-only dispatch.
The cron remains 00:47 America/Mexico_City; GitHub actually started this run
at 12:04 UTC, so this evidence does not promise punctual cron delivery.

Platform review retains Linux, macOS Apple Silicon and Windows. The macOS
Python 3.14 source job in that run identifies `macos-26-arm64` and
`osx-arm64`; pytest reports 135 passed and one collective-integration skip
because sibling checkouts are absent. Intel macOS is outside the support
claim. The release 0.12.0
[installed-artifact run 36823713839](https://github.com/uibcdf/depdigest/actions/runs/36823713839)
at `0da46d9ff31fbe2f92e4e667a32868aebe840b39` passed all twelve clean
installation cells, including the installed-resource and command smoke
step outside the checkout. Its macOS Python 3.14 runner also identifies
`macos-26-arm64`. Source tests, installed-artifact smoke and public-channel
verification remain separate evidence; none certifies scientific behavior
of optional consumer engines.

The Python 3.14 routine [run 37122615391](https://github.com/uibcdf/depdigest/actions/runs/37122615391)
passed at `39e581a13b44f2a7965d4e50eb7f4db9e65562aa`. The latest manually
dispatched [policy run 37123106456](https://github.com/uibcdf/depdigest/actions/runs/37123106456)
passed at `e38c7f35128d977772dceb2ccca856f75df798f1`; these results do not
certify later commits.

Local Python 3.14 verification of `tests/test_ci_backlog.py` and
`tests/test_reporting_protocol.py` passed all nine tests. The backlog guard
checks that ordinary commits do not erase skipped debt, a probe with an
unexecuted test step cannot advance the watermark, feature-branch matrices
cannot clear main's debt, and uncertain API evidence requests recovery.

The remaining acceptance item is a hosted PR execution. A documentation-only
PR from `skip-ci/depdigest-21-evidence`, with `[skip ci]` in its title and
without a commit skip marker, will check the three formerly local omission
routes together. [GitHub's native commit skip directives](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs) are different: they
may suppress workflow creation, but the required check stays pending and
does not authorize an external merge. Administrator direct-push permission
remains the accepted internal route.

## Closure evidence — 2026-10-03

The documentation-only [PR #24](https://github.com/uibcdf/depdigest/pull/24)
passed the full Linux/Python 3.14 `Run tests` step in
[run 37158721627](https://github.com/uibcdf/depdigest/actions/runs/37158721627)
at head `276845902649e6ecd322765ddf66dfcac08d1399`. Its title contains
`[skip ci]`, its branch is `skip-ci/depdigest-21-evidence`, and its only
changed file is Markdown. All three former local omission routes therefore
coexist in a real passing PR test. The
[policy run 37158722110](https://github.com/uibcdf/depdigest/actions/runs/37158722110)
and [Conda governance run 37158722057](https://github.com/uibcdf/depdigest/actions/runs/37158722057)
also passed for that PR head. These are PR results, separate from the
nightly, release-candidate and installed-package results above.

The scheduled recovery, hosted PR execution and platform review acceptance
items are now met. The existing `tests/test_ci_backlog.py` guard protects
the skipped-debt mechanism as explained above; the hosted PR demonstrates
the unfiltered entry route and the live required-check API verifies merge
enforcement. Archive this record and regenerate the queue/archive indexes
in the same change. Merge of PR #24 closes the local issue; the central
`uibcdf/molsyssuite#39` rollout remains independently owned and open. Its
registry still records DepDigest as partial until the suite owner adopts
this linked evidence; local closure does not assert central adoption.
