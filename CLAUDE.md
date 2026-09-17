# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read AGENTS.md first

`AGENTS.md` holds the operating rules for any agent working here, and they are not optional:
escrow state is checked before any work, an oracle is self-tested before any search, nothing
already listed in a folder's `analysis/tested.md` is re-run, a negative without a witness is
labeled uncertified, a search is sized (N, measured rate D, t = N/D) before it is started, and
no transaction is ever broadcast and no key material is ever posted. This file covers the
mechanics of the repository; `AGENTS.md` covers the conduct.

## What this repository is

A catalogue of public crypto treasure-hunt puzzles plus the Python and CUDA tooling used to
attack them. There is no application to run and no test suite. The deliverables are text and
data: one folder per puzzle, one JSON manifest per folder, one generated index at the root.

## Commands

```bash
python3 -m pip install -r tools/requirements.txt   # or requirements.lock for pinned versions

python3 tools/validate.py                          # 15 QA checks over the whole repository
python3 tools/validate.py --folder <tier>/<slug>   # one folder only (this is the pre-commit gate)
python3 tools/build_index.py                       # rewrite puzzles.json and generated README blocks
python3 tools/build_index.py --check               # exit 1 if the index is stale, write nothing
python3 tools/check_escrows.py --slug <slug>       # re-check one escrow against the chain
python3 tools/check_escrows.py --update            # write verified_on/verified_state back to manifests
python3 tools/derive.py bip39 "<words>" --path bip84 --target <address>   # test a candidate
python3 <tier>/<slug>/tools/oracle.py --selftest   # certify a folder oracle before searching
python3 tools/fig_prize_bars.py --offline          # regenerate assets/prize-map.svg without network
```

GPU engines (needs `nvcc`; binaries and `.so` files are gitignored, never committed):

```bash
engines/build.sh
python3 engines/pzl3_host.py --selftest            # host drivers all carry a --selftest
```

There is no single-test runner because there are no unit tests. The closest equivalents are
`tools/validate.py --folder <slug>` for one folder and `--selftest` on any oracle or engine host.

## Architecture

Data flows one way: folders are the source of truth, everything at the root is generated.

1. `<tier>/<slug>/puzzle.json` is the manifest, validated against `schema/puzzle.schema.json`.
   Tiers are `1-big-prizes`, `2-mid-prizes`, `3-small-prizes`, `4-solved`, and
   `archive/dead-ends` (whose puzzles have no folder and live as rows in
   `archive/dead-ends/rows.json`).
2. `tools/build_index.py` concatenates every manifest into the root `puzzles.json` and rewrites
   the marked blocks in the root and per-tier README files: `<!-- generated:start -->` tables and
   the root `<!-- totals:start -->` table. Never hand-edit inside those markers.
3. `tools/fig_prize_bars.py` reads `puzzles.json`, fetches live CoinGecko prices, and writes
   `assets/prize-map.svg`. A scheduled job (`.github/workflows/prize-map.yml`, daily at 06:17
   UTC) runs it and commits the SVG when it changes. That job is the only CI in the repository;
   validation is not run in CI, so run it locally.
4. `tools/check_escrows.py` is the reconciliation step between manifests and the chains. It
   exits 1 when an address claimed `funded-unspent` is observed swept or unfunded.
5. `tools/derive.py` is the shared derivation CLI. Per-folder `tools/oracle.py` scripts are the
   puzzle-specific final gate; both print `MATCH` or `NO MATCH` and exit 0 only on a match.

`tools/validate.py` is the contract that ties the layers together. Its checks cover manifest
schema and slug/tier/status consistency, README heading order and status badge, forbidden
characters, forbidden words, link resolution, README versus manifest cross-checks, file and
folder size limits, forbidden file types, a book-text volume guard, oracle self-tests and
absolute-path detection in scripts, figure bookkeeping, date sanity, index freshness, and empty
or incomplete folders. A failing check is a blocker, not a warning; only French leftovers are
reported as warnings.

## Puzzle folder anatomy

```
<tier>/<slug>/
  README.md              the whole story, fixed heading order
  puzzle.json            the manifest
  analysis/tested.md     what has been ruled out: count, method, witness, date
  analysis/leads.md      ranked open leads
  tools/oracle.py        candidate checker with --selftest
  tools/fig_*.py         figure generators for images/
  clues/                 the author's own public material, quoted
  data/                  small derived CSV or JSON
  images/                SVG figures, each referenced and captioned
```

README headings must appear in this order: At a glance, The puzzle as published, What is
understood, What has been tested, Open leads ranked, Files in this folder, Sources. Templates
for all four text files are in `docs/templates/`.

## Writing rules that the validator enforces

`docs/style-guide.md` is the full set; these are the ones that fail a build:

- No em dash, en dash, ellipsis, curly quotes, non-breaking space, emoji, or Unicode arrow.
- No banned vocabulary (`FORBIDDEN_WORDS` in `tools/validate.py`), which covers marketing
  register, verdict words for a search that cannot be done, and AI tool or vendor names.
- First person singular, ISO dates, full addresses in backticks with an explorer link on first
  mention, relative in-repo links, no absolute filesystem paths anywhere.
- No copyrighted third-party material: link to the source instead.

Tool and vendor names are allowed only in `AGENTS.md`, `CONTRIBUTING.md`, the root `README.md`,
and this file. Every other page is written in the author's own first-person voice and must not
say which software produced a finding. Commit messages follow the existing terse
`area: what changed` form.

## Known rough edges

- The root `README.md` credits the totals table to `tools/fig_readme_totals.py`, which does not
  exist. `tools/build_index.py` writes that block.
- The USD snapshot date and prices live in two places: `PRICE_SNAPSHOT` in
  `tools/build_index.py` and `ROOT_SNAPSHOT_DATE` in `tools/validate.py`. Changing one without
  the other fails the date-sanity check.
- This file is exempted from the tool-name check by `WORD_CHECK_TOOL_NAME_EXCEPTIONS` in
  `tools/validate.py`. Removing that entry makes the repository fail check 4.
