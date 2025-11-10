## Quick orientation for AI coding agents

This repository contains teaching labs for distributed systems (labs 1..6). Each lab is self-contained under `labN/` and uses small Python examples to illustrate networking, channels, threads/processes, and coordination protocols.

- Big picture:
  - Top-level: `lab1`..`lab6` directories, `lib/` contains shared helpers (`lab_channel`, `lab_logging`). See `README.md` for environment notes (pipenv, Redis, Jupyter).
  - Typical pattern: each lab exposes `Server` and `Client` classes (e.g. `lab1/clientserver.py`, `lab2/channel/channel.py`). Tests or example runners live alongside (`runsrv.py`, `runcl.py`, `doit.py`).

- Developer workflows (common commands):
  - Create environment and install deps: `pipenv install` (root `Pipfile`).
  - Run a notebook: `pipenv run jupyter notebook --ip 127.0.0.1`.
  - Start Redis (required for lab2+): `redis-server` then `redis-cli` for monitoring.

- Codebase conventions you must follow when editing:
  - Keep examples small and self-contained inside their lab directory. Avoid cross-lab imports except via `lib/`.
  - Logging: use `context.lab_logging.setup(...)` where provided (see `lab1/clientserver.py`) and obtain module loggers with the `vs2lab.labN...` naming convention.
  - Networking: many examples use blocking sockets with timeouts (see `clientserver.Server.__init__` socket timeout pattern). Preserve socket timeout/exception handling when refactoring.
  - Channels and 2PC: messaging uses `channel` interfaces in `lab2/` and `lab6/2pc`. Message constants are defined in `const*.py` files; prefer using them rather than hard-coded strings.

- Tests and quick checks:
  - Lab examples include small runnable scripts: `runcl.py`, `runsrv.py`, or `doit.py` per lab. Use these to reproduce behaviors manually.
  - Unit tests: see `lab1/test_clientserver.py` as a small example of test structure.

- Integration and external dependencies:
  - Redis: required for labs that use `redis-py` (see `lab2` and `lab3` projects). Start a local `redis-server` when running those labs.
  - Jupyter: notebooks are present under many labs and expect a working IPython kernel (use pipenv-installed interpreter or register an ipykernel).

- When making PRs / edits:
  - Keep changes to one lab per PR if possible.
  - Preserve pedagogical clarity: prefer explicit, readable code over micro-optimizations.
  - Add or update small examples/runners when API changes are introduced.

- Useful entry points (examples to read or run):
  - `lab1/clientserver.py` — socket echo server + client usage in `Client-Server-Arch.ipynb`.
  - `lab2/channel/channel.py` and `lib/lab_channel.py` — channel abstraction and usage patterns.
  - `lab6/2pc/coordinator.py`, `participant.py` — two-phase commit example with `stablelog`.

If anything in these notes is unclear or you want the agent to follow a stricter rule (naming, test coverage, or commit style), tell me and I'll update this file.
