import sys
from database import load_db, save_db

def print_all_report(month):
    db = load_db()
    print(f"\n{'='*75}")
    print(f"ALL-STAFF MONTHLY SUMMARY REPORT - {month}")
    print(f"{'='*75}")
    print(f"{'ID':<10} {'Name':<20} {'Department':<16} {'Present':<8} {'Late':<8} {'Leaves':<8} {'Hours':<8}")
    print(f"{'-'*75}")
    for s in db['staff']:
        logs = [a for a in db['attendance'] if a['staff_id'] == s['id'] and a['date'].startswith(month)]
        p = sum(1 for l in logs if l['status'] in ('Present', 'Late'))
        late = sum(1 for l in logs if l.get('is_late') or l['status'] == 'Late')
        leaves = sum(1 for l in logs if l['status'] == 'Leave')
        hrs = sum(l.get('work_hours', 0.0) for l in logs)
        print(f"{s['id']:<10} {s['name']:<20} {s['department']:<16} {p:<8} {late:<8} {leaves:<8} {round(hrs,1):<8}")
    print(f"{'='*75}\n")

def print_indiv_report(staff_id, month):
    db = load_db()
    staff = next((s for s in db['staff'] if s['id'] == staff_id), None)
    if not staff:
        print("Staff not found.")
        return
    logs = [a for a in db['attendance'] if a['staff_id'] == staff_id and a['date'].startswith(month)]
    print(f"\n{'='*65}")
    print(f"MONTHLY REPORT: {staff['name']} ({staff['id']}) - {month}")
    print(f"Department: {staff['department']} | Role: {staff['role']}")
    print(f"{'='*65}")
    print(f"{'Date':<12} {'Status':<12} {'In':<8} {'Out':<8} {'Hours':<8} {'Late Mins':<10}")
    print(f"{'-'*65}")
    for l in sorted(logs, key=lambda x: x['date']):
        print(f"{l['date']:<12} {l['status']:<12} {l.get('in_time') or '--':<8} {l.get('out_time') or '--':<8} {l.get('work_hours',0.0):<8} {l.get('late_minutes',0):<10}")
    print(f"{'='*65}\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 cli.py [all-report YYYY-MM | indiv-report STAFF_ID YYYY-MM]")
    elif sys.argv[1] == 'all-report':
        month = sys.argv[2] if len(sys.argv) > 2 else '2026-10'
        print_all_report(month)
    elif sys.argv[1] == 'indiv-report':
        staff_id = sys.argv[2] if len(sys.argv) > 2 else 'EMP-1001'
        month = sys.argv[3] if len(sys.argv) > 3 else '2026-10'
        print_indiv_report(staff_id, month)
