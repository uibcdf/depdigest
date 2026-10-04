# Collective Evidence Pack

Date: **2026-10-04**. Owning refresh: [DepDigest #26](https://github.com/uibcdf/depdigest/issues/26).
Public baseline: **0.12.0**. Source runtime baseline:
`a056c2fa9962e21c93b7c149118b41f9bf646947`.

The current local source integration passed. This checkpoint does not establish
collective release approval, installed-package compatibility for a future 1.0.0
candidate, another platform or a full consumer scientific suite. The release
decision remains pending under the [1.0 checklist](release_1.0.0_checklist.md).

## Sources and environment

The qualified `molsyssuite@uibcdf_3.14` environment supplied Python 3.14.7,
Pint 0.26.1 and ordinary runtime dependencies on Linux x86_64.
`python -m pip check` passed. DepDigest was imported from this checkout; the
three consumers/providers used clean temporary clones pinned to refreshed
remote sources. The probe checked every loaded package's actual origin.

| Component | Source commit | State used |
| --- | --- | --- |
| DepDigest | `a056c2fa9962e21c93b7c149118b41f9bf646947` | Runtime baseline; only validation/docs changes during the probe |
| SMonitor | `a1f5ee12bdc3065dbdc8660d48b91c8466d19d17` | Clean snapshot |
| ArgDigest | `a31be2823a7575a774f02e4b8490f6af884c38b5` | Clean snapshot |
| PyUnitWizard | `d70bdffe7cfdd7685c4830330c5f75d6465878da` | Clean snapshot |

The shared suite-status tool refreshed these four repositories before testing.
The original SMonitor, ArgDigest and PyUnitWizard checkouts were respectively
one, 44 and six commits behind; their worktrees and branches were preserved.
No consumer source, environment dependency or public artifact was changed.

## Executed contract evidence

`devtools/integration_probe.py` is the maintained standalone probe. The five
isolated cases in `tests/e2e/test_collective_error_path.py` invoke it. Two tests
in `tests/test_integration_probe.py` protect rejection of an invalid explicit
workspace and an eager conditional optional import.

The contracts case used the real ArgDigest quantity pipeline, PyUnitWizard
conversion/checking and Pint engine:

- A 1 nm quantity passed a length contract and returned 10 angstroms.
- A time quantity failed before the body with `ARG-ERR-VAL-001`.
- An **integrator fixture**, using the real PyUnitWizard declaration and a
  conditional DepDigest guard, simulated unyt absence with an import hook.
  Two valid-length calls selecting unyt each raised before the body and emitted
  `DEP-ERR-MISS-001` with `library=unyt`, `caller=accept_distance`, installation
  hints, a rendered message and an ArgDigest breadcrumb.
- Dict and JSON introspection agreed: unyt was missing and both pip and Conda
  routes were present. The normal Pint route did not require unyt.

The composed guard is a fixture, not a current PyUnitWizard production call
site. Absence is simulated, not a clean engine-free installation. The consumer
declaration supplies no `DOC_URL`, so messages retain the documented DepDigest
fallback; this test does not claim a consumer documentation override.

The intentionally retained normalized receipt is
[`evidence/pre_1_integration_2026-10-04.json`](evidence/pre_1_integration_2026-10-04.json).
It contains controlled fixture data and measurements, not raw workflow logs.
Public API, CLI, optional executable and cache guards remain in
`tests/test_public_api_contract.py`, `tests/test_cli_contract.py`,
`tests/test_optional_engines.py` and `tests/test_decorator_cache_contract.py`.

## Optional imports and static audits

Three fresh processes per package observed the first import after the probe's
standard-library setup. No declared optional root was loaded by ArgDigest or
PyUnitWizard. SMonitor and DepDigest have no `_depdigest.py` declaration for
this check; their rows describe imports, not unspecified optional dependencies.

| Package | Added modules | Import duration range (ms) | Optional roots checked |
| --- | ---: | ---: | --- |
| DepDigest | 60 | 34.48–34.88 | No declaration |
| SMonitor | 38 | 23.22–26.18 | No declaration |
| ArgDigest | 122 | 68.82–70.90 | beartype, pydantic, pyunitwizard |
| PyUnitWizard | 57 | 31.13–33.49 | ackredit, astropy, openmm, physipy, quantities, unyt |

These same-host durations have no accepted startup budget. They do not qualify
the full interpreter cold start or establish an application speedup. The
separate consumer-performance investigation in #6/#25 remains deferred.

The public audit CLI ran separately, without blanket adapter exemptions:

| Source tree / selection | Exit | Findings |
| --- | ---: | --- |
| DepDigest / openmm, mdtraj | 0 | None |
| ArgDigest / declared optional roots | 0 | None |
| PyUnitWizard / declared optional roots | 1 | `forms/template_api_form.py:1`, `import unyt` |
| Same PyUnitWizard tree / explicit single-template exemption | 0 | None |

The template is a tested adapter scaffold and was not loaded at startup. The
raw and narrowly exempted results are distinct. PyUnitWizard owns the policy
decision in [PyUnitWizard #93](https://github.com/uibcdf/pyunitwizard/issues/93).
DepDigest does not adopt the exemption on the consumer's behalf.

A synthetic `if True: import unyt` initializer returned zero static findings.
Direct AST imports are the current scanner's scope; conditional, try and class
traversal needs a decision in [DepDigest #27](https://github.com/uibcdf/depdigest/issues/27).
The runtime probe rejects the equivalent eager-import fixture. A clean static
audit therefore does not certify absence of runtime import leaks.

### Audit correction after this checkpoint (#27, 2026-10-04)

The dated table above and its receipt retain the earlier scanner's results.
The correction under #27 now scans module/class control flow, skips delayed
function bodies and recognizes simple explicit, unrebound typing-only guards.
Syntax-error behavior remains unchanged and is now documented as a limit.

On the same clean consumer snapshots, the expanded audit returns one finding
for ArgDigest (`contrib/pyunitwizard_support.py:13`) and eleven for PyUnitWizard
(the template plus ten imports across five adapter modules). The template-only
exemption now leaves ten findings. The root-import probes still pass. These
are source-scope findings, not evidence that the root packages load those
adapters eagerly. The normalized follow-up is
[`evidence/audit_control_flow_2026-10-04.json`](evidence/audit_control_flow_2026-10-04.json).

Consumer decisions are owned by [ArgDigest #22](https://github.com/uibcdf/argdigest/issues/22)
and [PyUnitWizard #93](https://github.com/uibcdf/pyunitwizard/issues/93).
[MolSysSuite #95](https://github.com/uibcdf/molsyssuite/issues/95) tracks the
provider/guide impact, pending guide synchronization and consumer adoption.
The public 0.12.0 provider and the original consumer checkouts are unchanged.

## Reproduction

Create clean SMonitor, ArgDigest and PyUnitWizard clones under one workspace,
pin them to the table's commits, and use the qualified Python 3.14 environment.
The probe always uses this DepDigest checkout.

```bash
python -I devtools/integration_probe.py --workspace /tmp/depdigest-1-integration --output /tmp/contracts.json
python -I devtools/integration_probe.py --workspace /tmp/depdigest-1-integration --case imports --package argdigest --output /tmp/argdigest-import.json
DEPDIGEST_INTEGRATION_WORKSPACE=/tmp/depdigest-1-integration python -m pytest --receptor=llm tests/e2e/test_collective_error_path.py tests/test_integration_probe.py
python -m depdigest audit --src-root /tmp/depdigest-1-integration/argdigest/argdigest --soft-deps beartype,pydantic,pyunitwizard --json
python -m depdigest audit --src-root /tmp/depdigest-1-integration/pyunitwizard/pyunitwizard --soft-deps ackredit,unyt,openmm,astropy,physipy,quantities --json
```

Run the import command for each package three times in new processes. For the
exempted PyUnitWizard comparison add
`--exempt-file /tmp/depdigest-1-integration/pyunitwizard/pyunitwizard/forms/template_api_form.py`.
Retain exit statuses: the raw PyUnitWizard audit is expected to exit 1.
An explicitly missing workspace fails. Hosted source suites without siblings
skip the five integration cases and do not establish cross-library evidence.

## Remaining decisions

- Consumer owners: settle the adapter/template boundaries in ArgDigest #22 and
  PyUnitWizard #93; the provider scanner contract is resolved under #27.
- MolSysSuite #95: synchronize the updated provider guide and track consumer
  source/installed adoption separately from provider implementation.
- Choose a numerical startup budget if required for 1.0 and validate it.
- Execute candidate-specific source/installed-artifact gates and record consumer
  acceptance before a 1.0 go/no-go decision. Existing 0.12.0 matrices are
  historical evidence, not a future candidate's certificate.

## Historical checkpoint (2026-03-04)

The previous checkpoint used DepDigest 0.10.0 at `09b2302`. It recorded SMonitor
`0.11.4-16-ge0e1a8c` and ArgDigest `0.9.0-9-gc543c1a` as in progress, and
PyUnitWizard `0.21.1-1-g9fd9b46` and DepDigest as done locally. Collective
closure, audit leak checks, remediation proof and startup budget remained
pending. Those states do not describe the October snapshots.
