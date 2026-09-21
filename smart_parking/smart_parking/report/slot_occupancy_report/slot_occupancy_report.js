frappe.query_reports["Slot Occupancy Report"] = {
    filters: [
        {
            fieldname: "zone",
            label: __("Parking Zone"),
            fieldtype: "Link",
            options: "Parking Zone",
        },
        {
            fieldname: "zone_type",
            label: __("Zone Type"),
            fieldtype: "Select",
            options: "\nOutdoor\nCovered\nMulti-Story\nBasement\nValet",
        },
    ],
};
