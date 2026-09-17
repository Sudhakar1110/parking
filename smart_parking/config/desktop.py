from __future__ import unicode_literals
from frappe import _

def get_data():
    return [
        {
            "module_name": "Parking Zone",
            "color": "#1565c0",
            "icon": "octicon octicon-location",
            "type": "module",
            "label": _("Parking Zone"),
        },
        {
            "module_name": "Vehicle Management",
            "color": "#2e7d32",
            "icon": "octicon octicon-car",
            "type": "module",
            "label": _("Vehicle Management"),
        },
        {
            "module_name": "Parking Billing",
            "color": "#e65100",
            "icon": "octicon octicon-credit-card",
            "type": "module",
            "label": _("Parking Billing"),
        },
        {
            "module_name": "Parking Operations",
            "color": "#6a1b9a",
            "icon": "octicon octicon-organization",
            "type": "module",
            "label": _("Parking Operations"),
        },
        {
            "module_name": "Smart Parking",
            "color": "#00695c",
            "icon": "octicon octicon-package",
            "type": "module",
            "label": _("Smart Parking"),
        },
    ]
