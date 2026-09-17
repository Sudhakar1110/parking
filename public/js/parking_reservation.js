frappe.ui.form.on("Parking Reservation", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1 && frm.doc.status === "Confirmed") {
            frm.add_custom_button(__("Cancel Reservation"), function () {
                frappe.confirm(
                    __("Cancel reservation {0}?", [frm.doc.name]),
                    function () {
                        frappe.call({
                            method: "frappe.client.set_value",
                            args: {
                                doctype: "Parking Reservation",
                                name: frm.doc.name,
                                fieldname: "status",
                                value: "Cancelled",
                            },
                            callback: function () {
                                frm.reload_doc();
                            },
                        });
                    }
                );
            }, __("Actions"));
        }
    },

    zone(frm) {
        if (frm.doc.zone) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Parking Slot",
                    filters: {
                        zone: frm.doc.zone,
                        is_active: 1,
                        is_occupied: 0,
                        is_reserved: 0,
                    },
                    fields: ["name", "slot_number", "slot_type"],
                    limit_page_length: 0,
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_df_property("slot", "options", r.message.map(s => s.name));
                    }
                },
            });
        }
    },

    start_time(frm) {
        calculate_duration(frm);
    },

    end_time(frm) {
        calculate_duration(frm);
    },
});

function calculate_duration(frm) {
    if (frm.doc.start_time && frm.doc.end_time) {
        let start = moment(frm.doc.start_time);
        let end = moment(frm.doc.end_time);
        let hours = end.diff(start, "hours", true);
        frm.set_value("duration_hours", Math.round(hours * 100) / 100);
    }
}