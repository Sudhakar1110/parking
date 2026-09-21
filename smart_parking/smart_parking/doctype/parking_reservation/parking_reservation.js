frappe.ui.form.on('Parking Reservation', {
    refresh(frm) {
    },

    zone(frm) {
        if (frm.doc.zone) {
            frm.set_query("slot", () => {
                return {
                    filters: {
                        zone: frm.doc.zone,
                        status: "Available",
                    },
                };
            });
        }
    },
});
