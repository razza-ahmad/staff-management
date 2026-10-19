import json
import os

DB_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.json')

DEFAULT_STAFF = [
    {'id': 'EMP-1001', 'name': 'Aarav Sharma', 'department': 'Engineering', 'role': 'Tech Lead', 'email': 'aarav.sharma@company.com', 'phone': '+91 98201 12345', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2024-03-15', 'status': 'Active'},
    {'id': 'EMP-1002', 'name': 'Priya Deshmukh', 'department': 'Operations', 'role': 'Operations Manager', 'email': 'priya.deshmukh@company.com', 'phone': '+91 98202 23456', 'shift_start': '09:30', 'shift_end': '18:30', 'grace_minutes': 15, 'joined_date': '2024-06-01', 'status': 'Active'},
    {'id': 'EMP-1003', 'name': 'Rohan Mehta', 'department': 'Engineering', 'role': 'Senior Software Engineer', 'email': 'rohan.mehta@company.com', 'phone': '+91 98203 34567', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2024-08-10', 'status': 'Active'},
    {'id': 'EMP-1004', 'name': 'Ananya Iyer', 'department': 'HR & Admin', 'role': 'HR Specialist', 'email': 'ananya.iyer@company.com', 'phone': '+91 98204 45678', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2025-01-10', 'status': 'Active'},
    {'id': 'EMP-1005', 'name': 'Vikram Joshi', 'department': 'Sales & Marketing', 'role': 'Sales Director', 'email': 'vikram.joshi@company.com', 'phone': '+91 98205 56789', 'shift_start': '10:00', 'shift_end': '19:00', 'grace_minutes': 15, 'joined_date': '2024-11-01', 'status': 'Active'},
    {'id': 'EMP-1006', 'name': 'Neha Patel', 'department': 'Finance', 'role': 'Senior Accountant', 'email': 'neha.patel@company.com', 'phone': '+91 98206 67890', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2025-02-15', 'status': 'Active'},
    {'id': 'EMP-1007', 'name': 'Kabir Verma', 'department': 'Engineering', 'role': 'DevOps Engineer', 'email': 'kabir.verma@company.com', 'phone': '+91 98207 78901', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2025-04-01', 'status': 'Active'},
    {'id': 'EMP-1008', 'name': 'Sneha Kulkarni', 'department': 'Operations', 'role': 'Logistics Coordinator', 'email': 'sneha.kulkarni@company.com', 'phone': '+91 98208 89012', 'shift_start': '09:00', 'shift_end': '18:00', 'grace_minutes': 15, 'joined_date': '2025-05-20', 'status': 'Active'}
]

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return init_db()

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def init_db():
    # Build demo attendance logs
    logs = []
    log_id = 1
    for day in range(1, 20): # Oct 1 to 19, 2026
        dt_day = (day + 3) % 7 # simulated day of week (0=Sun, 6=Sat)
        if dt_day in (0, 6): continue # weekend
        date_str = f"2026-10-{day:02d}"
        for idx, s in enumerate(DEFAULT_STAFF):
            seed = (day * 13 + idx * 7) % 100
            status = 'Present'
            is_late = 0
            late_mins = 0
            in_t = '08:55'
            out_t = '18:05'
            leave_t = ''
            notes = ''
            if seed < 70:
                pass
            elif seed < 85:
                status = 'Late'
                is_late = 1
                late_mins = 20 + (seed % 25)
                in_t = f"09:{late_mins:02d}"
                notes = 'Commute delay'
            elif seed < 94:
                status = 'Leave'
                in_t = ''
                out_t = ''
                leave_t = 'Casual Leave (CL)' if seed % 2 == 0 else 'Sick Leave (SL)'
                notes = 'Approved leave'
            else:
                status = 'Absent'
                in_t = ''
                out_t = ''
                notes = 'Unplanned absence'

            hrs = 0.0
            if in_t and out_t:
                hrs = 9.0

            logs.append({
                'id': f"LOG-{log_id}",
                'staff_id': s['id'],
                'date': date_str,
                'status': status,
                'in_time': in_t,
                'out_time': out_t,
                'is_late': is_late,
                'late_minutes': late_mins,
                'work_hours': hrs,
                'leave_type': leave_t,
                'notes': notes
            })
            log_id += 1

    data = {
        'staff': DEFAULT_STAFF,
        'attendance': logs
    }
    save_db(data)
    return data

if __name__ == '__main__':
    data = init_db()
    print(f"Initialized database with {len(data['staff'])} staff and {len(data['attendance'])} attendance records.")
