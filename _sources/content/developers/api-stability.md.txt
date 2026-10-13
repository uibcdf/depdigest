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
- `DeclaredRegistry` (from 0.14.0)
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

From 0.13.0, audits include module/class control flow. An audit can report
additional imports and return 1 on unchanged consumer source. Function bodies
remain delayed; simple explicit, unrebound `typing.TYPE_CHECKING` guards exclude
their typing branch. Unresolved or compound conditions are scanned conservatively.
The audit is neither a runtime reachability proof nor a syntax validator.
See the [audit CLI scope](../user/audit-cli.md) and the 0.13.0 migration notes
in `CHANGELOG.md` before upgrading an audit gate.

## Change management guidance

`DeclaredRegistry` retains legacy registry behavior and separates metadata from
materialization. Its ordering, mutation, filtering, discovery and cache contracts
are defined in the [registry contract](../user/declared-registry.md). Source
experiments must pin the implementation commit; consumer public adoption requires
published DepDigest >=0.14.0 before changing dependency floors. Publication is
tracked in DepDigest #35 and consumer qualification in MolSysMT #382.

From 0.15.0, #36 adds keyword-only `load_policy="adapter"` for explicit adapter
inspection. Omission or `"strict"` preserves 0.14.0's dependency precheck; visibility,
identity, caching and execution guards retain their contracts. Public 0.14.0 does
not accept this option. Public adoption requires admitted DepDigest >=0.15.0, tracked in #37; controlled
source pins alone do not establish publication or consumer conversion parity.

From 0.15.1, #39 serializes overlapping declared value requests on a shared
`DeclaredRegistry` through initialization. Waiters share the cached value or
failure cause; genuine recursion still fails. The constructor, defaults and
legacy registry remain unchanged. Mutation/discovery/configuration changes and
arbitrary cross-registry cycles require separate coordination. See the bounded
[concurrent reader contract](../user/declared-registry.md).
Public use requires admitted DepDigest >=0.15.1; source-only checks do not admit it.

Before changing public behavior:
- add/update contract tests first;
- update this page and `standards/DEPDIGEST_GUIDE.md`;
- call out compatibility impact in PR/release notes.
