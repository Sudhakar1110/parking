# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.utils import flt


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_summary(data)
    return columns, data, None, None, summary


def get_columns():
    return [
        {"fieldname": "zone", "fieldtype": "Link", "label": "Parking Zone", "options": "Parking Zone", "width": 200},
        {"fieldname": "total_entries", "fieldtype": "Int", "label": "Total Entries", "width": 100},
        {"fieldname": "total_revenue", "fieldtype": "Currency", "label": "Total Revenue", "width": 120},
        {"fieldname": "paid_amount", "fieldtype": "Currency", "label": "Paid", "width": 120},
        {"fieldname": "pending_amount", "fieldtype": "Currency", "label": "Pending", "width": 120},
        {"fieldname": "avg_fee", "fieldtype": "Currency", "label": "Avg Fee", "width": 100},
    ]


def get_data(filters):
    conditions = {"docstatus": 1}
    if filters:
        if filters.get("zone"):
            conditions["zone"] = filters.get("zone")
        if filters.get("from_date"):
            conditions["entry_time"] = [">=", filters.get("from_date")]
        if filters.get("to_date"):
            if "entry_time" in conditions:
                conditions["entry_time"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
            else:
                conditions["entry_time"] = ["<=", filters.get("to_date")]

    entries = frappe.get_all(
        "Vehicle Entry",
        filters=conditions,
        fields=["zone", "parking_fee", "fee_status"],
    )

    zone_data = {}
    for entry in entries:
        zone = entry.zone or "Unknown"
        if zone not in zone_data:
            zone_data[zone] = {"total_entries": 0, "total_revenue": 0, "paid_amount": 0, "pending_amount": 0}
        zone_data[zone]["total_entries"] += 1
        fee = flt(entry.parking_fee or 0)
        zone_data[zone]["total_revenue"] += fee
        if entry.fee_status == "Paid":
            zone_data[zone]["paid_amount"] += fee
        else:
            zone_data[zone]["pending_amount"] += fee

    data = []
    for zone, d in zone_data.items():
        avg_fee = flt(d["total_revenue"] / d["total_entries"], 2) if d["total_entries"] else 0
        data.append({
            "zone": zone,
            "total_entries": d["total_entries"],
            "total_revenue": d["total_revenue"],
            "paid_amount": d["paid_amount"],
            "pending_amount": d["pending_amount"],
            "avg_fee": avg_fee,
        })

    return data


def get_summary(data):
    total_revenue = sum(flt(row.get("total_revenue", 0)) for row in data)
    total_paid = sum(flt(row.get("paid_amount", 0)) for row in data)
    total_pending = sum(flt(row.get("pending_amount", 0)) for row in data)
    total_entries = sum(row.get("total_entries", 0) for row in data)

    return [
        {"label": "Total Revenue", "value": total_revenue, "indicator": "Green"},
        {"label": "Total Paid", "value": total_paid, "indicator": "Green"},
        {"label": "Total Pending", "value": total_pending, "indicator": "Orange"},
        {"label": "Total Entries", "value": total_entries, "indicator": "Blue"},
    ]
