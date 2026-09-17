frappe.ui.form.on("Vehicle Entry", {
    refresh(frm) {
        if (!frm.is_new() && frm.doc.docstatus === 1 && !frm.doc.exit_time) {
            frm.add_custom_button(__("Process Exit"), function () {
                frappe.confirm(
                    __("Process vehicle exit for {0}?", [frm.doc.vehicle]),
                    function () {
                        frappe.call({
                            method: "smart_parking.utils.entry_exit.process_vehicle_exit",
                            args: { doc: frm.doc },
                            callback: function (r) {
                                if (r.message) {
                                    frm.set_value("exit_time", frappe.datetime.now_datetime());
                                    frm.set_value("parking_fee", r.message.fee);
                                    frm.set_value("duration_hours", r.message.hours);
                                    frm.save();
                                }
                            },
                        });
                    }
                );
            }, __("Actions"));
        }

        if (!frm.is_new() && frm.doc.parking_fee > 0 && frm.doc.fee_status !== "Paid") {
            frm.add_custom_button(__("Create Payment"), function () {
                frappe.new_doc("Parking Payment", {
                    vehicle_entry: frm.doc.name,
                    vehicle: frm.doc.vehicle,
                    zone: frm.doc.zone,
                    amount_paid: frm.doc.parking_fee,
                    payment_date: frappe.datetime.get_today(),
                });
            }, __("Actions"));
        }
    },

    zone(frm) {
        if (frm.doc.zone) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Parking Zone",
                    filters: { name: frm.doc.zone },
                    fieldname: ["available_slots", "total_slots"],
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_df_property(
                            "zone_info",
                            "description",
                            `Available: ${r.message.available_slots || 0} / Total: ${r.message.total_slots || 0}`
                        );
                    }
                },
            });
        }
    },

    slot(frm) {
        if (frm.doc.slot) {
            frappe.call({
                method: "frappe.client.get_value",
                args: {
                    doctype: "Parking Slot",
                    filters: { name: frm.doc.slot },
                    fieldname: ["is_occupied", "is_reserved", "slot_number"],
                },
                callback: function (r) {
                    if (r.message) {
                        if (r.message.is_occupied) {
                            frappe.msgprint(__("Warning: This slot is currently occupied."));
                        }
                        if (r.message.is_reserved) {
                            frappe.msgprint(__("Warning: This slot is currently reserved."));
                        }
                    }
                },
            });
        }
    },

    exit_time(frm) {
        if (frm.doc.exit_time && frm.doc.entry_time) {
            frappe.call({
                method: "smart_parking.utils.calculations.calculate_parking_fee",
                args: {
                    zone: frm.doc.zone,
                    vehicle_type: frm.doc.vehicle_type,
                    entry_time: frm.doc.entry_time,
                    exit_time: frm.doc.exit_time,
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("parking_fee", r.message[0]);
                        frm.set_value("duration_hours", r.message[1]);
                    }
                },
            });
        }
    },
});