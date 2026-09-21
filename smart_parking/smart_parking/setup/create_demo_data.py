import frappe
from frappe.utils import nowdate, add_days, add_hours, today, now_datetime, cint
import random


def execute():
    """Create demo data for Smart Parking app.
    Run: bench --site <site> execute smart_parking.setup.create_demo_data
    """
    frappe.only_for("System Manager")

    print("Creating demo data for Smart Parking...")

    create_slot_types()
    create_zones()
    create_fee_structures()
    update_zone_fee_links()
    create_slots()
    create_vehicles()
    create_staff()
    create_shifts()
    create_vehicle_entries()
    create_reservations()
    create_fee_entries()
    create_payments()
    create_incidents()
    create_alerts()
    create_settings()

    frappe.db.commit()
    print("Demo data creation complete!")


def create_slot_types():
    slot_types = [
        {
            "type_name": "Standard Car",
            "type_code": "SC",
            "description": "Standard parking space for regular cars",
            "length_cm": 500,
            "width_cm": 250,
            "height_cm": 200,
            "max_vehicle_length_cm": 480,
            "hourly_rate": 3.00,
            "daily_rate": 20.00,
        },
        {
            "type_name": "Compact Car",
            "type_code": "CC",
            "description": "Smaller space for compact and hatchback cars",
            "length_cm": 420,
            "width_cm": 220,
            "height_cm": 200,
            "max_vehicle_length_cm": 400,
            "hourly_rate": 2.50,
            "daily_rate": 15.00,
        },
        {
            "type_name": "SUV / Large Vehicle",
            "type_code": "SV",
            "description": "Extra-wide space for SUVs and large vehicles",
            "length_cm": 550,
            "width_cm": 280,
            "height_cm": 210,
            "max_vehicle_length_cm": 530,
            "hourly_rate": 4.00,
            "daily_rate": 28.00,
        },
        {
            "type_name": "Motorcycle",
            "type_code": "MC",
            "description": "Dedicated space for motorcycles and scooters",
            "length_cm": 250,
            "width_cm": 120,
            "height_cm": 200,
            "max_vehicle_length_cm": 240,
            "hourly_rate": 1.00,
            "daily_rate": 6.00,
        },
        {
            "type_name": "EV Charging",
            "type_code": "EC",
            "description": "Space with electric vehicle charging station",
            "length_cm": 500,
            "width_cm": 260,
            "height_cm": 220,
            "max_vehicle_length_cm": 480,
            "has_ev_charger": 1,
            "hourly_rate": 5.00,
            "daily_rate": 30.00,
        },
        {
            "type_name": "Handicap Accessible",
            "type_code": "HA",
            "description": "Wider space with wheelchair access ramps",
            "length_cm": 500,
            "width_cm": 350,
            "height_cm": 200,
            "max_vehicle_length_cm": 480,
            "is_accessible": 1,
            "is_handicap_accessible": 1,
            "hourly_rate": 2.00,
            "daily_rate": 12.00,
        },
        {
            "type_name": "Covered Standard",
            "type_code": "CS",
            "description": "Covered/roofed parking for weather protection",
            "length_cm": 500,
            "width_cm": 250,
            "height_cm": 200,
            "max_vehicle_length_cm": 480,
            "is_covered": 1,
            "hourly_rate": 4.50,
            "daily_rate": 25.00,
        },
        {
            "type_name": "Bus / Heavy Vehicle",
            "type_code": "BH",
            "description": "Large space for buses and heavy vehicles",
            "length_cm": 1200,
            "width_cm": 350,
            "height_cm": 400,
            "max_vehicle_length_cm": 1100,
            "hourly_rate": 8.00,
            "daily_rate": 50.00,
        },
    ]

    for st in slot_types:
        if not frappe.db.exists("Parking Slot Type", {"type_name": st["type_name"]}):
            doc = frappe.get_doc({"doctype": "Parking Slot Type", **st})
            doc.insert(ignore_permissions=True)
            print(f"  Created Slot Type: {st['type_name']}")
        else:
            print(f"  Slot Type exists: {st['type_name']}")


def create_zones():
    zones = [
        {
            "zone_name": "City Center Plaza Parking",
            "zone_code": "CCP",
            "zone_type": "Multi-Story",
            "address": "123 Main Street, Downtown",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500001",
            "total_slots": 250,
            "occupied_slots": 180,
            "reserved_slots": 15,
            "available_slots": 55,
            "occupancy_percentage": 72,
            "alert_threshold": 85,
            "max_duration_hours": 24,
            "description": "Premium multi-story parking in the heart of the city center",
        },
        {
            "zone_name": "Mall Road Parking",
            "zone_code": "MRP",
            "zone_type": "Covered",
            "address": "45 Mall Road, Near Shopping Complex",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500003",
            "total_slots": 150,
            "occupied_slots": 95,
            "reserved_slots": 10,
            "available_slots": 45,
            "occupancy_percentage": 63,
            "alert_threshold": 90,
            "max_duration_hours": 12,
            "description": "Covered parking facility adjacent to the shopping mall",
        },
        {
            "zone_name": "Railway Station Parking",
            "zone_code": "RSP",
            "zone_type": "Outdoor",
            "address": "Station Road, Near Platform 1",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500003",
            "total_slots": 200,
            "occupied_slots": 160,
            "reserved_slots": 20,
            "available_slots": 20,
            "occupancy_percentage": 80,
            "alert_threshold": 85,
            "max_duration_hours": 48,
            "description": "Open-air parking near the railway station for commuters",
        },
        {
            "zone_name": "Tech Park Basement",
            "zone_code": "TPB",
            "zone_type": "Basement",
            "address": "IT Corridor, Hitech City",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500081",
            "total_slots": 500,
            "occupied_slots": 420,
            "reserved_slots": 50,
            "available_slots": 30,
            "occupancy_percentage": 84,
            "alert_threshold": 90,
            "max_duration_hours": 10,
            "description": "Underground parking for IT professionals in the tech park",
        },
        {
            "zone_name": "Hospital Visitor Parking",
            "zone_code": "HVP",
            "zone_type": "Outdoor",
            "address": "Healthcare Avenue, Banjara Hills",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500034",
            "total_slots": 100,
            "occupied_slots": 70,
            "reserved_slots": 10,
            "available_slots": 20,
            "occupancy_percentage": 70,
            "alert_threshold": 80,
            "max_duration_hours": 6,
            "description": "Visitor parking for the multi-specialty hospital",
        },
        {
            "zone_name": "Airport Long-Term Parking",
            "zone_code": "ALP",
            "zone_type": "Outdoor",
            "address": "Rajiv Gandhi International Airport",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500409",
            "total_slots": 800,
            "occupied_slots": 620,
            "reserved_slots": 30,
            "available_slots": 150,
            "occupancy_percentage": 77,
            "alert_threshold": 85,
            "max_duration_hours": 720,
            "description": "Long-term parking at the international airport",
        },
    ]

    for z in zones:
        if not frappe.db.exists("Parking Zone", {"zone_name": z["zone_name"]}):
            doc = frappe.get_doc({"doctype": "Parking Zone", **z})
            doc.insert(ignore_permissions=True)
            print(f"  Created Zone: {z['zone_name']}")
        else:
            print(f"  Zone exists: {z['zone_name']}")


def create_fee_structures():
    zones = frappe.get_all("Parking Zone", fields=["name", "zone_name"])
    vehicle_types = ["Car", "SUV", "Motorcycle", "Van", "Bus", "Electric Car", "Truck"]

    fee_data = {
        "City Center Plaza Parking": {
            "Car": {"hourly": 4.00, "daily": 25.00, "weekly": 120.00, "monthly": 400.00, "min": 5.00, "max_daily": 30.00},
            "SUV": {"hourly": 5.00, "daily": 30.00, "weekly": 150.00, "monthly": 500.00, "min": 6.00, "max_daily": 35.00},
            "Motorcycle": {"hourly": 2.00, "daily": 10.00, "weekly": 50.00, "monthly": 150.00, "min": 2.00, "max_daily": 12.00},
        },
        "Mall Road Parking": {
            "Car": {"hourly": 3.00, "daily": 20.00, "weekly": 100.00, "monthly": 350.00, "min": 4.00, "max_daily": 25.00},
            "SUV": {"hourly": 4.00, "daily": 25.00, "weekly": 120.00, "monthly": 400.00, "min": 5.00, "max_daily": 30.00},
            "Motorcycle": {"hourly": 1.50, "daily": 8.00, "weekly": 40.00, "monthly": 120.00, "min": 2.00, "max_daily": 10.00},
        },
        "Railway Station Parking": {
            "Car": {"hourly": 3.00, "daily": 15.00, "weekly": 80.00, "monthly": 250.00, "min": 3.00, "max_daily": 20.00},
            "Motorcycle": {"hourly": 1.00, "daily": 5.00, "weekly": 25.00, "monthly": 80.00, "min": 1.00, "max_daily": 7.00},
        },
        "Tech Park Basement": {
            "Car": {"hourly": 5.00, "daily": 35.00, "weekly": 180.00, "monthly": 600.00, "min": 5.00, "max_daily": 40.00},
            "Electric Car": {"hourly": 4.00, "daily": 30.00, "weekly": 160.00, "monthly": 550.00, "min": 5.00, "max_daily": 35.00},
        },
        "Hospital Visitor Parking": {
            "Car": {"hourly": 2.00, "daily": 10.00, "weekly": 50.00, "monthly": 150.00, "min": 2.00, "max_daily": 12.00},
            "Motorcycle": {"hourly": 1.00, "daily": 5.00, "weekly": 25.00, "monthly": 75.00, "min": 1.00, "max_daily": 6.00},
        },
        "Airport Long-Term Parking": {
            "Car": {"hourly": 6.00, "daily": 40.00, "weekly": 200.00, "monthly": 700.00, "min": 10.00, "max_daily": 50.00},
            "SUV": {"hourly": 8.00, "daily": 50.00, "weekly": 250.00, "monthly": 850.00, "min": 12.00, "max_daily": 60.00},
            "Van": {"hourly": 7.00, "daily": 45.00, "weekly": 220.00, "monthly": 750.00, "min": 10.00, "max_daily": 55.00},
        },
    }

    for zone in zones:
        vtypes = fee_data.get(zone.zone_name, {"Car": {"hourly": 3.00, "daily": 20.00, "weekly": 100.00, "monthly": 300.00, "min": 3.00, "max_daily": 25.00}})
        for vtype, rates in vtypes.items():
            fee_name = f"{zone.zone_name} - {vtype}"
            if not frappe.db.exists("Parking Fee Structure", {"fee_name": fee_name}):
                doc = frappe.get_doc({
                    "doctype": "Parking Fee Structure",
                    "fee_name": fee_name,
                    "zone": zone.name,
                    "vehicle_type": vtype,
                    "hourly_rate": rates["hourly"],
                    "daily_rate": rates["daily"],
                    "weekly_rate": rates.get("weekly", rates["daily"] * 7),
                    "monthly_rate": rates.get("monthly", rates["daily"] * 30),
                    "minimum_charge": rates["min"],
                    "grace_period_minutes": 15,
                    "max_daily_charge": rates["max_daily"],
                    "description": f"Fee structure for {vtype} vehicles at {zone.zone_name}",
                })
                doc.insert(ignore_permissions=True)
                print(f"  Created Fee: {fee_name}")


def update_zone_fee_links():
    zones = frappe.get_all("Parking Zone", fields=["name"])
    for zone in zones:
        fee = frappe.db.get_value("Parking Fee Structure", {"zone": zone.name, "vehicle_type": "Car"}, "name")
        if fee:
            frappe.db.set_value("Parking Zone", zone.name, "fee_structure", fee)
    frappe.db.commit()
    print("  Updated zone fee links")


def create_slots():
    zones = frappe.get_all("Parking Zone", fields=["name", "zone_name", "total_slots"])
    slot_types = frappe.get_all("Parking Slot Type", fields=["name", "type_name"])

    type_map = {st.type_name: st.name for st in slot_types}

    slot_configs = {
        "City Center Plaza Parking": {"floors": ["G", "1", "2", "3", "4"], "slots_per_floor": 50},
        "Mall Road Parking": {"floors": ["G", "1", "2"], "slots_per_floor": 50},
        "Railway Station Parking": {"floors": ["G"], "slots_per_floor": 200},
        "Tech Park Basement": {"floors": ["B1", "B2", "B3"], "slots_per_floor": 167},
        "Hospital Visitor Parking": {"floors": ["G", "1"], "slots_per_floor": 50},
        "Airport Long-Term Parking": {"floors": ["A", "B", "C", "D"], "slots_per_floor": 200},
    }

    for zone in zones:
        config = slot_configs.get(zone.zone_name, {"floors": ["G"], "slots_per_floor": 100})
        existing = frappe.db.count("Parking Slot", {"zone": zone.name})
        if existing > 0:
            print(f"  Slots exist for {zone.zone_name} ({existing} slots)")
            continue

        slot_count = 0
        statuses = ["Available", "Occupied", "Reserved", "Available", "Available", "Occupied"]
        for floor in config["floors"]:
            for i in range(1, min(config["slots_per_floor"], 30) + 1):
                st_type = random.choice(list(type_map.values()))
                status = random.choice(statuses)
                slot_num = f"{floor}-{i:03d}"

                doc = frappe.get_doc({
                    "doctype": "Parking Slot",
                    "slot_number": slot_num,
                    "zone": zone.name,
                    "slot_type": st_type,
                    "floor": floor,
                    "status": status,
                    "is_occupied": 1 if status == "Occupied" else 0,
                    "is_reserved": 1 if status == "Reserved" else 0,
                    "latitude": 17.3850 + random.uniform(-0.01, 0.01),
                    "longitude": 78.4867 + random.uniform(-0.01, 0.01),
                })
                doc.insert(ignore_permissions=True)
                slot_count += 1

        frappe.db.set_value("Parking Zone", zone.name, "total_slots", slot_count)
        print(f"  Created {slot_count} slots for {zone.zone_name}")

    frappe.db.commit()


def create_vehicles():
    vehicles_data = [
        {"license_plate": "TS09AA1234", "vehicle_type": "Car", "make": "Maruti Suzuki", "model": "Swift", "color": "White", "year_of_manufacture": 2023, "owner_name": "Rajesh Kumar", "owner_phone": "9876543210", "owner_email": "rajesh@example.com"},
        {"license_plate": "TS09BB5678", "vehicle_type": "SUV", "make": "Hyundai", "model": "Creta", "color": "Black", "year_of_manufacture": 2024, "owner_name": "Priya Sharma", "owner_phone": "9876543211", "owner_email": "priya@example.com"},
        {"license_plate": "TS09CC9012", "vehicle_type": "Car", "make": "Tata", "model": "Nexon", "color": "Blue", "year_of_manufacture": 2023, "owner_name": "Amit Patel", "owner_phone": "9876543212", "owner_email": "amit@example.com"},
        {"license_plate": "TS09DD3456", "vehicle_type": "Motorcycle", "make": "Bajaj", "model": "Pulsar", "color": "Red", "year_of_manufacture": 2022, "owner_name": "Vikram Singh", "owner_phone": "9876543213", "owner_email": "vikram@example.com"},
        {"license_plate": "TS09EE7890", "vehicle_type": "Car", "make": "Honda", "model": "City", "color": "Silver", "year_of_manufacture": 2024, "owner_name": "Sneha Reddy", "owner_phone": "9876543214", "owner_email": "sneha@example.com"},
        {"license_plate": "TS09FF1122", "vehicle_type": "Van", "make": "Force", "model": "Traveller", "color": "White", "year_of_manufacture": 2021, "owner_name": "Ravi Transport Co", "owner_phone": "9876543215", "owner_email": "ravi@example.com"},
        {"license_plate": "TS09GG3344", "vehicle_type": "Electric Car", "make": "Tata", "model": "Nexon EV", "color": "Teal", "year_of_manufacture": 2024, "owner_name": "Deepak Nair", "owner_phone": "9876543216", "owner_email": "deepak@example.com"},
        {"license_plate": "TS09HH5566", "vehicle_type": "Truck", "make": "Tata", "model": "Ace", "color": "Yellow", "year_of_manufacture": 2020, "owner_name": "Logistics Plus", "owner_phone": "9876543217", "owner_email": "logistics@example.com"},
        {"license_plate": "TS09II7788", "vehicle_type": "Car", "make": "Kia", "model": "Seltos", "color": "Grey", "year_of_manufacture": 2023, "owner_name": "Anitha Das", "owner_phone": "9876543218", "owner_email": "anitha@example.com"},
        {"license_plate": "TS09JJ9900", "vehicle_type": "Bus", "make": "Ashok Leyland", "model": "Viking", "color": "Orange", "year_of_manufacture": 2019, "owner_name": "City Transport", "owner_phone": "9876543219", "owner_email": "citytransport@example.com"},
        {"license_plate": "TS09KK1020", "vehicle_type": "SUV", "make": "Mahindra", "model": "XUV700", "color": "Deep Blue", "year_of_manufacture": 2024, "owner_name": "Suresh Babu", "owner_phone": "9876543220", "owner_email": "suresh@example.com"},
        {"license_plate": "TS09LL3040", "vehicle_type": "Car", "make": "Toyota", "model": "Innova", "color": "Pearl White", "year_of_manufacture": 2022, "owner_name": "Kavitha Menon", "owner_phone": "9876543221", "owner_email": "kavitha@example.com"},
        {"license_plate": "TS09MM5060", "vehicle_type": "Electric Motorcycle", "make": "Ola", "model": "S1 Pro", "color": "Matte Black", "year_of_manufacture": 2024, "owner_name": "Arjun Rao", "owner_phone": "9876543222", "owner_email": "arjun@example.com"},
        {"license_plate": "TS09NN7080", "vehicle_type": "Car", "make": "Hyundai", "model": "i20", "color": "Polar White", "year_of_manufacture": 2023, "owner_name": "Meena Kumari", "owner_phone": "9876543223", "owner_email": "meena@example.com"},
        {"license_plate": "TS09OO9101", "vehicle_type": "Motorcycle", "make": "Royal Enfield", "model": "Classic 350", "color": "Ash Black", "year_of_manufacture": 2022, "owner_name": "Karthik Iyer", "owner_phone": "9876543224", "owner_email": "karthik@example.com"},
    ]

    for v in vehicles_data:
        if not frappe.db.exists("Vehicle", {"license_plate": v["license_plate"]}):
            doc = frappe.get_doc({"doctype": "Vehicle", "naming_series": "VEH-.YYYY.-.####", **v})
            doc.insert(ignore_permissions=True)
            print(f"  Created Vehicle: {v['license_plate']}")
        else:
            print(f"  Vehicle exists: {v['license_plate']}")


def create_staff():
    zones = frappe.get_all("Parking Zone", fields=["name"])
    staff_data = [
        {"staff_name": "Ramesh Babu", "phone": "9800000001", "email": "ramesh@smartparking.com", "staff_type": "Manager", "date_of_joining": "2024-01-15"},
        {"staff_name": "Suresh Kumar", "phone": "9800000002", "email": "suresh@smartparking.com", "staff_type": "Supervisor", "date_of_joining": "2024-02-01"},
        {"staff_name": "Venkat Reddy", "phone": "9800000003", "email": "venkat@smartparking.com", "staff_type": "Attendant", "date_of_joining": "2024-03-10"},
        {"staff_name": "Lakshmi Devi", "phone": "9800000004", "email": "lakshmi@smartparking.com", "staff_type": "Attendant", "date_of_joining": "2024-03-15"},
        {"staff_name": "Prakash Raj", "phone": "9800000005", "email": "prakash@smartparking.com", "staff_type": "Security", "date_of_joining": "2024-01-20"},
        {"staff_name": "Anand Sharma", "phone": "9800000006", "email": "anand@smartparking.com", "staff_type": "Technician", "date_of_joining": "2024-04-01"},
        {"staff_name": "Divya Patel", "phone": "9800000007", "email": "divya@smartparking.com", "staff_type": "Supervisor", "date_of_joining": "2024-02-15"},
        {"staff_name": "Mohammed Ali", "phone": "9800000008", "email": "mohammed@smartparking.com", "staff_type": "Attendant", "date_of_joining": "2024-05-01"},
    ]

    for i, s in enumerate(staff_data):
        if not frappe.db.exists("Parking Staff", {"staff_name": s["staff_name"]}):
            zone = zones[i % len(zones)].name if zones else None
            doc = frappe.get_doc({
                "doctype": "Parking Staff",
                "staff_name": s["staff_name"],
                "phone": s["phone"],
                "email": s["email"],
                "staff_type": s["staff_type"],
                "zone": zone,
                "is_active": 1,
                "date_of_joining": s["date_of_joining"],
            })
            doc.insert(ignore_permissions=True)
            print(f"  Created Staff: {s['staff_name']}")
        else:
            print(f"  Staff exists: {s['staff_name']}")


def create_shifts():
    staff = frappe.get_all("Parking Staff", fields=["name"])
    zones = frappe.get_all("Parking Zone", fields=["name"])

    if not staff or not zones:
        print("  Skipped shifts (no staff or zones)")
        return

    today_str = today()
    shifts = [
        {"start_h": 6, "end_h": 14, "status": "Completed"},
        {"start_h": 14, "end_h": 22, "status": "Completed"},
        {"start_h": 22, "end_h": 6, "status": "Scheduled"},
    ]

    count = 0
    for i, s in enumerate(shifts):
        if count >= 6:
            break
        staff_doc = staff[i % len(staff)]
        zone_doc = zones[i % len(zones)]

        shift_name = f"Shift for {staff_doc.name} on {today_str} {s['start_h']:02d}:00"
        if not frappe.db.exists("Parking Shift", {"staff_member": staff_doc.name, "shift_date": today_str}):
            doc = frappe.get_doc({
                "doctype": "Parking Shift",
                "staff_member": staff_doc.name,
                "zone": zone_doc.name,
                "shift_date": today_str,
                "status": s["status"],
                "shift_start": f"{today_str} {s['start_h']:02d}:00:00",
                "shift_end": f"{today_str} {s['end_h']:02d}:00:00",
                "duration_hours": s["end_h"] - s["start_h"] if s["end_h"] > s["start_h"] else (24 - s["start_h"] + s["end_h"]),
            })
            doc.insert(ignore_permissions=True)
            count += 1
            print(f"  Created Shift: {s['start_h']:02d}:00 - {s['end_h']:02d}:00")


def create_vehicle_entries():
    vehicles = frappe.get_all("Vehicle", fields=["name", "vehicle_type"])
    zones = frappe.get_all("Parking Zone", fields=["name"])
    slots = frappe.get_all("Parking Slot", fields=["name", "zone", "status"], filters={"status": "Occupied"})

    if not vehicles or not zones:
        print("  Skipped vehicle entries (no vehicles or zones)")
        return

    now = now_datetime()
    purposes = ["General", "Visitor", "Delivery", "Employee", "Contractor"]
    entries = [
        {"h_ago": 48, "duration": 3, "status": "Paid"},
        {"h_ago": 36, "duration": 2, "status": "Paid"},
        {"h_ago": 24, "duration": 5, "status": "Paid"},
        {"h_ago": 12, "duration": 1, "status": "Paid"},
        {"h_ago": 8, "duration": 4, "status": "Pending"},
        {"h_ago": 6, "duration": 2, "status": "Pending"},
        {"h_ago": 4, "duration": 3, "status": "Pending"},
        {"h_ago": 2, "duration": 0, "status": "Pending"},
        {"h_ago": 1, "duration": 0, "status": "Pending"},
    ]

    for i, e in enumerate(entries):
        v = vehicles[i % len(vehicles)]
        z = zones[i % len(zones)]
        slot = slots[i % len(slots)].name if slots else None

        entry_time = add_hours(now, -e["h_ago"])
        exit_time = add_hours(entry_time, e["duration"]) if e["duration"] > 0 else None

        doc = frappe.get_doc({
            "doctype": "Vehicle Entry",
            "naming_series": "VE-.YYYY.MM.DD.-.#####",
            "vehicle": v.name,
            "zone": z.name,
            "slot": slot,
            "entry_time": str(entry_time),
            "exit_time": str(exit_time) if exit_time else None,
            "duration_hours": e["duration"] if e["duration"] > 0 else None,
            "parking_fee": round(e["duration"] * 4.00, 2) if e["duration"] > 0 else 0,
            "fee_status": e["status"],
            "purpose": random.choice(purposes),
            "docstatus": 1,
        })
        try:
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Vehicle Entry: {v.name} at {z.name}")
        except Exception as ex:
            frappe.db.rollback()
            print(f"  Skipped entry for {v.name}: {str(ex)[:60]}")


def create_reservations():
    customers = frappe.get_all("Customer", fields=["name"])
    vehicles = frappe.get_all("Vehicle", fields=["name", "vehicle_type"])
    zones = frappe.get_all("Parking Zone", fields=["name"])
    slots = frappe.get_all("Parking Slot", fields=["name", "zone"], filters={"status": ["in", ["Available", "Reserved"]]})

    if not vehicles or not zones:
        print("  Skipped reservations (no vehicles or zones)")
        return

    if not customers:
        print("  Skipped reservations (no customers found)")
        print("  TIP: Create Customer records first or let ERPNext handle it")
        return

    now = now_datetime()
    reservation_data = [
        {"days_from_now": -2, "duration": 4, "status": "Completed", "payment": "Paid"},
        {"days_from_now": -1, "duration": 8, "status": "Completed", "payment": "Paid"},
        {"days_from_now": 0, "duration": 3, "status": "Confirmed", "payment": "Paid"},
        {"days_from_now": 1, "duration": 6, "status": "Confirmed", "payment": "Unpaid"},
        {"days_from_now": 2, "duration": 2, "status": "Draft", "payment": "Unpaid"},
    ]

    for i, r in enumerate(reservation_data):
        v = vehicles[i % len(vehicles)]
        z = zones[i % len(zones)]
        slot = slots[i % len(slots)].name if slots else None
        if not slot:
            continue

        start = add_hours(now, r["days_from_now"] * 24)
        end = add_hours(start, r["duration"])

        try:
            doc = frappe.get_doc({
                "doctype": "Parking Reservation",
                "customer": customers[0].name,
                "vehicle": v.name,
                "vehicle_type": v.vehicle_type,
                "zone": z.name,
                "slot": slot,
                "start_time": str(start),
                "end_time": str(end),
                "duration_hours": r["duration"],
                "reservation_fee": round(r["duration"] * 3.00, 2),
                "payment_status": r["payment"],
                "status": r["status"],
                "docstatus": 1 if r["status"] in ["Completed", "Confirmed"] else 0,
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Reservation: {v.name} - {r['status']}")
        except Exception as ex:
            frappe.db.rollback()
            print(f"  Skipped reservation: {str(ex)[:60]}")


def create_fee_entries():
    vehicle_entries = frappe.get_all("Vehicle Entry", fields=["name", "vehicle", "zone", "entry_time"], filters={"docstatus": 1})
    fee_structures = frappe.get_all("Parking Fee Structure", fields=["name", "zone", "vehicle_type"])

    if not vehicle_entries:
        print("  Skipped fee entries (no vehicle entries)")
        return

    for ve in vehicle_entries[:6]:
        fs = None
        for f in fee_structures:
            if f.zone == ve.zone:
                fs = f.name
                break
        if not fs and fee_structures:
            fs = fee_structures[0].name

        doc = frappe.get_doc({
            "doctype": "Parking Fee Entry",
            "vehicle_entry": ve.name,
            "vehicle": ve.vehicle,
            "zone": ve.zone,
            "fee_structure": fs,
            "entry_time": ve.entry_time,
            "fee_amount": round(random.uniform(10, 50), 2),
            "fee_status": "Paid",
            "remarks": "Demo fee entry",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"  Created Fee Entry for: {ve.name}")


def create_payments():
    fee_entries = frappe.get_all("Parking Fee Entry", fields=["name", "vehicle_entry", "vehicle", "zone", "fee_amount"], filters={"fee_status": "Paid"})

    if not fee_entries:
        print("  Skipped payments (no paid fee entries)")
        return

    methods = ["Cash", "Card", "UPI", "Online Transfer", "Wallet"]

    for fe in fee_entries[:5]:
        doc = frappe.get_doc({
            "doctype": "Parking Payment",
            "fee_entry": fe.name,
            "vehicle_entry": fe.vehicle_entry,
            "vehicle": fe.vehicle,
            "zone": fe.zone,
            "amount_paid": fe.fee_amount,
            "payment_method": random.choice(methods),
            "payment_date": today(),
            "reference_number": f"REF{random.randint(100000, 999999)}",
            "docstatus": 1,
        })
        try:
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"  Created Payment: {fe.name}")
        except Exception as ex:
            frappe.db.rollback()
            print(f"  Skipped payment: {str(ex)[:60]}")


def create_incidents():
    zones = frappe.get_all("Parking Zone", fields=["name"])
    vehicles = frappe.get_all("Vehicle", fields=["name"])

    if not zones or not vehicles:
        print("  Skipped incidents (no zones or vehicles)")
        return

    incident_data = [
        {"type": "Damage", "severity": "Medium", "status": "Resolved", "desc": "Minor scratch on rear bumper reported by attendant"},
        {"type": "Vandalism", "severity": "High", "status": "In Progress", "desc": "Side mirror broken, CCTV footage under review"},
        {"type": "Unauthorized Parking", "severity": "Low", "status": "Resolved", "desc": "Vehicle parked in reserved spot without permit, owner notified"},
        {"type": "Breakdown", "severity": "Low", "status": "Resolved", "desc": "Vehicle battery dead, roadside assistance called"},
        {"type": "Theft", "severity": "Critical", "status": "Open", "desc": "Reported theft of side mirror, police complaint filed"},
    ]

    for i, inc in enumerate(incident_data):
        z = zones[i % len(zones)]
        v = vehicles[i % len(vehicles)]

        doc = frappe.get_doc({
            "doctype": "Parking Incident",
            "incident_type": inc["type"],
            "severity": inc["severity"],
            "status": inc["status"],
            "zone": z.name,
            "vehicle": v.name,
            "description": inc["desc"],
            "notes": "Handled as per standard procedure",
        })
        doc.insert(ignore_permissions=True)
        print(f"  Created Incident: {inc['type']} at {z.name}")


def create_alerts():
    zones = frappe.get_all("Parking Zone", fields=["name"])

    if not zones:
        print("  Skipped alerts (no zones)")
        return

    alert_data = [
        {"type": "Overstay", "priority": "High", "status": "Open", "title": "Vehicle TS09AA1234 overstaying in Zone CCP", "desc": "Vehicle has exceeded maximum parking duration by 2 hours"},
        {"type": "Equipment Failure", "priority": "Medium", "status": "In Progress", "title": "EV Charger malfunction in Tech Park Basement", "desc": "Charger station #3 not responding, technician dispatched"},
        {"type": "Security", "priority": "High", "status": "Resolved", "title": "Unauthorized entry detected at Railway Station", "desc": "Gate sensor triggered after hours, security patrol responded"},
        {"type": "Maintenance", "priority": "Low", "status": "Open", "title": "Lighting issue in Floor 2 of City Center", "desc": "Several lights on floor 2 not working, maintenance team notified"},
        {"type": "Slot Violation", "priority": "Medium", "status": "Dismissed", "title": "Compact car in SUV spot at Mall Road", "desc": "Upon inspection, vehicle fits within compact boundaries"},
    ]

    now = now_datetime()
    for i, a in enumerate(alert_data):
        z = zones[i % len(zones)]
        doc = frappe.get_doc({
            "doctype": "Parking Alert",
            "alert_type": a["type"],
            "priority": a["priority"],
            "status": a["status"],
            "zone": z.name,
            "title": a["title"],
            "description": a["desc"],
            "created_on": str(now),
        })
        doc.insert(ignore_permissions=True)
        print(f"  Created Alert: {a['title'][:50]}")


def create_settings():
    if not frappe.db.exists("Smart Parking Settings", "Smart Parking Settings"):
        doc = frappe.get_doc({
            "doctype": "Smart Parking Settings",
            "overdue_threshold_hours": 24,
            "auto_release_expired_reservations": 1,
            "send_occupancy_alerts": 1,
            "occupancy_alert_threshold": 85,
            "send_reservation_expiry_reminders": 1,
            "send_overdue_vehicle_alerts": 1,
            "auto_create_sales_invoice": 0,
            "auto_create_customer": 0,
        })
        doc.insert(ignore_permissions=True)
        print("  Created Smart Parking Settings")
    else:
        print("  Smart Parking Settings exists")
