# Local Storage Setup

Where every file lives right now, before the GitHub repo exists — "workspace" and "local computer" are the two real locations, and this is the first, one-time instruction for setting the second one up. Going forward, every new file gets its storage location stated explicitly when it's created — see the new rule in `00-workflow-and-rules.md`.

## The two locations

**Workspace (Claude's Project Knowledge)** — the 8 files marked 📌 in `00-project-index.md`'s registry. These stay loaded for me automatically in any conversation in this Project. You maintain these by re-uploading the current version when one changes materially — Project Knowledge doesn't watch this conversation for edits.

**Local computer** — everything else: the 12 files marked 💾, plus any reference PDFs you collect. These live on your machine in a folder structure that mirrors `00-repository-structure.md`'s eventual GitHub layout exactly, so nothing needs reorganizing when that repo gets created at Phase C — the folder just becomes the repo.

## Folder structure to create now

Only two folders have real content yet — everything else in the full repository structure (`/src`, `/testbed`, `/data`, `/results`, `/submission`) is Phase C onward and stays empty until then. Don't create them yet; an empty folder isn't tracking anything, it's just clutter.

```
ot-deception-placement/        ← root folder — name it to match what the GitHub repo will be called
  /docs
    (all 00-*, 01-*, 02-* files — flat, no subfolders; the prefix already sorts them)
  /references
    (empty for now — this is where the Devika Jay PDF and any future
     full-text papers go, named [source-number]-[short-slug].pdf)
```

## Step-by-step: initial setup

Two zips, one download each, instead of 22 individual clicks:

1. **`claude-project-knowledge.zip`** — the 9 files tagged 📌 in the registry, flat. Download it, extract, and bulk-select all 9 into Claude Project Knowledge (Project settings → add content) in one action.
2. **`local-storage-backup.zip`** — everything, pre-organized to match this document's structure exactly: `/docs` holds all 22 markdown files, `/references` holds the Jay PDF already renamed to `312-jay-2023-deception-substations.pdf`. Extract this as your `ot-deception-placement/` root folder — no reorganizing needed, it's already laid out right.
3. Rename nothing after extracting. The filenames already carry the organizing structure — a renamed file breaks the mapping in the registry.
4. Going forward, when files change enough to be worth re-syncing, ask for a refreshed pair of zips rather than tracking individual files — same two-download motion each time, not one-by-one.

## Providing a file back to me

When a task needs something from the offline tier, attach it the same way you did with the Jay PDF — no special process, just upload it into the chat when it's relevant. I'll use it for that conversation; it doesn't need to go into Project Knowledge just because it got used once.

## How this migrates to GitHub at Phase C

Directly. `/docs` and `/references` are already named and structured to match `00-repository-structure.md` exactly — at Phase C this folder becomes the repo root (`git init` in place, or copy it in), and `/src`, `/testbed`, `/data`, `/results`, `/submission` get created alongside it as they're actually needed. No restructuring, no renaming.
