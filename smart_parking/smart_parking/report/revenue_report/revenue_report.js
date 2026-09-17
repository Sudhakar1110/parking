frappe.query_reports["Revenue Report"] = {
    filters: [
        {
            fieldname: "zone",
            label: __("Parking Zone"),
            fieldtype: "Link",
            options: "Parking Zone",
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_days(frappe.datetime.get_today(), -30),
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
        },
    ],
};
