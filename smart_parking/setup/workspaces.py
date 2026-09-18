import frappe


def execute():
    """Run manually: bench --site <site> execute smart_parking.setup.workspaces.execute"""

    old_modules = ["Parking Zone", "Vehicle Management", "Parking Billing", "Parking Operations"]

    # Step 1: Update all references from old module names to Smart Parking
    tables = ["tabDocType", "tabReport", "tabNumber Card", "tabDashboard Chart", "tabWorkspace"]
    for mod_name in old_modules:
        for table in tables:
            try:
                frappe.db.sql(f"UPDATE `{table}` SET `module` = 'Smart Parking' WHERE `module` = %s", mod_name)
            except Exception:
                pass
        print(f"Updated: '{mod_name}' -> 'Smart Parking'")

    # Step 2: Delete old Module Defs
    for mod_name in old_modules:
        try:
            frappe.db.sql("DELETE FROM `tabModule Def` WHERE name = %s", mod_name)
            print(f"Deleted Module Def: {mod_name}")
        except Exception:
            pass

    frappe.db.commit()

    # Step 3: Clear caches
    frappe.clear_cache()
    print("DONE! Hard refresh browser with Ctrl+Shift+R")
