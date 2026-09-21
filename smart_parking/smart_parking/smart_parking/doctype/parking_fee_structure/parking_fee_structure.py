import frappe
from frappe.model.document import Document

class ParkingFeeStructure(Document):
    def validate(self):
        if not self.hourly_rate and not self.daily_rate and not self.weekly_rate and not self.monthly_rate:
            frappe.throw("At least one fee rate must be defined.")
