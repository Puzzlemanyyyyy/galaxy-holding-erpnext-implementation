#!/usr/bin/env python3
# setup_roles_permissions.py - Galaxy Holding Roles & Permissions Setup

import frappe
import json

def setup_galaxy_roles():
    """Setup custom roles and permissions for Galaxy Holding organizational structure"""
    
    # Define organizational layers and their roles
    organizational_roles = {
        "Galaxy Director": {
            "description": "Executive leadership with full system access",
            "permissions": {
                "read": ["*"],
                "write": ["*"],
                "create": ["*"],
                "delete": ["*"],
                "submit": ["*"],
                "cancel": ["*"],
                "amend": ["*"]
            },
            "modules": ["all"],
            "companies": ["all"]
        },
        "Galaxy Administrator": {
            "description": "Financial and administrative management",
            "permissions": {
                "read": ["Account", "Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice", "Budget"],
                "write": ["Account", "Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice", "Budget"],
                "create": ["Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice"],
                "submit": ["Journal Entry", "Payment Entry", "Purchase Invoice", "Sales Invoice"],
                "cancel": ["Journal Entry", "Payment Entry"]
            },
            "modules": ["Accounts", "Buying", "Selling", "HR"],
            "companies": ["all"]
        },
        "Galaxy IT Developer": {
            "description": "IT development and project management",
            "permissions": {
                "read": ["Project", "Task", "Timesheet", "Issue"],
                "write": ["Project", "Task", "Timesheet", "Issue"],
                "create": ["Project", "Task", "Timesheet", "Issue"],
                "submit": ["Timesheet"]
            },
            "modules": ["Projects", "Support", "HR"],
            "companies": ["Galaxy Holding", "Galaxy Software"]
        },
        "Galaxy Operations": {
            "description": "Operations and maintenance management",
            "permissions": {
                "read": ["Work Order", "Stock Entry", "Item", "BOM", "Quality Inspection"],
                "write": ["Work Order", "Stock Entry", "Item", "BOM", "Quality Inspection"],
                "create": ["Work Order", "Stock Entry", "Quality Inspection"],
                "submit": ["Work Order", "Stock Entry", "Quality Inspection"]
            },
            "modules": ["Manufacturing", "Stock", "Quality Management"],
            "companies": ["Galaxy Bio", "Galaxy Holding"]
        },
        "Galaxy Legal": {
            "description": "Legal and compliance management",
            "permissions": {
                "read": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"],
                "write": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"],
                "create": ["Customer", "Supplier", "Contract", "Lead", "Opportunity"]
            },
            "modules": ["CRM", "Buying", "Selling"],
            "companies": ["all"]
        }
    }
    
    print("Setting up Galaxy Holding organizational roles...")
    
    for role_name, role_config in organizational_roles.items():
        try:
            # Create or update role
            if frappe.db.exists("Role", role_name):
                role = frappe.get_doc("Role", role_name)
                print(f"Role {role_name} already exists, updating...")
            else:
                role = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": 1,
                    "is_custom": 1
                })
                role.insert()
                print(f"✅ Created role: {role_name}")
            
            # Setup permissions for this role
            setup_role_permissions(role_name, role_config["permissions"])
            
        except Exception as e:
            print(f"❌ Error creating role {role_name}: {str(e)}")
            frappe.db.rollback()
    
    # Setup user assignments
    setup_user_role_assignments()
    
    frappe.db.commit()
    print("\n🎉 Galaxy Holding roles and permissions setup completed!")

def setup_role_permissions(role_name, permissions_config):
    """Setup detailed permissions for a role"""
    
    # Key doctypes for each permission level
    doctype_mappings = {
        "Account": "Account",
        "Journal Entry": "Journal Entry",
        "Payment Entry": "Payment Entry",
        "Purchase Invoice": "Purchase Invoice",
        "Sales Invoice": "Sales Invoice",
        "Budget": "Budget",
        "Project": "Project",
        "Task": "Task",
        "Timesheet": "Timesheet",
        "Issue": "Issue",
        "Work Order": "Work Order",
        "Stock Entry": "Stock Entry",
        "Item": "Item",
        "BOM": "BOM",
        "Quality Inspection": "Quality Inspection",
        "Customer": "Customer",
        "Supplier": "Supplier",
        "Contract": "Contract",
        "Lead": "Lead",
        "Opportunity": "Opportunity"
    }
    
    for permission_type, doctypes in permissions_config.items():
        if doctypes == ["*"]:  # Full access
            continue  # Handle separately for system roles
            
        for doctype_name in doctypes:
            if doctype_name in doctype_mappings:
                try:
                    # Check if permission already exists
                    existing_perm = frappe.db.get_value(
                        "Custom DocPerm",
                        {"parent": doctype_mappings[doctype_name], "role": role_name},
                        "name"
                    )
                    
                    if not existing_perm:
                        # Create custom permission
                        perm = frappe.get_doc({
                            "doctype": "Custom DocPerm",
                            "parent": doctype_mappings[doctype_name],
                            "parenttype": "DocType",
                            "parentfield": "permissions",
                            "role": role_name,
                            "read": 1 if permission_type in ["read", "write", "create"] else 0,
                            "write": 1 if permission_type in ["write", "create"] else 0,
                            "create": 1 if permission_type == "create" else 0,
                            "delete": 1 if permission_type == "delete" else 0,
                            "submit": 1 if permission_type == "submit" else 0,
                            "cancel": 1 if permission_type == "cancel" else 0,
                            "amend": 1 if permission_type == "amend" else 0
                        })
                        perm.insert()
                        
                except Exception as e:
                    print(f"  ❌ Error setting permission for {doctype_name}: {str(e)}")

def setup_user_role_assignments():
    """Setup user role assignments based on organizational structure"""
    
    # User role mappings based on organizational analysis
    user_roles = {
        # Directors (6 employees) - Full access
        "alvaro.sanbasilio@galaxyholding.com": ["Galaxy Director", "System Manager"],
        "manuel.martinez@galaxyholding.com": ["Galaxy Director", "Galaxy IT Developer"],
        
        # Administration (1 employee)
        "natalia.rodriguez@galaxyholding.com": ["Galaxy Administrator", "Accounts Manager"],
        
        # IT/Development (6 employees)
        "dev1@galaxysoftware.com": ["Galaxy IT Developer"],
        "dev2@galaxysoftware.com": ["Galaxy IT Developer"],
        "dev3@galaxysoftware.com": ["Galaxy IT Developer"],
        "dev4@galaxysoftware.com": ["Galaxy IT Developer"],
        "dev5@galaxysoftware.com": ["Galaxy IT Developer"],
        "dev6@galaxysoftware.com": ["Galaxy IT Developer"],
        
        # Operations (3 employees)
        "francisco.vallejo@galaxybio.com": ["Galaxy Operations"],
        "ops1@galaxybio.com": ["Galaxy Operations"],
        "ops2@galaxybio.com": ["Galaxy Operations"]
    }
    
    print("\nSetting up user role assignments...")
    
    for email, roles in user_roles.items():
        try:
            # Check if user exists, create if not
            if not frappe.db.exists("User", email):
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": email,
                    "first_name": email.split("@")[0].replace(".", " ").title(),
                    "enabled": 1,
                    "user_type": "System User",
                    "send_welcome_email": 0
                })
                user.insert()
                print(f"  ✅ Created user: {email}")
            
            # Assign roles
            user = frappe.get_doc("User", email)
            for role in roles:
                if not any(r.role == role for r in user.roles):
                    user.append("roles", {"role": role})
            
            user.save()
            print(f"  ✅ Assigned roles to {email}: {', '.join(roles)}")
            
        except Exception as e:
            print(f"  ❌ Error setting up user {email}: {str(e)}")

if __name__ == "__main__":
    frappe.init(site="galaxy.local")
    frappe.connect()
    
    with frappe.init_site("galaxy.local"):
        setup_galaxy_roles()