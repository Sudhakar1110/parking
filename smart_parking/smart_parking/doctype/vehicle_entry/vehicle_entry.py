# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime, flt, time_diff_in_hours


class VehicleEntry(Document):
    def validate(self):
        self.validate_zone_active()
        self.calculate_parking_fee()
        self.validate_slot_availability()

    def validate_zone_active(self):
        if self.zone:
            is_active = frappe.db.get_value("Parking Zone", self.zone, "is_active")
            if not is_active:
                frappe.throw("Cannot create entry for an inactive parking zone.")

    def validate_slot_availability(self):
        if self.slot and not self.exit_time:
            slot_data = frappe.db.get_value(
                "Parking Slot", self.slot,
                ["is_active", "is_occupied", "is_reserved"],
                as_dict=True,
            )
            if not slot_data.is_active:
                frappe.throw("The selected parking slot is not active.")
            if slot_data.is_occupied:
                frappe.throw("The selected parking slot is already occupied.")
            if slot_data.is_reserved:
                reservation = frappe.db.get_value(
                    "Parking Reservation",
                    {"slot": self.slot, "status": "Confirmed"},
                    ["name", "customer", "vehicle"],
                    as_dict=True,
                )
                if reservation and reservation.vehicle != self.vehicle:
                    frappe.throw("The selected parking slot is reserved for another vehicle.")

    def calculate_parking_fee(self):
        if self.exit_time and self.entry_time:
            from smart_parking.utils.calculations import calculate_parking_fee
            fee, hours = calculate_parking_fee(
                self.zone, self.vehicle_type, self.entry_time, self.exit_time
            )
            self.parking_fee = fee
            self.duration_hours = hours
        elif self.entry_time and not self.exit_time:
            from smart_parking.utils.calculations import calculate_parking_fee
            fee, hours = calculate_parking_fee(
                self.zone, self.vehicle_type, self.entry_time, now_datetime()
            )
            self.estimated_fee = fee

    def before_save(self):
        if not self.entry_time:
            self.entry_time = now_datetime()

    def on_submit(self):
        if self.slot:
            frappe.db.set_value("Parking Slot", self.slot, {
                "is_occupied": 1,
                "current_vehicle": self.vehicle,
                "last_entry": self.name,
            })
        if self.zone:
            current = frappe.db.get_value("Parking Zone", self.zone, "occupied_slots") or 0
            frappe.db.set_value("Parking Zone", self.zone, "occupied_slots", current + 1)

    def on_cancel(self):
        if self.slot:
            frappe.db.set_value("Parking Slot", self.slot, {
                "is_occupied": 0,
                "current_vehicle": None,
                "last_entry": None,
            })
        if self.zone:
            current = frappe.db.get_value("Parking Zone", self.zone, "occupied_slots") or 0
            frappe.db.set_value("Parking Zone", self.zone, "occupied_slots", max(0, current - 1))
