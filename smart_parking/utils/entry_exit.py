"""
smart_parking/utils/entry_exit.py
Vehicle Entry/Exit handlers — called via hooks on Vehicle Entry
"""
import frappe
from frappe.utils import now_datetime, get_datetime
from smart_parking.utils.calculations import calculate_parking_fee


def validate_vehicle_entry(doc, method=None):
    """Validate vehicle entry before save."""
    if doc.zone:
        zone_active = frappe.db.get_value("Parking Zone", doc.zone, "is_active")
        if not zone_active:
            frappe.throw("Cannot create entry for an inactive parking zone.")

    if doc.slot:
        slot_status = frappe.db.get_value("Parking Slot", doc.slot, ["is_active", "is_occupied"], as_dict=True)
        if not slot_status.is_active:
            frappe.throw("The selected parking slot is not active.")
        if slot_status.is_occupied and not doc.exit_time:
            frappe.throw("The selected parking slot is already occupied.")


def on_vehicle_entry_submit(doc, method=None):
    """On Vehicle Entry submit: mark slot as occupied, create fee entry."""
    if doc.slot:
        frappe.db.set_value("Parking Slot", doc.slot, {
            "is_occupied": 1,
            "current_vehicle": doc.vehicle,
            "last_entry": doc.name,
        })

    if doc.zone:
        frappe.db.set_value("Parking Zone", doc.zone, "occupied_slots",
            frappe.db.get_value("Parking Zone", doc.zone, "occupied_slots") + 1)

    frappe.db.commit()


def on_vehicle_entry_cancel(doc, method=None):
    """On Vehicle Entry cancel: release slot."""
    if doc.slot:
        frappe.db.set_value("Parking Slot", doc.slot, {
            "is_occupied": 0,
            "current_vehicle": None,
            "last_entry": None,
        })

    if doc.zone:
        current = frappe.db.get_value("Parking Zone", doc.zone, "occupied_slots") or 0
        frappe.db.set_value("Parking Zone", doc.zone, "occupied_slots", max(0, current - 1))

    frappe.db.commit()


def process_vehicle_exit(doc, method=None):
    """Process vehicle exit — calculate fee and update slot."""
    if doc.exit_time and doc.entry_time:
        fee, hours = calculate_parking_fee(
            doc.zone, doc.vehicle_type, doc.entry_time, doc.exit_time
        )
        doc.parking_fee = fee
        doc.duration_hours = hours

    if doc.slot:
        frappe.db.set_value("Parking Slot", doc.slot, {
            "is_occupied": 0,
            "current_vehicle": None,
        })

    if doc.zone:
        current = frappe.db.get_value("Parking Zone", doc.zone, "occupied_slots") or 0
        frappe.db.set_value("Parking Zone", doc.zone, "occupied_slots", max(0, current - 1))
