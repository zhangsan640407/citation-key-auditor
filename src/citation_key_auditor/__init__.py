"""Citation key auditing for Markdown, LaTeX, and BibTeX files."""

from .core import (
    AuditResult,
    CitationSource,
    audit_citations,
    audit_manuscripts,
    audit_project,
    extract_bibtex_keys,
    extract_citation_keys,
    extract_citation_locations,
)

__all__ = [
    "AuditResult",
    "CitationSource",
    "audit_citations",
    "audit_manuscripts",
    "audit_project",
    "extract_bibtex_keys",
    "extract_citation_keys",
    "extract_citation_locations",
]

__version__ = "0.3.0"
