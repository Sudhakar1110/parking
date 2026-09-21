# Smart Parking Management System (SPMS)
# Standard Operating Procedure (SOP)

**Version:** 1.0.0
**Platform:** Frappe v15 / ERPNext v15
**Date:** September 2026
**Prepared by:** Sudhakar

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Installation & Setup](#2-installation--setup)
3. [Initial Configuration](#3-initial-configuration)
4. [Zone Management](#4-zone-management)
5. [Slot Management](#5-slot-management)
6. [Vehicle Registration](#6-vehicle-registration)
7. [Vehicle Entry/Exit Operations](#7-vehicle-entryexit-operations)
8. [Reservation Management](#8-reservation-management)
9. [Fee & Billing Operations](#9-fee--billing-operations)
10. [Payment Processing](#10-payment-processing)
11. [Staff & Shift Management](#11-staff--shift-management)
12. [Incident Management](#12-incident-management)
13. [Alert Management](#13-alert-management)
14. [Reports & Analytics](#14-reports--analytics)
15. [Customer Portal](#15-customer-portal)
16. [Settings & Configuration](#16-settings--configuration)
17. [Automated Tasks & Scheduler](#17-automated-tasks--scheduler)
18. [API Integration](#18-api-integration)
19. [Troubleshooting](#19-troubleshooting)
20. [Role-Based Access Control](#20-role-based-access-control)

---

## 1. System Overview

### 1.1 What is SPMS?

The Smart Parking Management System (SPMS) is a comprehensive parking facility management solution built on the Frappe framework and ERPNext. It handles:

- Multi-zone parking facility management
- Real-time slot availability tracking
- Vehicle entry/exit with automatic fee calculation
- Advance reservation booking
- Payment collection and ERPNext integration
- Staff scheduling and shift management
- Incident tracking and alert system
- Customer-facing web portal

### 1.2 Architecture

```
Frappe v15 + ERPNext v15
    |
    +-- Smart Parking App (14 DocTypes)
    |       |
    |       +-- Parking Zone -> Parking Slot -> Parking Slot Type
    |       +-- Vehicle -> Vehicle Entry -> Parking Fee Entry -> Parking Payment
    |       +-- Parking Reservation (links Vehicle + Zone + Slot)
    |       +-- Parking Staff -> Parking Shift
    |       +-- Parking Incident, Parking Alert
    |       +-- Parking Fee Structure
    |       +-- Smart Parking Settings (Singleton)
    |
    +-- Automated Tasks (Daily/Hourly/Weekly)
    +-- Reports & Dashboard Charts
    +-- Customer Web Portal
    +-- Email Notifications
    +-- REST API Endpoints
```

### 1.3 User Roles

| Role | Description | Key Responsibilities |
|------|-------------|---------------------|
| **Parking Manager** | Full system access | Zone config, billing, staff, reports, settings |
| **Parking Supervisor** | Operational oversight | Zone monitoring, shift approval, incident review |
| **Parking Attendant** | Front-line operations | Vehicle entry/exit, payment collection |
| **Customer** | Portal user | Check availability, book reservations, view vehicles |

---

## 2. Installation & Setup

### 2.1 Prerequisites

- Frappe Bench v15 installed and configured
- ERPNext v15 installed on the same bench
- MariaDB 10.6+ running
- Python 3.11+
- Redis for caching

### 2.2 Installation Steps

```bash
# Step 1: Get the app from GitHub
bench get-app smart_parking https://github.com/Sudhakar1110/parking.git

# Step 2: Install on your site
bench --site <site-name> install-app smart_parking

# Step 3: Run database migrations
bench --site <site-name> migrate

# Step 4: Build assets
bench build

# Step 5: Restart bench
bench restart

# Step 6: Clear cache
bench --site <site-name> clear-cache
```

### 2.3 Verify Installation

1. Log in to Frappe Desk as Administrator
2. Navigate to the **Smart Parking** workspace
3. Confirm all 14 DocTypes are visible in the sidebar
4. Check that custom roles (Parking Manager, Parking Attendant, Parking Supervisor) exist in Role settings

### 2.4 Load Demo Data (Optional)

```bash
bench --site <site-name> execute smart_parking.smart_parking.create_demo_data.execute
```

This creates sample data for testing:
- 8 slot types, 6 parking zones, 540+ slots
- 15 customers, 15 vehicles, 8 staff members
- Vehicle entries, reservations, payments, incidents, alerts
- Smart Parking Settings with defaults

---

## 3. Initial Configuration

### 3.1 Smart Parking Settings

Navigate to: **Smart Parking > Smart Parking Settings**

| Setting | Default | Description |
|---------|---------|-------------|
| Company | — | Link to ERPNext Company |
| Default Currency | — | Currency for all fee calculations |
| Overdue Threshold (Hours) | 24 | Hours after which a parked vehicle is flagged overdue |
| Auto Release Expired Reservations | Yes | Automatically release slots for expired reservations |
| Send Occupancy Alerts | Yes | Email alerts when zone occupancy exceeds threshold |
| Occupancy Alert Threshold (%) | 90 | Percentage at which occupancy alert triggers |
| Send Reservation Expiry Reminders | Yes | Notify customers before reservation expires |
| Send Overdue Vehicle Alerts | Yes | Alert when vehicles exceed overdue threshold |
| Auto Create Sales Invoice | No | Auto-create ERPNext Sales Invoice on payment |
| Auto Create Customer | No | Auto-create ERPNext Customer for new vehicle owners |

### 3.2 Role Assignment

Assign parking roles to users:

1. Go to **User** > select a user
2. In the **Role Profile** or **Roles** section, add:
   - **Parking Manager** — for administrators and zone managers
   - **Parking Supervisor** — for floor supervisors
   - **Parking Attendant** — for front-desk staff
   - **Customer** — for portal access (assigned automatically)

### 3.3 Email Configuration

Ensure the following email templates are set up:
- **Reservation Confirmation** — Sent when a reservation is confirmed
- **Parking Payment Receipt** — Sent when payment is received

---

## 4. Zone Management

### 4.1 Creating a Parking Zone

Navigate to: **Smart Parking > Parking Zone > New**

**Required Fields:**
1. **Zone Name** — Unique name (e.g., "City Center Plaza Parking")
2. **Zone Code** — Short code (e.g., "CCP")
3. **Zone Type** — Select: Outdoor / Covered / Multi-Story / Basement / Valet

**Optional Fields:**
- Address, City, State, Pincode
- Max Duration Hours (default: 24)
- Operating Hours (start/end time)
- Alert Threshold (% occupancy for alerts)
- Fee Structure (link to Parking Fee Structure)
- Description

**Steps:**
1. Click **New** to create a Parking Zone
2. Enter Zone Name and Zone Code
3. Select Zone Type
4. Set address details
5. Configure operating hours and max duration
6. Click **Save**

### 4.2 Zone Occupancy Tracking

The system automatically tracks:
- **Total Slots** — Count of all slots in the zone
- **Occupied Slots** — Count of currently occupied slots
- **Reserved Slots** — Count of reserved slots
- **Available Slots** — Total minus occupied minus reserved
- **Occupancy Percentage** — (Occupied + Reserved) / Total * 100

These values update automatically when:
- A vehicle entry is submitted (occupied increases)
- A vehicle entry is cancelled (occupied decreases)
- A reservation is submitted (reserved increases)
- A reservation is cancelled (reserved decreases)
- A slot is added or removed from the zone

### 4.3 Deactivating a Zone

1. Open the Parking Zone
2. Uncheck **Is Active**
3. Save

Active zones are used for vehicle entries and reservations. Inactive zones are excluded from availability checks.

---

## 5. Slot Management

### 5.1 Creating Slot Types

Navigate to: **Smart Parking > Parking Slot Type > New**

**Pre-configured types:**

| Type Name | Code | Features |
|-----------|------|----------|
| Standard Car | SC | Regular car slot |
| Compact Car | CC | Smaller dimensions |
| SUV / Large Vehicle | SV | Larger dimensions |
| Motorcycle | MC | Two-wheeler slot |
| EV Charging | EC | Has EV charger |
| Handicap Accessible | HA | Wheelchair accessible |
| Covered Standard | CS | Covered/roofed |
| Bus / Heavy Vehicle | BH | Large vehicle slot |

**Creating a new Slot Type:**
1. Enter Type Name (required, unique)
2. Enter Type Code (unique)
3. Set dimensions: Length, Width, Height (cm)
4. Check features: Has EV Charger, Is Accessible, Is Covered
5. Set rates: Hourly Rate, Daily Rate
6. Click **Save**

### 5.2 Creating Parking Slots

Navigate to: **Smart Parking > Parking Slot > New**

**Required Fields:**
1. **Slot Number** — e.g., "G-001" (Ground Floor, Slot 1)
2. **Zone** — Link to Parking Zone
3. **Slot Type** — Link to Parking Slot Type

**Steps:**
1. Click **New**
2. Enter Slot Number following a naming convention:
   - Ground Floor: G-001, G-002, ...
   - First Floor: 1-001, 1-002, ...
   - Basement: B1-001, B1-002, ...
3. Select the Zone
4. Select the Slot Type
5. Enter Floor/Level (optional)
6. Click **Save**

**Slot Status Values:**
| Status | Meaning |
|--------|---------|
| Available | Slot is free and can accept vehicles |
| Occupied | A vehicle is currently parked in this slot |
| Reserved | A reservation holds this slot |
| Maintenance | Slot is under maintenance, not available |

Status is managed automatically by the system. Manual changes are not recommended.

### 5.3 Bulk Slot Creation

For large parking facilities, create slots in bulk:

```bash
bench --site <site-name> execute "
import frappe
for i in range(1, 51):  # Create 50 slots
    doc = frappe.get_doc({
        'doctype': 'Parking Slot',
        'slot_number': f'G-{i:03d}',
        'zone': 'PZ-2026-0001',
        'slot_type': 'Standard Car',
        'floor': 'Ground'
    })
    doc.insert(ignore_permissions=True)
frappe.db.commit()
print('50 slots created')
"
```

---

## 6. Vehicle Registration

### 6.1 Registering a Vehicle

Navigate to: **Smart Parking > Vehicle > New**

**Required Fields:**
1. **License Plate** — Vehicle registration number (unique)
2. **Vehicle Type** — Car / SUV / Truck / Motorcycle / Van / Bus / Electric Car / Electric Motorcycle / Bicycle / Other

**Steps:**
1. Click **New**
2. Enter License Plate (e.g., "TS09AA1234")
3. Select Vehicle Type
4. Enter Make (brand), Model, Color
5. Enter Year of Manufacture
6. Enter Owner Name, Phone (+country code), Email
7. Click **Save**

### 6.2 Vehicle Entry via API

```python
import frappe
result = frappe.get_attr("smart_parking.api.book_slot")(
    zone="PZ-2026-0001",
    slot="PS-2026-00001",
    vehicle="VEH-2026-0001",
    start_time="2026-09-21 10:00:00",
    end_time="2026-09-21 14:00:00",
    customer="CUST-2026-0001"
)
```

---

## 7. Vehicle Entry/Exit Operations

### 7.1 Recording Vehicle Entry

Navigate to: **Smart Parking > Vehicle Entry > New**

**Required Fields:**
1. **Vehicle** — Link to registered Vehicle
2. **Zone** — Link to Parking Zone
3. **Entry Time** — Auto-set to current time

**Optional Fields:**
- **Slot** — Specific parking slot
- **Purpose** — General / Visitor / Delivery / Employee / Contractor / Event
- **Remarks** — Additional notes

**Steps:**
1. Click **New**
2. Select the Vehicle (auto-fills license plate, type, color)
3. Select the Zone
4. Optionally select a specific Slot
5. Entry Time defaults to now
6. Select Purpose
7. Click **Save**, then **Submit**

**On Submit:**
- Slot status changes to "Occupied"
- Zone occupied slot count increases
- Fee entry is created if a matching Fee Structure exists

### 7.2 Recording Vehicle Exit

**Steps:**
1. Open the Vehicle Entry document
2. Set the **Exit Time**
3. The system auto-calculates **Duration (Hours)** and **Parking Fee**
4. Click **Submit** (or Save if amending)

**On Submit with Exit Time:**
- Slot status changes to "Available"
- Zone occupied slot count decreases
- Parking Fee is finalized

### 7.3 Cancelling a Vehicle Entry

1. Open the submitted Vehicle Entry
2. Click **Cancel**
3. The slot is released and zone counts are updated

### 7.4 Fee Calculation Logic

The system calculates fees based on the Fee Structure:

| Duration | Calculation |
|----------|-------------|
| Up to 1 hour | Hourly rate |
| 1-24 hours | min(hourly rate x hours, daily rate) |
| 1-7 days | min(hourly x hours, daily x days, weekly rate) |
| 7+ days | Monthly rate or weekly + hourly combination |

Grace period (default 15 minutes) is applied before charges begin.

---

## 8. Reservation Management

### 8.1 Creating a Reservation

Navigate to: **Smart Parking > Parking Reservation > New**

**Required Fields:**
1. **Customer** — Link to ERPNext Customer
2. **Vehicle** — Link to Vehicle
3. **Vehicle Type** — Car / SUV / etc.
4. **Zone** — Parking Zone
5. **Slot** — Parking Slot (filtered to Available slots in selected zone)
6. **Start Time** — Reservation start datetime
7. **End Time** — Reservation end datetime

**Steps:**
1. Click **New**
2. Select Customer
3. Select Vehicle
4. Select Zone (slot dropdown filters to Available slots only)
5. Select Slot
6. Set Start Time and End Time
7. System auto-calculates Duration (Hours) and Reservation Fee
8. Click **Save**, then **Submit**

**On Submit:**
- Status changes to "Confirmed"
- Slot status changes to "Reserved"
- Slot shows reserved_by and reservation link

### 8.2 Reservation Validation

The system validates:
- No overlapping confirmed reservations for the same slot
- Slot must be Available (not Occupied or Reserved)
- End Time must be after Start Time
- Duration and fee are auto-calculated from Fee Structure

### 8.3 Cancelling a Reservation

1. Open the submitted Reservation
2. Click **Cancel**
3. Status changes to "Cancelled"
4. Slot is released (status returns to "Available")

### 8.4 Reservation Status Flow

```
Draft -> Submit -> Confirmed -> Complete -> Completed
  |                                      |
  +-> Cancel -> Cancelled                +-> Expired (auto by scheduler)
```

---

## 9. Fee & Billing Operations

### 9.1 Fee Structure Setup

Navigate to: **Smart Parking > Parking Fee Structure > New**

**Required Fields:**
1. **Fee Name** — Descriptive name (e.g., "City Center Plaza - Car")
2. **Zone** — Parking Zone
3. **Vehicle Type** — Car / SUV / Motorcycle / etc.

**Rate Fields:**
| Field | Description |
|-------|-------------|
| Hourly Rate | Charge per hour |
| Daily Rate | Charge per 24 hours |
| Weekly Rate | Charge per 7 days |
| Monthly Rate | Charge per 30 days |
| Minimum Charge | Minimum fee regardless of duration |
| Grace Period (minutes) | Free period before charges apply (default: 15) |
| Max Daily Charge | Cap on daily charges |

**Steps:**
1. Click **New**
2. Enter Fee Name
3. Select Zone and Vehicle Type
4. Set hourly, daily, weekly, and monthly rates
5. Set grace period and max daily charge
6. Check **Is Active**
7. Click **Save**

### 9.2 Fee Entry

Fee entries are created automatically when a Vehicle Entry is submitted and a matching Fee Structure exists. They can also be created manually:

Navigate to: **Smart Parking > Parking Fee Entry > New**

**Fields:**
- Vehicle Entry (link)
- Vehicle (link)
- Zone (link)
- Fee Structure (link)
- Fee Amount (calculated or manual)
- Fee Status: Pending / Paid / Waived / Overdue / Cancelled

---

## 10. Payment Processing

### 10.1 Recording a Payment

Navigate to: **Smart Parking > Parking Payment > New**

**Required Fields:**
1. **Amount Paid** — Payment amount
2. **Payment Date** — Defaults to today

**Steps:**
1. Click **New**
2. Link to Fee Entry and/or Vehicle Entry
3. Select Vehicle and Zone
4. Enter Amount Paid
5. Select Payment Method: Cash / Card / UPI / Online Transfer / Wallet / Other
6. Enter Reference Number (for non-cash payments)
7. Optionally enter Customer details
8. Check **Create Sales Invoice** to auto-create ERPNext Sales Invoice
9. Click **Save**, then **Submit**

**On Submit:**
- Linked Fee Entry status changes to "Paid"
- Linked Vehicle Entry fee_status changes to "Paid"
- If "Create Sales Invoice" is checked, an ERPNext Sales Invoice is created

### 10.2 ERPNext Integration

When **Create Sales Invoice** is checked on submit:
1. System resolves Customer from Vehicle owner or manual entry
2. Creates an ERPNext Sales Invoice with the parking fee as a line item
3. Submits the Sales Invoice

---

## 11. Staff & Shift Management

### 11.1 Registering Staff

Navigate to: **Smart Parking > Parking Staff > New**

**Required Fields:**
1. **Staff Name** — Full name
2. **Staff Type** — Attendant / Supervisor / Manager / Security / Maintenance / Technician

**Steps:**
1. Click **New**
2. Enter Staff Name
3. Link to ERPNext Employee (optional)
4. Link to Frappe User (optional, for login access)
5. Enter Phone and Email
6. Select Staff Type
7. Assign to Zone
8. Check **Is Active**
9. Click **Save**

### 11.2 Creating Shifts

Navigate to: **Smart Parking > Parking Shift > New**

**Required Fields:**
1. **Staff Member** — Link to Parking Staff
2. **Zone** — Parking Zone
3. **Shift Date** — Date of the shift
4. **Shift Start** — Start datetime
5. **Shift End** — End datetime

**Steps:**
1. Click **New**
2. Select Staff Member
3. Select Zone
4. Set Shift Date
5. Set Shift Start and End times
6. System auto-calculates Duration (Hours)
7. Click **Save**

**Validation:** The system prevents overlapping shifts for the same staff member.

**Shift Status Flow:** Draft -> Scheduled -> In Progress -> Completed / Cancelled

---

## 12. Incident Management

### 12.1 Reporting an Incident

Navigate to: **Smart Parking > Parking Incident > New**

**Required Fields:**
1. **Incident Type** — Damage / Accident / Theft / Vandalism / Breakdown / Unauthorized Parking / Noise Complaint / Other
2. **Severity** — Low / Medium / High / Critical
3. **Zone** — Parking Zone
4. **Description** — Detailed description

**Steps:**
1. Click **New**
2. Select Incident Type
3. Select Severity
4. Select Zone and optionally Slot/Vehicle
5. Enter Description
6. Set Reported Date (defaults to now)
7. Click **Save**

### 12.2 Resolving an Incident

1. Open the Incident
2. Change Status to "In Progress" or "Resolved"
3. Enter Resolution details
4. Set Resolved By and Resolved Date
5. Save

---

## 13. Alert Management

### 13.1 Alert Types

| Type | Description | Auto-generated? |
|------|-------------|:---------------:|
| Overstay | Vehicle exceeded max parking duration | Yes |
| Equipment Failure | Equipment malfunction reported | No |
| Security | Security concern | No |
| Maintenance | Maintenance needed | No |
| Slot Violation | Wrong vehicle type in designated slot | No |
| Unauthorized Entry | Unauthorized access detected | Yes (scheduler) |

### 13.2 Alert Priority Levels

| Priority | Description |
|----------|-------------|
| Low | Minor issue, no immediate action needed |
| Medium | Needs attention within 24 hours |
| High | Needs immediate attention |
| Critical | Emergency, requires immediate action |

### 13.3 Alert Status Flow

```
Open -> In Progress -> Resolved
  |                    |
  +-> Dismissed        +-> Closed
```

---

## 14. Reports & Analytics

### 14.1 Available Reports

**Revenue Report:**
- Navigate to: Smart Parking > Reports > Revenue Report
- Filters: Parking Zone, From Date, To Date
- Shows: Total entries, revenue, paid/pending amounts by zone

**Slot Occupancy Report:**
- Navigate to: Smart Parking > Reports > Slot Occupancy Report
- Filters: Parking Zone, Zone Type
- Shows: Slot counts and occupancy percentages by zone

**Vehicle Entry Register:**
- Navigate to: Smart Parking > Reports > Vehicle Entry Register
- Filters: Parking Zone, Date Range, Vehicle Type
- Shows: Detailed entry/exit log with fees and durations

### 14.2 Dashboard Charts

| Chart | Type | Description |
|-------|------|-------------|
| Daily Occupancy Trend | Line | Occupancy over time |
| Monthly Revenue Trend | Line | Revenue trend over months |
| Revenue by Zone | Bar | Revenue comparison across zones |
| Vehicle Type Distribution | Donut | Distribution of vehicle types |

### 14.3 Number Cards

| Card | Metric |
|------|--------|
| Available Slots | Total available slots across active zones |
| Occupied Slots | Total occupied slots |
| Today Revenue | Total payments received today |
| Today Vehicle Entries | Number of vehicle entries today |
| Active Reservations | Number of confirmed reservations |

---

## 15. Customer Portal

### 15.1 Portal Pages

| Page | URL | Description |
|------|-----|-------------|
| Parking Portal | /parking-portal/ | Main portal with zone overview |
| Check Availability | /parking-portal/availability | Real-time slot availability |
| My Reservations | /parking-portal/my-reservations | Customer's reservations |
| My Vehicles | /parking-portal/my-vehicles | Customer's registered vehicles |

### 15.2 Accessing the Portal

1. Navigate to `https://<your-site>/parking-portal/`
2. Log in with your Frappe credentials
3. Browse zones and check availability
4. Create reservations directly from the portal

---

## 16. Settings & Configuration

### 16.1 Global Settings

Navigate to: **Smart Parking > Smart Parking Settings**

| Setting | Recommended Value | Description |
|---------|-------------------|-------------|
| Overdue Threshold | 24 hours | Time limit for parking |
| Occupancy Alert Threshold | 90% | When to trigger high-occupancy alerts |
| Auto Release Expired Reservations | Enabled | Automatically free expired slots |
| Send Occupancy Alerts | Enabled | Email notifications for high occupancy |
| Send Reservation Expiry Reminders | Enabled | Notify customers before expiry |
| Send Overdue Vehicle Alerts | Enabled | Alert for overstaying vehicles |

### 16.2 ERPNext Integration Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Auto Create Sales Invoice | Disabled | Enable to auto-create invoices on payment |
| Auto Create Customer | Disabled | Enable to auto-create customers for new vehicles |
| Default Customer Group | — | Group for auto-created customers |

---

## 17. Automated Tasks & Scheduler

### 17.1 Scheduler Configuration

The app uses Frappe's built-in scheduler. Ensure the scheduler is enabled:

```bash
bench --site <site-name> enable-scheduler
```

### 17.2 Task Schedule

| Task | Schedule | What It Does |
|------|----------|--------------|
| `check_slot_occupancy_alerts` | Daily | Checks zone occupancy vs threshold; creates alerts |
| `check_reservation_expiry` | Daily | Expires overdue reservations; releases slots |
| `check_overdue_vehicles` | Daily | Flags vehicles parked beyond threshold |
| `update_slot_availability` | Hourly | Syncs zone slot counts |
| `generate_daily_occupancy_summary` | Daily | Creates daily occupancy summary alert |
| `generate_weekly_revenue_report` | Weekly | Emails weekly revenue summary |

### 17.3 Manual Task Execution

```bash
# Run a specific task
bench --site <site-name> execute smart_parking.tasks.check_slot_occupancy_alerts

# Check scheduler status
bench --site <site-name> scheduler status
```

---

## 18. API Integration

### 18.1 Available API Endpoints

**Check Availability:**
```
POST /api/method/smart_parking.api.check_availability
Parameters: zone (optional), date (optional), vehicle_type (optional)
Returns: Zone availability summary with slot counts
```

**Book Slot:**
```
POST /api/method/smart_parking.api.book_slot
Parameters: zone, slot, vehicle, start_time, end_time, customer
Returns: Reservation ID and calculated fee
```

**Get Dashboard Data:**
```
POST /api/method/smart_parking.api.get_parking_dashboard_data
Returns: Zones with occupancy, today's revenue, entries, reservations
```

**Process Exit:**
```
POST /api/method/smart_parking.api.process_exit
Parameters: vehicle_entry
Returns: Updated entry with calculated fee
```

**Get Slot Details:**
```
POST /api/method/smart_parking.api.get_slot_details
Parameters: slot
Returns: Full slot details including status and current vehicle
```

### 18.2 API Authentication

All API endpoints require authentication. Use Frappe's API key or session-based auth:

```bash
# Using API key
curl -X POST "https://<site>/api/method/smart_parking.api.check_availability" \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json"
```

---

## 19. Troubleshooting

### 19.1 Common Issues

**Issue: "Cannot create Parking Zone"**
- Cause: Naming series conflict or workspace name collision
- Solution: Ensure `naming_rule` is set to `By "naming_series" field` in doctype JSON. Run `bench migrate`.

**Issue: "Slot is already reserved" when submitting reservation**
- Cause: Duplicate validation in hook and controller
- Solution: Ensure hooks.py does not have Parking Reservation events (controller handles it). Run `bench restart`.

**Issue: Phone number validation error**
- Cause: Frappe v15 requires country code in phone numbers
- Solution: Use format "+91 XXXXXXXXXX" for Indian numbers.

**Issue: Customer Group validation error**
- Cause: ERPNext requires non-group Customer Group
- Solution: Use `frappe.db.get_value("Customer Group", {"is_group": 0}, "name")` to get valid group.

**Issue: `add_hours` import error**
- Cause: `add_hours` was removed in Frappe v15
- Solution: Use `add_to_date(date, hours=N)` instead.

**Issue: Old code errors after git pull**
- Cause: Python bytecode cache
- Solution: Always run `bench restart` after pulling code changes.

### 19.2 Cache Management

```bash
# Clear all caches
bench --site <site-name> clear-cache

# Clear website cache
bench --site <site-name> clear-website-cache

# Rebuild assets
bench build

# Full restart
bench restart
```

### 19.3 Database Reset (Development Only)

```bash
# Reset all parking slots to Available
bench --site <site-name> execute "
import frappe
frappe.db.sql(\"UPDATE tab\`Parking Slot\` SET status='Available', is_occupied=0, is_reserved=0\")
frappe.db.commit()
print('All slots reset')
"
```

---

## 20. Role-Based Access Control

### 20.1 Permissions Matrix

| DocType | Parking Manager | Parking Supervisor | Parking Attendant |
|---------|:---:|:---:|:---:|
| Parking Zone | Full CRUD | R/W/C/Report | Read |
| Parking Slot | Full CRUD | R/W/C/Report | R/W |
| Parking Slot Type | Full CRUD | R/W/C/Report | — |
| Vehicle | Full CRUD | R/W/C/Report | R/W/C/Report |
| Vehicle Entry | Full CRUD+Submit | R/W/C/Submit | R/W/C/Submit |
| Parking Reservation | Full CRUD+Submit | R/W/C/Submit | R/W/C/Submit |
| Parking Payment | Full CRUD+Submit | R/W/C/Submit | R/W/C/Submit |
| Parking Fee Structure | Full CRUD | R/W/C/Report | — |
| Parking Fee Entry | Full CRUD | R/W/C/Report | R/W/C/Report |
| Parking Incident | Full CRUD | R/W/C/Delete/Report | R/W/C/Report |
| Parking Alert | Full CRUD | R/W/C/Report | R/W/C/Report |
| Parking Staff | Full CRUD | R/W/C/Report | — |
| Parking Shift | Full CRUD | R/W/C/Report | R/W/C/Report |
| Smart Parking Settings | R/W | — | — |

**Legend:** Full = Read+Write+Create+Delete, R/W = Read+Write, C = Create

### 20.2 Configuring Access

1. Go to **User** > select user
2. Under **Role Profile**, assign appropriate parking role
3. Or under **Roles** tab, check individual roles
4. Save and test access

---

## Appendix A: Naming Series Reference

| DocType | Pattern | Example |
|---------|---------|---------|
| Parking Zone | PZ-.YYYY.-.#### | PZ-2026-0001 |
| Parking Slot | PS-.YYYY.-.##### | PS-2026-00001 |
| Parking Slot Type | (by type_name) | Standard Car |
| Vehicle | VEH-.YYYY.-.#### | VEH-2026-0001 |
| Vehicle Entry | VE-.YYYY.MM.DD.-.##### | VE-20260921-00001 |
| Parking Reservation | PRES-.YYYY.-.#### | PRES-2026-0001 |
| Parking Payment | PPAY-.YYYY.-.#### | PPAY-2026-0001 |
| Parking Fee Structure | PFS-.YYYY.-.#### | PFS-2026-0001 |
| Parking Fee Entry | PFE-.YYYY.-.#### | PFE-2026-0001 |
| Parking Incident | PINC-.YYYY.-.#### | PINC-2026-0001 |
| Parking Alert | PAL-.YYYY.-.#### | PAL-2026-0001 |
| Parking Staff | PSTF-.YYYY.-.#### | PSTF-2026-0001 |
| Parking Shift | PSHF-.YYYY.-.#### | PSHF-2026-0001 |

---

## Appendix B: Database Schema Relationships

```
Parking Zone (1) ----< (N) Parking Slot
Parking Zone (1) ----< (N) Vehicle Entry
Parking Zone (1) ----< (N) Parking Reservation
Parking Zone (1) ----< (N) Parking Fee Structure
Parking Zone (1) ----< (N) Parking Staff
Parking Zone (1) ----< (N) Parking Incident
Parking Zone (1) ----< (N) Parking Alert

Parking Slot Type (1) ----< (N) Parking Slot

Vehicle (1) ----< (N) Vehicle Entry
Vehicle (1) ----< (N) Parking Reservation

Vehicle Entry (1) ----< (N) Parking Fee Entry
Vehicle Entry (1) ----< (N) Parking Payment
Vehicle Entry (1) ---- (N) Parking Slot

Parking Fee Structure (1) ----< (N) Parking Fee Entry

Parking Fee Entry (1) ----< (N) Parking Payment

Parking Staff (1) ----< (N) Parking Shift
```

---

## Appendix C: Email Templates

### Reservation Confirmation
- **Subject:** Reservation Confirmed - {{ doc.name }}
- **Body:** Includes customer name, vehicle, zone, slot, start/end times, and fee

### Parking Payment Receipt
- **Subject:** Parking Payment Receipt - {{ doc.name }}
- **Body:** Includes payment details, vehicle, zone, amount, and payment method

---

## Appendix D: Print Format

### Parking Receipt
- Header: "SMART PARKING" branding
- Receipt number, date, vehicle details
- Zone, slot, duration, amount paid
- Payment method and reference number
- Footer: "Thank you for parking with us!"

---

*End of SOP Document*
