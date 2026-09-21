"""
smart_parking/utils/jinja_methods.py
Jinja template methods for web portal and print formats
"""
import frappe


def get_available_slots(zone):
    """Get count of available slots in a zone."""
    if not zone:
        return 0
    return frappe.db.get_value("Parking Zone", zone, "available_slots") or 0


def get_zone_status(zone):
    """Get zone status summary."""
    if not zone:
        return {}
    data = frappe.db.get_value(
        "Parking Zone", zone,
        ["zone_name", "total_slots", "occupied_slots", "available_slots", "reserved_slots"],
        as_dict=True,
    )
    if data and data.total_slots:
        data.occupancy_percentage = round((data.occupied_slots / data.total_slots) * 100, 1)
    else:
        data.occupancy_percentage = 0
    return data
