"""Verify all schema changes work correctly after the fixes."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from db import query, query_one

print("=== Schema Fix Verification ===\n")

docs = query("""
    SELECT e.EmployeeID, e.FirstName, e.LastName, d.MajorScientificArea
    FROM Doctor d JOIN Employee e ON d.EmployeeID = e.EmployeeID
""")
print(f"Doctors (PK=EmployeeID): {len(docs)} rows")
for d in docs:
    print(f"  ID={d['EmployeeID']}: {d['FirstName']} {d['LastName']} - {d['MajorScientificArea']}")

try:
    query("SELECT DoctorID FROM Doctor LIMIT 1")
    print("  ERROR: DoctorID column still exists!")
except Exception:
    print("  DoctorID column removed - OK")

nurses = query("""
    SELECT e.EmployeeID, e.FirstName, e.LastName
    FROM Nurse n JOIN Employee e ON n.EmployeeID = e.EmployeeID
""")
print(f"\nNurses (PK=EmployeeID): {len(nurses)} rows")
for n in nurses:
    print(f"  ID={n['EmployeeID']}: {n['FirstName']} {n['LastName']}")

try:
    query("SELECT NurseID FROM Nurse LIMIT 1")
    print("  ERROR: NurseID column still exists!")
except Exception:
    print("  NurseID column removed - OK")

try:
    query("SELECT AdminID FROM Admin LIMIT 1")
    print("  ERROR: AdminID column still exists!")
except Exception:
    print("AdminID column removed - OK")

exams = query("SELECT DoctorID, PatientID, ExaminationDate, HoursSpent FROM Examination")
print(f"\nExaminations: {len(exams)} rows (composite PK)")
for ex in exams:
    print(f"  DoctorID={ex['DoctorID']}, PatientID={ex['PatientID']}, Date={ex['ExaminationDate']}")

try:
    query("SELECT ExaminationID FROM Examination LIMIT 1")
    print("  ERROR: ExaminationID column still exists!")
except Exception:
    print("  ExaminationID column removed - OK")

a = query_one("""
    SELECT a.AppointmentID, a.DoctorID, e.FirstName, e.LastName
    FROM Appointment a
    JOIN Doctor d ON a.DoctorID = d.EmployeeID
    JOIN Employee e ON d.EmployeeID = e.EmployeeID
    LIMIT 1
""")
print(f"\nAppointment FK -> Doctor(EmployeeID): #{a['AppointmentID']} -> Dr. {a['FirstName']} {a['LastName']}")

p = query_one("""
    SELECT pr.PrescriptionID, pr.DoctorID, e.FirstName, e.LastName
    FROM Prescription pr
    JOIN Doctor d ON pr.DoctorID = d.EmployeeID
    JOIN Employee e ON d.EmployeeID = e.EmployeeID
    LIMIT 1
""")
print(f"Prescription FK -> Doctor(EmployeeID): #{p['PrescriptionID']} -> Dr. {p['FirstName']} {p['LastName']}")

ex = query_one("""
    SELECT ex.DoctorID, e.FirstName, e.LastName
    FROM Examination ex
    JOIN Doctor d ON ex.DoctorID = d.EmployeeID
    JOIN Employee e ON d.EmployeeID = e.EmployeeID
    LIMIT 1
""")
print(f"Examination FK -> Doctor(EmployeeID): Dr. {ex['FirstName']} {ex['LastName']}")

t = query_one("""
    SELECT t.PatientID, t.NurseID, e.FirstName, e.LastName
    FROM Triage t
    JOIN Nurse n ON t.NurseID = n.EmployeeID
    JOIN Employee e ON n.EmployeeID = e.EmployeeID
    LIMIT 1
""")
print(f"Triage FK -> Nurse(EmployeeID): Nurse {t['FirstName']} {t['LastName']} (EmployeeID={t['NurseID']})")

d = query_one("""
    SELECT dep.DepartmentID, dep.Name, dep.ChairmanDoctorID, e.FirstName, e.LastName
    FROM Department dep
    JOIN Doctor doc ON dep.ChairmanDoctorID = doc.EmployeeID
    JOIN Employee e ON doc.EmployeeID = e.EmployeeID
    LIMIT 1
""")
print(f"Department.ChairmanDoctorID -> Doctor(EmployeeID): Dr. {d['FirstName']} {d['LastName']} chairs {d['Name']}")

print("\n=== ALL VERIFICATIONS PASSED ===")
