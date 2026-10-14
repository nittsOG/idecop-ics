# Setup Guide — running the prototype on your own computer

This guide takes a fresh clone to a working prototype: the database, the backend, and the browser screens you need for the A32 review. It also lets the evaluation scripts run.

The environment is pinned (D29), and one script sets everything up. You install Git and uv, then run `uv run scripts/setup.py` once. It builds `.venv` with:
- Python 3.13;
- every Python package, at the exact version recorded in `requirements.lock`;
- Node.js.

It then builds the database, installs the frontend's packages, and checks the result. The commands are the same on Windows, Linux (including Kali) and macOS. `README.md`'s *Running it* section is the short form of this guide.

**How this was checked.** On 14 October 2026, from a fresh clone of commit `d490df7` with this guide's batch applied, using uv 0.13.1 on Linux:
- **The setup script** was run first on the fresh clone, then again, and then in its check mode.
- **Recovery cases:** a `.venv` made with Python 3.12, a package removed by hand, a database built from an older seed, a database read in the wrong encoding, and a run with uv missing.
- **The other routes:** the setup by hand, the fallback without uv, and steps 4 to 6 were run as written too.
- **Not run here:** the uv installers in step 1 (uv was installed from PyPI instead), and anything on Windows or macOS, because neither system was available. A dry run confirmed that every locked package has a ready-made build for Windows (64-bit), macOS (Intel and Apple silicon) and Linux.

---

## What you are setting up

| Part | What it is | Where it lives |
|---|---|---|
| uv | One program that builds the environment and runs commands inside it | Installed once per computer (step 1) |
| Setup script | Builds the environment, the database and the frontend's packages, then checks them | `scripts/setup.py`, run once per clone (step 3) |
| Environment | Python 3.13, every package at its locked version, and Node.js 24 | `.venv/` in the repository, not tracked by git |
| Database | One SQLite file. It holds the network, the five attack paths, the ten candidate cards and your confirmations | `data/deception_placement.db`, not tracked by git |
| Backend | The FastAPI server. The screens read and write the database only through it | `http://127.0.0.1:8000`, terminal 1 |
| Frontend | The screens you use in the browser: Dashboard (Screen 1) and Plausibility Review (Screen 3) | `http://localhost:5173`, terminal 2 |
| Scripts | Command-line checks, the comparison runs, and the review's export and import | `scripts/` |

**Three tracked files define the environment.**
- `.python-version` says `3.13`.
- `requirements.txt` lists the direct dependencies, with minimum versions.
- `requirements.lock` is generated from `requirements.txt`. It records the exact version and checksums of every package, Node included.

The `.venv` folder itself is never committed. It is built on each computer, because it holds paths and programs specific to that computer and operating system.

The backend and the frontend are two separate programs that keep running, so they need a terminal each. Both listen only on your own computer and are not reachable from your network.

**Not part of this setup:**
- The scoring notebook runs in Google Colab, on Google's GPU, in your browser. It uses Colab's own environment, with the pins D26 gave it, and you install nothing for it. Its steps are in A20 (`00-action-items.md`) and come at A32 step 3.
- Ollama is needed only by the explanation layer, which is not built yet (A6).
- The VM testbed (A21) is a separate build.

---

## 1. Install Git and uv (once per computer)

You do not need to install Python or Node.js yourself. uv downloads Python 3.13 if your computer lacks it, and Node comes inside the environment.

**Git.** Check it with `git --version`. If it is missing, install Git for Windows, or run `sudo apt install git` on Kali, Debian or Ubuntu.

**uv.** These are uv's own instructions (#392):
- **Windows (PowerShell):**
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Linux, Kali or macOS:**
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **With a Python you already have:** `pip install uv` or `pipx install uv`.

The first two download a script and run it, like any installer. The pip route avoids that.

Then **open a new terminal**, so that it finds uv, and check it with `uv --version`.

---

## 2. Bring the clone up to date

```
cd path/to/idecop-ics
git pull
git log -1 --oneline
```

The last line should show the newest commit on GitHub.

Run every command in this guide from the repository root, the folder that holds `README.md`, unless a step says otherwise.

---

## 3. Run the setup script (once per clone)

```
uv run scripts/setup.py
```

It works through four steps and prints `ok` after each check.
1. **Environment.** It creates `.venv` with Python 3.13, downloading Python first if needed. Then it installs exactly the locked packages, Node included, and checks every file's checksum. A `.venv` with another Python version, such as one made with the earlier instructions, is replaced.
2. **Database.** It builds `data/deception_placement.db` if it does not exist.
   - **It never changes an existing database,** because that holds your confirmations.
   - If the existing one no longer matches the current schema and seed, it prints a `WARNING` and leaves it alone. *Your review data* says what to do.
3. **Frontend.** It installs the exact JavaScript packages recorded in `src/frontend/package-lock.json`, using the Node inside `.venv`.
4. **Checks.** It checks the Python and Node versions, that the backend and its libraries import, the database's contents, and that the frontend builds.

It ends with `Setup complete.` and the commands that start the app.
- **How long it takes.** The first run takes a minute or two, mostly downloading about 130 MB. Later runs take seconds.
- **If it stops,** it prints `SETUP STOPPED:` and what to do.

**Re-running is safe.** Run it again after a pull that changes `requirements.lock` or `src/frontend/package-lock.json`.

**To check without changing anything,** run `uv run scripts/setup.py --check`. The only thing it writes is the frontend's build output, which git ignores. Use it whenever something seems wrong.

*Setup by hand*, below, lists the same steps as separate commands, if you would rather run them one at a time.

---

## 4. Start the backend (terminal 1)

From the repository root:

```
uv run python -m uvicorn src.api.main:app --reload
```

- **Started:** you see `Uvicorn running on http://127.0.0.1:8000` and `Application startup complete.` Leave it running.
- **Check it:** open `http://127.0.0.1:8000/health`. It should show `{"status":"ok","db_exists":true}`.
- **Endpoints:** `http://127.0.0.1:8000/docs` lists every endpoint.
- **Reloading:** `--reload` restarts the server whenever a Python file changes.
- **Stopping:** press Ctrl+C.

`uv run` runs a command inside `.venv` without activating it. It finds `.venv` from the repository root or any folder below it. On Windows it also avoids PowerShell's "running scripts is disabled" block, because no activation script is involved.

---

## 5. Start the frontend (terminal 2)

Open a second terminal at the repository root:

```
cd src/frontend
uv run npm run dev
```

It prints `Local: http://localhost:5173/`. Open exactly that address. `uv run` puts the environment first, so this uses the Node inside `.venv`, whatever else is installed on your computer.

**Use `localhost`, not `127.0.0.1`.** The backend accepts requests only from a page served at `http://localhost:5173`. At `http://127.0.0.1:5173` the page loads, but Screen 3 says "Can't reach the backend at http://127.0.0.1:8000", even though the backend is running.

---

## 6. Check that it is right

1. Click **Plausibility Review**. The header reads `0 of 10 confirmed · 0 on the shortlist · 0 of 3 blind cards done`.
2. The section *Blind cards — score these first* holds DMZ Jump Host, Historian and PLC-03 (RTU).
3. The DMZ Jump Host card lists two steps, P2 step 1 and P5 step 1. Both are `T0822 External Remote Services`.
4. The HMI card reads `P1 · step 5 of 5 · Impact · T0832 Manipulation of View`.
5. On the **Dashboard**, choosing a method and pressing Run shows `No candidate locations yet: L is empty until the A32 review ...`. That is expected until the review confirms an asset that passes Filter 1.

**The scripts behave the same way.** `uv run python scripts/run_comparison.py` prints `No candidate set yet. L is empty until the A32 review ...` and exits. `sweep.py` and `structure_check.py` do the same. This is expected until A32 is done.

You are ready to score the three blind cards. That is A32 step 2, and step 1 of *The Filter 1 review* in `README.md`.

---

## Every session after this

The commands are the same on every operating system.

**Terminal 1:**
```
cd path/to/idecop-ics
uv run python -m uvicorn src.api.main:app --reload
```

**Terminal 2:**
```
cd path/to/idecop-ics/src/frontend
uv run npm run dev
```

Then open `http://localhost:5173`. To stop, press Ctrl+C in each terminal.

---

## Your review data — read this before deleting anything

- **Where your confirmations live.** They live only in `data/deception_placement.db`, which git does not track. Nothing you score reaches GitHub until you export it.
- **Export after every sitting.** `uv run python scripts/review_io.py export` writes `data/review/plausibility_review.csv`. This is a recommendation, not a rule from D26.
  - A mid-review export is safe. On a blind card that is still open, the script leaves the AI's fields blank.
  - `--require-complete` is for the final export only (A32 step 5).
- **Blind answers cannot be redone.** A blind card's first answers are written once and cannot be re-scored blind (D26). If the database is lost before an export, they are gone for good.
- **When the database must be rebuilt.** That happens when a pull changes `data/schema.sql` or `data/seed.sql`, or when the setup script warns that the database does not match. Do this in order:
  1. Export.
  2. Stop the backend.
  3. Delete `data/deception_placement.db`.
  4. Run `uv run scripts/setup.py`. It builds a fresh database.
  5. Run `uv run python scripts/review_io.py restore data/review/plausibility_review.csv`. It runs only on a freshly built database.
  6. If you had imported the notebook's suggestions, import them again: `uv run python scripts/import_plausibility_scores.py ai_suggestions.csv`.

---

## Setup by hand

These are the setup script's steps as separate commands, from the repository root.

```
uv venv
uv pip sync requirements.lock
uv run python -c "import sqlite3; c = sqlite3.connect('data/deception_placement.db'); c.executescript(open('data/schema.sql', encoding='utf-8').read()); c.executescript(open('data/seed.sql', encoding='utf-8').read()); c.commit(); print('Database built')"
cd src/frontend
uv run npm ci
```

- **`uv venv`** reads `.python-version` and creates `.venv` with Python 3.13. If a `.venv` already exists, it stops with `A virtual environment already exists at: .venv`; use `uv venv --clear` to replace it.
- **`uv pip sync requirements.lock`** installs exactly the locked packages, checks every checksum, and removes anything else.
- **The database line** prints `Database built`. Run a second time, it stops with `table zones already exists` and changes nothing. `encoding='utf-8'` is needed on Windows; *Notes* explains why.
- **`npm ci`** installs the exact versions in `package-lock.json`.
- **Watch out:** if no `.venv` exists, `uv run` quietly uses your computer's own Python instead.

---

## Without uv

Use this only if uv cannot be installed. First install Python 3.13 yourself from python.org, or with `sudo apt install python3.13` where your system offers it. Then, from the repository root:

**Windows (PowerShell):**
```
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.lock
.venv\Scripts\Activate.ps1
```

**Linux and macOS:**
```
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
source .venv/bin/activate
```

- pip checks the same checksums as uv.
- After activating, build the database and install the frontend's packages as in *Setup by hand*, and use every command in this guide without the `uv run` prefix. Each new terminal needs the activation line again.
- If PowerShell says `running scripts is disabled on this system`, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, answering `Y` if asked, and reopen PowerShell.

---

## Troubleshooting

| What you see | Why | Fix |
|---|---|---|
| `uv` is not recognised, or `SETUP STOPPED: uv was not found` | uv is not installed, or the terminal was opened before the install | Install uv (step 1), then open a new terminal |
| `WARNING  The database does not match the current data/schema.sql and data/seed.sql` | The database was built from older files, or read in the wrong encoding | Follow *Your review data*: export, rebuild, restore |
| `SETUP STOPPED: The packages in .venv do not match requirements.lock` (in `--check` mode) | Something changed `.venv`, or a pull changed the lock | Run `uv run scripts/setup.py` without `--check` |
| `uv` cannot download Python | No internet, or a network that blocks the download | Install Python 3.13 yourself; uv then uses it |
| `Hash mismatch` from uv or pip | A download does not match the checksum recorded in the lock | Do not work around it. Delete `.venv` and run the setup script again. If it repeats, stop and report it: the check exists to catch corrupted or substituted packages |
| `uv run python --version` is not 3.13, or `No module named uvicorn` | `uv run` found no `.venv` and used your computer's own Python | Run the setup script from the repository root |
| Screen 3: "Can't reach the backend at http://127.0.0.1:8000" | Either the backend is not running, or the page is open at `127.0.0.1:5173` or on a port other than 5173 | Start the backend (step 4). Open `http://localhost:5173` |
| `Port 5173 is in use, trying another one...`, then `Local: http://localhost:5174/` | A dev server is already running. The backend accepts only port 5173 | Stop the other one with Ctrl+C in its terminal, then run `uv run npm run dev` again |
| `/health` shows `"db_exists":false`, or a screen shows `Database not found at ...` | No database in this folder | Run the setup script from the repository root |
| HTTP 500 on Confirm or Run, after a pull | The database was built from an older `schema.sql`, whose constraints SQLite does not update | Rebuild, following *Your review data* |
| `npm ci`: `1 high severity vulnerability` | On 13 October 2026, npm's audit flagged `source-map-js`, which the build tools use (vite → postcss). A crafted source map can stall the dev build. It does not touch the API or your data | Ignore it for local use. `npm audit fix` rewrites `package-lock.json`, a tracked file, so make that change only as its own deliberate commit |
| Without uv: `No matching distribution found` | The virtual environment was made with a Python the lock does not cover, such as 3.11 or 3.15 | Delete `.venv` and make it again with `py -3.13` or `python3.13` |
| Odd `database is locked` or file errors | *A precaution, not reproduced here:* sync tools such as OneDrive can lock files inside a synced folder | Keep the clone outside OneDrive, Dropbox or similar folders |

---

## Notes — why some commands look the way they do

- **Why a setup script.** One command runs every step in the right order and checks the result, so nothing is mistyped or skipped.
  - It changes only `.venv`, the frontend's packages, and a database that does not exist yet.
  - It runs only when you run it. Nothing changes the environment behind your back.
  - It uses only Python's standard library. `python scripts/setup.py` works too, as long as uv is on PATH.
- **How the script spots an outdated database.** It builds a fresh copy in memory from `schema.sql` and `seed.sql`, and compares the seeded tables with the database on disk.
  - It ignores your confirmations, and the scores the code writes back into `assets`.
  - So a database built before a seed change, or one read in the wrong encoding, is caught without any number written into the script.
- **Why a lock file.** `requirements.txt` sets only minimum versions, so an unpinned install takes whatever is newest that day. On 13 October 2026 the same file installed NetworkX 3.4.2 on Python 3.10, 3.6.1 on 3.11 and 3.7 on 3.13. The centrality code runs on NetworkX. The lock fixes every version, and D29 records when it may change.
- **Why checksums.** The lock also records each file's SHA-256 checksum. uv and pip refuse a download that does not match, so the environment cannot silently change underneath the evaluation.
- **Where Node comes from.** Node is installed by the `nodejs-wheel` package from PyPI (#391).
  - Its own description calls it an unofficial build of Node.js. It is published by one maintainer, not by the Node.js project.
  - The user chose this on 14 October 2026 so that one environment holds everything (D29).
  - Node runs only the screens, not the evaluation.
  - To use the official installer from nodejs.org instead, remove the `nodejs-wheel` line from `requirements.txt` and regenerate the lock. That is an environment change, so D29's rule applies.
- **`npm ci` rather than `npm install`.** `npm ci` installs exactly what `package-lock.json` records and never rewrites that file.
- **`encoding='utf-8'` when building the database.** `seed.sql` contains a few characters outside plain ASCII, such as "—" and "→".
  - Without naming the encoding, Python reads the file in the computer's default encoding, which on Windows is often not UTF-8.
  - **What a non-UTF-8 read did.** This was tested by reading the files as cp1252, a common Windows default. Three kinds of value were stored garbled: the Purdue level of the Attacker and of two zones ("—" became "â€”"), and two conduit descriptions.
  - **What it changed in the numbers.** The garbled Purdue level gave the Attacker a placeholder SL of 0.5 instead of 0.3. The comparison and the sweep printed identical output, because the Attacker is never a candidate or a path target. Only the superseded pre-D20 section of `structure_check.py` printed different numbers.
  - **No recorded result is affected.** The recorded results were produced in Claude's sessions, on Linux, which reads the files as UTF-8. The README's command lacked the encoding until 13 October 2026.
- **`.venv/` in `.gitignore`.** uv, and Python 3.13's own `venv`, write a `.gitignore` inside each new environment, so git ignores it. Python 3.12 and earlier do not, so the repository's `.gitignore` lists `.venv/` too.

## Keeping this guide true

- `README.md`'s *Running it* section is the short form of this guide. Change both in the same commit.
- **The lock changes only under D29's rule:**
  - by a decisions-log entry that states the effect;
  - never between the freeze before Phase D and the end of Phase D.

  The command that regenerates it is at the top of `requirements.lock`. After regenerating, run the setup script, step 6 and the legacy reproduction in `README.md` again, and compare the output.
- **If the code starts writing another column of a seeded table,** add it to `COMPUTED_COLUMNS` in `scripts/setup.py`. Otherwise the script reports a mismatch that isn't there.
- After any change to `requirements.lock`, `src/frontend/package.json` or `data/seed.sql`, run the setup script and step 6 again, and update the expected text here if it moved.
