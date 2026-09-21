"""
smart_parking/tasks.py
Scheduler tasks — invoked by hooks.py scheduler_events
"""
import frappe
from frappe.utils import today, add_days, getdate, now_datetime, flt, cint


def check_slot_occupancy_alerts():
    """Daily task: Send alerts when slot occupancy exceeds threshold."""
    zones = frappe.get_all("Parking Zone", filters={"is_active": 1}, fields=["name", "zone_name", "total_slots", "occupied_slots", "alert_threshold"])

    for zone in zones:
        if zone.total_slots and zone.occupied_slots:
            occupancy_pct = (zone.occupied_slots / zone.total_slots) * 100
            if occupancy_pct >= (zone.alert_threshold or 90):
                frappe.get_doc({
                    "doctype": "Parking Alert",
                    "alert_type": "Occupancy Threshold",
                    "zone": zone.name,
                    "message": f"Zone '{zone.zone_name}' has reached {occupancy_pct:.1f}% occupancy ({zone.occupied_slots}/{zone.total_slots} slots).",
                    "priority": "High" if occupancy_pct >= 95 else "Medium",
                }).insert(ignore_permissions=True)
                frappe.db.commit()

                frappe.sendmail(
                    recipients=frappe.db.get_value("User", {"role_profile_name": "Parking Manager"}, "email") or [],
                    subject=f"[SPMS] High Occupancy Alert — {zone.zone_name}",
                    message=f"Zone '{zone.zone_name}' has reached {occupancy_pct:.1f}% occupancy. Please take action.",
                )


def check_reservation_expiry():
    """Daily task: Mark expired reservations and release slots."""
    now = now_datetime()
    expired = frappe.get_all(
        "Parking Reservation",
        filters={"status": "Confirmed", "end_time": ["<", now]},
        fields=["name", "slot", "vehicle"],
    )

    for res in expired:
        frappe.db.set_value("Parking Reservation", res.name, "status", "Expired")
        if res.slot:
            slot_occupied = frappe.db.get_value("Parking Slot", res.slot, "is_occupied")
            if slot_occupied:
                frappe.db.set_value("Parking Slot", res.slot, "is_occupied", 0)
                frappe.db.set_value("Parking Slot", res.slot, "current_vehicle", None)

    frappe.db.commit()

    if expired:
        frappe.get_doc({
            "doctype": "Parking Alert",
            "alert_type": "Reservation Expiry",
            "message": f"{len(expired)} reservation(s) have expired and slots have been released.",
            "priority": "Low",
        }).insert(ignore_permissions=True)
        frappe.db.commit()


def check_overdue_vehicles():
    """Daily task: Alert for vehicles parked beyond expected duration."""
    threshold_hours = cint(frappe.db.get_single_value("Smart Parking Settings", "overdue_threshold_hours") or 24)
    now = now_datetime()

    overdue = frappe.get_all(
        "Vehicle Entry",
        filters={"status": "Parked", "entry_time": ["<", add_days(now, -1)]},
        fields=["name", "vehicle", "slot", "entry_time", "zone"],
    )

    for entry in overdue:
        frappe.get_doc({
            "doctype": "Parking Alert",
            "alert_type": "Overdue Vehicle",
            "zone": entry.zone,
            "vehicle_entry": entry.name,
            "message": f"Vehicle {entry.vehicle} has been parked since {entry.entry_time}. Duration exceeds {threshold_hours} hours.",
            "priority": "Medium",
        }).insert(ignore_permissions=True)

    frappe.db.commit()


def update_slot_availability():
    """Hourly task: Sync slot availability counts on zones."""
    zones = frappe.get_all("Parking Zone", filters={"is_active": 1}, fields=["name"])

    for zone in zones:
        total = frappe.db.count("Parking Slot", {"zone": zone.name, "is_active": 1})
        occupied = frappe.db.count("Parking Slot", {"zone": zone.name, "is_occupied": 1, "is_active": 1})
        reserved = frappe.db.count("Parking Slot", {"zone": zone.name, "is_reserved": 1, "is_occupied": 0, "is_active": 1})

        frappe.db.set_value("Parking Zone", zone.name, {
            "total_slots": total,
            "occupied_slots": occupied,
            "reserved_slots": reserved,
            "available_slots": total - occupied - reserved,
        })

    frappe.db.commit()


def generate_daily_occupancy_summary():
    """Daily task: Create an occupancy summary log entry."""
    zones = frappe.get_all(
        "Parking Zone",
        filters={"is_active": 1},
        fields=["name", "zone_name", "total_slots", "occupied_slots", "available_slots", "reserved_slots"],
    )

    summary_lines = []
    for z in zones:
        occ_pct = (z.occupied_slots / z.total_slots * 100) if z.total_slots else 0
        summary_lines.append(f"{z.zone_name}: {z.occupied_slots}/{z.total_slots} ({occ_pct:.1f}%)")

    if summary_lines:
        frappe.get_doc({
            "doctype": "Parking Alert",
            "alert_type": "System Notification",
            "message": "Daily Occupancy Summary:\n" + "\n".join(summary_lines),
            "priority": "Low",
        }).insert(ignore_permissions=True)
        frappe.db.commit()


def generate_weekly_revenue_report():
    """Weekly task: Aggregate revenue data and send summary email."""
    from frappe.utils import get_first_day, get_last_day

    today_date = getdate(today())
    week_start = add_days(today_date, -7)

    payments = frappe.get_all(
        "Parking Payment",
        filters={"payment_date": ["between", [week_start, today_date]], "docstatus": 1},
        fields=["amount_paid", "zone"],
    )

    if not payments:
        return

    total_revenue = sum(flt(p.amount_paid or 0) for p in payments)
    zone_revenue = {}
    for p in payments:
        zone_revenue[p.zone] = zone_revenue.get(p.zone, 0) + flt(p.amount_paid or 0)

    report_lines = [f"Total Revenue: {frappe.currency(total_revenue, 'INR')}"]
    for zone, rev in zone_revenue.items():
        zone_name = frappe.db.get_value("Parking Zone", zone, "zone_name") or zone
        report_lines.append(f"  {zone_name}: {frappe.currency(rev, 'INR')}")

    frappe.sendmail(
        recipients=frappe.db.get_value("User", {"role_profile_name": "Parking Manager"}, "email") or [],
        subject="[SPMS] Weekly Revenue Report",
        message="<br>".join(report_lines),
    )
