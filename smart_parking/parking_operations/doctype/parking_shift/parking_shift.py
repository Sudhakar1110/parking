import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class ParkingShift(Document):
    def validate(self):
        if self.staff_member and self.shift_start and self.shift_end:
            overlaps = frappe.get_all("Parking Shift", filters={"staff_member": self.staff_member, "name": ["!=", self.name], "status": ["in", ["Scheduled", "In Progress"]], "shift_start": ["<", self.shift_end], "shift_end": [">", self.shift_start]}, fields=["name"])
            if overlaps:
                frappe.throw(f"Shift overlaps with existing shift {overlaps[0].name}.")
