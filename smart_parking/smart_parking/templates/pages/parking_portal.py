# Copyright (c) 2026, Sudhakar and contributors
# License: MIT. See LICENSE

import frappe
from frappe.utils import now_datetime


def get_context(context):
    context.no_cache = 1
    context.title = "Smart Parking Portal"

    zones = frappe.get_all(
        "Parking Zone",
        filters={"is_active": 1},
        fields=["name", "zone_name", "zone_type", "total_slots", "occupied_slots", "available_slots"],
    )

    for zone in zones:
        zone.occupancy_pct = round(
            (zone.occupied_slots / zone.total_slots * 100), 1
        ) if zone.total_slots else 0

    context.zones = zones
    context.user = frappe.session.user
