# Smart Parking Management System (SPMS) — Frappe App

[![Frappe](https://img.shields.io/badge/Frappe-v15-blue)](https://frappe.io)
[![ERPNext](https://img.shields.io/badge/ERPNext-v15-green)](https://erpnext.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A production-ready **custom Frappe app** built on ERPNext v15+ for comprehensive parking management.

## Features

- Zone & Slot Management with real-time occupancy tracking
- Vehicle Entry/Exit with automatic fee calculation
- Reservation system with overlap detection
- Fee structures (hourly/daily/weekly/monthly)
- Payment processing with ERPNext Sales Invoice integration
- Staff & Shift management
- Incident & Alert tracking
- Customer web portal
- Automated scheduler tasks
- Dashboard charts, number cards, and reports

## DocTypes (14)

| DocType | Naming | Submittable |
|---------|--------|:-----------:|
| Parking Zone | PZ-.YYYY.-.#### | No |
| Parking Slot | PS-.YYYY.-.##### | No |
| Parking Slot Type | (by type_name) | No |
| Vehicle | VEH-.YYYY.-.#### | No |
| Vehicle Entry | VE-.YYYY.MM.DD.-.##### | Yes |
| Parking Reservation | PRES-.YYYY.-.#### | Yes |
| Parking Payment | PPAY-.YYYY.-.#### | Yes |
| Parking Fee Structure | PFS-.YYYY.-.#### | No |
| Parking Fee Entry | PFE-.YYYY.-.#### | No |
| Parking Incident | PINC-.YYYY.-.#### | No |
| Parking Alert | PAL-.YYYY.-.#### | No |
| Parking Staff | PSTF-.YYYY.-.#### | No |
| Parking Shift | PSHF-.YYYY.-.#### | No |
| Smart Parking Settings | (Single) | No |

## Installation

```bash
bench get-app smart_parking https://github.com/Sudhakar1110/parking.git
bench --site <site-name> install-app smart_parking
bench --site <site-name> migrate
bench restart
```

## Demo Data

```bash
bench --site <site-name> execute smart_parking.smart_parking.create_demo_data.execute
```## Custom Roles

- **Parking Manager** — Full CRUD on all doctypes
- **Parking Supervisor** — Read/write/create/submit
- **Parking Attendant** — Read/write/create on entries/payments
- **Customer** — Portal access

## Planned Features (Roadmap)

### Payments & Billing
- Online payment gateway integration (Razorpay / Stripe / PayPal)
- Monthly passes / subscriptions for regular parkers
- Wallet / prepaid balance per customer
- Discount & promo code support
- Tax configuration (GST/VAT) on parking fees
- Refund & cancellation charge workflow
- Late fee / penalty for overstays

### Hardware & IoT
- ANPR / license plate camera recognition for automatic entry/exit
- RFID / NFC tag-based access
- Boom barrier / gate control integration
- IoT slot occupancy sensors (ultrasonic / camera) for real-time slot status
- LED display board integration (available slot counts)
- QR-code tickets for self check-in/check-out

### Customer Experience
- Prepayment at reservation booking
- Extend / modify reservation from the portal
- Slot map / floor-plan navigation view
- Push / SMS / WhatsApp notifications
- Guest booking without account registration
- Multi-language portal support

### Operations
- Auto slot assignment (nearest / first-available)
- EV charging session tracking & electricity billing
- Slot maintenance scheduling (preventive maintenance calendar)
- Vehicle blacklist/whitelist with auto-alert on entry
- Multi-facility / multi-site support
- Valet management workflow

### Analytics & Reporting
- Peak-hour analysis / occupancy heatmap
- Demand forecasting for capacity planning
- Revenue export (Excel/PDF) and scheduled report delivery
- Repeat-customer / revenue-per-customer analytics

## License
MIT License — Copyright (c) 2026 Sudhakar
