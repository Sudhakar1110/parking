frappe.provide("smart_parking.dashboard");

smart_parking.dashboard = {
    refresh() {
        this.load_zone_status();
    },

    load_zone_status() {
        frappe.call({
            method: "smart_parking.api.get_parking_dashboard_data",
            callback: function (r) {
                if (r.message) {
                    smart_parking.dashboard.render_zones(r.message.zones);
                    smart_parking.dashboard.render_stats(r.message.stats);
                }
            },
        });
    },

    render_zones(zones) {
        let html = '<div class="row">';
        zones.forEach(function (zone) {
            let color = zone.occupancy_pct >= 90 ? "danger" : zone.occupancy_pct >= 70 ? "warning" : "success";
            html += `
                <div class="col-sm-4">
                    <div class="card border-${color} mb-3">
                        <div class="card-body">
                            <h5 class="card-title">${zone.zone_name}</h5>
                            <p class="card-text">
                                <strong>${zone.occupied_slots}/${zone.total_slots}</strong> slots occupied<br>
                                <span class="text-${color}">${zone.occupancy_pct}% occupancy</span>
                            </p>
                        </div>
                    </div>
                </div>`;
        });
        html += "</div>";
        $("#parking-zone-status").html(html);
    },

    render_stats(stats) {
        $("#total-slots").text(stats.total_slots);
        $("#occupied-slots").text(stats.occupied_slots);
        $("#available-slots").text(stats.available_slots);
        $("#today-revenue").text(frappe.format_amount(stats.today_revenue));
    },
};