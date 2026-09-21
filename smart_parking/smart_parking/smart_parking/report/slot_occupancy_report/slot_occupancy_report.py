# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {"fieldname": "zone", "fieldtype": "Link", "label": "Parking Zone", "options": "Parking Zone", "width": 200},
        {"fieldname": "zone_type", "fieldtype": "Data", "label": "Zone Type", "width": 120},
        {"fieldname": "total_slots", "fieldtype": "Int", "label": "Total Slots", "width": 100},
        {"fieldname": "occupied_slots", "fieldtype": "Int", "label": "Occupied", "width": 100},
        {"fieldname": "reserved_slots", "fieldtype": "Int", "label": "Reserved", "width": 100},
        {"fieldname": "available_slots", "fieldtype": "Int", "label": "Available", "width": 100},
        {"fieldname": "occupancy_pct", "fieldtype": "Percent", "label": "Occupancy %", "width": 120},
    ]


def get_data(filters):
    conditions = {"is_active": 1}

    if filters and filters.get("zone"):
        conditions["name"] = filters.get("zone")

    if filters and filters.get("zone_type"):
        conditions["zone_type"] = filters.get("zone_type")

    zones = frappe.get_all(
        "Parking Zone",
        filters=conditions,
        fields=["name", "zone_name", "zone_type", "total_slots", "occupied_slots", "reserved_slots", "available_slots"],
    )

    data = []
    for zone in zones:
        total = zone.total_slots or 0
        occupied = zone.occupied_slots or 0
        occupancy_pct = flt((occupied / total * 100), 1) if total else 0

        data.append({
            "zone": zone.zone_name,
            "zone_type": zone.zone_type,
            "total_slots": total,
            "occupied_slots": occupied,
            "reserved_slots": zone.reserved_slots or 0,
            "available_slots": zone.available_slots or 0,
            "occupancy_pct": occupancy_pct,
        })

    return data
