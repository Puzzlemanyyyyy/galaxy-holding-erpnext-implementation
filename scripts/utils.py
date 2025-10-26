"""Utility helpers for Galaxy Holding ERPNext automation scripts."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, Optional

import frappe


@contextlib.contextmanager
def frappe_site_connection(site: str) -> Iterator[None]:
    """Context manager that initializes and tears down a Frappe site connection."""

    frappe.init(site=site)
    frappe.connect()

    try:
        yield
    finally:
        frappe.destroy()


def ensure_doc(doctype: str, filters: Dict[str, Any], values: Dict[str, Any]) -> Any:
    """Get an existing document or create a new one if it does not exist."""

    name = frappe.db.exists(doctype, filters)

    if name:
        doc = frappe.get_doc(doctype, name)
        doc.update(values)
        doc.save(ignore_permissions=True)
        return doc

    doc = frappe.get_doc({"doctype": doctype, **values})
    doc.insert(ignore_permissions=True)
    return doc


def commit_or_rollback(exc: Optional[BaseException]) -> None:
    """Commit if no exception occurred otherwise rollback the transaction."""

    if exc is None:
        frappe.db.commit()
    else:
        frappe.db.rollback()


@dataclass(frozen=True)
class CompanyConfig:
    """Reusable configuration payload for company provisioning."""

    company_name: str
    abbr: str
    domain: str
    country: str = "Spain"
    default_currency: str = "EUR"
    is_group: int = 0
    parent_company: str = ""


def iter_missing_records(doctype: str, keys: Iterable[str]) -> Iterable[str]:
    """Yield identifiers that do not already exist in the provided doctype."""

    for key in keys:
        if not frappe.db.exists(doctype, key):
            yield key
