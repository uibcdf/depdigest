---
summary: Distinguish internal relative adapters from external optional imports.
issue: uibcdf/depdigest#47
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [audit, imports]
guard: tests/test_relative_import_audit.py
normative:
blocked_by: []
supersedes: []
---

# Relative import audit classification

## What

The scanner reports an internal `from .vina import VinaBackend` as an external
optional Vina import. DockingMT #19 reproduces the finding without loading Vina
or molecular libraries. Provider runtime is unchanged between reported 0884f0c
and reviewed main 9dc562144b6fed9d6408ac9b64997c8636b1ccbe.

## How

Only absolute ImportFrom nodes (level zero) can name an external optional
package. Relative nodes retain their internal-package meaning. Import and
absolute ImportFrom matching, eager module/class control flow, typing guards,
delayed function scopes, original source lines and public CLI behavior remain.

The 27 new controls reproduce fifteen failures/twelve passes before correction.
They cover relative levels, dotted modules, aliases, wildcard/from-dot forms,
mixed eager scopes and lazy functions. CLI controls assert exact JSON findings,
normal and allow-violations exits and exact-file exemption behavior. All 27 pass
after the narrow correction; absolute-import adverse controls still report.

## Why

Reusable syntax classification belongs in DepDigest. A consumer-side adapter
rename, duplicated scanner, broad directory exemption or suppressed true external
import would conceal the distinction instead of correcting it. DockingMT's
selected widget-base inheritance has a separate exact-file disposition.

## Resolution boundary

This guarded resolution is proposed for owner review; main acceptance closes #47.
Shared advance impact/receiving is MolSysSuite #166. DockingMT #19 owns consumer
inventory and receiving; other registered audit users retain their own checks.
No public release, dependency floor, scientific gate or molecular behavior changes.

## Owner acceptance — 2026-11-05

PR #48 was reviewed and accepted as merge
`02339c2917588a91ba938575be44816d706b5e27`; #47 is closed. Main independently
reproduced the erroneous relative finding before acceptance. An isolated exact
proposal copy passed 79 audit, CLI, API and reporting cases, including all 27
owning controls. The merge's source CI `42072573073`, policy `42072574324` and
publication governance `42072574288` passed, inspected through GH Run Receptor.
This appends the receiving state to the original proposal boundary; the original
measurements and dates above retain their scope. The correction is accepted
source, not a new public package. Consumer receiving remains DockingMT #19 and
shared impact remains MolSysSuite #166.
