#!/usr/bin/env python3
"""Automate Galaxy Holding role, permission and user provisioning."""

from __future__ import annotations

import argparse
from typing import Dict, Iterable, List

import frappe

from utils import commit_or_rollback, frappe_site_connection


RolePermissions = Dict[str, List[str]]


def setup_galaxy_roles() -> None:
    """Create tailored roles, grant permissions and assign users."""

    for role_name, role_config in ORGANIZATIONAL_ROLES.items():
        try:
            provision_role(role_name, role_config)
            setup_role_permissions(role_name, role_config["permissions"])
        except Exception as exc:  # pragma: no cover - frappe specific
            print(f"❌ Error creating role {role_name}: {exc}")
            frappe.db.rollback()

    setup_user_role_assignments(USER_ROLE_MATRIX)
    frappe.db.commit()
    print("\n🎉 Galaxy Holding roles and permissions setup completed!")


def provision_role(role_name: str, role_config: Dict[str, object]) -> None:
    if frappe.db.exists("Role", role_name):
        role = frappe.get_doc("Role", role_name)
        role.update({"desk_access": 1, "is_custom": 1})
        role.save(ignore_permissions=True)
        print(f"• Role {role_name} already exists, updating configuration")
        return

    role = frappe.get_doc(
        {
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1,
            "is_custom": 1,
            "restrict_to_domain": role_config.get("domain"),
        }
    )
    role.insert(ignore_permissions=True)
    print(f"  ✅ Created role: {role_name}")


def setup_role_permissions(role_name: str, permissions_config: RolePermissions) -> None:
    for permission_type, doctypes in permissions_config.items():
        if doctypes == ["*"]:
            continue

        for doctype_name in doctypes:
            try:
                provision_permission(role_name, doctype_name, permission_type)
            except Exception as exc:  # pragma: no cover - frappe specific
                print(f"  ❌ Error setting permission for {doctype_name}: {exc}")


def provision_permission(role_name: str, doctype_name: str, permission_type: str) -> None:
    existing_perm = frappe.db.get_value(
        "Custom DocPerm",
        {"parent": doctype_name, "role": role_name, "permlevel": 0},
        "name",
    )

    values = {
        "doctype": "Custom DocPerm",
        "parent": doctype_name,
        "parenttype": "DocType",
        "parentfield": "permissions",
        "role": role_name,
        "read": 1 if permission_type in {"read", "write", "create"} else 0,
        "write": 1 if permission_type in {"write", "create"} else 0,
        "create": 1 if permission_type == "create" else 0,
        "delete": 1 if permission_type == "delete" else 0,
        "submit": 1 if permission_type == "submit" else 0,
        "cancel": 1 if permission_type == "cancel" else 0,
        "amend": 1 if permission_type == "amend" else 0,
    }

    if existing_perm:
        perm = frappe.get_doc("Custom DocPerm", existing_perm)
        perm.update(values)
        perm.save(ignore_permissions=True)
    else:
        perm = frappe.get_doc(values)
        perm.insert(ignore_permissions=True)


def setup_user_role_assignments(user_matrix: Dict[str, List[str]]) -> None:
    print("\n👥 Setting up user role assignments...")

    for email, roles in user_matrix.items():
        try:
            ensure_user(email)
            assign_roles(email, roles)
            print(f"  ✅ Assigned roles to {email}: {', '.join(roles)}")
        except Exception as exc:  # pragma: no cover - frappe specific
            print(f"  ❌ Error setting up user {email}: {exc}")


def ensure_user(email: str) -> None:
    if frappe.db.exists("User", email):
        return

    first_name = email.split("@")[0].replace(".", " ").title()
    user = frappe.get_doc(
        {
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "enabled": 1,
            "user_type": "System User",
            "send_welcome_email": 0,
        }
    )
    user.insert(ignore_permissions=True)
    print(f"  ✅ Created user: {email}")


def assign_roles(email: str, roles: Iterable[str]) -> None:
    user = frappe.get_doc("User", email)
    current_roles = {entry.role for entry in user.roles}

    for role in roles:
        if role not in current_roles:
            user.append("roles", {"role": role})

    user.save(ignore_permissions=True)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Provision Galaxy Holding roles")
    parser.add_argument("--site", default="galaxy.local", help="Frappe site name")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    with frappe_site_connection(args.site):
        exc: Exception | None = None
        try:
            setup_galaxy_roles()
        except Exception as err:  # pragma: no cover - frappe specific
            exc = err
            print(f"❌ Fatal error provisioning roles: {err}")
            raise
        finally:
            commit_or_rollback(exc)


ORGANIZATIONAL_ROLES: Dict[str, Dict[str, object]] = {
    "Galaxy Director": {
        "description": "Executive leadership with unrestricted access",
        "permissions": {
            "read": ["*"],
            "write": ["*"],
            "create": ["*"],
            "delete": ["*"],
            "submit": ["*"],
            "cancel": ["*"],
            "amend": ["*"],
        },
        "modules": ["all"],
    },
    "Galaxy Administrator": {
        "description": "Finance and administration",
        "permissions": {
            "read": [
                "Account",
                "Journal Entry",
                "Payment Entry",
                "Purchase Invoice",
                "Sales Invoice",
                "Budget",
            ],
            "write": [
                "Account",
                "Journal Entry",
                "Payment Entry",
                "Purchase Invoice",
                "Sales Invoice",
                "Budget",
            ],
            "create": ["Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice"],
            "submit": ["Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice"],
            "cancel": ["Journal Entry", "Payment Entry"],
        },
        "modules": ["Accounts", "Buying", "Selling", "HR"],
    },
    "Galaxy IT Developer": {
        "description": "IT development and project delivery",
        "permissions": {
            "read": ["Project", "Task", "Timesheet", "Issue"],
            "write": ["Project", "Task", "Timesheet", "Issue"],
            "create": ["Project", "Task", "Timesheet", "Issue"],
            "submit": ["Timesheet"],
        },
        "modules": ["Projects", "Support", "HR"],
    },
    "Galaxy Operations": {
        "description": "Manufacturing and quality operations",
        "permissions": {
            "read": ["Work Order", "Stock Entry", "Item", "BOM", "Quality Inspection"],
            "write": ["Work Order", "Stock Entry", "Item", "BOM", "Quality Inspection"],
            "create": ["Work Order", "Stock Entry", "Quality Inspection"],
            "submit": ["Work Order", "Stock Entry", "Quality Inspection"],
        },
        "modules": ["Manufacturing", "Stock", "Quality Management"],
    },
    "Galaxy Legal": {
        "description": "Legal and compliance governance",
        "permissions": {
            "read": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"],
            "write": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"],
            "create": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"],
        },
        "modules": ["CRM", "Buying", "Selling"],
    },
}


USER_ROLE_MATRIX: Dict[str, List[str]] = {
    "alvaro.sanbasilio@galaxyholding.com": ["Galaxy Director", "System Manager"],
    "manuel.martinez@galaxyholding.com": ["Galaxy Director", "Galaxy IT Developer"],
    "natalia.rodriguez@galaxyholding.com": ["Galaxy Administrator", "Accounts Manager"],
    "dev1@galaxysoftware.com": ["Galaxy IT Developer"],
    "dev2@galaxysoftware.com": ["Galaxy IT Developer"],
    "dev3@galaxysoftware.com": ["Galaxy IT Developer"],
    "dev4@galaxysoftware.com": ["Galaxy IT Developer"],
    "dev5@galaxysoftware.com": ["Galaxy IT Developer"],
    "dev6@galaxysoftware.com": ["Galaxy IT Developer"],
    "francisco.vallejo@galaxybio.com": ["Galaxy Operations"],
    "ops1@galaxybio.com": ["Galaxy Operations"],
    "ops2@galaxybio.com": ["Galaxy Operations"],
}


if __name__ == "__main__":
    main()