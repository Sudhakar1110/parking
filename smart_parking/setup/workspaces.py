import frappe
from json import dumps

def execute():
    """Set up all Smart Parking workspaces with proper cards and links."""
    workspaces = [
        {
            "name": "Smart Parking",
            "label": "Smart Parking",
            "title": "Smart Parking",
            "module": "Smart Parking",
            "icon": "car",
            "indicator_color": "",
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
                {"type": "Card Break", "label": "Quick Access", "icon": "list", "idx": 1},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "idx": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "idx": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "idx": 4},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "idx": 5},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "idx": 6},
                {"type": "Card Break", "label": "Zone Management", "icon": "database", "idx": 7},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "idx": 8},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "idx": 9},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "idx": 10},
                {"type": "Card Break", "label": "Billing", "icon": "coins", "idx": 11},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "idx": 12},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "idx": 13},
                {"type": "Card Break", "label": "Operations", "icon": "settings", "idx": 14},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "idx": 15},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "idx": 16},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "idx": 17},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 18},
                {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "idx": 19},
                {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "idx": 20},
                {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "idx": 21}
            ]
        },
        {
            "name": "Parking Zone",
            "label": "Parking Zone",
            "title": "Parking Zone",
            "module": "Parking Zone",
            "icon": "map-pin",
            "indicator_color": "blue",
            "content": dumps([
                {"id": "pz1", "type": "header", "data": {"text": "Parking Zone Management"}},
                {"id": "pz2", "type": "card", "data": {"card_name": "Zone Management", "col": 6}},
                {"id": "pz3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Zone Management", "icon": "database", "idx": 1},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "idx": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "idx": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "idx": 4},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 5},
                {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "idx": 6}
            ]
        },
        {
            "name": "Vehicle Management",
            "label": "Vehicle Management",
            "title": "Vehicle Management",
            "module": "Vehicle Management",
            "icon": "car",
            "indicator_color": "green",
            "content": dumps([
                {"id": "vm1", "type": "header", "data": {"text": "Vehicle Management"}},
                {"id": "vm2", "type": "card", "data": {"card_name": "Vehicle Management", "col": 6}},
                {"id": "vm3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Vehicle Management", "icon": "database", "idx": 1},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "idx": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "idx": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "idx": 4},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "idx": 5},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 6},
                {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "idx": 7}
            ]
        },
        {
            "name": "Parking Billing",
            "label": "Parking Billing",
            "title": "Parking Billing",
            "module": "Parking Billing",
            "icon": "credit-card",
            "indicator_color": "orange",
            "content": dumps([
                {"id": "pb1", "type": "header", "data": {"text": "Parking Billing"}},
                {"id": "pb2", "type": "card", "data": {"card_name": "Billing", "col": 6}},
                {"id": "pb3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Billing", "icon": "coins", "idx": 1},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "idx": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "idx": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "idx": 4},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 5},
                {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "idx": 6}
            ]
        },
        {
            "name": "Parking Operations",
            "label": "Parking Operations",
            "title": "Parking Operations",
            "module": "Parking Operations",
            "icon": "settings",
            "indicator_color": "purple",
            "content": dumps([
                {"id": "po1", "type": "header", "data": {"text": "Parking Operations"}},
                {"id": "po2", "type": "card", "data": {"card_name": "Operations", "col": 12}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Operations", "icon": "database", "idx": 1},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "idx": 2},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "idx": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "idx": 4}
            ]
        }
    ]

    created = 0
    updated = 0
    for ws_data in workspaces:
        links = ws_data.pop("links")
        content = ws_data["content"]
        name = ws_data["name"]

        existing = frappe.db.exists("Workspace", name)
        if existing:
            doc = frappe.get_doc("Workspace", name)
            doc.content = content
            doc.set("links", [])
            for link in links:
                doc.append("links", link)
            doc.save(ignore_permissions=True)
            updated += 1
        else:
            doc = frappe.get_doc({
                "doctype": "Workspace",
                "public": 1,
                "type": "Workspace",
                "link_type": "DocType",
                "content": content,
                **ws_data
            })
            for link in links:
                doc.append("links", link)
            doc.insert(ignore_permissions=True)
            created += 1

    frappe.db.commit()
    print(f"Workspaces: {created} created, {updated} updated")
