import frappe
from json import dumps


def execute():
    """Fix sidebar by updating module references and recreating workspaces."""

    old_modules = ["Parking Zone", "Vehicle Management", "Parking Billing", "Parking Operations"]

    # Step 1: Update ALL references via SQL
    for mod_name in old_modules:
        for table in ["tabDocType", "tabReport", "tabNumber Card", "tabDashboard Chart", "tabWorkspace"]:
            try:
                frappe.db.sql(f"UPDATE `{table}` SET `module` = 'Smart Parking' WHERE `module` = %s", mod_name)
            except Exception:
                pass
        print(f"Updated refs from '{mod_name}'")

    # Step 2: Delete extra Module Defs
    for mod_name in old_modules:
        try:
            frappe.db.sql("DELETE FROM `tabModule Def` WHERE name = %s", mod_name)
            print(f"Deleted Module Def: {mod_name}")
        except Exception as e:
            print(f"Could not delete Module Def '{mod_name}': {e}")

    frappe.db.commit()

    # Step 3: Delete existing workspaces
    for name in ["Smart Parking", "Parking Zone", "Vehicle Management", "Parking Billing", "Parking Operations"]:
        if frappe.db.exists("Workspace", name):
            frappe.delete_doc("Workspace", name, ignore_permissions=True)

    # Step 4: Create all workspaces under Smart Parking
    all_ws = _get_workspace_data()
    for ws_data in all_ws:
        links = ws_data.pop("links")
        content = ws_data["content"]
        doc = frappe.get_doc({
            "doctype": "Workspace",
            "public": 1,
            "standard": 1,
            "type": "Workspace",
            "link_type": "DocType",
            "content": content,
            "parent_page": "",
            "for_user": "",
            **ws_data
        })
        for link in links:
            doc.append("links", link)
        doc.insert(ignore_permissions=True)
        print(f"Created: {ws_data['name']}")

    frappe.db.commit()

    # Step 5: Clear ALL caches
    frappe.clear_cache()
    print("Cleared all caches")
    print("DONE! Hard refresh browser with Ctrl+Shift+R")


def _get_workspace_data():
    return [
        {
            "name": "Smart Parking", "label": "Smart Parking", "title": "Smart Parking",
            "module": "Smart Parking", "icon": "car", "indicator_color": "", "sequence_id": 1.0,
            "content": dumps([
                {"id": "sp1", "type": "header", "data": {"text": "Welcome to Smart Parking Management"}},
                {"id": "sp2", "type": "paragraph", "data": {"text": "Manage parking zones, slots, vehicles, billing and operations."}},
                {"id": "sp3", "type": "card", "data": {"card_name": "Quick Access", "col": 12}},
                {"id": "sp4", "type": "card", "data": {"card_name": "Zone Management", "col": 6}},
                {"id": "sp5", "type": "card", "data": {"card_name": "Billing", "col": 6}},
                {"id": "sp6", "type": "card", "data": {"card_name": "Operations", "col": 6}},
                {"id": "sp7", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Quick Access", "icon": "list", "link_count": 5},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Zone Management", "icon": "database", "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Billing", "icon": "coins", "link_count": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Operations", "icon": "settings", "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "link_count": 3},
                {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "onboard": 0, "is_query_report": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "onboard": 0, "is_query_report": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Parking Zone", "label": "Parking Zone", "title": "Parking Zone",
            "module": "Smart Parking", "icon": "map-pin", "indicator_color": "blue", "sequence_id": 2.0,
            "content": dumps([
                {"id": "pz1", "type": "header", "data": {"text": "Parking Zone Management"}},
                {"id": "pz2", "type": "card", "data": {"card_name": "Zone Management", "col": 6}},
                {"id": "pz3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Zone Management", "icon": "database", "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Vehicle Management", "label": "Vehicle Management", "title": "Vehicle Management",
            "module": "Smart Parking", "icon": "car", "indicator_color": "green", "sequence_id": 3.0,
            "content": dumps([
                {"id": "vm1", "type": "header", "data": {"text": "Vehicle Management"}},
                {"id": "vm2", "type": "card", "data": {"card_name": "Vehicle Management", "col": 6}},
                {"id": "vm3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Vehicle Management", "icon": "database", "link_count": 4},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Parking Billing", "label": "Parking Billing", "title": "Parking Billing",
            "module": "Smart Parking", "icon": "credit-card", "indicator_color": "orange", "sequence_id": 4.0,
            "content": dumps([
                {"id": "pb1", "type": "header", "data": {"text": "Parking Billing"}},
                {"id": "pb2", "type": "card", "data": {"card_name": "Billing", "col": 6}},
                {"id": "pb3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Billing", "icon": "coins", "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Parking Operations", "label": "Parking Operations", "title": "Parking Operations",
            "module": "Smart Parking", "icon": "settings", "indicator_color": "purple", "sequence_id": 5.0,
            "content": dumps([
                {"id": "po1", "type": "header", "data": {"text": "Parking Operations"}},
                {"id": "po2", "type": "card", "data": {"card_name": "Operations", "col": 12}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Operations", "icon": "database", "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "onboard": 0, "is_query_report": 0}
            ]
        }
    ]
