# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class Vehicle(Document):
    def validate(self):
        self.validate_registration()

    def validate_registration(self):
        if self.license_plate:
            existing = frappe.db.get_value(
                "Vehicle",
                {"license_plate": self.license_plate, "name": ["!=", self.name]},
                "name",
            )
            if existing:
                frappe.throw(f"Vehicle with registration {self.license_plate} already exists ({existing}).")
