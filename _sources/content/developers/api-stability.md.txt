# API Stability

This page defines the current public contract guarantees in DepDigest.

## Public API surface

The public API is defined by `depdigest.__all__`.

Current exported symbols:
- `is_installed`
- `check_dependency`
- `get_info`
- `dep_digest`
- `LazyRegistry`
- `DepConfig`
- `resolve_config`
- `register_package_config`
- `unregister_package_config`
- `temporary_package_config`
- `clear_package_configs`

Compatibility rule:
- removing or renaming these symbols is a breaking change.

## `get_info` schema contract

For `format="dict"` and `format="json"`, the schema is:
- name: `depdigest.get_info`
- version: `1.0`

Top-level keys:
- `schema`
- `module_path`
- `dependency_count`
- `installed_count`
- `missing_count`
- `dependencies`

Dependency entry keys:
- `library`
- `installed`
- `status`
- `type`
- `package_name`
- `install`

Compatibility rule:
- changing/removing keys or schema version without migration notes is a breaking change.

## CLI contract

`depdigest audit` behavior expected by integrators:
- returns `0` when no violations are found;
- returns `1` when violations exist (unless `--allow-violations`);
- `--json` output is machine-readable and deterministic.

## Change management guidance

Before changing public behavior:
- add/update contract tests first;
- update this page and `standards/DEPDIGEST_GUIDE.md`;
- call out compatibility impact in PR/release notes.
