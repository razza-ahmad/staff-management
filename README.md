# StaffPulse - Staff Attendance & Management System

An end-to-end, full-featured staff management, attendance tracking, and monthly reporting system.

## Features
- **Staff Directory**: Add new staff, edit profile, configure individualized shift timings, grace periods, and employment status.
- **Fast Attendance Tracking**: One-click Clock In / Clock Out, manual entry for any date, and bulk attendance marking.
- **Late Mark Detection**: Automatically compares clock-in timestamps against scheduled shift start times + grace periods (e.g. 09:00 + 15 min grace = 09:15 threshold) and logs exact minutes of tardiness.
- **Leave & Absence Tracking**: Supports Casual Leave (CL), Sick Leave (SL), Paid / Earned Leave (PL), Maternity/Paternity Leave, and Leave Without Pay (LWP), with unexcused absence calculations.
- **Individual Staff Monthly Reports**: Metric scorecard, interactive visual monthly calendar grid, itemized daily log, printable PDF format with employee & HR sign-off lines, and CSV export.
- **All Staff Monthly Summary Report**: Organization-wide attendance rate %, total late marks, department breakdown charts (Chart.js), master employee summary table, executive printable layout, and CSV export.

## Quick Start Options

### Option 1: Browser-Only (Standalone)
Double-click `index.html` or open it directly in any modern web browser (Chrome, Edge, Safari, Firefox). All data is saved automatically in your browser's `localStorage`.

### Option 2: Python / SQLite API Server
1. Ensure Python 3 is installed.
2. Install Flask (if not present): `pip install flask`
3. Initialize the database and launch the server:
   ```bash
   python3 app.py
   ```
4. Open `http://localhost:5000` in your browser.

### Option 3: Terminal CLI Interface
Run reports directly from the command line:
```bash
python3 cli.py all-report 2026-10
python3 cli.py indiv-report EMP-1001 2026-10
```
