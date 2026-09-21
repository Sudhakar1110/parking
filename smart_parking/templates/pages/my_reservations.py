import frappe

def get_context(context):
    context.no_cache = 1
    context.title = "My Reservations"

    if frappe.session.user == "Guest":
        context.reservations = []
        return

    reservations = frappe.get_all(
        "Parking Reservation",
        filters={"owner": frappe.session.user},
        fields=["name", "vehicle", "zone", "slot", "start_time", "end_time", "status", "reservation_fee", "payment_status"],
        order_by="start_time desc",
        limit_page_length=50,
    )

    context.reservations = reservations
