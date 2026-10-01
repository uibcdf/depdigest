---
summary: Share optional-engine availability and truthful installation routes across scientific consumers.
issue: uibcdf/depdigest#22
status: resolved
opened: 2026-09-30
closed: 2026-10-01
severity: medium
verification: reproduced
area: [dependency, integration]
guard: tests/test_optional_engines.py
normative: docs/content/user/optional-engines.md
blocked_by: []
supersedes: []
---

# Optional scientific engines

## What

Complete the existing DepDigest/SMonitor optional-dependency recipe for original
Python engines and local executable engines. Ownership remains in DepDigest;
scientific execution and result conversion remain in the consumer.

## How

TopoMT needs pip-only Pocketeer, AlphaSpace2 and pyCASTA plus the Conda-installed
fpocket command. Main at `edce73e10ffb8b94a336f1862e7b5700f989d1cf` already supplies
conditional guards and consumer documentation/channel metadata. However, explicit
`conda=None` is treated as an absent value, disabled routes produce commands naming
`None` in the inventory, the inventory ignores the channel, and executable plugins
use Python discovery.

The prepared implementation shares kind-aware availability between the checker,
decorator, inventory and LazyRegistry. Executables use current PATH/permissions
without executing a command. Explicit disabled routes return `None` in the
inventory and are absent from hints. Existing Python defaults and public inventory
keys remain compatible. The adoption page describes both provider and consumer
responsibilities; the canonical provider-owned integration guide is updated.
Suite adoption is tracked in `uibcdf/molsyssuite#62`.

Evidence: provider suite 129 passed and one collective sibling test skipped in an
isolated checkout; Ruff passed; HTML documentation built with two existing index
heading warnings. TopoMT's latest consumer regression selection passed 61 tests;
29 dependency/catalog tests passed against this prepared provider, and three
installed-distribution comparisons passed on Linux/Python 3.13.14. AlphaSpace2's
published unbound contact initialization requires a consumer compatibility step;
pyCASTA's absolute internal imports require process isolation. Those are not
availability mechanisms to move into DepDigest.

## Why

MolSysMT already adopts the core guard mechanism, while MolSysViewer uses a
different consumer exception contract. Future DockingMT and ElastNetMT should find
one owned recipe and shared tests rather than duplicate executable discovery,
invent install commands, or silently substitute a scientific method.

## Acceptance criteria

- Review, integrate and release the provider changes; do not mark this proposal
  complete merely because its isolated implementation passes tests.
- Preserve Python guard behavior and SMonitor event contracts.
- Keep disabled installers and declared channels consistent across entry points.
- Synchronize the accepted canonical guide through MolSysSuite.
- Track consumer adoption and retirement of local executable compatibility checks.
- Keep transitive imports, service state, execution failures and scientific parity
  distinct from availability.

## Integration update: 2026-09-30

The implementation is committed on `main` in `08f8263`; `457e72a` formats the
owned documentation examples. The maintainer-authorized direct push was
verified. The proposal remains open for release and consumer adoption;
canonical-guide distribution has since completed under uibcdf/molsyssuite#63.
TopoMT's consumer checks against this implementation
passed 29 tests; its full suite remains non-green due to viewer-addon
compatibility and native pyCASTA parity, independently tracked from availability.

## Publication candidate: 0.12.0

Canonical `DEPDIGEST_GUIDE.md` distribution is resolved under
uibcdf/molsyssuite#63. The new shared optional-engine policy and generated starter
worksheet are recorded under uibcdf/molsyssuite#62. The component-facing
`MOLSYSSUITE_GUIDE.md` now requires the recipe at applicable boundaries; its
generated copy is committed locally in `b6e0238`.

The maintainer authorized publishing the capability and subsequent TopoMT adoption.
The candidate selects `0.12.0`, staged build `py_0`, and exact-source full matrix
plus suite policy gates. The existing twelve-cell installed-artifact workflow
verifies the exact producer receipts, file SHA-256, Python/package versions,
public SMonitor dependency, off-checkout import and launcher. Additional installed
optional-engine contract checks verify the new behavior before public promotion.
Keep source, producer, installed and public evidence separate. No tag is moved and
no occupied file is overwritten. Final SHA, runs and digest follow once measured.

Release and consumer gates remain open. TopoMT must preserve custom executable
selection, catch compatibility and internal execution failures when it replaces
the local fpocket missing-command translation with the published provider.

The installed gate now exercises the new capability in every 0.12.0-or-newer
cell using the already verified installed import. It checks the actual configured
Python executable and an absent command without launching either, inventory
availability, disabled installers, the declared Conda channel and the missing-command
diagnostic. Older recorded candidates retain their original verification scope.
Three regression tests failed before this gate existed; they now also reject an
invented disabled installer and ignoring the configured command. The initial gate
draft incorrectly passed executable options to Python-only `is_installed`; it was
corrected to the published `check_dependency` interface before committing.

Local candidate verification: 133 tests passed on Linux/Python 3.13.15 with public
Conda SMonitor 0.17.3, including the available-sibling collective contract. Ruff
lint/format over 135 files, report indexes and central repository conformance passed.
The first citation check correctly rejected a stale 0.11.2 citation after changing
the release plan; CITATION.cff now names the 0.12.0 candidate and release date.
HTML documentation builds with the same two existing index-heading warnings.
The public registry returned explicit HTTP 404 for version 0.12.0 before staging;
the producer must still verify its immutable target coordinate when uploading.

Candidate `0b2175544f3ead3fca62d778d02380a006a0c751` passed routine CI
36788218185 and suite policy 36788218727. Its full matrix 36788295286 passed
all eight Linux/macOS cells but failed all four Windows `Run tests` steps.
Native Windows logs identify four existing optional-engine fixture failures:
an extensionless POSIX command was not discoverable through Windows PATHEXT,
and chmod-based executable removal is not a Windows contract. The new installed
release-gate tests passed in those cells. No public tag or staging upload was made.

The fixture correction uses a `.exe` name on Windows and the existing POSIX
name elsewhere. PATH changes, explicit paths and file removal are asserted on
every platform; mode-bit assertions remain in POSIX branches. All four tests
still execute on Windows, with no new platform skips and no provider runtime
or scientific assertions changed. The corrected exact candidate requires a new
complete source matrix; the prior failure remains evidence, not a waiver.


## Resolution: 2026-10-01

DepDigest 0.12.0 is published at immutable commit
`0da46d9ff31fbe2f92e4e667a32868aebe840b39`. Source matrix `36788849230`,
policy `36788753565`, staging producer `36789413638`, installed matrix
`36823713839` and promotion `36824539168` passed. Both source and installed
matrices executed all twelve Linux/macOS/Windows × Python 3.11–3.14 cells.
The promoted public file preserves SHA-256
`03d5aa569bfeb95bdd253a52e68e59094d9af5a6c4c7bc4ba228d3e36cfb30a3`.
Independent public download and clean Linux/Python 3.13.15 installation verified
version, off-checkout import, Conda URL/digest, optional-engine contract and CLI.
No tag moved, file overwritten, scientific assertion weakened or failure waived.

TopoMT adopted the published capability in `1aa25c4`, declared the >=0.12.0 floor
in runtime manifests and retained the exact release commit in its controlled pin.
Its fpocket boundary uses shared discovery for the supplied command and translates
only an explicit absence sentinel into the existing public error contract.
Unrelated provider/import/filesystem/execution failures remain separate.
Its six-test focused workflow `36825125490` passed on Linux/macOS and Python
3.11–3.13, with actual public artifact origin/version/URL/digest verified in
every cell. Seven administrative checks also passed locally. The broad consumer
review remains under uibcdf/topomt#56/#15; scientific full suites are not certified.

The provider-owned guide distribution was already resolved under
uibcdf/molsyssuite#63. The component-facing common recipe is now distributed to
all fifteen registered consumers under uibcdf/molsyssuite#62, with remote audits
`36787721831` and `36788852416` passing. Guidance requires adoption whenever an
applicable optional boundary is introduced or changed, with bounded exceptions.
MolSysMT/MolSysViewer scientific execution reviews remain deferred.

The guard `tests/test_optional_engines.py` exercises executable discovery through
PATH and explicit commands, inventory/LazyRegistry consistency, disabled
installers/channels and preserved transitive imports. These assertions cover the
reported shared failure mechanisms; Windows fixtures retain PATH/absolute-path
and file-removal checks with no new skips. Installed-gate regression tests also
reject invented installer routes and ignoring the configured command.
All provider proposal acceptance criteria are met; future consumer scientific
work and broad support-library reviews retain their own issue ownership.
