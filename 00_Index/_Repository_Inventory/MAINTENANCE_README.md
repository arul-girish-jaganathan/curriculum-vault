# Repository Maintenance Toolkit

## Authoritative workflow

Run maintenance against a complete local checkout of the repository. Do not use the GitHub web UI as a substitute for filesystem-wide validation.

Recommended commands from the repository root:

```bash
python3 00_Index/_Repository_Inventory/curriculum_tools.py .
```

The existing `run_analysis.sh` is retained for history but should not be treated as the authoritative runner because it clones into `/tmp` and may not analyze the exact working tree being reviewed.

## Reports

The toolkit can generate:

- `curriculum_analysis.json`
- `curriculum_status.md`
- `broken_wikilinks.md`

These are evidence artifacts and should be timestamped/regenerated during audits.

## Known validator limitations

The current toolkit is an initial analyzer, not a semantic proof system:

- Placeholder detection uses heuristics.
- Duplicate detection currently relies primarily on normalized filename matches.
- Orphan detection is based on incoming wikilinks and can flag legitimate entry points.
- Wikilink validation is stem-based and does not fully model Obsidian path/alias semantics.
- Generated reports only retain a bounded subset of some findings.

Before declaring repository-wide completion, strengthen these validators or supplement them with deterministic checks.
