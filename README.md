# Smart Parking Management System (SPMS) — Frappe App

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://frappe.io)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-green)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **custom Frappe app** built on ERPNext v15+ for comprehensive parking management — from zone and slot configuration through vehicle entry/exit tracking, reservations, fee collection, and real-time analytics.

---

## Modules

| # | Module | DocTypes | Description |
|---|--------|----------|-------------|
| 1 | **Parking Zone** | Parking Zone, Parking Slot Type, Parking Slot | Zone configuration, slot types, slot inventory |
| 2 | **Vehicle Management** | Vehicle, Vehicle Entry, Parking Reservation, Parking Incident | Vehicle registry, entry/exit, reservations, incidents |
| 3 | **Parking Billing** | Parking Fee Structure, Parking Fee Entry, Parking Payment | Fee configuration, billing, payment tracking |
| 4 | **Parking Operations** | Parking Staff, Parking Shift, Parking Alert | Staff management, shift scheduling, alerts |
| 5 | **Reports & Analytics** | Slot Occupancy Report, Vehicle Entry Register, Revenue Report | Dashboards and analytics |

---

## Installation

```bash
# 1. Get the app
bench get-app smart_parking https://github.com/Sudhakar1110/solar.git

# 2. Install on your ERPNext site
bench --site your-site.local install-app smart_parking

# 3. Run migrations
bench --site your-site.local migrate

# 4. Restart and clear cache
bench restart
bench --site your-site.local clear-cache
```

---

## Script Reports

| Report | Module | Filters |
|--------|--------|---------|
| Slot Occupancy Report | Parking Zone | Zone, Date Range, Slot Type |
| Vehicle Entry Register | Vehicle Management | Zone, Date Range, Vehicle Type |
| Revenue Report | Parking Billing | Zone, Date Range, Payment Status |

---

## Key Technical Features

- **Real-time Slot Tracking** — Live availability updates on vehicle entry/exit
- **Dynamic Fee Calculation** — Hourly, daily, weekly, and monthly fee structures
- **Reservation System** — Pre-book parking slots with automatic conflict detection
- **Staff Shift Management** — Auto-scheduling and shift overlap prevention
- **Automated Alerts** — Occupancy thresholds, expired reservations, overdue vehicles
- **ERPNext Integration** — Sales Invoice auto-creation, Customer linking
- **Web Portal** — Public slot availability checker and reservation booking

---

## Custom Roles

| Role | Description |
|------|-------------|
| Parking Manager | Full access to all SPMS modules |
| Parking Attendant | Entry/exit operations, shift management |
| Parking Supervisor | Zone management, billing oversight |
| Customer | Portal access for reservations |

---

## Naming Series

| DocType | Series |
|---------|--------|
| Parking Zone | PZ-.YYYY.-.#### |
| Parking Slot | PS-.YYYY.-.##### |
| Vehicle | VEH-.YYYY.-.#### |
| Vehicle Entry | VE-.YYYY.MM.DD.-.##### |
| Parking Reservation | PRES-.YYYY.-.#### |
| Parking Fee Entry | PFE-.YYYY.-.#### |
| Parking Payment | PPAY-.YYYY.-.#### |

---

## License

MIT License — Copyright (c) 2026 Sudhakar
