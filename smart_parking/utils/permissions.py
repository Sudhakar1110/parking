"""
smart_parking/utils/permissions.py
Custom permission checks for DocTypes
"""
import frappe


def has_vehicle_permission(doc, user=None, permission_type=None):
    """Check if user has permission to access Vehicle records."""
    if not user:
        user = frappe.session.user

    if frappe.db.exists("Has Role", {"parent": user, "role": "Parking Manager"}):
        return True
    if frappe.db.exists("Has Role", {"parent": user, "role": "Parking Supervisor"}):
        return True

    return False


def has_vehicle_entry_permission(doc, user=None, permission_type=None):
    """Check if user has permission to access Vehicle Entry records."""
    if not user:
        user = frappe.session.user

    if frappe.db.exists("Has Role", {"parent": user, "role": "Parking Manager"}):
        return True
    if frappe.db.exists("Has Role", {"parent": user, "role": "Parking Attendant"}):
        return True

    return False
