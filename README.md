# Smart Parking Management System (SPMS) — Frappe App

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://frappe.io)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-green)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **custom Frappe app** built on ERPNext v15+ for comprehensive parking management — from zone and slot configuration through vehicle entry/exit tracking, reservations, fee collection, and real-time analytics.

---

## Features

- **Zone & Slot Management** — Create parking zones with types (Outdoor, Covered, Multi-Story, Basement, Valet), slot types (Car, SUV, Motorcycle, EV Charging, Handicap), and real-time occupancy tracking
- **Vehicle Entry/Exit** — Submit/cancel/amend vehicle entries with automatic fee calculation and slot occupation
- **Reservations** — Pre-book parking slots with overlap detection, automatic fee calculation from fee structures
- **Billing & Payments** — Fee structures with hourly/daily/weekly/monthly rates, payment tracking with ERPNext Sales Invoice integration
- **Staff & Shift Management** — Staff registry with roles, shift scheduling with overlap prevention
- **Incidents & Alerts** — Track damage, theft, vandalism; automated alerts for occupancy thresholds, overdue vehicles, expired reservations
- **Reports & Analytics** — Revenue reports, slot occupancy reports, vehicle entry registers, dashboard charts, and number cards
- **Customer Portal** — Public-facing pages for checking availability, managing reservations, and viewing vehicles
- **Automated Tasks** — Daily occupancy alerts, reservation expiry, overdue vehicle detection, weekly revenue reports

---

## DocTypes (14)

| # | DocType | Naming | Submittable | Description |
|---|---------|--------|:-----------:|-------------|
| 1 | Parking Zone | PZ-.YYYY.-.#### | No | Parking area configuration with occupancy tracking |
| 2 | Parking Slot | PS-.YYYY.-.##### | No | Individual parking spot within a zone |
| 3 | Parking Slot Type | (by type_name) | No | Slot categories (Car, SUV, EV, etc.) |
| 4 | Vehicle | VEH-.YYYY.-.#### | No | Registered vehicle with owner details |
| 5 | Vehicle Entry | VE-.YYYY.MM.DD.-.##### | **Yes** | Vehicle entry/exit record with fee tracking |
| 6 | Parking Reservation | PRES-.YYYY.-.#### | **Yes** | Pre-booked slot reservation |
| 7 | Parking Payment | PPAY-.YYYY.-.#### | **Yes** | Payment record with ERPNext integration |
| 8 | Parking Fee Structure | PFS-.YYYY.-.#### | No | Fee rates per zone and vehicle type |
| 9 | Parking Fee Entry | PFE-.YYYY.-.#### | No | Calculated fee for a vehicle entry |
| 10 | Parking Incident | PINC-.YYYY.-.#### | No | Incident tracking (damage, theft, etc.) |
| 11 | Parking Alert | PAL-.YYYY.-.#### | No | System and operational alerts |
| 12 | Parking Staff | PSTF-.YYYY.-.#### | No | Staff members with roles and zones |
| 13 | Parking Shift | PSHF-.YYYY.-.#### | No | Staff shift scheduling |
| 14 | Smart Parking Settings | (Single) | No | Global app configuration |

---

## Custom Roles

| Role | Access Level |
|------|-------------|
| Parking Manager | Full CRUD + submit/cancel/amend/delete on all doctypes |
| Parking Supervisor | Read/write/create/submit/cancel on most doctypes |
| Parking Attendant | Read/write/create/submit on entries and payments |
| Customer | Portal access for reservations and vehicle management |

---

## Installation

```bash
# 1. Get the app
bench get-app smart_parking https://github.com/Sudhakar1110/parking.git

# 2. Install on your ERPNext site
bench --site your-site.local install-app smart_parking

# 3. Run migrations
bench --site your-site.local migrate

# 4. Restart and clear cache
bench restart
bench --site your-site.local clear-cache
```

---

## Demo Data

```bash
bench --site your-site.local execute smart_parking.smart_parking.create_demo_data.execute
```

Creates: 8 slot types, 6 zones, 540+ slots, 15 customers, 15 vehicles, 8 staff, 3 shifts, 9 vehicle entries, 5 reservations, 6 fee entries, 5 payments, 5 incidents, 5 alerts, and settings.

---

## Scheduled Tasks

| Task | Frequency | Purpose |
|------|-----------|---------|
| check_slot_occupancy_alerts | Daily | Alerts when zone occupancy exceeds threshold (default 90%) |
| check_reservation_expiry | Daily | Expires reservations past end_time, releases slots |
| check_overdue_vehicles | Daily | Alerts for vehicles parked longer than threshold (default 24h) |
| update_slot_availability | Hourly | Syncs zone slot counts from actual slot data |
| generate_daily_occupancy_summary | Daily | Creates occupancy summary alert for all zones |
| generate_weekly_revenue_report | Weekly | Emails revenue summary by zone to Parking Manager |

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `check_availability` | Check slot availability across zones |
| `book_slot` | Book a parking reservation |
| `get_parking_dashboard_data` | Get dashboard summary data |
| `process_exit` | Process vehicle exit with fee calculation |
| `get_slot_details` | Get detailed info for a specific slot |

---

## Reports

| Report | Description |
|--------|-------------|
| Revenue Report | Revenue by zone with paid/pending breakdown |
| Slot Occupancy Report | Occupancy percentages across all zones |
| Vehicle Entry Register | Detailed vehicle entry/exit log |

---

## Module Structure

```
smart_parking/
  doctype/              # 14 DocTypes with Python controllers and JS
  utils/                # Event handlers (entry/exit, billing, reservations, permissions, jinja)
  setup/                # Module migration utilities
  config/               # Desktop and docs config
  templates/pages/      # Customer portal pages (4 pages)
  report/               # 3 query reports
  notification/         # 4 notification rules
  email_template/       # 2 email templates
  workflow/             # 1 reservation approval workflow (inactive)
  dashboard_chart/      # 4 dashboard charts
  number_card/          # 5 number cards
  workspace/            # 1 workspace (Smart Parking)
  print_format/         # 1 print format (Parking Receipt)
  public/               # Global JS and CSS
```

---

## Tech Stack

- **Framework:** Frappe v15
- **ERP:** ERPNext v15
- **Database:** MariaDB
- **Python:** 3.11+
- **Frontend:** Frappe Desk + Web Portal

---

## License

MIT License — Copyright (c) 2026 Sudhakar
