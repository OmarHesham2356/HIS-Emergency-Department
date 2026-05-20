#!/usr/bin/env python3
"""
SQL Schema Validator — HIS Emergency Department

Validates SQL DDL by:
  1. Attempting to run against a live MySQL instance
  2. Falling back to static analysis if MySQL is unavailable

Usage:
    python sql/validate.py                  # Validate all members + merge
    python sql/validate.py --member 1       # Only Omar
    python sql/validate.py --member 2       # Only Ziad
    python sql/validate.py --member 3       # Only Youssef
    python sql/validate.py --merge          # Only merged schema
    python sql/validate.py --reset          # Drop all tables first
    python sql/validate.py --static         # Force static analysis only
"""

import re
import sys
import os
import subprocess
import argparse
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# MySQL connection command (updated if --password is provided)
MYSQL_CMD = ['mysql', '-u', 'root']

MEMBERS = {
    1: {
        'name': 'Omar Hesham',
        'focus': 'Patient Flow & Appointments',
        'tables': {
            'Patient':           ['PatientID', 'SSN', 'PatientNumber', 'FirstName', 'LastName', 'Address', 'BirthDate', 'Sex', 'MedicalHistory', 'BloodPressure', 'HeartRate', 'Temperature'],
            'Payment':           ['PaymentID', 'Amount', 'PaymentDate', 'PaymentMethod', 'Status'],
            'Patient_Phone':     ['PatientID', 'Phone'],
            'Bed':               ['BedID', 'RoomNumber', 'LocationID', 'BedType', 'Status'],
            'Users':             ['UserID', 'PatientID', 'EmployeeID', 'Username', 'PasswordHash', 'Email', 'Role', 'CreatedAt'],
            'Appointment':       ['AppointmentID', 'PatientID', 'DoctorID', 'PaymentID', 'AppointmentDateTime', 'Status', 'Type', 'Notes'],
            'EmergencyVisit':    ['VisitID', 'PatientID', 'TriageID', 'BedID', 'AdmissionDateTime', 'DischargeDateTime', 'Disposition'],
        },
        'file': BASE / 'sql' / 'Member1' / 'omar_schema.sql',
    },
    2: {
        'name': 'Ziad Khaled',
        'focus': 'Staff Hierarchy & Locations',
        'tables': {
            'Hospital':             ['HospitalID', 'Name', 'Address', 'Phone', 'Email', 'EstablishedYear'],
            'Employee':             ['EmployeeID', 'UserID', 'FirstName', 'LastName', 'BirthDate', 'Sex', 'SSN', 'HireDate', 'JobTitle', 'EmployeeType'],
            'Department':           ['DepartmentID', 'HospitalID', 'Name', 'Code', 'ChairmanDoctorID', 'SupervisionStartDate'],
            'Doctor':               ['EmployeeID', 'DepartmentID', 'MajorScientificArea', 'Degree', 'JoinDate'],
            'Nurse':                ['EmployeeID', 'DepartmentID', 'JoinDate'],
            'Admin':                ['EmployeeID'],
            'DepartmentLocation':   ['LocationID', 'DepartmentID', 'Address', 'Latitude', 'Longitude'],
        },
        'file': BASE / 'sql' / 'Member 2' / 'Member 2.sql',
    },
    3: {
        'name': 'Youssef Amir',
        'focus': 'Clinical & Medication',
        'tables': {
            'Medication':           ['MedicationID', 'Name', 'Description'],
            'Prescription':         ['PrescriptionID', 'DoctorID', 'PatientID', 'VisitID', 'PrescriptionDate'],
            'PrescriptionDetail':   ['PrescriptionDetailID', 'PrescriptionID', 'MedicationID', 'Directions', 'Dosage', 'TimesPerDay', 'StartDate', 'EndDate'],
            'Triage':               ['PatientID', 'TriageID', 'NurseID', 'DateTime', 'ChiefComplaint', 'TriageLevel', 'BloodPressure', 'HeartRate', 'Temperature'],
            'Examination':          ['DoctorID', 'PatientID', 'VisitID', 'ExaminationDate', 'HoursSpent'],
            'Document':             ['DocumentID', 'PatientID', 'VisitID', 'FileName', 'FilePath', 'UploadDate', 'Description'],
        },
        'file': BASE / 'sql' / 'Member 3' / 'youssef_schema.sql',
    },
}

MERGE_FILE = BASE / 'sql' / 'merge' / 'full_schema.sql'
RESET_FILE = BASE / 'sql' / 'reset.sql'

ALL_TABLES = {}
for m in MEMBERS.values():
    ALL_TABLES.update(m['tables'])


# ═══════════════════════════════════════════════════════════════
# Live MySQL runner
# ═══════════════════════════════════════════════════════════════

def _try_mysql_connect() -> bool:
    """Check if MySQL is reachable."""
    try:
        r = subprocess.run(
            MYSQL_CMD + ['-e', 'SELECT 1'],
            capture_output=True, text=True, timeout=5,
        )
        return r.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _run_mysql(sql_input: str) -> tuple[int, str, str]:
    """Execute SQL via mysql CLI. Returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            MYSQL_CMD,
            input=sql_input,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return -1, '', 'MySQL client not found'
    except subprocess.TimeoutExpired:
        return -1, '', 'TIMEOUT'


def _live_check_tables(tables: list[str]) -> dict:
    """Check which tables exist in the database via information_schema."""
    results = {}
    for table in tables:
        sql = (
            f"SELECT COUNT(*) FROM information_schema.TABLES "
            f"WHERE TABLE_SCHEMA = 'emergency_dept' AND TABLE_NAME = '{table}';"
        )
        rc, out, err = _run_mysql(sql)
        exists = rc == 0 and out.strip().split('\n')[-1].strip() == '1' if out.strip() else False
        results[table] = exists
    return results


def _live_get_columns(table: str) -> list[str]:
    """Get column names for a table via information_schema."""
    sql = (
        f"SELECT COLUMN_NAME FROM information_schema.COLUMNS "
        f"WHERE TABLE_SCHEMA = 'emergency_dept' AND TABLE_NAME = '{table}' "
        f"ORDER BY ORDINAL_POSITION;"
    )
    rc, out, err = _run_mysql(sql)
    if rc != 0:
        return []
    return [line.strip() for line in out.strip().split('\n')
            if line.strip() and not line.startswith('COLUMN_NAME')]


# ═══════════════════════════════════════════════════════════════
# Static analyser
# ═══════════════════════════════════════════════════════════════

def _static_extract_tables(sql: str) -> dict[str, list[str]]:
    """Extract table names and column names from CREATE TABLE statements.
    Handles nested parentheses (CHECK constraints, DECIMAL params).
    """
    tables = {}
    # Remove comments and string literals
    cleaned = re.sub(r"--[^\n]*", '', sql)
    cleaned = re.sub(r"'[^']*'", '', cleaned)

    pattern = re.compile(r'CREATE\s+TABLE\s+(\w+)\s*\(', re.IGNORECASE)
    for match in pattern.finditer(cleaned):
        tname = match.group(1)
        start = match.end()
        depth = 1
        i = start
        while depth > 0 and i < len(cleaned):
            if cleaned[i] == '(':
                depth += 1
            elif cleaned[i] == ')':
                depth -= 1
            i += 1
        body = cleaned[start:i-1]

        # Extract column definitions: line starts with name followed by SQL type keyword
        cols = []
        col_pattern = re.compile(
            r'^\s+(\w+)\s+(INT|VARCHAR|DATE|DATETIME|DECIMAL|TEXT|ENUM|BIGINT|FLOAT|DOUBLE|CHAR|TINYINT|SMALLINT|BOOLEAN|INTEGER|NUMERIC|REAL)',
            re.IGNORECASE | re.MULTILINE
        )
        for cm in col_pattern.finditer(body):
            cols.append(cm.group(1))
        tables[tname] = cols
    return tables


def _static_validate_member(mid: int) -> dict:
    """Validate a member's SQL file using static analysis."""
    info = MEMBERS[mid]
    sql_file = info['file']
    if not sql_file.exists():
        return {'status': 'SKIP', 'error': f'File not found: {sql_file}'}

    sql = sql_file.read_text()
    extracted = _static_extract_tables(sql)
    expected = info['tables']

    table_results = {}
    column_results = {}
    errors = []

    for tname, expected_cols in expected.items():
        if tname not in extracted:
            table_results[tname] = False
            errors.append(f'{tname}: table not found in SQL')
            continue
        table_results[tname] = True
        actual_cols = extracted[tname]
        # Check expected columns exist (ignore order)
        missing = [c for c in expected_cols if c not in actual_cols]
        extra = [c for c in actual_cols if c not in expected_cols]
        column_results[tname] = {
            'expected': len(expected_cols),
            'found': len(actual_cols),
            'missing': missing,
            'extra': extra,
        }
        if missing:
            errors.append(f'{tname}: missing columns {missing}')

    # Check for ALTER TABLE statements (FK additions)
    alter_count = len(re.findall(r'ALTER\s+TABLE', sql, re.IGNORECASE))
    alter_ok = re.search(r'ALTER\s+TABLE\s+Department\s+ADD\s+CONSTRAINT\s+fk_dept_chairman', sql, re.IGNORECASE)

    return {
        'status': 'PASS' if not errors else 'PARTIAL',
        'tables': table_results,
        'columns': column_results,
        'errors': errors,
        'alter_count': alter_count,
        'has_chairman_alter': alter_ok is not None,
    }


def _static_validate_merge() -> dict:
    """Validate merged schema using static analysis."""
    if not MERGE_FILE.exists():
        return {'status': 'SKIP', 'error': f'File not found: {MERGE_FILE}'}

    sql = MERGE_FILE.read_text()
    extracted = _static_extract_tables(sql)

    table_results = {}
    column_results = {}
    errors = []

    for tname, expected_cols in ALL_TABLES.items():
        if tname not in extracted:
            table_results[tname] = False
            errors.append(f'{tname}: table not found in SQL')
            continue
        table_results[tname] = True
        actual_cols = extracted[tname]
        missing = [c for c in expected_cols if c not in actual_cols]
        extra = [c for c in actual_cols if c not in expected_cols]
        column_results[tname] = {
            'expected': len(expected_cols),
            'found': len(actual_cols),
            'missing': missing,
            'extra': extra,
        }
        if missing:
            errors.append(f'{tname}: missing columns {missing}')

    # Check FK count: merged should have many active FKs
    fk_count = len(re.findall(r'FOREIGN\s+KEY', sql, re.IGNORECASE))

    return {
        'status': 'PASS' if not errors else 'PARTIAL',
        'tables': table_results,
        'columns': column_results,
        'errors': errors,
        'fk_count': fk_count,
    }


# ═══════════════════════════════════════════════════════════════
# Live runner (wraps static for comparison)
# ═══════════════════════════════════════════════════════════════

def _live_validate_member(mid: int, reset_first: bool = False) -> dict:
    """Run a member's SQL against MySQL and validate."""
    info = MEMBERS[mid]
    sql_file = info['file']
    if not sql_file.exists():
        return {'status': 'SKIP', 'error': f'File not found: {sql_file}'}

    if reset_first:
        _run_mysql(RESET_FILE.read_text())

    sql = sql_file.read_text()
    rc, out, err = _run_mysql(sql)

    if rc != 0:
        return {'status': 'FAIL', 'error': err.strip()[:500]}

    tables_found = _live_check_tables(list(info['tables'].keys()))
    column_counts = {}
    for table, exists in tables_found.items():
        if exists:
            cols = _live_get_columns(table)
            column_counts[table] = len(cols)

    return {
        'status': 'PASS' if all(tables_found.values()) else 'PARTIAL',
        'tables': tables_found,
        'columns': column_counts,
    }


def _live_validate_merge(reset_first: bool = False) -> dict:
    """Run merged schema and validate against MySQL."""
    if not MERGE_FILE.exists():
        return {'status': 'SKIP', 'error': f'File not found: {MERGE_FILE}'}

    if reset_first:
        _run_mysql(RESET_FILE.read_text())

    sql = MERGE_FILE.read_text()
    rc, out, err = _run_mysql(sql)

    if rc != 0:
        return {'status': 'FAIL', 'error': err.strip()[:500]}

    tables_found = _live_check_tables(list(ALL_TABLES.keys()))
    column_counts = {}
    for table, exists in tables_found.items():
        if exists:
            cols = _live_get_columns(table)
            column_counts[table] = len(cols)

    return {
        'status': 'PASS' if all(tables_found.values()) else 'PARTIAL',
        'tables': tables_found,
        'columns': column_counts,
    }


# ═══════════════════════════════════════════════════════════════
# Report printer
# ═══════════════════════════════════════════════════════════════

def _print_static_table(tname: str, expected: list[str], col_info: dict, exists: bool):
    """Print one table row for static analysis."""
    if not exists:
        print(f'    ✗ {tname:<25s} TABLE NOT FOUND')
        return
    info = col_info.get(tname, {})
    missing = info.get('missing', [])
    extra = info.get('extra', [])
    status = '✓' if not missing else '~'
    label = f'{info.get("found", "?")}/{info.get("expected", "?")} cols'
    if missing:
        label += f'  MISSING: {", ".join(missing)}'
    print(f'    {status} {tname:<25s} ({label})')


def _print_report(member_results: dict, merge_result: dict = None, mode: str = 'static'):
    """Print a formatted validation report."""
    W = 60
    mode_label = 'STATIC ANALYSIS' if mode == 'static' else 'LIVE MySQL'
    print('╔' + '═' * W + '╗')
    print(f'║  SQL VALIDATION REPORT ({mode_label:^27s})  ║')
    print('╚' + '═' * W + '╝')
    print()

    all_ok = True

    for mid, result in sorted(member_results.items()):
        info = MEMBERS[mid]
        label = f'Member {mid} — {info["name"]} ({info["focus"]})'
        print(f'  {label}')
        print(f'  {"─" * len(label)}')

        if result['status'] == 'FAIL':
            print(f'  ✗ FAILED — {result.get("error", "")}')
            all_ok = False
        elif result['status'] == 'SKIP':
            print(f'  - SKIPPED — {result.get("error", "")}')
        else:
            if mode == 'static':
                errors = result.get('errors', [])
                columns = result.get('columns', {})
                tables = result.get('tables', {})
                passed = sum(1 for v in tables.values() if v)
                total = len(tables)
                for tname in info['tables']:
                    _print_static_table(tname, info['tables'][tname], columns, tables.get(tname, False))
                if result.get('alter_count', 0) > 0:
                    print(f'    ℹ  ALTER TABLE statements: {result["alter_count"]}')
                if result.get('has_chairman_alter'):
                    print(f'    ℹ  Chairman circular dep resolved ✓')
                if errors:
                    print(f'    → {passed}/{total} tables OK — {total - passed} with issues')
                    all_ok = False
                else:
                    print(f'    → {passed}/{total} tables: all columns match ✓')
            else:
                tables = result.get('tables', {})
                cols = result.get('columns', {})
                passed = sum(1 for v in tables.values() if v)
                total = len(tables)
                for table, exists in tables.items():
                    status = '✓' if exists else '✗'
                    ncols = cols.get(table, '?')
                    print(f'    {status} {table:<25s} ({ncols} cols)')
                if all(tables.values()):
                    print(f'    → {passed}/{total} tables created successfully ✓')
                else:
                    print(f'    → {passed}/{total} tables created — {total - passed} missing')
                    all_ok = False
        print()

    if merge_result:
        print(f'  Merged Schema — all {len(ALL_TABLES)} tables')
        print(f'  {"─" * 35}')
        if merge_result['status'] == 'FAIL':
            print(f'  ✗ FAILED — {merge_result.get("error", "")}')
            all_ok = False
        elif merge_result['status'] == 'SKIP':
            print(f'  - SKIPPED — {merge_result.get("error", "")}')
        else:
            if mode == 'static':
                columns = merge_result.get('columns', {})
                tables = merge_result.get('tables', {})
                errors = merge_result.get('errors', [])
                passed = sum(1 for v in tables.values() if v)
                total = len(tables)
                for tname in ALL_TABLES:
                    _print_static_table(tname, ALL_TABLES[tname], columns, tables.get(tname, False))
                fk_count = merge_result.get('fk_count', 0)
                print(f'    ℹ  Active FOREIGN KEY constraints: {fk_count}')
                if errors:
                    print(f'    → {passed}/{total} tables OK — {total - passed} with issues')
                    all_ok = False
                else:
                    print(f'    → {passed}/{total} tables: all columns match ✓')
            else:
                tables = merge_result.get('tables', {})
                cols = merge_result.get('columns', {})
                passed = sum(1 for v in tables.values() if v)
                total = len(tables)
                for table, exists in tables.items():
                    status = '✓' if exists else '✗'
                    ncols = cols.get(table, '?')
                    print(f'    {status} {table:<25s} ({ncols} cols)')
                print(f'    → {passed}/{total} tables created')
        print()

    footer = '✅ ALL VALIDATIONS PASSED' if all_ok else '❌ SOME VALIDATIONS FAILED'
    print(f'  {"─" * len(footer)}')
    print(f'  {footer}')
    print()


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Validate SQL schemas for HIS Emergency Department')
    parser.add_argument('--member', type=int, choices=[1, 2, 3], help='Validate specific member only')
    parser.add_argument('--merge', action='store_true', help='Validate merged schema only')
    parser.add_argument('--reset', action='store_true', help='Drop all tables before live validation')
    parser.add_argument('--password', '-p', type=str, default='', help='MySQL root password')
    parser.add_argument('--static', action='store_true', help='Force static analysis (no DB connection)')
    args = parser.parse_args()

    # Decide mode
    use_live = False
    if args.password:
        MYSQL_CMD[:] = ['mysql', '-u', 'root', f'-p{args.password}']
        use_live = True
    elif not args.static:
        use_live = _try_mysql_connect()
        if not use_live:
            print('  ℹ  MySQL not reachable (tried `mysql -u root` without password).')
            print('     Falling back to static analysis.\n')
            print('     To run live: create a MySQL root user that can connect without password,')
            print('     or use: mysql -u root -p < file.sql')
            print()

    mode = 'live' if use_live else 'static'
    member_results = {}
    merge_result = None

    if args.member:
        mid = args.member
        if use_live:
            member_results[mid] = _live_validate_member(mid, reset_first=args.reset)
        else:
            member_results[mid] = _static_validate_member(mid)
    elif args.merge:
        if use_live:
            merge_result = _live_validate_merge(reset_first=args.reset)
        else:
            merge_result = _static_validate_merge()
    else:
        # All members + merge
        if use_live:
            if args.reset:
                _run_mysql(RESET_FILE.read_text())
            for mid in [1, 2, 3]:
                if args.reset or mid > 1:
                    _run_mysql(RESET_FILE.read_text())
                member_results[mid] = _live_validate_member(mid)
            _run_mysql(RESET_FILE.read_text())
            merge_result = _live_validate_merge()
        else:
            for mid in [1, 2, 3]:
                member_results[mid] = _static_validate_member(mid)
            merge_result = _static_validate_merge()

    _print_report(member_results, merge_result, mode=mode)


if __name__ == '__main__':
    main()
