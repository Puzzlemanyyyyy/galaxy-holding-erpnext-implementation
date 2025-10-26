#!/usr/bin/env python3
"""Provision operational ERPNext and CRM datasets for Galaxy Holding."""

from __future__ import annotations

import argparse
import json
import os
from textwrap import dedent
from typing import Dict, List

import frappe

from utils import commit_or_rollback, ensure_doc, frappe_site_connection


def provision_all(*, verifactu_api_key: str | None) -> None:
    print("🚀 Bootstrapping ERPNext & CRM records...")
    setup_customers()
    setup_suppliers()
    setup_items()
    setup_projects()
    setup_crm_pipeline()
    setup_manufacturing_templates()
    configure_verifactu_integration(verifactu_api_key)
    print("\n✅ ERPNext and CRM data provisioning complete!")


def setup_customers() -> None:
    print("\n👔 Creating customers and contacts...")
    customers: List[Dict[str, object]] = [
        {
            "customer_name": "BioPharma Iberia",
            "customer_group": "Commercial",
            "territory": "Spain",
            "customer_type": "Company",
            "primary_contact": {
                "first_name": "Laura",
                "last_name": "Gomez",
                "email_id": "laura.gomez@biopharmaiberia.com",
                "phone": "+34 600 111 222",
            },
        },
        {
            "customer_name": "Asterion Renewable",
            "customer_group": "Commercial",
            "territory": "Portugal",
            "customer_type": "Company",
            "primary_contact": {
                "first_name": "Miguel",
                "last_name": "Ferreira",
                "email_id": "miguel.ferreira@asterionrenew.com",
                "phone": "+351 910 222 333",
            },
        },
    ]

    for customer in customers:
        ensure_doc(
            "Customer",
            {"customer_name": customer["customer_name"]},
            {
                "customer_name": customer["customer_name"],
                "customer_group": customer["customer_group"],
                "territory": customer["territory"],
                "customer_type": customer["customer_type"],
            },
        )

        contact_filters = {"email_id": customer["primary_contact"]["email_id"]}
        contact = ensure_doc(
            "Contact",
            contact_filters,
            {
                "first_name": customer["primary_contact"]["first_name"],
                "last_name": customer["primary_contact"]["last_name"],
                "email_id": customer["primary_contact"]["email_id"],
                "phone": customer["primary_contact"]["phone"],
            },
        )
        contact.links = []
        contact.append(
            "links",
            {"link_doctype": "Customer", "link_name": customer["customer_name"]},
        )
        contact.save(ignore_permissions=True)

    frappe.db.commit()


def setup_suppliers() -> None:
    print("\n🏭 Creating suppliers...")
    suppliers = [
        {
            "supplier_name": "Sygma Raw Materials",
            "supplier_group": "Local",
            "supplier_type": "Company",
            "country": "Spain",
        },
        {
            "supplier_name": "Helios Packaging",
            "supplier_group": "International",
            "supplier_type": "Company",
            "country": "Germany",
        },
    ]

    for supplier in suppliers:
        ensure_doc("Supplier", {"supplier_name": supplier["supplier_name"]}, supplier)

    frappe.db.commit()


def setup_items() -> None:
    print("\n📦 Seeding inventory items...")
    items = [
        {
            "item_code": "BIO-INS-001",
            "item_name": "Bio Insulin Lot",
            "description": "Pharmaceutical-grade insulin batch",
            "item_group": "Products",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "company": "Galaxy Bio",
        },
        {
            "item_code": "SOFT-DEV-001",
            "item_name": "Custom Software Sprint",
            "description": "Four-week agile delivery sprint",
            "item_group": "Services",
            "stock_uom": "Hour",
            "is_stock_item": 0,
            "company": "Galaxy Software",
        },
    ]

    for item in items:
        ensure_doc("Item", {"item_code": item["item_code"]}, item)

    frappe.db.commit()


def setup_projects() -> None:
    print("\n📁 Creating flagship projects...")
    projects = [
        {
            "project_name": "Galaxy Bio GMP Upgrade",
            "company": "Galaxy Bio",
            "is_active": 1,
            "expected_start_date": "2024-01-01",
            "expected_end_date": "2024-12-31",
            "tasks": [
                {
                    "subject": "Facility Assessment",
                    "start_date": "2024-01-05",
                    "end_date": "2024-02-15",
                },
                {
                    "subject": "Validation Protocols",
                    "start_date": "2024-02-16",
                    "end_date": "2024-05-30",
                },
            ],
        },
        {
            "project_name": "Galaxy Software ERP Rollout",
            "company": "Galaxy Software",
            "is_active": 1,
            "expected_start_date": "2024-03-01",
            "expected_end_date": "2024-09-30",
            "tasks": [
                {
                    "subject": "Requirement Workshops",
                    "start_date": "2024-03-05",
                    "end_date": "2024-04-15",
                },
                {
                    "subject": "MVP Delivery",
                    "start_date": "2024-04-16",
                    "end_date": "2024-07-31",
                },
            ],
        },
    ]

    for project in projects:
        doc = ensure_doc(
            "Project",
            {"project_name": project["project_name"]},
            {
                "project_name": project["project_name"],
                "company": project["company"],
                "is_active": project["is_active"],
                "expected_start_date": project["expected_start_date"],
                "expected_end_date": project["expected_end_date"],
            },
        )

        doc.tasks = []
        for task in project["tasks"]:
            doc.append(
                "tasks",
                {
                    "subject": task["subject"],
                    "start_date": task["start_date"],
                    "end_date": task["end_date"],
                },
            )
        doc.save(ignore_permissions=True)

    frappe.db.commit()


def setup_crm_pipeline() -> None:
    print("\n🧲 Building CRM pipeline...")
    leads = [
        {
            "company_name": "Solaria Health",
            "lead_name": "Solaria Health",
            "lead_owner": "natalia.rodriguez@galaxyholding.com",
            "status": "Interested",
            "email_id": "contact@solariahealth.eu",
            "phone": "+34 655 444 555",
            "source": "Website",
            "company": "Galaxy Holding",
        },
        {
            "company_name": "Andes Pharma",
            "lead_name": "Andes Pharma",
            "lead_owner": "manuel.martinez@galaxyholding.com",
            "status": "Open",
            "email_id": "info@andespharma.co",
            "phone": "+57 310 789 0000",
            "source": "Referral",
            "company": "Galaxy Holding",
        },
    ]

    opportunities = [
        {
            "opportunity_name": "Solaria MES Deployment",
            "party_type": "Customer",
            "company": "Galaxy Software",
            "with_items": 1,
            "opportunity_from": "Lead",
            "lead": "Solaria Health",
            "expected_closing": "2024-06-30",
            "items": [
                {"item_code": "SOFT-DEV-001", "qty": 1, "rate": 65000},
            ],
        },
        {
            "opportunity_name": "Andes Pharma Manufacturing",
            "party_type": "Customer",
            "company": "Galaxy Bio",
            "with_items": 1,
            "opportunity_from": "Lead",
            "lead": "Andes Pharma",
            "expected_closing": "2024-08-15",
            "items": [
                {"item_code": "BIO-INS-001", "qty": 5, "rate": 18000},
            ],
        },
    ]

    for lead in leads:
        ensure_doc("Lead", {"company_name": lead["company_name"]}, lead)

    for opportunity in opportunities:
        doc = ensure_doc(
            "Opportunity",
            {"opportunity_name": opportunity["opportunity_name"]},
            {key: value for key, value in opportunity.items() if key != "items"},
        )
        doc.items = []
        for item in opportunity["items"]:
            doc.append("items", item)
        doc.save(ignore_permissions=True)

    frappe.db.commit()


def setup_manufacturing_templates() -> None:
    print("\n⚙️  Creating BOM & routing templates...")
    if frappe.db.exists("BOM", {"item": "BIO-INS-001"}):
        return

    bom = frappe.get_doc(
        {
            "doctype": "BOM",
            "item": "BIO-INS-001",
            "company": "Galaxy Bio",
            "quantity": 1,
            "is_active": 1,
            "is_default": 1,
            "items": [
                {"item_code": "BIO-INS-001", "qty": 1, "rate": 0},
            ],
        }
    )
    bom.insert(ignore_permissions=True)
    frappe.db.commit()


def configure_verifactu_integration(api_key: str | None) -> None:
    print("\n🧾 Configuring Verifactu sandbox webhook...")
    if not api_key:
        print("  ⚠️ No Verifactu API key provided, creating placeholder configuration")

    payload_template = dedent(
        """
        {
          "invoice_number": "{{ doc.name }}",
          "customer": "{{ doc.customer_name }}",
          "total": "{{ doc.rounded_total or doc.grand_total }}",
          "issue_date": "{{ doc.posting_date }}",
          "tax_id": "{{ doc.tax_id or '' }}",
          "items": [
            {% for item in doc.items %}
            {
              "code": "{{ item.item_code }}",
              "description": "{{ item.description }}",
              "amount": "{{ item.base_net_amount }}",
              "quantity": "{{ item.qty }}"
            }{% if not loop.last %},{% endif %}
            {% endfor %}
          ]
        }
        """
    ).strip()

    ensure_doc(
        "Webhook",
        {"webhook_name": "Verifactu Sandbox"},
        {
            "webhook_name": "Verifactu Sandbox",
            "webhook_docevent": "on_submit",
            "webhook_doctype": "Sales Invoice",
            "request_method": "POST",
            "request_url": "https://api.verifactu.sandbox/v1/invoices",
            "headers": json.dumps(
                [
                    {"key": "Content-Type", "value": "application/json"},
                    {"key": "X-API-KEY", "value": api_key or "REPLACE_ME"},
                ]
            ),
            "data": payload_template,
            "enabled": 1 if api_key else 0,
        },
    )

    frappe.db.commit()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision Galaxy ERPNext & CRM data")
    parser.add_argument("--site", default="galaxy.local", help="Frappe site name")
    parser.add_argument(
        "--verifactu-api-key",
        default=os.environ.get("VERIFACTU_API_KEY"),
        help="Sandbox API key for Verifactu integration",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    with frappe_site_connection(args.site):
        exc: Exception | None = None
        try:
            provision_all(verifactu_api_key=args.verifactu_api_key)
        except Exception as err:  # pragma: no cover - frappe specific
            exc = err
            print(f"❌ Fatal error provisioning ERPNext data: {err}")
            raise
        finally:
            commit_or_rollback(exc)


if __name__ == "__main__":
    main()
