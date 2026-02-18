# Architecture & Critical Decisions

DepDigest is designed around contract-driven, runtime dependency control.

## Architectural model

1. Contract declaration

Host packages declare dependency policy in `_depdigest.py`.

2. Runtime resolution

DepDigest resolves package configuration at call time, not decorator-definition/import time.

3. Execution guarding

`@dep_digest` enforces dependency presence immediately before protected logic executes.

4. Lazy access

`LazyRegistry` defers plugin imports until registry access requests them.

5. Diagnostics emission

SMonitor emits structured events for missing dependencies and orchestration paths.

## Critical decisions

1. Runtime config resolution

This keeps tests and dynamic package contexts flexible.

2. Mapping-like lazy registry

`LazyRegistry` behaves as a mapping to integrate easily with existing plugin registries.

3. Automatic package context discovery

DepDigest minimizes boilerplate in host libraries by inferring package root context.

## Current limits

- DepDigest does not solve full environment/package management.
- Version-range enforcement is not a first-class policy yet.
- Cross-soft-dependency transitive modeling remains explicit in host library code.
