# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class ParkingStaff(Document):
    def validate(self):
        self.validate_user()

    def validate_user(self):
        if self.user:
            exists = frappe.db.get_value(
                "Parking Staff",
                {"user": self.user, "name": ["!=", self.name]},
                "name",
            )
            if exists:
                frappe.throw(f"This user is already linked to staff member {exists}.")
