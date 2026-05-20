import streamlit as st
import bcrypt
import pandas as pd
from datetime import datetime, date
from db import query, query_one, execute, execute_last_id

st.set_page_config(page_title="ED HIS - Emergency Department", layout="wide")

# ─── Session State Init ───
for key in ('authenticated', 'user_id', 'username', 'role', 'employee_id', 'patient_id'):
    if key not in st.session_state:
        st.session_state[key] = None if key != 'authenticated' else False

PAGES = ['Dashboard', 'Patients', 'Emergency Visits', 'Appointments', 'Pharmacy', 'Staff', 'Admin']

ROLE_PAGES = {
    'Admin':   PAGES,
    'Doctor':  [p for p in PAGES if p != 'Admin'],
    'Nurse':   ['Dashboard', 'Patients', 'Emergency Visits', 'Appointments', 'Staff'],
    'Patient': ['Dashboard', 'Appointments'],
}


# ─── Auth ───
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🏥 Emergency Department HIS")
        st.markdown("---")
        with st.form("login_form"):
            username = st.text_input("Username").strip()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password")
                    return
                user = query_one(
                    "SELECT UserID, Username, PasswordHash, Role, EmployeeID, PatientID FROM Users WHERE Username = %s",
                    (username,)
                )
                if user and bcrypt.checkpw(password.encode(), user['PasswordHash'].encode()):
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['UserID']
                    st.session_state.username = user['Username']
                    st.session_state.role = user['Role']
                    st.session_state.employee_id = user['EmployeeID']
                    st.session_state.patient_id = user['PatientID']
                    st.session_state.page = 'Dashboard'
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("---")
        st.caption("Test accounts: `admin` / `admin123` · `doctor1` / `doc123` · `nurse1` / `nurse123` · `patient1` / `pat123`")


# ─── Sidebar ───
def sidebar_nav():
    with st.sidebar:
        st.title(f"🏥 ED HIS")
        st.caption(f"👤 {st.session_state.username} · **{st.session_state.role}**")
        st.divider()

        allowed = ROLE_PAGES.get(st.session_state.role, ['Dashboard'])
        for page in allowed:
            if st.button(page, use_container_width=True,
                         type="primary" if st.session_state.get('page') == page else "secondary"):
                st.session_state.page = page
                st.rerun()

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─── Helper ───
def role_required(*roles):
    if st.session_state.role not in roles:
        st.error("You do not have permission to access this page.")
        st.stop()


def render_table(df, title=None):
    if title:
        st.subheader(title)
    if df.empty:
        st.info("No data found.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════════
#  PAGES
# ════════════════════════════════════════════════════════════════

def page_dashboard():
    st.header("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        c = query_one("SELECT COUNT(*) c FROM Patient")['c']
        st.metric("Total Patients", c)
    with col2:
        c = query_one("SELECT COUNT(*) c FROM EmergencyVisit WHERE DischargeDateTime IS NULL")['c']
        st.metric("Active Visits", c)
    with col3:
        c = query_one("SELECT COUNT(*) c FROM Bed WHERE Status = 'Occupied'")['c']
        t = query_one("SELECT COUNT(*) c FROM Bed")['c']
        st.metric("Beds Occupied", f"{c}/{t}")
    with col4:
        c = query_one("SELECT COUNT(*) c FROM Employee")['c']
        st.metric("Staff Count", c)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        visits = query("""
            SELECT v.VisitID, p.FirstName, p.LastName, v.AdmissionDateTime, v.Disposition
            FROM EmergencyVisit v
            JOIN Patient p ON v.PatientID = p.PatientID
            WHERE v.DischargeDateTime IS NULL
            ORDER BY v.AdmissionDateTime DESC
            LIMIT 10
        """)
        render_table(pd.DataFrame(visits), "Active Emergency Visits")

    with col2:
        appts = query("""
            SELECT a.AppointmentID, p.FirstName, p.LastName, a.AppointmentDateTime, a.Status
            FROM Appointment a
            JOIN Patient p ON a.PatientID = p.PatientID
            ORDER BY a.AppointmentDateTime DESC
            LIMIT 10
        """)
        render_table(pd.DataFrame(appts), "Recent Appointments")


def page_patients():
    st.header("👤 Patients")
    role_required('Admin', 'Doctor', 'Nurse')

    tab1, tab2 = st.tabs(["📋 View Patients", "➕ Add Patient"])

    with tab1:
        search = st.text_input("Search by name or SSN", placeholder="Type to search...")
        if search:
            patients = query("""
                SELECT PatientID, SSN, PatientNumber, FirstName, LastName,
                       Sex, BirthDate, Address, MedicalHistory
                FROM Patient
                WHERE FirstName LIKE %s OR LastName LIKE %s OR SSN LIKE %s
                ORDER BY LastName
            """, (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            patients = query("""
                SELECT PatientID, SSN, PatientNumber, FirstName, LastName,
                       Sex, BirthDate, Address
                FROM Patient ORDER BY LastName
            """)

        df = pd.DataFrame(patients)
        render_table(df)

        if not df.empty:
            selected = st.selectbox("Select a patient to view details",
                                    options=df['PatientID'].tolist(),
                                    format_func=lambda x: f"{df[df['PatientID']==x].iloc[0]['FirstName']} {df[df['PatientID']==x].iloc[0]['LastName']}")
            if selected:
                p = query_one("SELECT * FROM Patient WHERE PatientID = %s", (selected,))
                if p:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**SSN:** {p['SSN']}")
                        st.write(f"**Patient #:** {p['PatientNumber']}")
                        st.write(f"**Name:** {p['FirstName']} {p['LastName']}")
                        st.write(f"**Sex:** {p['Sex']}")
                    with col2:
                        st.write(f"**Birth Date:** {p['BirthDate']}")
                        st.write(f"**Address:** {p['Address']}")
                        st.write(f"**Medical History:** {p['MedicalHistory'] or 'N/A'}")

                    phones = query("SELECT Phone FROM Patient_Phone WHERE PatientID = %s", (selected,))
                    if phones:
                        st.write("**Phones:** " + ", ".join(ph['Phone'] for ph in phones))

                    # Show patient's visits
                    pvisits = query("""
                        SELECT VisitID, AdmissionDateTime, DischargeDateTime, Disposition
                        FROM EmergencyVisit WHERE PatientID = %s ORDER BY AdmissionDateTime DESC
                    """, (selected,))
                    if pvisits:
                        render_table(pd.DataFrame(pvisits), "Visit History")

    with tab2:
        role_required('Admin', 'Doctor')
        with st.form("add_patient"):
            col1, col2 = st.columns(2)
            with col1:
                ssn = st.text_input("SSN *")
                pnum = st.text_input("Patient Number *")
                fn = st.text_input("First Name *")
                ln = st.text_input("Last Name *")
            with col2:
                sex = st.selectbox("Sex *", ['M', 'F'])
                bd = st.date_input("Birth Date", value=None)
                addr = st.text_area("Address")
                medhist = st.text_area("Medical History")

            if st.form_submit_button("Add Patient"):
                if not all([ssn, pnum, fn, ln]):
                    st.error("SSN, Patient Number, First Name, Last Name, and Sex are required")
                else:
                    try:
                        pid = execute_last_id("""
                            INSERT INTO Patient (SSN, PatientNumber, FirstName, LastName, Sex, BirthDate, Address, MedicalHistory)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (ssn, pnum, fn, ln, sex, bd, addr, medhist or None))
                        st.success(f"Patient added with ID: {pid}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")


def page_visits():
    st.header("🚑 Emergency Visits")
    role_required('Admin', 'Doctor', 'Nurse')

    tab1, tab2, tab3 = st.tabs(["📋 Active Visits", "➕ Admit Patient", "📜 Visit History"])

    with tab1:
        visits = query("""
            SELECT v.VisitID, p.FirstName, p.LastName, v.AdmissionDateTime,
                   t.TriageLevel, t.ChiefComplaint, b.RoomNumber, b.Status as BedStatus
            FROM EmergencyVisit v
            JOIN Patient p ON v.PatientID = p.PatientID
            LEFT JOIN Triage t ON v.TriageID = t.TriageID
            LEFT JOIN Bed b ON v.BedID = b.BedID
            WHERE v.DischargeDateTime IS NULL
            ORDER BY t.TriageLevel ASC, v.AdmissionDateTime ASC
        """)
        df = pd.DataFrame(visits)
        render_table(df)

        if st.session_state.role in ('Admin', 'Doctor') and not df.empty:
            st.subheader("Discharge Patient")
            visit_id = st.selectbox("Select Visit to Discharge",
                                    options=df['VisitID'].tolist(),
                                    format_func=lambda x: f"#{x} - {df[df['VisitID']==x].iloc[0]['FirstName']} {df[df['VisitID']==x].iloc[0]['LastName']}")
            disp = st.selectbox("Disposition", ['Discharged', 'Transferred', 'Left Without Being Seen'])
            if st.button("Discharge Patient"):
                execute("""
                    UPDATE EmergencyVisit SET DischargeDateTime = NOW(), Disposition = %s WHERE VisitID = %s
                """, (disp, visit_id))
                execute("UPDATE Bed SET Status = 'Cleaning' WHERE BedID = (SELECT BedID FROM EmergencyVisit WHERE VisitID = %s)", (visit_id,))
                st.success(f"Visit #{visit_id} discharged")
                st.rerun()

    with tab2:
        role_required('Admin', 'Doctor', 'Nurse')
        patients = query("SELECT PatientID, FirstName, LastName, PatientNumber FROM Patient ORDER BY LastName")
        beds = query("SELECT BedID, RoomNumber FROM Bed WHERE Status = 'Available'")

        if not patients:
            st.warning("No patients available. Add a patient first.")
        else:
            with st.form("admit_form"):
                pid = st.selectbox("Patient *", options=[p['PatientID'] for p in patients],
                                   format_func=lambda x: f"{next(p for p in patients if p['PatientID']==x)['FirstName']} {next(p for p in patients if p['PatientID']==x)['LastName']} ({next(p for p in patients if p['PatientID']==x)['PatientNumber']})")
                bid = st.selectbox("Bed (optional)", options=[None] + [b['BedID'] for b in beds],
                                   format_func=lambda x: "None" if x is None else f"Bed #{next(b for b in beds if b['BedID']==x)['RoomNumber']}")
                if st.form_submit_button("Admit Patient"):
                    vid = execute_last_id("""
                        INSERT INTO EmergencyVisit (PatientID, AdmissionDateTime, BedID)
                        VALUES (%s, NOW(), %s)
                    """, (pid, bid))
                    if bid:
                        execute("UPDATE Bed SET Status = 'Occupied' WHERE BedID = %s", (bid,))
                    st.success(f"Patient admitted: Visit #{vid}")
                    st.rerun()

    with tab3:
        visits_all = query("""
            SELECT v.VisitID, p.FirstName, p.LastName, v.AdmissionDateTime,
                   v.DischargeDateTime, v.Disposition, t.TriageLevel
            FROM EmergencyVisit v
            JOIN Patient p ON v.PatientID = p.PatientID
            LEFT JOIN Triage t ON v.TriageID = t.TriageID
            ORDER BY v.AdmissionDateTime DESC
            LIMIT 50
        """)
        render_table(pd.DataFrame(visits_all))


def page_appointments():
    st.header("📅 Appointments")
    role_required('Admin', 'Doctor', 'Nurse', 'Patient')

    tab1, tab2 = st.tabs(["📋 View Appointments", "➕ New Appointment"])

    with tab1:
        if st.session_state.role == 'Patient':
            appts = query("""
                SELECT a.AppointmentID, a.AppointmentDateTime, a.Status, a.Type,
                       CONCAT(doc_e.FirstName, ' ', doc_e.LastName) AS Doctor
                FROM Appointment a
                JOIN Doctor d ON a.DoctorID = d.EmployeeID
                JOIN Employee doc_e ON d.EmployeeID = doc_e.EmployeeID
                WHERE a.PatientID = %s
                ORDER BY a.AppointmentDateTime DESC
            """, (st.session_state.patient_id,))
        else:
            status_filter = st.selectbox("Filter by status", ['All', 'Scheduled', 'Completed', 'Cancelled', 'No-Show'])
            if status_filter == 'All':
                appts = query("""
                    SELECT a.AppointmentID, p.FirstName, p.LastName, a.AppointmentDateTime,
                           a.Status, a.Type, CONCAT(e.FirstName, ' ', e.LastName) AS Doctor
                    FROM Appointment a
                    JOIN Patient p ON a.PatientID = p.PatientID
                    JOIN Doctor d ON a.DoctorID = d.EmployeeID
                    JOIN Employee e ON d.EmployeeID = e.EmployeeID
                    ORDER BY a.AppointmentDateTime DESC
                    LIMIT 50
                """)
            else:
                appts = query("""
                    SELECT a.AppointmentID, p.FirstName, p.LastName, a.AppointmentDateTime,
                           a.Status, a.Type, CONCAT(e.FirstName, ' ', e.LastName) AS Doctor
                    FROM Appointment a
                    JOIN Patient p ON a.PatientID = p.PatientID
                    JOIN Doctor d ON a.DoctorID = d.EmployeeID
                    JOIN Employee e ON d.EmployeeID = e.EmployeeID
                    WHERE a.Status = %s
                    ORDER BY a.AppointmentDateTime DESC
                """, (status_filter,))

        render_table(pd.DataFrame(appts))

        if st.session_state.role in ('Admin', 'Doctor', 'Nurse') and appts:
            st.subheader("Update Status")
            appt_id = st.selectbox("Appointment", options=[a['AppointmentID'] for a in appts],
                                   format_func=lambda x: f"#{x}")
            new_status = st.selectbox("New Status", ['Scheduled', 'Completed', 'Cancelled', 'No-Show'])
            if st.button("Update Status"):
                execute("UPDATE Appointment SET Status = %s WHERE AppointmentID = %s", (new_status, appt_id))
                st.success(f"Appointment #{appt_id} updated to {new_status}")
                st.rerun()

    with tab2:
        role_required('Admin', 'Doctor', 'Nurse')
        patients = query("SELECT PatientID, FirstName, LastName FROM Patient ORDER BY LastName")
        doctors = query("""
            SELECT d.EmployeeID AS DoctorID, e.FirstName, e.LastName, dep.Name AS Dept
            FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Department dep ON d.DepartmentID = dep.DepartmentID
            ORDER BY e.LastName
        """)

        if not patients or not doctors:
            st.warning("Need both patients and doctors to create an appointment.")
        else:
            with st.form("add_appointment"):
                pid = st.selectbox("Patient *", options=[p['PatientID'] for p in patients],
                                   format_func=lambda x: f"{next(p for p in patients if p['PatientID']==x)['FirstName']} {next(p for p in patients if p['PatientID']==x)['LastName']}")
                did = st.selectbox("Doctor *", options=[d['DoctorID'] for d in doctors],
                                   format_func=lambda x: f"Dr. {next(d for d in doctors if d['DoctorID']==x)['FirstName']} {next(d for d in doctors if d['DoctorID']==x)['LastName']} ({next(d for d in doctors if d['DoctorID']==x)['Dept']})")
                dt = st.datetime_input("Appointment DateTime *")
                atype = st.selectbox("Type *", ['Walk-in', 'Booked'])
                notes = st.text_area("Notes")
                if st.form_submit_button("Create Appointment"):
                    if dt is None:
                        st.error("Please select a date/time")
                    else:
                        aid = execute_last_id("""
                            INSERT INTO Appointment (PatientID, DoctorID, AppointmentDateTime, Type, Status, Notes)
                            VALUES (%s, %s, %s, %s, 'Scheduled', %s)
                        """, (pid, did, dt, atype, notes or None))
                        st.success(f"Appointment #{aid} created!")
                        st.rerun()


def page_pharmacy():
    st.header("💊 Pharmacy")
    role_required('Admin', 'Doctor', 'Nurse')

    tab1, tab2, tab3 = st.tabs(["📋 Medications", "📜 Prescriptions", "➕ New Prescription"])

    with tab1:
        meds = query("SELECT * FROM Medication ORDER BY Name")
        render_table(pd.DataFrame(meds))

        if st.session_state.role == 'Admin':
            with st.expander("Add New Medication"):
                with st.form("add_med"):
                    mname = st.text_input("Medication Name *")
                    mdesc = st.text_area("Description")
                    if st.form_submit_button("Add"):
                        if mname:
                            execute("INSERT INTO Medication (Name, Description) VALUES (%s, %s)", (mname, mdesc or None))
                            st.success(f"Added {mname}")
                            st.rerun()

    with tab2:
        prescs = query("""
            SELECT pr.PrescriptionID, CONCAT(p.FirstName, ' ', p.LastName) AS Patient,
                   CONCAT(e.FirstName, ' ', e.LastName) AS Doctor, pr.PrescriptionDate
            FROM Prescription pr
            JOIN Patient p ON pr.PatientID = p.PatientID
            JOIN Doctor d ON pr.DoctorID = d.EmployeeID
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            ORDER BY pr.PrescriptionDate DESC
            LIMIT 50
        """)
        df = pd.DataFrame(prescs)
        render_table(df)

        if not df.empty:
            sel = st.selectbox("View Prescription Details",
                               options=df['PrescriptionID'].tolist(),
                               format_func=lambda x: f"#{x}")
            details = query("""
                SELECT pd.PrescriptionDetailID, m.Name AS Medication, pd.Dosage,
                       pd.TimesPerDay, pd.Directions, pd.StartDate, pd.EndDate
                FROM PrescriptionDetail pd
                JOIN Medication m ON pd.MedicationID = m.MedicationID
                WHERE pd.PrescriptionID = %s
            """, (sel,))
            render_table(pd.DataFrame(details), f"Prescription #{sel} Details")

    with tab3:
        role_required('Admin', 'Doctor')
        patients = query("SELECT PatientID, FirstName, LastName FROM Patient ORDER BY LastName")
        visits_q = query("""
            SELECT ev.VisitID, CONCAT(p.FirstName, ' ', p.LastName) AS Patient
            FROM EmergencyVisit ev
            JOIN Patient p ON ev.PatientID = p.PatientID
            WHERE ev.DischargeDateTime IS NULL
            ORDER BY ev.AdmissionDateTime DESC
        """)
        doctors = query("""
            SELECT d.EmployeeID AS DoctorID, e.FirstName, e.LastName FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
        """)
        meds = query("SELECT MedicationID, Name FROM Medication ORDER BY Name")

        with st.form("add_prescription"):
            col1, col2 = st.columns(2)
            with col1:
                pid = st.selectbox("Patient *", options=[p['PatientID'] for p in patients],
                                   format_func=lambda x: f"{next(p for p in patients if p['PatientID']==x)['FirstName']} {next(p for p in patients if p['PatientID']==x)['LastName']}")
                if st.session_state.role == 'Doctor':
                    did = next(d for d in doctors if d['DoctorID'] == doctors[0]['DoctorID'])['DoctorID']
                    auto_doctor = query_one("SELECT EmployeeID AS DoctorID FROM Doctor WHERE EmployeeID = %s", (st.session_state.employee_id,))
                    if auto_doctor:
                        did = auto_doctor['DoctorID']
                else:
                    did = st.selectbox("Doctor *", options=[d['DoctorID'] for d in doctors],
                                       format_func=lambda x: f"Dr. {next(d for d in doctors if d['DoctorID']==x)['FirstName']} {next(d for d in doctors if d['DoctorID']==x)['LastName']}")
            with col2:
                vid = st.selectbox("Visit (optional)", options=[None] + [v['VisitID'] for v in visits_q],
                                   format_func=lambda x: "None" if x is None else f"#{x} - {next(v for v in visits_q if v['VisitID']==x)['Patient']}")
                pr_date = st.date_input("Prescription Date", value=date.today())

            st.markdown("**Medications to prescribe:**")
            med_rows = st.number_input("Number of medications", min_value=1, max_value=5, value=1)
            med_details = []
            for i in range(med_rows):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    med = st.selectbox(f"Medication {i+1}", options=[m['MedicationID'] for m in meds],
                                       format_func=lambda x: next(m['Name'] for m in meds if m['MedicationID']==x),
                                       key=f"med_{i}")
                with col2:
                    dose = st.text_input(f"Dosage {i+1}", key=f"dose_{i}")
                with col3:
                    tpd = st.number_input(f"×/day {i+1}", min_value=1, max_value=10, value=3, key=f"tpd_{i}")
                with col4:
                    dur = st.number_input(f"Days {i+1}", min_value=1, max_value=90, value=7, key=f"dur_{i}")
                med_details.append((med, dose, tpd, dur))

            if st.form_submit_button("Create Prescription"):
                try:
                    presc_id = execute_last_id("""
                        INSERT INTO Prescription (DoctorID, PatientID, VisitID, PrescriptionDate)
                        VALUES (%s, %s, %s, %s)
                    """, (did, pid, vid or None, pr_date))

                    for med, dose, tpd, dur in med_details:
                        sd = pr_date
                        ed = date.fromordinal(pr_date.toordinal() + dur)
                        execute("""
                            INSERT INTO PrescriptionDetail (PrescriptionID, MedicationID, Dosage, TimesPerDay, StartDate, EndDate)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (presc_id, med, dose or None, tpd, sd, ed))

                    st.success(f"Prescription #{presc_id} created with {len(med_details)} medications!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


def page_staff():
    st.header("👨‍⚕️ Staff Directory")
    role_required('Admin', 'Doctor', 'Nurse')

    tab1, tab2, tab3, tab4 = st.tabs(["All Employees", "Doctors", "Nurses", "Departments"])

    with tab1:
        emp = query("""
            SELECT e.EmployeeID, e.FirstName, e.LastName, e.EmployeeType, e.JobTitle,
                   e.HireDate, dep.Name AS Department
            FROM Employee e
            LEFT JOIN Doctor d ON e.EmployeeID = d.EmployeeID
            LEFT JOIN Nurse n ON e.EmployeeID = n.EmployeeID
            LEFT JOIN Department dep ON
                (d.DepartmentID = dep.DepartmentID) OR (n.DepartmentID = dep.DepartmentID)
            ORDER BY e.LastName
        """)
        render_table(pd.DataFrame(emp))

    with tab2:
        docs = query("""
            SELECT d.EmployeeID AS DoctorID, e.FirstName, e.LastName, d.MajorScientificArea, d.Degree,
                   dep.Name AS Department
            FROM Doctor d
            JOIN Employee e ON d.EmployeeID = e.EmployeeID
            JOIN Department dep ON d.DepartmentID = dep.DepartmentID
            ORDER BY e.LastName
        """)
        render_table(pd.DataFrame(docs))

    with tab3:
        nurses_q = query("""
            SELECT n.EmployeeID AS NurseID, e.FirstName, e.LastName, dep.Name AS Department
            FROM Nurse n
            JOIN Employee e ON n.EmployeeID = e.EmployeeID
            JOIN Department dep ON n.DepartmentID = dep.DepartmentID
            ORDER BY e.LastName
        """)
        render_table(pd.DataFrame(nurses_q))

    with tab4:
        depts = query("""
            SELECT d.DepartmentID, d.Name, d.Code, d.SupervisionStartDate,
                   CONCAT(e.FirstName, ' ', e.LastName) AS Chairman
            FROM Department d
            LEFT JOIN Doctor doc ON d.ChairmanDoctorID = doc.EmployeeID
            LEFT JOIN Employee e ON doc.EmployeeID = e.EmployeeID
            ORDER BY d.Name
        """)
        render_table(pd.DataFrame(depts))


def page_admin():
    st.header("⚙️ Admin Panel")
    role_required('Admin')

    tab1, tab2, tab3 = st.tabs(["👥 User Management", "🏥 System Data", "📊 Database Stats"])

    with tab1:
        users = query("""
            SELECT u.UserID, u.Username, u.Email, u.Role,
                   CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
                   CONCAT(p.FirstName, ' ', p.LastName) AS PatientName
            FROM Users u
            LEFT JOIN Employee e ON u.EmployeeID = e.EmployeeID
            LEFT JOIN Patient p ON u.PatientID = p.PatientID
            ORDER BY u.Role, u.Username
        """)
        render_table(pd.DataFrame(users), "All Users")

        st.divider()
        st.subheader("Create New User")
        employees_no_user = query("""
            SELECT e.EmployeeID, e.FirstName, e.LastName, e.EmployeeType
            FROM Employee e
            LEFT JOIN Users u ON e.EmployeeID = u.EmployeeID
            WHERE u.UserID IS NULL
        """)
        patients_no_user = query("""
            SELECT p.PatientID, p.FirstName, p.LastName
            FROM Patient p
            LEFT JOIN Users u ON p.PatientID = u.PatientID
            WHERE u.UserID IS NULL
        """)

        with st.form("add_user"):
            username = st.text_input("Username *")
            password = st.text_input("Password *", type="password")
            email = st.text_input("Email")
            role = st.selectbox("Role *", ['Patient', 'Doctor', 'Nurse', 'Admin'])

            emp_options = [{'EmployeeID': None, 'FullName': 'None'}]
            pat_options = [{'PatientID': None, 'FullName': 'None'}]

            if role in ('Doctor', 'Nurse', 'Admin'):
                emp_options += [{'EmployeeID': e['EmployeeID'],
                                 'FullName': f"{e['FirstName']} {e['LastName']} ({e['EmployeeType']})"}
                                for e in employees_no_user]
                selected_emp = st.selectbox("Link Employee",
                                            options=range(len(emp_options)),
                                            format_func=lambda i: emp_options[i]['FullName'])
            else:
                pat_options += [{'PatientID': p['PatientID'],
                                 'FullName': f"{p['FirstName']} {p['LastName']}"}
                                for p in patients_no_user]
                selected_pat = st.selectbox("Link Patient",
                                            options=range(len(pat_options)),
                                            format_func=lambda i: pat_options[i]['FullName'])

            if st.form_submit_button("Create User"):
                if not username or not password:
                    st.error("Username and password are required")
                else:
                    pwhash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    try:
                        if role in ('Doctor', 'Nurse', 'Admin'):
                            eid = emp_options[selected_emp]['EmployeeID']
                            uid = execute_last_id("""
                                INSERT INTO Users (Username, PasswordHash, Email, Role, EmployeeID)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (username, pwhash, email or None, role, eid))
                        else:
                            pid = pat_options[selected_pat]['PatientID']
                            uid = execute_last_id("""
                                INSERT INTO Users (Username, PasswordHash, Email, Role, PatientID)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (username, pwhash, email or None, role, pid))
                        st.success(f"User #{uid} created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            hospitals = query("SELECT * FROM Hospital")
            render_table(pd.DataFrame(hospitals), "Hospitals")
        with col2:
            departments = query("SELECT DepartmentID, Name, Code FROM Department")
            render_table(pd.DataFrame(departments), "Departments")

        dept_locs = query("""
            SELECT dl.LocationID, dep.Name AS Department, dl.Address
            FROM DepartmentLocation dl
            JOIN Department dep ON dl.DepartmentID = dep.DepartmentID
        """)
        render_table(pd.DataFrame(dept_locs), "Department Locations")

        beds = query("""
            SELECT b.BedID, b.RoomNumber, b.BedType, b.Status, dep.Name AS Department
            FROM Bed b
            JOIN DepartmentLocation dl ON b.LocationID = dl.LocationID
            JOIN Department dep ON dl.DepartmentID = dep.DepartmentID
            ORDER BY dep.Name, b.RoomNumber
        """)
        render_table(pd.DataFrame(beds), "Beds")

    with tab3:
        tables = ['Hospital', 'Patient', 'Employee', 'Users', 'Doctor', 'Nurse', 'Admin',
                  'Department', 'DepartmentLocation', 'Bed', 'Payment', 'Appointment',
                  'EmergencyVisit', 'Prescription', 'PrescriptionDetail', 'Triage',
                  'Examination', 'Document', 'Medication', 'Patient_Phone']
        stats = []
        for t in tables:
            c = query_one(f"SELECT COUNT(*) c FROM {t}")['c']
            stats.append({'Table': t, 'Row Count': c})
        render_table(pd.DataFrame(stats), "Row Counts")


# ════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════

if not st.session_state.authenticated:
    login_page()
else:
    sidebar_nav()
    page = st.session_state.get('page', 'Dashboard')
    {
        'Dashboard': page_dashboard,
        'Patients': page_patients,
        'Emergency Visits': page_visits,
        'Appointments': page_appointments,
        'Pharmacy': page_pharmacy,
        'Staff': page_staff,
        'Admin': page_admin,
    }.get(page, page_dashboard)()
