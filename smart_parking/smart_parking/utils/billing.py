"""
smart_parking/utils/billing.py
Billing and payment handlers — called via hooks on Parking Payment
"""
import frappe
from frappe.utils import flt


def on_payment_submit(doc, method=None):
    """On Parking Payment submit: update fee entry status and create Sales Invoice."""
    if doc.fee_entry:
        frappe.db.set_value("Parking Fee Entry", doc.fee_entry, "fee_status", "Paid")
        frappe.db.set_value("Parking Fee Entry", doc.fee_entry, "payment", doc.name)

    if getattr(doc, "create_sales_invoice", 0):
        create_sales_invoice_from_payment(doc)

    frappe.db.commit()


def create_sales_invoice_from_payment(doc):
    """Create a Sales Invoice from Parking Payment for ERPNext integration."""
    customer = doc.customer
    if not customer:
        vehicle = frappe.db.get_value("Vehicle", doc.vehicle, "owner_name") if doc.vehicle else None
        customer = frappe.db.get_value("Customer", {"customer_name": vehicle}, "name") if vehicle else None

    if not customer:
        frappe.msgprint("No customer found. Sales Invoice not created.")
        return

    si = frappe.new_doc("Sales Invoice")
    si.customer = customer
    si.posting_date = doc.payment_date
    si.due_date = doc.payment_date
    si.append("items", {
        "item_name": f"Parking Fee - {doc.zone}",
        "description": f"Parking fee for zone {doc.zone}",
        "qty": 1,
        "rate": doc.amount_paid,
        "amount": doc.amount_paid,
    })
    si.insert(ignore_permissions=True)
    si.submit()
    frappe.db.commit()
