# DepDigest 1.0.0 preparation checklist

Updated: **2026-10-22**, under [#41](https://github.com/uibcdf/depdigest/issues/41).
Original integration checkpoint: 2026-10-04, under
[#26](https://github.com/uibcdf/depdigest/issues/26).
This preparation checkpoint does not authorize tagging or publishing 1.0.0.
The current public release is **0.15.1**, published and qualified under #39.
No 1.0 candidate or publication date has been selected.

## Dated preparation evidence

The following integration results are the **2026-10-04 source checkpoint**,
not a new run against current consumer sources or a future 1.0 artifact.

- [x] Run source integration with pinned, clean SMonitor, ArgDigest and
  PyUnitWizard sources in qualified Python 3.14 at that checkpoint.
- [x] Verify real quantity success, dimensionality failure and composed
  missing-dependency diagnostics with an isolated regression.
- [x] Check declared optional root imports independently of static audits.
- [x] Retain revisions, measurements, outcomes and limitations in
  [the collective evidence pack](collective_evidence_pack.md).
- [x] Keep #6 and #8 deferred without a compelling current consumer requirement.
- [x] Reconcile delivered LazyRegistry diagnostics with the roadmap.

Subsequent public qualification is recorded separately:

| Public release | Delivered capability | Retained release evidence |
| --- | --- | --- |
| 0.14.0 | `DeclaredRegistry` metadata and selective loading (#34/#35) | [2026-10-10 receipt](evidence/release_0.14.0_2026-10-10.json) |
| 0.15.0 | Explicit adapter inspection with strict default preserved (#36/#37) | [2026-10-13 receipt](evidence/release_0.15.0_2026-10-13.json) |
| 0.15.1 | Bounded concurrent declared value requests (#39) | [2026-10-13 receipt](evidence/release_0.15.1_2026-10-13.json) |

Each receipt separates exact source, installed artifact, public verification
and archival evidence. None claims MolSysMT adoption or conversion/scientific
parity. Capability floors and limitations are documented in the
[API stability guidance](../docs/content/developers/api-stability.md).

## Decisions before a release candidate

- [x] Resolve the source audit scope in
  [#27](https://github.com/uibcdf/depdigest/issues/27), including module-level
  control flow and separate syntax-error semantics.
- [x] Record consumer adapter-boundary decisions in
  [ArgDigest #22](https://github.com/uibcdf/argdigest/issues/22) and provider
  guide/adoption tracking in [MolSysSuite #95](https://github.com/uibcdf/molsyssuite/issues/95).
- [x] Record the consumer-owned template decision in
  [PyUnitWizard #93](https://github.com/uibcdf/pyunitwizard/issues/93).
- [ ] Decide whether a numerical startup budget is required; establish and
  validate it if so. Current timings impose no budget.
- [ ] Name the release decision owner and record consumer acceptance and
  remaining compatibility limitations.
- [ ] Finish public contract review, migration notes, changelog, support
  narrative and release version plan, including the public API through 0.15.1.

### Resolved audit-boundary decisions (reconciled 2026-10-22)

- **ArgDigest #22: closed.** The optional PyUnitWizard adapter uses a guarded
  execution-time import without an audit exemption. The published 0.13.0
  scanner returned zero findings on reviewed source
  `42b2f93346fdcd1573ade66a3f82a1717a496184`.
- **PyUnitWizard #93: closed.** The template and five runtime adapters have six
  individually documented exact-file exceptions, with root/public-export and
  requested-backend isolation regressions. On reviewed source
  `ef85201d619d2e50d4fd200a9196035d177f5a79`, the raw scan returned eleven
  findings, template-only exemption returned ten, and the six-file scope
  returned zero. No directory exemption or `--allow-violations` pass was used.
- **MolSysSuite #95: closed.** Guide delivery, owner notices and the two audit
  decisions were reconciled. The immutable
  [coordination record](https://github.com/uibcdf/molsyssuite/blob/4234be4a222846f189af290600a04c6162fde701/devguide/archive/coordinate_depdigest_expanded_audit_adoption.md)
  and [reconciliation receipt](https://github.com/uibcdf/molsyssuite/blob/4234be4a222846f189af290600a04c6162fde701/devguide/rollouts/depdigest_owner_reconciliation_95_20261004.json)
  retain exact sources, scanner identity and measured scope.

These closures resolve the earlier audit-boundary decisions. They do not certify
current public consumer artifacts, broader adoption or a future 1.0 integration.
Receiving `DeclaredRegistry` integration remains open in
[MolSysMT #382](https://github.com/uibcdf/molsysmt/issues/382), with suite impact
tracked in [MolSysSuite #115](https://github.com/uibcdf/molsyssuite/issues/115).
The receiving owner retains scientific/conversion parity and acceptance.

### Deferred work

- [#6](https://github.com/uibcdf/depdigest/issues/6) and
  [#8](https://github.com/uibcdf/depdigest/issues/8) remain deferred pending a
  justified consumer requirement; neither blocks 1.0.
- [#40](https://github.com/uibcdf/depdigest/issues/40) explicitly defers Python
  3.15 lazy-import implementation. It creates no support-bound change, 1.0
  commitment or deadline. The Python 3.11--3.14 support contract stays in place.

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

Existing 0.12.0--0.15.1 matrices and their public artifacts are historical
evidence, not closure of future candidate gates. Follow
[the release routes](conda_release_routes.md). This documentation reconciliation
reruns no integration or release qualification and changes no runtime contract,
dependency floor or public artifact.
