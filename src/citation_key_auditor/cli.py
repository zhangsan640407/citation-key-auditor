"""Command-line interface for Citation Key Auditor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .core import AuditResult, CitationSource, audit_manuscripts


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
        "citation_sources": _sources_payload(result.citation_sources),
        "missing_key_sources": _sources_payload(
            {
                key: result.citation_sources.get(key, ())
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


def _sources_payload(
    sources: dict[str, tuple[CitationSource, ...]]
) -> dict[str, list[dict[str, int | str]]]:
    return {
        key: [{"file": source.path, "line": source.line} for source in source_values]
        for key, source_values in sorted(sources.items())
    }


def _format_source_locations(sources: tuple[CitationSource, ...]) -> str:
    if not sources:
        return "source unknown"

    grouped: dict[str, list[int]] = {}
    for source in sources:
        grouped.setdefault(source.path, []).append(source.line)

    parts = []
    for path, lines in sorted(grouped.items()):
        formatted_lines = ", ".join(str(line) for line in sorted(set(lines)))
        parts.append(f"{path}:{formatted_lines}")
    return ", ".join(parts)


def _as_text(result: AuditResult, show_source_names: bool = False) -> str:
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
            _format_missing_key_line(result, key, show_source_names)
            for key in sorted(result.missing_keys)
        )

    if result.unused_keys:
        lines.append("")
        lines.append("Unused keys")
        lines.extend(f"- {key}" for key in sorted(result.unused_keys))

    return "\n".join(lines)


def _format_missing_key_line(
    result: AuditResult, key: str, show_source_names: bool
) -> str:
    if show_source_names:
        source_locations = _format_source_locations(result.citation_sources.get(key, ()))
        return f"- {key} ({source_locations})"

    return f"- {key} ({_format_line_numbers(result.citation_locations.get(key, ()))})"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="citation-key-audit",
        description="Check manuscript citation keys against BibTeX entries.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check",
        help="compare Markdown or LaTeX manuscripts with a BibTeX file",
    )
    check_parser.add_argument(
        "paths",
        metavar="path",
        type=Path,
        nargs="+",
        help="one or more manuscript paths followed by a BibTeX path",
    )
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
        if len(args.paths) < 2:
            parser.error("check requires at least one manuscript path and one BibTeX path")

        manuscript_paths = args.paths[:-1]
        bibtex_path = args.paths[-1]
        manuscripts = {str(path): _read_text(path) for path in manuscript_paths}
        bibtex_text = _read_text(bibtex_path)
        result = audit_manuscripts(manuscripts, bibtex_text)

        output = (
            _as_json(result)
            if args.json
            else _as_text(result, show_source_names=len(manuscript_paths) > 1)
        )
        print(output)

        if result.has_missing or (args.fail_on_unused and result.has_unused):
            return 1
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
