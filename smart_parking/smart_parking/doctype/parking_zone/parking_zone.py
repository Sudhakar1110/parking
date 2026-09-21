# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.model.document import Document


class ParkingZone(Document):
    def validate(self):
        self.set_total_slots()
        self.calculate_occupancy()

    def set_total_slots(self):
        """Recalculate total slots from child table if needed."""
        pass

    def calculate_occupancy(self):
        """Calculate occupancy percentage."""
        if self.total_slots:
            self.occupancy_percentage = round(
                (self.occupied_slots / self.total_slots) * 100, 1
            )
        else:
            self.occupancy_percentage = 0

    def before_save(self):
        self.calculate_occupancy()

    def get_available_slots_count(self):
        """Return number of available slots."""
        return (self.total_slots or 0) - (self.occupied_slots or 0) - (self.reserved_slots or 0)
