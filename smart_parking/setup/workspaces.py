import frappe
from json import dumps

def execute():
    """Set up Smart Parking workspaces with parent/child structure."""

    # First create/update the main Smart Parking workspace
    main_content = dumps([
        {"id": "sp1", "type": "header", "data": {"text": "Welcome to Smart Parking Management"}},
        {"id": "sp2", "type": "paragraph", "data": {"text": "Manage parking zones, slots, vehicles, billing and operations."}},
        {"id": "sp3", "type": "card", "data": {"card_name": "Quick Access", "col": 12}},
        {"id": "sp4", "type": "card", "data": {"card_name": "Zone Management", "col": 6}},
        {"id": "sp5", "type": "card", "data": {"card_name": "Billing", "col": 6}},
        {"id": "sp6", "type": "card", "data": {"card_name": "Operations", "col": 6}},
        {"id": "sp7", "type": "card", "data": {"card_name": "Reports", "col": 6}}
    ])

    main_links = [
        {"type": "Card Break", "label": "Quick Access", "icon": "list", "idx": 1, "link_count": 5},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "idx": 2, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "idx": 3, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "idx": 4, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "idx": 5, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "idx": 6, "onboard": 0, "is_query_report": 0},
        {"type": "Card Break", "label": "Zone Management", "icon": "database", "idx": 7, "link_count": 3},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "idx": 8, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "idx": 9, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "idx": 10, "onboard": 0, "is_query_report": 0},
        {"type": "Card Break", "label": "Billing", "icon": "coins", "idx": 11, "link_count": 2},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "idx": 12, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "idx": 13, "onboard": 0, "is_query_report": 0},
        {"type": "Card Break", "label": "Operations", "icon": "settings", "idx": 14, "link_count": 3},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "idx": 15, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "idx": 16, "onboard": 0, "is_query_report": 0},
        {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "idx": 17, "onboard": 0, "is_query_report": 0},
        {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 18, "link_count": 3},
        {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "idx": 19, "onboard": 0, "is_query_report": 1},
        {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "idx": 20, "onboard": 0, "is_query_report": 1},
        {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "idx": 21, "onboard": 0, "is_query_report": 1}
    ]

    # Create or update main workspace
    _upsert_workspace({
        "name": "Smart Parking",
        "label": "Smart Parking",
        "title": "Smart Parking",
        "module": "Smart Parking",
        "icon": "car",
        "indicator_color": "",
        "parent_page": "",
        "sequence_id": 1.0,
        "content": main_content,
        "links": main_links,
    })

    # Sub-workspaces config
    sub_workspaces = [
        {
            "name": "Parking Zone",
            "label": "Parking Zone",
            "title": "Parking Zone",
            "module": "Parking Zone",
            "icon": "map-pin",
            "indicator_color": "blue",
            "sequence_id": 2.0,
            "content": dumps([
                {"id": "pz1", "type": "header", "data": {"text": "Parking Zone Management"}},
                {"id": "pz2", "type": "card", "data": {"card_name": "Zone Management", "col": 6}},
                {"id": "pz3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Zone Management", "icon": "database", "idx": 1, "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Zone", "label": "Parking Zone", "idx": 2, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot Type", "label": "Parking Slot Type", "idx": 3, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Slot", "label": "Parking Slot", "idx": 4, "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 5, "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Slot Occupancy Report", "label": "Slot Occupancy Report", "idx": 6, "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Vehicle Management",
            "label": "Vehicle Management",
            "title": "Vehicle Management",
            "module": "Vehicle Management",
            "icon": "car",
            "indicator_color": "green",
            "sequence_id": 3.0,
            "content": dumps([
                {"id": "vm1", "type": "header", "data": {"text": "Vehicle Management"}},
                {"id": "vm2", "type": "card", "data": {"card_name": "Vehicle Management", "col": 6}},
                {"id": "vm3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Vehicle Management", "icon": "database", "idx": 1, "link_count": 4},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle", "label": "Vehicle", "idx": 2, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Entry", "label": "Vehicle Entry", "idx": 3, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Reservation", "label": "Parking Reservation", "idx": 4, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Incident", "label": "Parking Incident", "idx": 5, "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 6, "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Vehicle Entry Register", "label": "Vehicle Entry Register", "idx": 7, "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Parking Billing",
            "label": "Parking Billing",
            "title": "Parking Billing",
            "module": "Parking Billing",
            "icon": "credit-card",
            "indicator_color": "orange",
            "sequence_id": 4.0,
            "content": dumps([
                {"id": "pb1", "type": "header", "data": {"text": "Parking Billing"}},
                {"id": "pb2", "type": "card", "data": {"card_name": "Billing", "col": 6}},
                {"id": "pb3", "type": "card", "data": {"card_name": "Reports", "col": 6}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Billing", "icon": "coins", "idx": 1, "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Structure", "label": "Parking Fee Structure", "idx": 2, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Fee Entry", "label": "Parking Fee Entry", "idx": 3, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Payment", "label": "Parking Payment", "idx": 4, "onboard": 0, "is_query_report": 0},
                {"type": "Card Break", "label": "Reports", "icon": "list", "idx": 5, "link_count": 1},
                {"type": "Link", "link_type": "Report", "link_to": "Revenue Report", "label": "Revenue Report", "idx": 6, "onboard": 0, "is_query_report": 1}
            ]
        },
        {
            "name": "Parking Operations",
            "label": "Parking Operations",
            "title": "Parking Operations",
            "module": "Parking Operations",
            "icon": "settings",
            "indicator_color": "purple",
            "sequence_id": 5.0,
            "content": dumps([
                {"id": "po1", "type": "header", "data": {"text": "Parking Operations"}},
                {"id": "po2", "type": "card", "data": {"card_name": "Operations", "col": 12}}
            ]),
            "links": [
                {"type": "Card Break", "label": "Operations", "icon": "database", "idx": 1, "link_count": 3},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Staff", "label": "Parking Staff", "idx": 2, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Shift", "label": "Parking Shift", "idx": 3, "onboard": 0, "is_query_report": 0},
                {"type": "Link", "link_type": "DocType", "link_to": "Parking Alert", "label": "Parking Alert", "idx": 4, "onboard": 0, "is_query_report": 0}
            ]
        }
    ]

    for ws_data in sub_workspaces:
        links = ws_data.pop("links")
        content = ws_data["content"]
        ws_data["parent_page"] = "Smart Parking"
        _upsert_workspace(ws_data, links)

    frappe.db.commit()
    print("All workspaces configured with Smart Parking as main workspace!")


def _upsert_workspace(ws_data, links=None):
    name = ws_data["name"]
    content = ws_data.pop("content")
    parent_page = ws_data.pop("parent_page", "")

    existing = frappe.db.exists("Workspace", name)
    if existing:
        doc = frappe.get_doc("Workspace", name)
        doc.content = content
        doc.parent_page = parent_page
        doc.sequence_id = ws_data.get("sequence_id", 1.0)
        if links is not None:
            doc.set("links", [])
            for link in links:
                doc.append("links", link)
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc({
            "doctype": "Workspace",
            "public": 1,
            "type": "Workspace",
            "link_type": "DocType",
            "content": content,
            "parent_page": parent_page,
            **ws_data
        })
        if links:
            for link in links:
                doc.append("links", link)
        doc.insert(ignore_permissions=True)
