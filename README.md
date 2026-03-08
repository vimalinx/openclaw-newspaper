# OpenClaw Newspaper

A newspaper-style local publishing and reading surface for long-form agent output.

This project turns high-value agent output into readable, archivable HTML editions, then groups them by project inside a portal + project-reader flow.

## What it does

- stores project and edition metadata in a single source-of-truth layer
- renders a portal page and per-project reader pages
- publishes new editions through a minimal `PublishRequest` pipeline
- supports a first-stage "default output bridge" for turning long-form agent replies into newspaper pages
- serves well as a local report surface for agents, project updates, research briefs, and implementation plans

## Current scope

This repository is the **first-stage usable system**:

- source-of-truth data layer
- static HTML rendering pipeline
- edition publishing pipeline
- default-output bridge example
- local HTTP serving for browser reading

It does **not** yet include:

- direct runtime hook integration into an agent host
- real-time chat replacement UI
- auth / multi-user publishing
- queueing / permissions / production CMS features

## Core structure

- `data/source/` — single source-of-truth for projects and editions
- `data/schema/` — lightweight JSON schemas
- `projects/` — generated project pages and edition HTML files
- `site/` — generated portal page and portal data
- `templates/` — portal / project templates
- `scripts/render_newspaper.py` — regenerates portal + project pages from source data
- `scripts/publish_to_newspaper.py` — publishes a new edition into the system
- `scripts/publish_bridge_example.py` — example bridge from a long-form output object to a `PublishRequest`
- `scripts/serve_newspaper.sh` — local static server helper

## Minimal content model

### Project

Tracks a project reader surface:
- `slug`
- `label`
- `description`
- `summary`
- `stage`
- `blockers`
- `next`
- `updatedAt`
- `status`

### Edition

Tracks one newspaper page / issue:
- `projectSlug`
- `slug`
- `title`
- `summary`
- `density`
- `htmlUrl`
- `publishedAt`
- `tags`

### PublishRequest

The minimum input contract for publishing a new edition.

### PublishReceipt

The minimum output contract confirming what was rebuilt and where the edition landed.

## Local usage

```bash
cd /path/to/openclaw-newspaper

# rebuild portal + project pages from source data
python scripts/render_newspaper.py

# publish an example edition
python scripts/publish_bridge_example.py --input examples/default-output-sample.json --publish

# serve locally
./scripts/serve_newspaper.sh 39117
```

Then open:

- `http://127.0.0.1:39117/site/index.html`

## Design intent

This project exists for a specific workflow:

1. an agent finishes a high-value long-form output
2. the output is normalized into a `PublishRequest`
3. an edition HTML page is generated
4. the project reader and portal are rebuilt
5. the user reads the result in a newspaper-like local browser surface instead of a crowded chat bubble

## Near-term next steps

- hook the publish pipeline into a real agent/runtime finalize step
- add slug normalization and de-duplication for generated edition filenames
- improve template consistency and reduce duplicated generated content
- add browser-based acceptance checks for the local served experience

## Notes

This repository intentionally contains:
- generated example editions
- generated portal/project pages
- example source data

It intentionally avoids bundling private workspace context or live runtime secrets.
