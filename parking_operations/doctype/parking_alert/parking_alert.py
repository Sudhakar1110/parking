# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ParkingAlert(Document):
    def before_insert(self):
        if not self.created_on:
            self.created_on = now_datetime()
        if not self.status:
            self.status = "Open"
