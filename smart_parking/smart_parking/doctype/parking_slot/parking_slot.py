# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class ParkingSlot(Document):
    def validate(self):
        self.validate_zone_active()
        self.update_zone_counts()

    def validate_zone_active(self):
        if self.zone:
            is_active = frappe.db.get_value("Parking Zone", self.zone, "is_active")
            if not is_active:
                frappe.throw("Cannot add slot to an inactive zone.")

    def update_zone_counts(self):
        """Update zone slot counts."""
        if self.zone:
            zone = frappe.get_doc("Parking Zone", self.zone)
            zone.reload()

    def before_save(self):
        if self.is_occupied:
            self.status = "Occupied"
        elif self.is_reserved:
            self.status = "Reserved"
        else:
            self.status = "Available"

    def after_insert(self):
        self._update_zone_slot_count()

    def on_update(self):
        self._update_zone_slot_count()

    def on_trash(self):
        self._update_zone_slot_count()

    def _update_zone_slot_count(self):
        if self.zone:
            total = frappe.db.count("Parking Slot", {"zone": self.zone, "is_active": 1})
            occupied = frappe.db.count("Parking Slot", {"zone": self.zone, "is_occupied": 1, "is_active": 1})
            reserved = frappe.db.count("Parking Slot", {"zone": self.zone, "is_reserved": 1, "is_active": 1})
            frappe.db.set_value("Parking Zone", self.zone, {
                "total_slots": total,
                "occupied_slots": occupied,
                "reserved_slots": reserved,
                "available_slots": total - occupied - reserved,
            })
