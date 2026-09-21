"""
smart_parking/utils/reservations.py
Reservation handlers — called via hooks on Parking Reservation
"""
import frappe
from frappe.utils import now_datetime


def on_reservation_submit(doc, method=None):
    """On Reservation submit: mark slot as reserved."""
    if doc.slot:
        frappe.db.set_value("Parking Slot", doc.slot, {
            "is_reserved": 1,
            "reserved_by": doc.customer,
            "reservation": doc.name,
            "status": "Reserved",
        })

    frappe.db.commit()


def on_reservation_cancel(doc, method=None):
    """On Reservation cancel: release slot reservation."""
    if doc.slot:
        frappe.db.set_value("Parking Slot", doc.slot, {
            "is_reserved": 0,
            "reserved_by": None,
            "reservation": None,
        })

    frappe.db.commit()
