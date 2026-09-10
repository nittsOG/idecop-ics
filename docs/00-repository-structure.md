# Repository Structure

The full file/folder layout for when the GitHub repo gets created at the start of Phase C. Written now so the structure is ready and doesn't need retrofitting once code, testbed configs, and data start accumulating alongside the documents. `00-workflow-and-rules.md` still governs naming *within* `/docs`; this document governs the repo as a whole.

## Layout

```
/docs
  00-*.md          meta — index, phases, rules, decisions log, action items
  01-*.md          research — sources, iteration findings, synthesis
  02-*.md          specification — problem definition, threat model, testbed, data model, etc.
  03-*.md          evaluation — methodology, results write-up
  05-*.md          thesis chapter drafts
/references        PDFs of papers cited in sources.md
/src               code — graph model, optimizer, AI explanation layer, API, frontend
/testbed           VM configs, pfSense export, OpenPLC programs, Node-RED flows
/data              SQLite database, seed data, migrations
/results           Phase D outputs — logs, CSVs, generated charts
/submission        final formatted thesis document, once truly final
```

No `04-*` in `/docs` — the implementation roadmap lives entirely in `00-project-phases.md`, so a separate `04-` category would just be an empty folder. If that changes later, add it then rather than leaving a placeholder now.

## What goes where

| You have... | It goes in... |
|---|---|
| A new planning, spec, or research document | `/docs`, following `00-workflow-and-rules.md`'s naming convention |
| A reference paper (PDF) cited in `sources.md` | `/references/[source-number]-[short-slug].pdf` — e.g. `references/312-jay-2023-deception-substations.pdf` |
| Code for the optimizer, graph model, API | `/src`, in the relevant subfolder (standard Python/module naming, not the `00-`/`01-` scheme — that convention is specific to `/docs`) |
| VM configs, pfSense export, OpenPLC programs | `/testbed` |
| The SQLite database, seed/fixture data | `/data` |
| Evaluation logs, CSVs, generated charts | `/results` |
| The final formatted thesis | `/submission` |

## Linking `/references` to `sources.md`

Filename carries the source number; that's the only link needed. Don't duplicate citation metadata (author, year, venue) inside `/references` — `sources.md` is the single place that information lives, per the "one canonical file per document" rule. A PDF with no matching source number is a PDF that shouldn't be there yet — add the source entry first.

## Git hygiene — what NOT to commit directly

- **VM disk images or other large binary exports** — these can run into GBs and don't belong in git at all. Keep them local or on external storage; track the *config that recreates them* (the pfSense rules, the OpenPLC program files) instead.
- **The live/working SQLite database**, if it grows or changes often — commit the schema and seed data, `.gitignore` the working `.db` file itself. If you want history on the data too, commit periodic snapshots to `/data/snapshots` deliberately, rather than tracking the live file.
- **Credentials, tokens, API keys** — never, obviously. This includes anything used to authenticate the AI-explanation layer's Ollama instance if that ever needs a key.

Starter `.gitignore` for when the repo exists:
```
*.vmdk
*.vdi
*.ova
data/*.db
!data/schema.sql
!data/seed/
.env
*.key
__pycache__/
*.pyc
```

## This is happening now, not deferred anymore

Phase C has real code across multiple sessions — a database schema, a FastAPI backend, a React frontend, a graph model, four optimizer implementations, all tested. That's exactly the trigger this document named for creating the repo. One concrete reason it matters beyond principle: right now, this code exists only as a zip I regenerate each turn from a sandbox that resets between turns — every session starts with re-extracting, reinstalling dependencies, and rebuilding state from scratch. A real repo fixes that going forward: a stable, versioned home that doesn't depend on me reconstructing everything correctly every time.

## The actual workflow, code specifically

Different from the docs workflow in one important way: I can't push to GitHub directly (no clean way to hold a credential safely across turns — the same reasoning that ruled this out earlier still applies). So:

1. **You create the repo and do the initial push** — steps below. Everything currently in `phase-c-build.zip` becomes the first commit.
2. **I keep producing code as files/zips each turn, same as now.** Nothing changes about how I hand it to you.
3. **You commit and push it** — a real, quick step, not a manual rewrite: extract what I give you over your local clone, `git add -A`, commit (I'll suggest a message tied to the relevant decisions-log entry, e.g. "Fix: seed missing edges/conduits, per D14"), push.
4. **If the repo is public, I can `git clone` it fresh at the start of a code turn** instead of restoring from my own last zip — a more reliable source of truth than my own memory of what I last did, since it reflects whatever you've actually committed, including anything you changed by hand.

Step 4 only works cleanly if the repo is public — a private repo means I'm back to zip-reconstruction regardless, since read access needs a credential too.

## Setting it up

1. Create a new GitHub repository named `ot-deception-placement` (or whatever you prefer — just tell me if it's not this, since references elsewhere assume this name).
2. Don't let GitHub auto-generate a README or `.gitignore` — the ones already prepared (this document's starter above, and the one now included in `phase-c-build.zip`) are ready to use as-is.
3. Extract `phase-c-build.zip` into the repo folder, `git init` (if not done via GitHub's own setup), `git add -A`, commit as "Initial commit — Phase C build through API wiring (D14–D17)", push.
4. Send me the repo URL once it's up.

## When this actually gets created

Now — see above. This section used to say "wait for Phase C"; Phase C is the current phase.
