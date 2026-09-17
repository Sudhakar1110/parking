import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, flt

class ParkingPayment(Document):
    def validate(self):
        if self.amount_paid and self.amount_paid <= 0:
            frappe.throw("Amount paid must be greater than zero.")
        if not self.payment_date:
            self.payment_date = now_datetime().date()
        if not self.payment_method:
            self.payment_method = "Cash"

    def on_submit(self):
        if self.fee_entry:
            frappe.db.set_value("Parking Fee Entry", self.fee_entry, {"fee_status": "Paid", "payment": self.name, "paid_amount": self.amount_paid, "payment_date": self.payment_date})
        if self.vehicle_entry:
            frappe.db.set_value("Vehicle Entry", self.vehicle_entry, "fee_status", "Paid")
        frappe.db.commit()

    def on_cancel(self):
        if self.fee_entry:
            frappe.db.set_value("Parking Fee Entry", self.fee_entry, {"fee_status": "Pending", "payment": None, "paid_amount": 0, "payment_date": None})
        if self.vehicle_entry:
            frappe.db.set_value("Vehicle Entry", self.vehicle_entry, "fee_status", "Pending")
        frappe.db.commit()
