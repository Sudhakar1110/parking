# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ParkingShift(Document):
    def validate(self):
        self.validate_shift_overlap()
        self.set_status()

    def validate_shift_overlap(self):
        if self.staff_member and self.shift_start and self.shift_end:
            overlaps = frappe.get_all(
                "Parking Shift",
                filters={
                    "staff_member": self.staff_member,
                    "name": ["!=", self.name],
                    "status": ["in", ["Scheduled", "In Progress"]],
                    "shift_start": ["<", self.shift_end],
                    "shift_end": [">", self.shift_start],
                },
                fields=["name"],
            )
            if overlaps:
                frappe.throw(f"Shift overlaps with existing shift {overlaps[0].name}.")

    def set_status(self):
        now = now_datetime()
        if self.status == "Draft":
            return
        if self.shift_start and now >= self.shift_start and (not self.shift_end or now <= self.shift_end):
            self.status = "In Progress"
        elif self.shift_end and now > self.shift_end:
            self.status = "Completed"
