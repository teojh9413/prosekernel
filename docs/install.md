# Installing and Running ProseKernel Locally

ProseKernel is currently a repo-local Python CLI plus a rights-safe writing library. It needs access to the repository/data root because commands read `library/`, `patterns/`, `evals/`, `learning/`, and related docs.

## Repo-local install

From the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Then verify the CLI is available:

```bash
prosekernel --help
```

## Recommended local usage

The simplest path is to run commands from the ProseKernel repo root:

```bash
cd /path/to/prosekernel
prosekernel search-examples "write a launch email for ProseKernel"
prosekernel brief "write a launch email for ProseKernel"
prosekernel validate-library
prosekernel validate-learning
prosekernel eval
```

When run from the repo root, ProseKernel auto-detects the data root by finding these markers:

- `pyproject.toml`
- `library/`
- `patterns/`
- `src/prosekernel`

## Running from another directory with `--root`

If you installed the CLI but are working elsewhere, pass the repo/data root explicitly:

```bash
prosekernel search-examples "rewrite checkout recovery microcopy" --root /path/to/prosekernel
prosekernel brief "write a security incident update" --root /path/to/prosekernel
prosekernel validate-library --root /path/to/prosekernel
prosekernel validate-learning --root /path/to/prosekernel
prosekernel eval --root /path/to/prosekernel
```

## Running from another directory with `PROSEKERNEL_ROOT`

You can also set an environment variable once per shell session:

```bash
export PROSEKERNEL_ROOT=/path/to/prosekernel
prosekernel search-examples "write a launch email for ProseKernel"
prosekernel brief "write a launch email for ProseKernel"
```

## Root resolution order

Root-aware commands resolve the repo/data root in this order:

1. explicit `--root`
2. `PROSEKERNEL_ROOT`
3. upward search from the current working directory
4. clear failure message if no valid root can be found

The failure message tells you to run from the repo root, pass `--root /path/to/prosekernel`, or set `PROSEKERNEL_ROOT=/path/to/prosekernel`.

## No silent empty retrieval

If ProseKernel cannot find its repo/data root, retrieval commands fail cleanly instead of silently returning empty search results. This is intentional: an empty result from a missing library is a setup error, not a writing judgment.
