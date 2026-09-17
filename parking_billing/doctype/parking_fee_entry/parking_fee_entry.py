# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ParkingFeeEntry(Document):
    def validate(self):
        if not self.created_date:
            self.created_date = now_datetime()
