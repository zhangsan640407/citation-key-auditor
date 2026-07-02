"""Core citation-key extraction and comparison logic."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


PANDOC_CITATION_BLOCK_RE = re.compile(r"\[[^\]]*@[-A-Za-z0-9_:.]+[^\]]*\]")
PANDOC_KEY_RE = re.compile(r"@([-A-Za-z0-9_:.]+)")

LATEX_CITE_RE = re.compile(
    r"\\(?:"
    r"cite|citep|citet|citealp|citealt|autocite|parencite|textcite|footcite|"
    r"supercite|fullcite"
    r")\*?"
    r"(?:\s*\[[^\]]*\])*"
    r"\s*\{([^}]+)\}"
)

BIBTEX_KEY_RE = re.compile(r"@\s*[A-Za-z]+\s*[{(]\s*([^,\s]+)\s*,")


@dataclass(frozen=True)
class AuditResult:
    """Result of comparing cited keys with BibTeX keys."""

    cited_keys: set[str]
    bibtex_keys: set[str]
    missing_keys: set[str]
    unused_keys: set[str]
    citation_locations: dict[str, tuple[int, ...]] = field(default_factory=dict)

    @property
    def has_missing(self) -> bool:
        return bool(self.missing_keys)

    @property
    def has_unused(self) -> bool:
        return bool(self.unused_keys)


def extract_citation_keys(text: str) -> set[str]:
    """Extract citation keys from Pandoc Markdown and common LaTeX commands."""

    return set(extract_citation_locations(text))


def extract_citation_locations(text: str) -> dict[str, tuple[int, ...]]:
    """Extract citation keys and the 1-based lines where each key appears."""

    locations: dict[str, set[int]] = {}

    for line_number, line in enumerate(text.splitlines(), start=1):
        for key in _extract_markdown_line_keys(line):
            locations.setdefault(key, set()).add(line_number)

        for key in _extract_latex_line_keys(line):
            locations.setdefault(key, set()).add(line_number)

    return {key: tuple(sorted(lines)) for key, lines in sorted(locations.items())}


def _extract_markdown_line_keys(line: str) -> set[str]:
    keys: set[str] = set()

    for block_match in PANDOC_CITATION_BLOCK_RE.finditer(line):
        block = block_match.group(0)
        keys.update(PANDOC_KEY_RE.findall(block))

    return keys


def _extract_latex_line_keys(line: str) -> set[str]:
    keys: set[str] = set()

    for cite_match in LATEX_CITE_RE.finditer(line):
        grouped_keys = cite_match.group(1)
        for key in grouped_keys.split(","):
            cleaned = key.strip()
            if cleaned:
                keys.add(cleaned)

    return keys


def extract_bibtex_keys(text: str) -> set[str]:
    """Extract entry keys from BibTeX text."""

    return set(BIBTEX_KEY_RE.findall(text))


def audit_citations(manuscript_text: str, bibtex_text: str) -> AuditResult:
    """Compare cited keys in a manuscript with entries in a BibTeX file."""

    citation_locations = extract_citation_locations(manuscript_text)
    cited_keys = set(citation_locations)
    bibtex_keys = extract_bibtex_keys(bibtex_text)
    return AuditResult(
        cited_keys=cited_keys,
        bibtex_keys=bibtex_keys,
        missing_keys=cited_keys - bibtex_keys,
        unused_keys=bibtex_keys - cited_keys,
        citation_locations=citation_locations,
    )
