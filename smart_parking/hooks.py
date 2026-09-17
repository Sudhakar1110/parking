from __future__ import unicode_literals

app_name = "smart_parking"
app_title = "Smart Parking"
app_publisher = "Sudhakar"
app_description = "Smart Parking Management System — zone management, slot tracking, vehicle entry/exit, reservations, billing, and analytics"
app_email = "admin@example.com"
app_license = "MIT"
app_version = "1.0.0"

# Required Apps
required_apps = ["frappe", "erpnext"]

# Asset Configuration
app_include_js = "/assets/smart_parking/js/smart_parking.min.js"
app_include_css = "/assets/smart_parking/css/smart_parking.min.css"

# Portal Configuration
portal_menu_items = [
    {"title": "Check Availability", "route": "/parking-portal/availability", "role": "Customer"},
    {"title": "My Reservations", "route": "/parking-portal/my-reservations", "role": "Customer"},
    {"title": "My Vehicles", "route": "/parking-portal/my-vehicles", "role": "Customer"},
]

# Fixtures
fixtures = [
    {
        "dt": "Role",
        "filters": [["role_name", "in", [
            "Parking Manager",
            "Parking Attendant",
            "Parking Supervisor",
            "Customer",
        ]]],
    },
    "Custom Field",
    "Property Setter",
    {
        "dt": "Module Def",
        "filters": [["module_name", "=", "Smart Parking"]],
    },
    {
        "dt": "Workspace",
        "filters": [["name", "=", "Smart Parking"]],
    },
    {
        "dt": "Notification",
        "filters": [["name", "in", [
            "Parking Slot Occupancy Alert",
            "Reservation Expiry Reminder",
            "Vehicle Overdue Alert",
            "Payment Received Notification",
        ]]],
    },
    {
        "dt": "Number Card",
        "filters": [["name", "in", [
            "Available Slots",
            "Occupied Slots",
            "Today Revenue",
            "Active Reservations",
            "Today Vehicle Entries",
        ]]],
    },
    {
        "dt": "Dashboard Chart",
        "filters": [["name", "in", [
            "Daily Occupancy Trend",
            "Revenue by Zone",
            "Vehicle Type Distribution",
            "Monthly Revenue Trend",
        ]]],
    },
]

# Custom Roles
roles = [
    {"role_name": "Parking Manager"},
    {"role_name": "Parking Attendant"},
    {"role_name": "Parking Supervisor"},
    {"role_name": "Customer"},
]

# Scheduler Events
scheduler_events = {
    "daily": [
        "smart_parking.tasks.check_slot_occupancy_alerts",
        "smart_parking.tasks.check_reservation_expiry",
        "smart_parking.tasks.check_overdue_vehicles",
        "smart_parking.tasks.generate_daily_occupancy_summary",
    ],
    "hourly": [
        "smart_parking.tasks.update_slot_availability",
    ],
    "weekly": [
        "smart_parking.tasks.generate_weekly_revenue_report",
    ],
}

# Document Events
doc_events = {
    "Vehicle Entry": {
        "on_submit": "smart_parking.utils.entry_exit.on_vehicle_entry_submit",
        "on_cancel": "smart_parking.utils.entry_exit.on_vehicle_entry_cancel",
    },
    "Vehicle Entry": {
        "validate": "smart_parking.utils.entry_exit.validate_vehicle_entry",
    },
    "Parking Reservation": {
        "on_submit": "smart_parking.utils.reservations.on_reservation_submit",
        "on_cancel": "smart_parking.utils.reservations.on_reservation_cancel",
    },
    "Parking Payment": {
        "on_submit": "smart_parking.utils.billing.on_payment_submit",
    },
}

# Website Route Rules
website_route_rules = [
    {"from_route": "/parking-portal/<path:app_path>", "to_route": "parking_portal"},
]

# Override DocType Dashboards
override_doctype_dashboards = {
    "Sales Invoice": "smart_parking.parking_billing.doctype.parking_payment.parking_payment_dashboard.get_data",
}

# Jinja
jinja = {
    "methods": [
        "smart_parking.utils.jinja_methods.get_available_slots",
        "smart_parking.utils.jinja_methods.get_zone_status",
    ],
    "filters": [],
}

# Doc Hooks
has_permission = {
    "Vehicle": "smart_parking.utils.permissions.has_vehicle_permission",
    "Vehicle Entry": "smart_parking.utils.permissions.has_vehicle_entry_permission",
}

# Override whitelisted methods
override_whitelisted_methods = {
    "smart_parking.api.check_availability": "smart_parking.api.check_availability",
    "smart_parking.api.book_slot": "smart_parking.api.book_slot",
    "smart_parking.api.get_parking_dashboard_data": "smart_parking.api.get_parking_dashboard_data",
}
