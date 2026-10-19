import os
from flask import Flask, jsonify, request, send_from_directory
from database import load_db, save_db, init_db

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/staff', methods=['GET', 'POST'])
def handle_staff():
    db = load_db()
    if request.method == 'GET':
        return jsonify(db['staff'])
    else:
        new_staff = request.json
        # Remove existing if any
        db['staff'] = [s for s in db['staff'] if s['id'] != new_staff['id']]
        db['staff'].append(new_staff)
        save_db(db)
        return jsonify({'status': 'success', 'staff': new_staff})

@app.route('/api/attendance', methods=['GET', 'POST'])
def handle_attendance():
    db = load_db()
    if request.method == 'GET':
        date = request.args.get('date')
        staff_id = request.args.get('staff_id')
        month = request.args.get('month')
        results = db['attendance']
        if date:
            results = [a for a in results if a['date'] == date]
        if staff_id:
            results = [a for a in results if a['staff_id'] == staff_id]
        if month:
            results = [a for a in results if a['date'].startswith(month)]
        return jsonify(results)
    else:
        record = request.json
        db['attendance'] = [a for a in db['attendance'] if not (a['staff_id'] == record['staff_id'] and a['date'] == record['date'])]
        db['attendance'].append(record)
        save_db(db)
        return jsonify({'status': 'success'})

@app.route('/api/reports/individual/<staff_id>/<month>')
def report_individual(staff_id, month):
    db = load_db()
    staff = next((s for s in db['staff'] if s['id'] == staff_id), None)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    logs = [a for a in db['attendance'] if a['staff_id'] == staff_id and a['date'].startswith(month)]
    present = sum(1 for l in logs if l['status'] in ('Present', 'Late'))
    late = sum(1 for l in logs if l.get('is_late') or l['status'] == 'Late')
    leaves = sum(1 for l in logs if l['status'] == 'Leave')
    absences = sum(1 for l in logs if l['status'] == 'Absent')
    hours = sum(l.get('work_hours', 0.0) for l in logs)

    return jsonify({
        'staff': staff,
        'month': month,
        'metrics': {
            'present_days': present,
            'late_marks': late,
            'leaves_taken': leaves,
            'absences': absences,
            'total_hours': round(hours, 1)
        },
        'logs': sorted(logs, key=lambda x: x['date'])
    })

@app.route('/api/reports/all/<month>')
def report_all_staff(month):
    db = load_db()
    report = []
    for s in db['staff']:
        logs = [a for a in db['attendance'] if a['staff_id'] == s['id'] and a['date'].startswith(month)]
        present = sum(1 for l in logs if l['status'] in ('Present', 'Late'))
        late = sum(1 for l in logs if l.get('is_late') or l['status'] == 'Late')
        leaves = sum(1 for l in logs if l['status'] == 'Leave')
        absences = sum(1 for l in logs if l['status'] == 'Absent')
        hours = sum(l.get('work_hours', 0.0) for l in logs)
        report.append({
            'staff_id': s['id'],
            'name': s['name'],
            'department': s['department'],
            'role': s['role'],
            'present_days': present,
            'late_marks': late,
            'leaves': leaves,
            'absences': absences,
            'total_hours': round(hours, 1)
        })
    return jsonify({'month': month, 'roster': report})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
