import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import bcrypt
from db import get_conn, execute, execute_last_id
from datetime import datetime, date, timedelta
import random


def seed():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # ─── HOSPITAL ───
            cur.execute("""
                INSERT INTO Hospital (Name, Address, Phone, Email, EstablishedYear)
                VALUES (%s, %s, %s, %s, %s)
            """, ('City General Hospital', '123 Main St, Cairo', '+20-2-12345678',
                  'info@citygeneral.com', 1990))
            hospital_id = cur.lastrowid

            # ─── PATIENTS ───
            patients = [
                ('123-45-6789', 'P-001', 'Ahmed', 'Hassan', '10 Tahrir Sq, Cairo',
                 date(1985, 3, 15), 'M'),
                ('234-56-7890', 'P-002', 'Sara', 'Ali', '25 Zamalek St, Cairo',
                 date(1992, 7, 22), 'F'),
                ('345-67-8901', 'P-003', 'Mohamed', 'Omar', '5 Nasr Rd, Alexandria',
                 date(1978, 11, 2), 'M'),
                ('456-78-9012', 'P-004', 'Fatima', 'Khalid', '15 Maadi Ave, Cairo',
                 date(2000, 1, 30), 'F'),
                ('567-89-0123', 'P-005', 'Youssef', 'Nabil', '3 Hurghada St, Red Sea',
                 date(1965, 9, 14), 'M'),
            ]

            patient_ids = {}
            for ssn, pnum, fn, ln, addr, bd, sx in patients:
                cur.execute("""
                    INSERT INTO Patient (SSN, PatientNumber, FirstName, LastName,
                                         Address, BirthDate, Sex)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (ssn, pnum, fn, ln, addr, bd, sx))
                patient_ids[fn + ln] = cur.lastrowid

            # ─── PATIENT PHONE ───
            phones = [
                (patient_ids['AhmedHassan'], '+20-100-111-1111'),
                (patient_ids['AhmedHassan'], '+20-100-111-1112'),
                (patient_ids['SaraAli'], '+20-100-222-2221'),
                (patient_ids['MohamedOmar'], '+20-100-333-3331'),
                (patient_ids['FatimaKhalid'], '+20-100-444-4441'),
                (patient_ids['YoussefNabil'], '+20-100-555-5551'),
            ]
            for pid, ph in phones:
                cur.execute("INSERT INTO Patient_Phone (PatientID, Phone) VALUES (%s, %s)",
                            (pid, ph))

            # ─── PAYMENTS ───
            payments = []
            for i in range(5):
                amt = round(random.uniform(50, 500), 2)
                cur.execute("""
                    INSERT INTO Payment (Amount, PaymentMethod, Status)
                    VALUES (%s, %s, %s)
                """, (amt, random.choice(['Cash', 'Card', 'Online']),
                      random.choice(['Paid', 'Pending'])))
                payments.append(cur.lastrowid)

            # ─── MEDICATIONS ───
            meds = [
                'Paracetamol', 'Ibuprofen', 'Amoxicillin', 'Omeprazole',
                'Metformin', 'Atorvastatin', 'Lisinopril', 'Salbutamol',
                'Diazepam', 'Morphine'
            ]
            med_ids = {}
            for m in meds:
                cur.execute("INSERT INTO Medication (Name, Description) VALUES (%s, %s)",
                            (m, f'{m} description'))
                med_ids[m] = cur.lastrowid

            # ─── USERS (staff) ───
            # hash passwords
            users_data = [
                ('admin', 'admin123', 'admin@hospital.com', 'Admin', None),
                ('doctor1', 'doc123', 'doctor1@hospital.com', 'Doctor', None),
                ('doctor2', 'doc123', 'doctor2@hospital.com', 'Doctor', None),
                ('nurse1', 'nurse123', 'nurse1@hospital.com', 'Nurse', None),
                ('nurse2', 'nurse123', 'nurse2@hospital.com', 'Nurse', None),
                ('patient1', 'pat123', 'patient1@email.com', 'Patient', patient_ids['AhmedHassan']),
                ('patient2', 'pat123', 'patient2@email.com', 'Patient', patient_ids['SaraAli']),
            ]
            user_ids = {}
            for uname, pw, email, role, pid in users_data:
                pwhash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
                cur.execute("""
                    INSERT INTO Users (Username, PasswordHash, Email, Role, PatientID)
                    VALUES (%s, %s, %s, %s, %s)
                """, (uname, pwhash, email, role, pid))
                user_ids[uname] = cur.lastrowid

            # ─── EMPLOYEES ───
            employees = [
                ('doctor1', 'Khaled', 'Mostafa', date(1980, 5, 10), 'M',
                 '111-11-1111', date(2010, 3, 1), 'Senior Physician', 'Doctor'),
                ('doctor2', 'Mona', 'Shawky', date(1985, 8, 22), 'F',
                 '222-22-2222', date(2012, 6, 15), 'Physician', 'Doctor'),
                ('nurse1', 'Huda', 'Fahmy', date(1990, 1, 15), 'F',
                 '333-33-3333', date(2015, 9, 1), 'Head Nurse', 'Nurse'),
                ('nurse2', 'Samir', 'Gamal', date(1992, 4, 8), 'M',
                 '444-44-4444', date(2017, 2, 10), 'Staff Nurse', 'Nurse'),
                ('admin', 'Admin', 'User', date(1988, 12, 20), 'M',
                 '555-55-5555', date(2011, 1, 1), 'System Admin', 'Admin'),
            ]
            emp_ids = {}
            for uname, fn, ln, bd, sx, ssn, hd, jt, etype in employees:
                cur.execute("""
                    INSERT INTO Employee (UserID, FirstName, LastName, BirthDate,
                                          Sex, SSN, HireDate, JobTitle, EmployeeType)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_ids[uname], fn, ln, bd, sx, ssn, hd, jt, etype))
                emp_ids[uname] = cur.lastrowid

            # Link EmployeeID back to Users
            for uname, eid in emp_ids.items():
                cur.execute("UPDATE Users SET EmployeeID = %s WHERE UserID = %s",
                            (eid, user_ids[uname]))

            # ─── DEPARTMENT ───
            depts = [
                ('Emergency Department', 'ER', hospital_id, None, None),
                ('Cardiology', 'CARD', hospital_id, None, None),
                ('Pediatrics', 'PED', hospital_id, None, None),
                ('Orthopedics', 'ORTH', hospital_id, None, None),
            ]
            dept_ids = {}
            for name, code, hid, _, _ in depts:
                cur.execute("""
                    INSERT INTO Department (Name, Code, HospitalID)
                    VALUES (%s, %s, %s)
                """, (name, code, hid))
                dept_ids[name] = cur.lastrowid

            # ─── DOCTOR ───
            doctor_info = [
                ('doctor1', dept_ids['Emergency Department'], 'Emergency Medicine', 'MD', date(2010, 3, 1)),
                ('doctor2', dept_ids['Cardiology'], 'Cardiology', 'MD', date(2012, 6, 15)),
            ]
            doc_ids = {}
            for uname, did, msa, deg, jd in doctor_info:
                cur.execute("""
                    INSERT INTO Doctor (EmployeeID, DepartmentID, MajorScientificArea, Degree, JoinDate)
                    VALUES (%s, %s, %s, %s, %s)
                """, (emp_ids[uname], did, msa, deg, jd))
                doc_ids[uname] = emp_ids[uname]  # PK inherited from Employee

            # ─── NURSE ───
            nurse_info = [
                ('nurse1', dept_ids['Emergency Department'], date(2015, 9, 1)),
                ('nurse2', dept_ids['Pediatrics'], date(2017, 2, 10)),
            ]
            nurse_ids = {}
            for uname, did, jd in nurse_info:
                cur.execute("""
                    INSERT INTO Nurse (EmployeeID, DepartmentID, JoinDate)
                    VALUES (%s, %s, %s)
                """, (emp_ids[uname], did, jd))
                nurse_ids[uname] = emp_ids[uname]  # PK inherited from Employee

            # ─── ADMIN ───
            cur.execute("INSERT INTO Admin (EmployeeID) VALUES (%s)", (emp_ids['admin'],))
            admin_id = emp_ids['admin']  # PK inherited from Employee

            # Set ChairmanDoctorID for departments
            cur.execute("""
                UPDATE Department SET ChairmanDoctorID = %s WHERE DepartmentID = %s
            """, (doc_ids['doctor1'], dept_ids['Emergency Department']))
            cur.execute("""
                UPDATE Department SET ChairmanDoctorID = %s WHERE DepartmentID = %s
            """, (doc_ids['doctor2'], dept_ids['Cardiology']))

            # ─── DEPARTMENT LOCATION ───
            locs = [
                (dept_ids['Emergency Department'], 'Floor 1, Wing A, City General Hospital', 30.0444, 31.2357),
                (dept_ids['Cardiology'], 'Floor 2, Wing B, City General Hospital', 30.0445, 31.2358),
                (dept_ids['Pediatrics'], 'Floor 3, Wing A, City General Hospital', 30.0446, 31.2359),
                (dept_ids['Orthopedics'], 'Floor 1, Wing C, City General Hospital', 30.0447, 31.2360),
            ]
            loc_ids = {}
            for did, addr, lat, lng in locs:
                cur.execute("""
                    INSERT INTO DepartmentLocation (DepartmentID, Address, Latitude, Longitude)
                    VALUES (%s, %s, %s, %s)
                """, (did, addr, lat, lng))
                loc_ids[did] = cur.lastrowid

            # ─── BED ───
            bed_ids = []
            for i in range(1, 11):
                cur.execute("""
                    INSERT INTO Bed (RoomNumber, LocationID, BedType, Status)
                    VALUES (%s, %s, %s, %s)
                """, (f'ER-{i:03d}', loc_ids[dept_ids['Emergency Department']],
                      'Stretcher' if i <= 4 else 'Regular Bed',
                      'Available'))
                bed_ids.append(cur.lastrowid)

            # ─── APPOINTMENTS ───
            appt_data = [
                (patient_ids['AhmedHassan'], doc_ids['doctor1'], payments[0],
                 datetime(2025, 6, 1, 10, 0), 'Scheduled', 'Booked', 'Routine checkup'),
                (patient_ids['SaraAli'], doc_ids['doctor2'], payments[1],
                 datetime(2025, 6, 2, 14, 30), 'Scheduled', 'Walk-in', 'Chest pain'),
                (patient_ids['MohamedOmar'], doc_ids['doctor1'], None,
                 datetime(2025, 5, 28, 9, 0), 'Completed', 'Booked', 'Follow-up'),
                (patient_ids['FatimaKhalid'], doc_ids['doctor2'], payments[2],
                 datetime(2025, 5, 25, 11, 0), 'Completed', 'Booked', 'Annual physical'),
                (patient_ids['YoussefNabil'], doc_ids['doctor1'], payments[3],
                 datetime(2025, 5, 20, 16, 0), 'Cancelled', 'Booked', 'Rescheduled'),
            ]
            for pid, did, payid, dt, status, atype, notes in appt_data:
                cur.execute("""
                    INSERT INTO Appointment (PatientID, DoctorID, PaymentID,
                                             AppointmentDateTime, Status, Type, Notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (pid, did, payid, dt, status, atype, notes))

            # ─── EMERGENCY VISITS ───
            visits = [
                (patient_ids['AhmedHassan'], None, bed_ids[0],
                 datetime(2025, 5, 20, 8, 30), None, None),
                (patient_ids['SaraAli'], None, bed_ids[1],
                 datetime(2025, 5, 21, 14, 0), None, None),
                (patient_ids['MohamedOmar'], None, None,
                 datetime(2025, 5, 19, 22, 15),
                 datetime(2025, 5, 20, 6, 0), 'Discharged'),
                (patient_ids['FatimaKhalid'], None, None,
                 datetime(2025, 5, 18, 11, 0),
                 datetime(2025, 5, 18, 16, 30), 'Discharged'),
            ]
            visit_ids = []
            for pid, tid, bid, adm, ddt, disp in visits:
                cur.execute("""
                    INSERT INTO EmergencyVisit (PatientID, TriageID, BedID,
                                                AdmissionDateTime, DischargeDateTime, Disposition)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (pid, tid, bid, adm, ddt, disp))
                visit_ids.append(cur.lastrowid)

            # Mark occupied beds
            cur.execute("UPDATE Bed SET Status = 'Occupied' WHERE BedID IN (%s, %s)",
                        (bed_ids[0], bed_ids[1]))

            # ─── TRIAGE ───
            triages = [
                (patient_ids['AhmedHassan'], nurse_ids['nurse1'],
                 datetime(2025, 5, 20, 8, 35), 'Severe abdominal pain', 2,
                 '140/90', 110, 38.5),
                (patient_ids['SaraAli'], nurse_ids['nurse1'],
                 datetime(2025, 5, 21, 14, 5), 'Chest pain and shortness of breath', 1,
                 '160/100', 120, 37.2),
                (patient_ids['MohamedOmar'], nurse_ids['nurse2'],
                 datetime(2025, 5, 19, 22, 20), 'Laceration on left arm from accident', 3,
                 '120/80', 85, 36.8),
            ]
            triage_ids = []
            for pid, nid, dt, cc, tl, bp, hr, tmp in triages:
                cur.execute("""
                    INSERT INTO Triage (PatientID, NurseID, DateTime, ChiefComplaint,
                                        TriageLevel, BloodPressure, HeartRate, Temperature)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (pid, nid, dt, cc, tl, bp, hr, tmp))
                triage_ids.append(cur.lastrowid)

            # Link TriageID to EmergencyVisit
            for i, tid in enumerate(triage_ids):
                if i < len(visit_ids):
                    cur.execute("UPDATE EmergencyVisit SET TriageID = %s WHERE VisitID = %s",
                                (tid, visit_ids[i]))

            # ─── PRESCRIPTIONS ───
            presc = [
                (doc_ids['doctor1'], patient_ids['AhmedHassan'], visit_ids[0],
                 date(2025, 5, 20)),
                (doc_ids['doctor2'], patient_ids['SaraAli'], visit_ids[1],
                 date(2025, 5, 21)),
                (doc_ids['doctor1'], patient_ids['MohamedOmar'], visit_ids[2],
                 date(2025, 5, 20)),
            ]
            presc_ids = []
            for did, pid, vid, dt in presc:
                cur.execute("""
                    INSERT INTO Prescription (DoctorID, PatientID, VisitID, PrescriptionDate)
                    VALUES (%s, %s, %s, %s)
                """, (did, pid, vid, dt))
                presc_ids.append(cur.lastrowid)

            # ─── PRESCRIPTION DETAILS ───
            details = [
                (presc_ids[0], med_ids['Paracetamol'], 'Take with food', '500mg', 3,
                 date(2025, 5, 20), date(2025, 5, 27)),
                (presc_ids[0], med_ids['Omeprazole'], 'Before breakfast', '20mg', 1,
                 date(2025, 5, 20), date(2025, 6, 3)),
                (presc_ids[1], med_ids['Atorvastatin'], 'Take at bedtime', '10mg', 1,
                 date(2025, 5, 21), date(2025, 8, 21)),
                (presc_ids[1], med_ids['Lisinopril'], 'Take in the morning', '5mg', 1,
                 date(2025, 5, 21), date(2025, 8, 21)),
                (presc_ids[2], med_ids['Amoxicillin'], 'Take with water', '250mg', 3,
                 date(2025, 5, 20), date(2025, 5, 27)),
            ]
            for presc_id, med_id, dirs, dose, tpd, sd, ed in details:
                cur.execute("""
                    INSERT INTO PrescriptionDetail (PrescriptionID, MedicationID, Directions,
                                                    Dosage, TimesPerDay, StartDate, EndDate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (presc_id, med_id, dirs, dose, tpd, sd, ed))

            # ─── EXAMINATIONS ───
            exams = [
                (doc_ids['doctor1'], patient_ids['AhmedHassan'], visit_ids[0],
                 datetime(2025, 5, 20, 9, 0), 1.5),
                (doc_ids['doctor2'], patient_ids['SaraAli'], visit_ids[1],
                 datetime(2025, 5, 21, 14, 30), 2.0),
                (doc_ids['doctor1'], patient_ids['MohamedOmar'], visit_ids[2],
                 datetime(2025, 5, 19, 22, 45), 1.0),
            ]
            for did, pid, vid, dt, hrs in exams:
                cur.execute("""
                    INSERT INTO Examination (DoctorID, PatientID, VisitID,
                                             ExaminationDate, HoursSpent)
                    VALUES (%s, %s, %s, %s, %s)
                """, (did, pid, vid, dt, hrs))

            # ─── DOCUMENTS ───
            docs = [
                (patient_ids['AhmedHassan'], visit_ids[0], 'lab_results.pdf',
                 '/docs/lab_results_001.pdf', 'Blood test results'),
                (patient_ids['SaraAli'], visit_ids[1], 'ecg_report.pdf',
                 '/docs/ecg_002.pdf', 'ECG report'),
                (patient_ids['MohamedOmar'], visit_ids[2], 'xray_arm.pdf',
                 '/docs/xray_003.pdf', 'X-ray of left arm'),
            ]
            for pid, vid, fname, fpath, desc in docs:
                cur.execute("""
                    INSERT INTO Document (PatientID, VisitID, FileName, FilePath, Description)
                    VALUES (%s, %s, %s, %s, %s)
                """, (pid, vid, fname, fpath, desc))

        conn.commit()
        print("Seed data inserted successfully!")
        print(f"  Hospital: {hospital_id}")
        print(f"  Patients: {len(patients)}")
        print(f"  Users: {len(users_data)}")
        print(f"  Employees: {len(employees)}")
        print(f"  Doctors: {len(doctor_info)}")
        print(f"  Nurses: {len(nurse_info)}")
        print(f"  Visits: {len(visit_ids)}")
        print(f"  Prescriptions: {len(presc_ids)}")

    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    seed()
