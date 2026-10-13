---
summary: Correct inherited descriptive metadata and preserve it across dependency broadcasts.
issue: uibcdf/depdigest#38
status: resolved
opened: 2026-10-13
closed: 2026-10-13
severity: low
verification: measured
area: [packaging, metadata]
guard: tests/test_broadcast_requirements.py::test_committed_profiles_are_generated_without_python_duplicates
normative: devtools/conda-build/README.md
blocked_by: []
supersedes: []
---

# Correct Conda recipe metadata

## What

The recipe has an empty summary, a quantities-library description and an
organization-wide home URL. DepDigest owns optional dependency checks, lazy/selective
plugin loading and optional-import audits. Diego authorized this correction.

## How

The existing broadcaster updates dependency sections/environment profiles while
preserving recipe `about`. Correct that maintained metadata directly, document this
bounded case, and execute existing generation/reporting guards. Compare the complete
recipe outside `about` and all dependency inputs/generated environments for equality.

## Why

Package metadata should identify the library and its project/documentation accurately.
The existing generator can preserve these fields but cannot derive them. No new
metadata generator, runtime feature or dependency change is needed. Published 0.15.0
identity/bytes and existing release evidence remain historical and immutable.

## Acceptance criteria

- Summary/description describe DepDigest; URLs identify this project and documentation.
- Broadcast preserves the correction and all dependency/profile/build/version/CLI fields.
- Local and hosted checks pass; archive the report and close its owning issue.

## Resolution — 2026-10-13

Corrected recipe summary to match the maintained project description, replaced
the quantities description with DepDigest's actual dependency/plugin/audit scope,
and selected project-specific canonical repository/documentation URLs. The project
Documentation URL now matches the verified canonical www route used by the recipe.

No generator change or new test was needed. The recipe README documents that
`about` is maintained directly because the existing broadcaster preserves rather
than derives it, the bounded non-dependency metadata case allowed by devtools
instructions. This is not permission to edit generated dependency sections.
The existing selected guard compares the complete regenerated recipe, including
`about`, with maintained bytes; it protects retention across broadcast rather than
judging descriptive wording. The maintained metadata rule and explicit local
comparison protect summary/project URL agreement and semantic ownership.

The eight existing broadcast/reporting cases pass with routine Python 3.14 tools.
An independent comparison proves the entire recipe outside `about` unchanged,
plus byte-identical requirements input and six generated environment profiles.
Version/build/entry-point/runtime dependency fields and scientific code are intact.
The published 0.15.0 tag/archive/evidence are preserved; this source correction
applies to future package builds and is not a replacement release.

## Published closeout — 2026-10-13

Implementation `1bb8e855c6edf6e17228a9511eafbae728ef51c8` is published directly.
Exact-head CI 38423532253, MolSysSuite policy 38423532720 and publication governance
38423532703 pass; GH Run Receptor confirms an executed successful test job.
Issue #38 is closed with its outcome and archive path.

After checks and owning-issue handoff, the manifest-owned exact root
`/tmp/depdigest-metadata-9zo6o2v3` and its private broadcast/test fixtures were removed.
No active process referred to it, its absence was confirmed and no cleanup error
occurred. Primary generated outputs, shared environments and public artifacts are
preserved. No environment was created or updated for this metadata-only task.
