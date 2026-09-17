import frappe
from frappe.model.document import Document

class ParkingStaff(Document):
    def validate(self):
        if self.user:
            exists = frappe.db.get_value("Parking Staff", {"user": self.user, "name": ["!=", self.name]}, "name")
            if exists:
                frappe.throw(f"This user is already linked to staff member {exists}.")
