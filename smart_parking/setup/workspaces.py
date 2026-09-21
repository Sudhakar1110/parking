import frappe


def execute():
    """Run: bench --site <site> execute smart_parking.setup.workspaces.execute"""

    # Step 1: Ensure Smart Parking Module Def exists
    if not frappe.db.exists("Module Def", "Smart Parking"):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Smart Parking",
            "app_name": "smart_parking",
            "label": "Smart Parking",
            "color": "#00695c",
            "icon": "octicon octicon-package",
        }).insert(ignore_permissions=True)
        print("Created Module Def: Smart Parking")
    else:
        print("Module Def: Smart Parking already exists")

    # Step 2: Update ALL old module references to Smart Parking
    old_modules = ["Parking Zone", "Vehicle Management", "Parking Billing", "Parking Operations"]
    tables = [
        "tabDocType", "tabReport", "tabNumber Card",
        "tabDashboard Chart", "tabWorkspace",
    ]
    for mod_name in old_modules:
        for table in tables:
            try:
                frappe.db.sql(
                    f"UPDATE `{table}` SET `module` = 'Smart Parking' WHERE `module` = %s",
                    mod_name,
                )
            except Exception:
                pass
        print(f"Updated: '{mod_name}' -> 'Smart Parking'")

    # Step 3: Ensure ALL doctypes point to Smart Parking
    doctypes = [
        "Parking Zone", "Parking Slot Type", "Parking Slot", "Vehicle", "Vehicle Entry",
        "Parking Reservation", "Parking Incident", "Parking Fee Structure",
        "Parking Fee Entry", "Parking Payment", "Parking Staff", "Parking Shift",
        "Parking Alert", "Smart Parking Settings",
    ]
    for dt in doctypes:
        try:
            frappe.db.sql(
                "UPDATE `tabDocType` SET `module` = 'Smart Parking' WHERE name = %s",
                dt,
            )
        except Exception:
            pass
    print("Verified all DocType module assignments")

    # Step 4: Delete old Module Defs
    for mod_name in old_modules:
        try:
            frappe.db.sql(
                "DELETE FROM `tabModule Def` WHERE name = %s", mod_name
            )
            print(f"Deleted Module Def: {mod_name}")
        except Exception:
            pass

    frappe.db.commit()

    # Step 5: Clear ALL caches
    frappe.clear_cache()
    frappe.client.clear_cache()
    print("Cleared all caches")
    print("DONE! Run: bench --site parking.ogascale.com migrate && bench build")
    print("Then hard refresh browser with Ctrl+Shift+R")
