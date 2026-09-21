import frappe

def get_context(context):
    context.no_cache = 1
    context.title = "My Vehicles"

    if frappe.session.user == "Guest":
        context.vehicles = []
        return

    vehicles = frappe.get_all(
        "Vehicle",
        filters={"owner": frappe.session.user},
        fields=["name", "license_plate", "vehicle_name", "vehicle_type", "make", "model", "color"],
    )

    context.vehicles = vehicles
