# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class ParkingIncident(Document):
    def validate(self):
        if not self.reported_date:
            self.reported_date = now_datetime()

    def before_save(self):
        if not self.status:
            self.status = "Open"
