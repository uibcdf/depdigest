# Developing guide

## Developers' Guide in the documentation

Check, first of all, the "Developers' Guide" section of the online documentation.

## Adding the required dependencies

This library needs some third python packages to work. And not only to work, but be documented,
tested or developed, for instance. The file 'requirements.yaml' contains a list of conda
channels and packages required to:

- Run the setup.py script ('setup' section)
- Use the library for production ('production' section)
- Run the library tests ('test' section)
- Compile the documentation ('docs' section)
- Work in the library development ('development' section)
- Build a conda package with this library ('conda-build')

This is the file where the library dependencies need to be included. And once the file has been
updated, execute the Python script 'broadcast\_requirements.py'. This last step will produce
individual yaml files to create and update, following the instructions of the next section, different conda
environments depending on the tasks you need to do.

## How to prepare the conda environments to work with this repository

You will find here a directory called 'conda-envs'. This directory contains all the info and
scripts you need to create and update a conda environment. Let's first have a look to the yaml
files:

```python
cd conda-envs
ls *.yaml
build_env.yaml  development_env.yaml  docs_env.yaml  production_env.yaml  setup_env.yaml  test_env.yaml
```

Each yaml file has the list of required packages and conda channels in case you want to:
- Build a conda package with this library ('build_env.yaml').
- Work in the library development ('development_env.yaml')
- Compile the documentation of this library ('docs_env.yaml')
- Use the library just for production ('production_env.yaml')
- Run the setup.py script ('setup_env.yaml')
- Run the library tests ('test_env.yaml')

This yaml files were produced with the script 'broadcast_requirements.py' and the file
'requirements.yaml' as indicated in the previous exception.

Finnally, to create a conda environment use the script 'create_conda_env.py' the following way:

```bash
# In this case the name of the environment is also "depdigest-dev"
# the Python version of our new environment is 3.13
# and the yaml file will be the one to work on the library development
python create_conda_env.py -n depdigest-dev -p 3.13 development_env.yaml
```

You can already activate the environment to start working in the library development:

```bash
conda activate depdigest-dev
```

In case the list of dependencies changed and the environment needs to be updated, use the Python
script 'update_conda_env.py' with the environment activated:

```bash
conda activate depdigest-dev
python update_conda_env.py development_env.yaml
```

## How to contribute changes
- Clone the repository if you have write access to the main repo, fork the repository if you are a collaborator.
- Make a new branch with `git checkout -b {your branch name}`
- Make changes and test your code
- Ensure that the test environment dependencies (`conda-envs`) line up with the build and deploy dependencies (`conda-recipe/meta.yaml`)
- Push the branch to the repo (either the main or your fork) with `git push -u origin {your branch name}`
  * Note that `origin` is the default name assigned to the remote, yours may be different
- Make a PR on GitHub with your changes
- We'll review the changes and get your code into the repo after lively discussion!

## Validating source integrations

Use `integration_probe.py` with the qualified Python 3.14 environment and clean,
pinned SMonitor, ArgDigest and PyUnitWizard clones under one workspace. Every
invocation must run in a fresh process; DepDigest always comes from this checkout.

```bash
python -I devtools/integration_probe.py --workspace /tmp/integration --output /tmp/contracts.json
python -I devtools/integration_probe.py --workspace /tmp/integration --case imports --package argdigest --output /tmp/imports.json
DEPDIGEST_INTEGRATION_WORKSPACE=/tmp/integration python -m pytest --receptor=llm tests/e2e/test_collective_error_path.py
```

`--case contracts` (default) checks a real Pint quantity through ArgDigest and
PyUnitWizard, wrong dimensionality, and an integrator fixture composing their
public APIs with DepDigest's conditional guard. An import hook simulates absent
unyt; both missing calls must raise before the body, emit coded events with
consumer fields and a breadcrumb, and agree with dict/JSON introspection. This
fixture is not presented as an existing PyUnitWizard production call site.

`--case imports` requires `--package`, one of the four participating packages.
It records module counts and a local import duration, and rejects loaded optional
roots declared in that package's `_depdigest.py`. Packages without a declaration
have no optional-root assertions. Durations have no accepted performance budget.
The probe verifies source origins for loaded packages and records Git state.
The JSON receipt goes to stdout or the `--output` file; diagnostics go to stderr.
`--help` requires no sibling imports. Invalid explicit workspaces fail; pytest
only skips the five integration cases when no workspace was requested and
siblings are absent. No installation or sibling worktree modification occurs.

Run the existing `python -m depdigest audit` separately for static source checks.
Its module/class control-flow findings, delayed function bodies, typing-only
guards and explicit exemptions are distinct from root-import execution. The
expanded scanner contract is documented under `uibcdf/depdigest#27`; consumer
audit boundaries and guide adoption remain under `uibcdf/molsyssuite#95`.
The dated outcomes and limitations are maintained in
`devguide/collective_evidence_pack.md`; this probe qualifies neither public
artifacts nor full scientific suites.

## Validating a staged Conda package

For a staged release candidate, use the exact commit, version, build number,
and successful producer run ID with the manual **Test staged Conda package**
workflow. It verifies the retained route and producer receipts and installs the
immutable artifact in clean Python 3.11–3.14 environments on Linux, macOS, and
Windows. It checks the installed SHA-256, exact source URLs, import, and CLI.
SMonitor is explicitly selected from the public channel to avoid accidentally
testing a staged dependency. See `devguide/conda_release_routes.md` for the
release route and promotion rules.

`devtools/conda-build/verify_staged_install.py receipts --help` lists the
producer-receipt inputs; `verify_staged_install.py installed --help` lists the
off-checkout installed-package checks. The validation workflow may be newer
than the candidate commit because it validates the immutable producer evidence,
not its own checkout as the package under test.

From candidate 0.13.0, the installed gate also exercises module/class audit
findings, typing-only and delayed exclusions, source lines, JSON and the visible
`--allow-violations` result. Earlier candidates retain their original gates.

Release archival uses `.github/workflows/verify-zenodo-releases.yaml`, pinned to
the shared MolSysSuite verifier. It performs one public probe after publication,
resumes every six hours from the fixed adoption cutoff, and accepts a manual
exact tag. Inspect the retained per-release state: a successful pending probe
does not prove archival. The intervention deadline stays 72 hours from original
publication, and only verified source-snapshot evidence permits a DOI claim.

## Checklist for updates
- [ ] Make sure there is an/are issue(s) opened for your specific update
- [ ] Create the PR, referencing the issue
- [ ] Debug the PR as needed until tests pass
- [ ] Tag the final, debugged version 
   *  `git tag -a X.Y.Z [latest pushed commit] && git push --follow-tags`
- [ ] Get the PR merged in

## Versioneer Auto-version
[Versioneer](https://github.com/warner/python-versioneer) will automatically infer what version 
is installed by looking at the `git` tags and how many commits ahead this version is. The format follows 
[PEP 440](https://www.python.org/dev/peps/pep-0440/) and has the regular expression of:
```regexp
\d+.\d+.\d+(?\+\d+-[a-z0-9]+)
```
If the version of this commit is the same as a `git` tag, the installed version is the same as the tag, 
e.g. `depdigest-0.1.2`, otherwise it will be appended with `+X` where `X` is the number of commits 
ahead from the last tag, and then `-YYYYYY` where the `Y`'s are replaced with the `git` commit hash.
