#!/usr/bin/env python3
# setup_companies.py - Galaxy Holding Company Setup

import frappe
import json
from frappe.utils import nowdate

def setup_galaxy_companies():
    """Setup multi-company structure for Galaxy Holding"""
    
    # Company configurations
    companies = [
        {
            "company_name": "Galaxy Holding",
            "abbr": "GH",
            "domain": "Services",
            "country": "Spain",
            "default_currency": "EUR",
            "is_group": 1,
            "parent_company": ""
        },
        {
            "company_name": "Galaxy Bio",
            "abbr": "GB",
            "domain": "Manufacturing",
            "country": "Spain",
            "default_currency": "EUR",
            "is_group": 0,
            "parent_company": "Galaxy Holding"
        },
        {
            "company_name": "Galaxy Software",
            "abbr": "GS",
            "domain": "Services",
            "country": "Spain",
            "default_currency": "EUR",
            "is_group": 0,
            "parent_company": "Galaxy Holding"
        }
    ]
    
    # Future expansion companies
    future_companies = [
        {"company_name": "Galaxy Pay", "abbr": "GP", "domain": "Services"},
        {"company_name": "Galaxy Financial", "abbr": "GF", "domain": "Services"},
        {"company_name": "Asterion Capital", "abbr": "AC", "domain": "Services"},
        {"company_name": "Sygma Insurance", "abbr": "SI", "domain": "Services"},
        {"company_name": "Galaxy Tower", "abbr": "GT", "domain": "Services"},
        {"company_name": "Galaxy Engineering", "abbr": "GE", "domain": "Manufacturing"},
        {"company_name": "Galaxy Flash", "abbr": "GFL", "domain": "Services"}
    ]
    
    print("Setting up Galaxy Holding companies...")
    
    for company_data in companies:
        try:
            # Check if company already exists
            if frappe.db.exists("Company", company_data["company_name"]):
                print(f"Company {company_data['company_name']} already exists, skipping...")
                continue
            
            # Create company
            company = frappe.get_doc({
                "doctype": "Company",
                "company_name": company_data["company_name"],
                "abbr": company_data["abbr"],
                "domain": company_data["domain"],
                "country": company_data["country"],
                "default_currency": company_data["default_currency"],
                "is_group": company_data["is_group"],
                "parent_company": company_data["parent_company"] or None,
                "date_of_establishment": nowdate(),
                "date_of_incorporation": nowdate()
            })
            
            company.insert()
            frappe.db.commit()
            
            print(f"✅ Created company: {company_data['company_name']}")
            
            # Setup default accounts and cost centers
            setup_company_defaults(company.name)
            
        except Exception as e:
            print(f"❌ Error creating company {company_data['company_name']}: {str(e)}")
            frappe.db.rollback()
    
    # Create placeholder companies for future expansion
    print("\nCreating placeholder companies for future expansion...")
    for future_company in future_companies:
        try:
            if frappe.db.exists("Company", future_company["company_name"]):
                continue
                
            company = frappe.get_doc({
                "doctype": "Company",
                "company_name": future_company["company_name"],
                "abbr": future_company["abbr"],
                "domain": future_company["domain"],
                "country": "Spain",
                "default_currency": "EUR",
                "is_group": 0,
                "parent_company": "Galaxy Holding",
                "date_of_establishment": nowdate(),
                "date_of_incorporation": nowdate(),
                "is_active": 0  # Inactive until expansion
            })
            
            company.insert()
            print(f"📋 Created placeholder: {future_company['company_name']}")
            
        except Exception as e:
            print(f"❌ Error creating placeholder {future_company['company_name']}: {str(e)}")
    
    frappe.db.commit()
    print("\n🎉 Galaxy Holding company structure setup completed!")

def setup_company_defaults(company_name):
    """Setup default accounts and cost centers for a company"""
    
    try:
        # Create default cost center
        if not frappe.db.exists("Cost Center", f"Main - {frappe.get_value('Company', company_name, 'abbr')}"):
            cost_center = frappe.get_doc({
                "doctype": "Cost Center",
                "cost_center_name": "Main",
                "company": company_name,
                "is_group": 0
            })
            cost_center.insert()
        
        # Setup intercompany accounts if not parent company
        if company_name != "Galaxy Holding":
            setup_intercompany_accounts(company_name)
            
        print(f"  ✅ Setup defaults for {company_name}")
        
    except Exception as e:
        print(f"  ❌ Error setting up defaults for {company_name}: {str(e)}")

def setup_intercompany_accounts(company_name):
    """Setup intercompany accounts for subsidiary companies"""
    
    abbr = frappe.get_value("Company", company_name, "abbr")
    
    # Intercompany receivable account
    intercompany_receivable = frappe.get_doc({
        "doctype": "Account",
        "account_name": "Intercompany Receivable",
        "parent_account": f"Accounts Receivable - {abbr}",
        "company": company_name,
        "account_type": "Receivable",
        "account_currency": "EUR"
    })
    
    # Intercompany payable account
    intercompany_payable = frappe.get_doc({
        "doctype": "Account",
        "account_name": "Intercompany Payable",
        "parent_account": f"Accounts Payable - {abbr}",
        "company": company_name,
        "account_type": "Payable",
        "account_currency": "EUR"
    })
    
    try:
        intercompany_receivable.insert()
        intercompany_payable.insert()
        print(f"  ✅ Created intercompany accounts for {company_name}")
    except Exception as e:
        print(f"  ❌ Error creating intercompany accounts: {str(e)}")

if __name__ == "__main__":
    frappe.init(site="galaxy.local")
    frappe.connect()
    
    with frappe.init_site("galaxy.local"):
        setup_galaxy_companies()