#!/usr/bin/env python3
"""Provision the complete multi-company structure for Galaxy Holding."""

from __future__ import annotations

import argparse
from typing import Iterable, List

import frappe
from frappe.utils import nowdate

from utils import CompanyConfig, commit_or_rollback, frappe_site_connection


def setup_galaxy_companies(
    company_configs: Iterable[CompanyConfig],
    future_configs: Iterable[CompanyConfig],
    *,
    include_future: bool = True,
) -> None:
    """Create the base holding structure and optional future companies."""

    print("🏢 Setting up Galaxy Holding companies...")

    for company_config in company_configs:
        try:
            name = frappe.db.exists("Company", company_config.company_name)
            if name:
                print(f"• Company {company_config.company_name} already exists, refreshing defaults")
                setup_company_defaults(company_config.company_name)
                continue

            company = frappe.get_doc(
                {
                    "doctype": "Company",
                    "company_name": company_config.company_name,
                    "abbr": company_config.abbr,
                    "domain": company_config.domain,
                    "country": company_config.country,
                    "default_currency": company_config.default_currency,
                    "is_group": company_config.is_group,
                    "parent_company": company_config.parent_company or None,
                    "date_of_establishment": nowdate(),
                    "date_of_incorporation": nowdate(),
                }
            )
            company.insert(ignore_permissions=True)
            setup_company_defaults(company.name)
            frappe.db.commit()
            print(f"  ✅ Created company: {company_config.company_name}")
        except Exception as exc:  # pragma: no cover - frappe specific
            print(f"  ❌ Error creating company {company_config.company_name}: {exc}")
            frappe.db.rollback()

    if not include_future:
        return

    print("\n🗂️  Creating placeholder companies for future expansion...")
    for future_config in future_configs:
        try:
            if frappe.db.exists("Company", future_config.company_name):
                continue

            company = frappe.get_doc(
                {
                    "doctype": "Company",
                    "company_name": future_config.company_name,
                    "abbr": future_config.abbr,
                    "domain": future_config.domain,
                    "country": future_config.country,
                    "default_currency": future_config.default_currency,
                    "is_group": future_config.is_group,
                    "parent_company": future_config.parent_company or "Galaxy Holding",
                    "date_of_establishment": nowdate(),
                    "date_of_incorporation": nowdate(),
                    "is_active": 0,
                }
            )
            company.insert(ignore_permissions=True)
            print(f"  📋 Created placeholder: {future_config.company_name}")
        except Exception as exc:  # pragma: no cover - frappe specific
            print(f"  ❌ Error creating placeholder {future_config.company_name}: {exc}")
            frappe.db.rollback()

    frappe.db.commit()
    print("\n🎉 Galaxy Holding company structure setup completed!")


def setup_company_defaults(company_name: str) -> None:
    """Create cost centres, warehouses and intercompany accounts."""

    try:
        abbr = frappe.get_value("Company", company_name, "abbr")

        ensure_cost_center(company_name, abbr)
        ensure_warehouse(company_name, abbr)

        if company_name != "Galaxy Holding":
            setup_intercompany_accounts(company_name, abbr)

        print(f"    ↳ Defaults ready for {company_name}")
    except Exception as exc:  # pragma: no cover - frappe specific
        print(f"    ❌ Error setting up defaults for {company_name}: {exc}")
        frappe.db.rollback()


def ensure_cost_center(company_name: str, abbr: str) -> None:
    name = f"Main - {abbr}"
    if frappe.db.exists("Cost Center", name):
        return

    cost_center = frappe.get_doc(
        {
            "doctype": "Cost Center",
            "cost_center_name": "Main",
            "company": company_name,
            "is_group": 0,
        }
    )
    cost_center.insert(ignore_permissions=True)


def ensure_warehouse(company_name: str, abbr: str) -> None:
    name = f"Main Warehouse - {abbr}"
    if frappe.db.exists("Warehouse", name):
        return

    warehouse = frappe.get_doc(
        {
            "doctype": "Warehouse",
            "warehouse_name": "Main Warehouse",
            "company": company_name,
            "is_group": 0,
        }
    )
    warehouse.insert(ignore_permissions=True)


def setup_intercompany_accounts(company_name: str, abbr: str) -> None:
    receivable_parent = f"Accounts Receivable - {abbr}"
    payable_parent = f"Accounts Payable - {abbr}"

    if not frappe.db.exists("Account", {"company": company_name, "account_name": "Intercompany Receivable"}):
        intercompany_receivable = frappe.get_doc(
            {
                "doctype": "Account",
                "account_name": "Intercompany Receivable",
                "parent_account": receivable_parent,
                "company": company_name,
                "account_type": "Receivable",
                "account_currency": "EUR",
            }
        )
        intercompany_receivable.insert(ignore_permissions=True)

    if not frappe.db.exists("Account", {"company": company_name, "account_name": "Intercompany Payable"}):
        intercompany_payable = frappe.get_doc(
            {
                "doctype": "Account",
                "account_name": "Intercompany Payable",
                "parent_account": payable_parent,
                "company": company_name,
                "account_type": "Payable",
                "account_currency": "EUR",
            }
        )
        intercompany_payable.insert(ignore_permissions=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision Galaxy Holding companies")
    parser.add_argument("--site", default="galaxy.local", help="Frappe site name")
    parser.add_argument(
        "--skip-future",
        action="store_true",
        help="Do not create placeholder companies",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    companies: List[CompanyConfig] = [
        CompanyConfig("Galaxy Holding", "GH", "Services", is_group=1),
        CompanyConfig("Galaxy Bio", "GB", "Manufacturing", parent_company="Galaxy Holding"),
        CompanyConfig("Galaxy Software", "GS", "Services", parent_company="Galaxy Holding"),
    ]

    future_companies: List[CompanyConfig] = [
        CompanyConfig("Galaxy Pay", "GP", "Services", parent_company="Galaxy Holding"),
        CompanyConfig("Galaxy Financial", "GF", "Services", parent_company="Galaxy Holding"),
        CompanyConfig("Asterion Capital", "AC", "Services", parent_company="Galaxy Holding"),
        CompanyConfig("Sygma Insurance", "SI", "Services", parent_company="Galaxy Holding"),
        CompanyConfig("Galaxy Tower", "GT", "Services", parent_company="Galaxy Holding"),
        CompanyConfig("Galaxy Engineering", "GE", "Manufacturing", parent_company="Galaxy Holding"),
        CompanyConfig("Galaxy Flash", "GFL", "Services", parent_company="Galaxy Holding"),
    ]

    with frappe_site_connection(args.site):
        exc: Exception | None = None
        try:
            setup_galaxy_companies(
                companies,
                future_companies,
                include_future=not args.skip_future,
            )
        except Exception as err:  # pragma: no cover - frappe specific
            exc = err
            print(f"❌ Fatal error provisioning companies: {err}")
            raise
        finally:
            commit_or_rollback(exc)


if __name__ == "__main__":
    main()