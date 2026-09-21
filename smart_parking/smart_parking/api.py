# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.utils import now_datetime, flt, cint


@frappe.whitelist()
def check_availability(zone=None, date=None, vehicle_type="Car"):
    """Check slot availability for a zone."""
    filters = {"is_active": 1}
    if zone:
        filters["name"] = zone

    zones = frappe.get_all(
        "Parking Zone",
        filters=filters,
        fields=["name", "zone_name", "total_slots", "occupied_slots", "reserved_slots", "available_slots"],
    )

    result = []
    for z in zones:
        result.append({
            "zone": z.name,
            "zone_name": z.zone_name,
            "total_slots": z.total_slots or 0,
            "occupied": z.occupied_slots or 0,
            "reserved": z.reserved_slots or 0,
            "available": z.available_slots or 0,
        })

    return result


@frappe.whitelist()
def book_slot(zone, slot, vehicle, start_time, end_time, customer=None):
    """Book a parking slot reservation."""
    if not customer:
        customer = frappe.session.user

    vehicle_doc = frappe.get_doc("Vehicle", vehicle)
    zone_doc = frappe.get_doc("Parking Zone", zone)
    slot_doc = frappe.get_doc("Parking Slot", slot)

    if slot_doc.is_occupied:
        frappe.throw("Slot is currently occupied.")
    if slot_doc.is_reserved:
        frappe.throw("Slot is already reserved.")

    reservation = frappe.get_doc({
        "doctype": "Parking Reservation",
        "customer": customer,
        "vehicle": vehicle,
        "vehicle_type": vehicle_doc.vehicle_type or "Car",
        "contact_phone": vehicle_doc.owner_phone,
        "zone": zone,
        "slot": slot,
        "start_time": start_time,
        "end_time": end_time,
    })

    reservation.insert(ignore_permissions=True)
    reservation.submit()

    return {
        "reservation": reservation.name,
        "status": reservation.status,
        "fee": reservation.reservation_fee,
    }


@frappe.whitelist()
def get_parking_dashboard_data():
    """Get aggregated dashboard data."""
    zones = frappe.get_all(
        "Parking Zone",
        filters={"is_active": 1},
        fields=["name", "zone_name", "total_slots", "occupied_slots", "available_slots", "reserved_slots"],
    )

    total_slots = 0
    occupied = 0
    available = 0

    zone_list = []
    for z in zones:
        t = z.total_slots or 0
        o = z.occupied_slots or 0
        a = z.available_slots or 0
        total_slots += t
        occupied += o
        available += a

        occ_pct = flt((o / t * 100), 1) if t else 0
        zone_list.append({
            "zone_name": z.zone_name,
            "total_slots": t,
            "occupied_slots": o,
            "available_slots": a,
            "reserved_slots": z.reserved_slots or 0,
            "occupancy_pct": occ_pct,
        })

    today_payments = frappe.get_all(
        "Parking Payment",
        filters={"payment_date": now_datetime().date(), "docstatus": 1},
        fields=["amount_paid"],
    )
    today_revenue = sum(flt(p.amount_paid or 0) for p in today_payments)

    today_entries = frappe.db.count(
        "Vehicle Entry",
        {"docstatus": 1, "entry_time": ["like", f"{now_datetime().date()}%"]},
    )

    active_reservations = frappe.db.count(
        "Parking Reservation",
        {"status": "Confirmed", "docstatus": 1},
    )

    return {
        "zones": zone_list,
        "stats": {
            "total_slots": total_slots,
            "occupied_slots": occupied,
            "available_slots": available,
            "today_revenue": today_revenue,
            "today_entries": today_entries,
            "active_reservations": active_reservations,
        },
    }


@frappe.whitelist()
def process_exit(vehicle_entry):
    """Process vehicle exit and calculate fee."""
    doc = frappe.get_doc("Vehicle Entry", vehicle_entry)
    if doc.exit_time:
        frappe.throw("Exit already processed.")

    from smart_parking.utils.calculations import calculate_parking_fee

    fee, hours = calculate_parking_fee(
        doc.zone, doc.vehicle_type, doc.entry_time, now_datetime()
    )

    doc.exit_time = now_datetime()
    doc.parking_fee = fee
    doc.duration_hours = hours
    doc.save(ignore_permissions=True)

    return {
        "fee": fee,
        "hours": hours,
        "exit_time": doc.exit_time,
    }


@frappe.whitelist()
def get_slot_details(slot):
    """Get details of a specific parking slot."""
    slot_doc = frappe.get_doc("Parking Slot", slot)
    zone_doc = frappe.get_doc("Parking Zone", slot_doc.zone) if slot_doc.zone else None

    return {
        "slot_number": slot_doc.slot_number,
        "zone": slot_doc.zone,
        "zone_name": zone_doc.zone_name if zone_doc else "",
        "slot_type": slot_doc.slot_type,
        "status": slot_doc.status,
        "is_occupied": slot_doc.is_occupied,
        "is_reserved": slot_doc.is_reserved,
        "current_vehicle": slot_doc.current_vehicle,
        "floor": slot_doc.floor,
    }
