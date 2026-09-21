"""
smart_parking/utils/calculations.py
Fee Calculation Engine — computes parking fees based on duration and fee structure
"""
import frappe
from frappe.utils import flt, time_diff_in_hours, get_datetime


def calculate_parking_fee(zone, vehicle_type, entry_time, exit_time=None):
    """
    Calculate parking fee based on zone, vehicle type, and duration.
    Returns (fee_amount, hours_parked).
    """
    if not exit_time:
        exit_time = get_datetime()

    hours = flt(time_diff_in_hours(exit_time, entry_time), 2)
    if hours <= 0:
        hours = 0.25

    fee_structure = frappe.db.get_value(
        "Parking Fee Structure",
        {"zone": zone, "vehicle_type": vehicle_type, "is_active": 1},
        ["name", "hourly_rate", "daily_rate", "weekly_rate", "monthly_rate"],
        as_dict=True,
    )

    if not fee_structure:
        return 0, hours

    hourly = flt(fee_structure.hourly_rate or 0)
    daily = flt(fee_structure.daily_rate or 0)
    weekly = flt(fee_structure.weekly_rate or 0)
    monthly = flt(fee_structure.monthly_rate or 0)

    if hours <= 1:
        fee = hourly
    elif hours <= 24:
        if daily and daily < hourly * hours:
            fee = daily
        else:
            fee = hourly * hours
    elif hours <= 168:
        if weekly and weekly < hourly * hours:
            fee = weekly
        elif daily and daily * (hours / 24) > weekly:
            fee = weekly
        else:
            fee = hourly * hours
    else:
        days = hours / 24
        if monthly:
            fee = monthly
        elif weekly:
            weeks = int(days / 7)
            remaining_hours = hours - (weeks * 168)
            fee = (weekly * weeks) + (hourly * remaining_hours)
        elif daily:
            full_days = int(days)
            remaining_hours = hours - (full_days * 24)
            fee = (daily * full_days) + (hourly * remaining_hours)
        else:
            fee = hourly * hours

    return flt(fee, 2), hours


def create_fee_entry(vehicle_entry_doc, method=None):
    """Create Parking Fee Entry on Vehicle Entry submit."""
    if vehicle_entry_doc.parking_fee and vehicle_entry_doc.parking_fee > 0:
        fee_entry = frappe.get_doc({
            "doctype": "Parking Fee Entry",
            "vehicle_entry": vehicle_entry_doc.name,
            "vehicle": vehicle_entry_doc.vehicle,
            "zone": vehicle_entry_doc.zone,
            "slot": vehicle_entry_doc.slot,
            "entry_time": vehicle_entry_doc.entry_time,
            "fee_amount": vehicle_entry_doc.parking_fee,
            "fee_status": "Pending",
        })
        fee_entry.insert(ignore_permissions=True)
        frappe.db.commit()


def calculate_fee_on_exit(doc, method=None):
    """Calculate final parking fee when vehicle exits."""
    if doc.exit_time and doc.entry_time:
        fee, hours = calculate_parking_fee(
            doc.zone, doc.vehicle_type, doc.entry_time, doc.exit_time
        )
        doc.parking_fee = fee
        doc.duration_hours = hours
