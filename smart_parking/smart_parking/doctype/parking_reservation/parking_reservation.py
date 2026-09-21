# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime, time_diff_in_hours, flt


class ParkingReservation(Document):
    def validate(self):
        self.validate_slot_availability()
        self.calculate_duration()
        self.calculate_reservation_fee()

    def validate_slot_availability(self):
        if self.slot and self.start_time:
            existing = frappe.get_all(
                "Parking Reservation",
                filters={
                    "slot": self.slot,
                    "status": "Confirmed",
                    "name": ["!=", self.name],
                    "start_time": ["<", self.end_time],
                    "end_time": [">", self.start_time],
                },
                fields=["name"],
            )
            if existing:
                frappe.throw(f"Slot is already reserved for the selected time period ({existing[0].name}).")

    def calculate_duration(self):
        if self.start_time and self.end_time:
            self.duration_hours = flt(time_diff_in_hours(self.end_time, self.start_time), 2)

    def calculate_reservation_fee(self):
        if self.zone and self.duration_hours:
            fee_structure = frappe.db.get_value(
                "Parking Fee Structure",
                {"zone": self.zone, "vehicle_type": self.vehicle_type, "is_active": 1},
                ["hourly_rate", "daily_rate"],
                as_dict=True,
            )
            if fee_structure:
                hours = self.duration_hours or 0
                if hours <= 24:
                    self.reservation_fee = flt((fee_structure.hourly_rate or 0) * hours, 2)
                else:
                    days = hours / 24
                    self.reservation_fee = flt((fee_structure.daily_rate or 0) * days, 2)

    def before_save(self):
        if not self.status:
            self.status = "Draft"

    def on_submit(self):
        self.status = "Confirmed"
        if self.slot:
            frappe.db.set_value("Parking Slot", self.slot, {
                "is_reserved": 1,
                "reserved_by": self.customer,
                "reservation": self.name,
            })

    def on_cancel(self):
        self.status = "Cancelled"
        if self.slot:
            frappe.db.set_value("Parking Slot", self.slot, {
                "is_reserved": 0,
                "reserved_by": None,
                "reservation": None,
            })
