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
        {"fieldname": "name", "fieldtype": "Link", "label": "Entry ID", "options": "Vehicle Entry", "width": 160},
        {"fieldname": "vehicle", "fieldtype": "Link", "label": "Vehicle", "options": "Vehicle", "width": 160},
        {"fieldname": "license_plate", "fieldtype": "Data", "label": "License Plate", "width": 120},
        {"fieldname": "vehicle_type", "fieldtype": "Data", "label": "Vehicle Type", "width": 100},
        {"fieldname": "zone", "fieldtype": "Link", "label": "Zone", "options": "Parking Zone", "width": 160},
        {"fieldname": "slot", "fieldtype": "Link", "label": "Slot", "options": "Parking Slot", "width": 100},
        {"fieldname": "entry_time", "fieldtype": "Datetime", "label": "Entry Time", "width": 160},
        {"fieldname": "exit_time", "fieldtype": "Datetime", "label": "Exit Time", "width": 160},
        {"fieldname": "duration_hours", "fieldtype": "Float", "label": "Duration (Hrs)", "width": 100},
        {"fieldname": "parking_fee", "fieldtype": "Currency", "label": "Fee", "width": 100},
        {"fieldname": "fee_status", "fieldtype": "Data", "label": "Fee Status", "width": 100},
        {"fieldname": "docstatus", "fieldtype": "Int", "label": "Status", "width": 80},
    ]


def get_data(filters):
    conditions = {"docstatus": ["in", [0, 1]]}

    if filters:
        if filters.get("zone"):
            conditions["zone"] = filters.get("zone")
        if filters.get("from_date") and filters.get("to_date"):
            conditions["entry_time"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
        elif filters.get("from_date"):
            conditions["entry_time"] = [">=", filters.get("from_date")]
        elif filters.get("to_date"):
            conditions["entry_time"] = ["<=", filters.get("to_date")]
        if filters.get("vehicle_type"):
            conditions["vehicle_type"] = filters.get("vehicle_type")

    entries = frappe.get_all(
        "Vehicle Entry",
        filters=conditions,
        fields=["name", "vehicle", "vehicle_type", "zone", "slot", "entry_time", "exit_time", "duration_hours", "parking_fee", "fee_status", "docstatus"],
        order_by="entry_time desc",
    )

    data = []
    for entry in entries:
        license_plate = frappe.db.get_value("Vehicle", entry.vehicle, "license_plate") if entry.vehicle else ""
        data.append({
            "name": entry.name,
            "vehicle": entry.vehicle,
            "license_plate": license_plate,
            "vehicle_type": entry.vehicle_type,
            "zone": entry.zone,
            "slot": entry.slot,
            "entry_time": entry.entry_time,
            "exit_time": entry.exit_time,
            "duration_hours": entry.duration_hours,
            "parking_fee": entry.parking_fee,
            "fee_status": entry.fee_status,
            "docstatus": entry.docstatus,
        })

    return data
