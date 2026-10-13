# DepDigest Conda recipe

`meta.yaml` is derived from `devtools/requirements.yaml` by
`python devtools/broadcast_requirements.py`; edit the source requirements and
regenerate the recipe instead of changing dependency lines here by hand.

The broadcaster preserves the recipe's `about` section; it does not derive
descriptive metadata from `requirements.yaml`. Maintain those fields directly
in `meta.yaml`, the bounded metadata case recorded in DepDigest #38. Keep the
summary consistent with `pyproject.toml` and use this project's repository and
documentation URLs. Run the broadcaster after editing to check that the metadata
survives and dependency sections/generated environments stay unchanged.

Publication is owned by the repository workflows, not by a local `anaconda
upload` command. Read `devguide/conda_release_routes.md` before preparing a tag:
the committed plan chooses either a guarded direct release or an exact-file
staging and promotion route. The workflow uses one noarch build and retains
evidence; a local render is only a recipe check and never a publication gate.

For a tagged release, `python devtools/conda-build/release_route.py select
--version X.Y.Z` prints the route committed in that tag or fails when the
version and plan disagree. The release workflow uses this command before any
direct build step. Run `python devtools/conda-build/release_route.py --help`
for the route checker and public-verification commands.

Do not use `--force`, rebuild a staged filename for another label, or place the
staging channel ahead of the public channel in ordinary consumer environments.


From 0.15.1, the installed verifier runs `concurrent_registry_probe.py` in an
isolated subprocess with a 30-second deadlock bound. Its reusable operation
exercises strict/adapter and filesystem/entry-point readers, shared results and
failure causes, explicit retry, real recursion and an unrelated sentinel. Events
observe actual lock contention rather than a scheduling sleep. The subprocess
imports the selected environment's package, never the checked-out library.
The parent owns a private temporary root for child fixtures and retires it on
success, failure or timeout, even when a killed child cannot run its finalizers.
