"""Citation key auditing for Markdown, LaTeX, and BibTeX files."""

from .core import AuditResult, audit_citations, extract_bibtex_keys, extract_citation_keys

__all__ = [
    "AuditResult",
    "audit_citations",
    "extract_bibtex_keys",
    "extract_citation_keys",
]

__version__ = "0.1.0"
