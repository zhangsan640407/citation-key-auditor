"""Citation key auditing for Markdown, LaTeX, and BibTeX files."""

from .core import (
    AuditResult,
    audit_citations,
    extract_bibtex_keys,
    extract_citation_keys,
    extract_citation_locations,
)

__all__ = [
    "AuditResult",
    "audit_citations",
    "extract_bibtex_keys",
    "extract_citation_keys",
    "extract_citation_locations",
]

__version__ = "0.2.0"
