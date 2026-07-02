"""Command-line interface for Citation Key Auditor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import AuditResult, audit_citations


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"Could not read {path} as UTF-8: {exc}") from exc
    except OSError as exc:
        raise SystemExit(f"Could not read {path}: {exc}") from exc


def _as_json(result: AuditResult) -> str:
    payload = {
        "cited_keys": sorted(result.cited_keys),
        "bibtex_keys": sorted(result.bibtex_keys),
        "missing_keys": sorted(result.missing_keys),
        "unused_keys": sorted(result.unused_keys),
        "citation_locations": _locations_payload(result.citation_locations),
        "missing_key_locations": _locations_payload(
            {
                key: result.citation_locations.get(key, ())
                for key in sorted(result.missing_keys)
            }
        ),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _locations_payload(locations: dict[str, tuple[int, ...]]) -> dict[str, list[int]]:
    return {key: list(lines) for key, lines in sorted(locations.items())}


def _format_line_numbers(lines: tuple[int, ...]) -> str:
    if not lines:
        return "line unknown"
    if len(lines) == 1:
        return f"line {lines[0]}"
    return "lines " + ", ".join(str(line) for line in lines)


def _as_text(result: AuditResult) -> str:
    lines = [
        "Citation Key Auditor",
        f"Cited keys: {len(result.cited_keys)}",
        f"BibTeX keys: {len(result.bibtex_keys)}",
        f"Missing keys: {len(result.missing_keys)}",
        f"Unused keys: {len(result.unused_keys)}",
    ]

    if result.missing_keys:
        lines.append("")
        lines.append("Missing keys")
        lines.extend(
            f"- {key} ({_format_line_numbers(result.citation_locations.get(key, ()))})"
            for key in sorted(result.missing_keys)
        )

    if result.unused_keys:
        lines.append("")
        lines.append("Unused keys")
        lines.extend(f"- {key}" for key in sorted(result.unused_keys))

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="citation-key-audit",
        description="Check manuscript citation keys against BibTeX entries.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check",
        help="compare a Markdown or LaTeX manuscript with a BibTeX file",
    )
    check_parser.add_argument("manuscript", type=Path)
    check_parser.add_argument("bibtex", type=Path)
    check_parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable JSON output",
    )
    check_parser.add_argument(
        "--fail-on-unused",
        action="store_true",
        help="return a non-zero exit code when unused BibTeX keys are found",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
        manuscript_text = _read_text(args.manuscript)
        bibtex_text = _read_text(args.bibtex)
        result = audit_citations(manuscript_text, bibtex_text)

        output = _as_json(result) if args.json else _as_text(result)
        print(output)

        if result.has_missing or (args.fail_on_unused and result.has_unused):
            return 1
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
