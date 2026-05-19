# 💻 SQL Code Implementation — Phase 1 Deliverable 3

## 👥 Team Members
| Member | Role |
|--------|------|
| **Omar Hesham** | Team Leader — Patient Flow & Appointments Tables |
| **Ziad Khaled** | Staff Hierarchy & Location Tables |
| **Youssef Amir** | Clinical & Medication Tables |

---

## 📋 Table of Contents
1. [What Is SQL Code Implementation?](#what-is-sql-code-implementation)
2. [File Structure & Naming](#file-structure--naming)
3. [SQL Dialect](#sql-dialect)
4. [Member 1 — Omar Hesham](#member-1--omar-hesham-team-leader)
   - Users · Patient · EmergencyVisit · Bed · Appointment · Payment
5. [Member 2 — Ziad Khaled](#member-2--ziad-khaled)
   - Hospital · Employee · Doctor · Nurse · Admin · Department · DepartmentLocation
6. [Member 3 — Youssef Amir](#member-3--youssef-amir)
   - Triage · Examination · Prescription · PrescriptionDetail · Medication · Document
7. [Sample Data (INSERT Statements)](#sample-data-insert-statements)
8. [Indexes & Performance](#indexes--performance)
9. [How to Run & Test the SQL File](#how-to-run--test-the-sql-file)
10. [Common Errors & Fixes](#common-errors--fixes)
11. [Final Checklist](#final-checklist)
12. [Timeline](#timeline)

---

## What Is SQL Code Implementation?

This is the process of converting your **relational schema** into actual **SQL CREATE TABLE statements** that can be executed in a database. Each table definition must include:
- Column names with correct data types
- Primary key constraints
- Foreign key constraints with references
- Unique constraints
- CHECK constraints
- NOT NULL constraints
- Default values
- ENUM types (or equivalent)

### Your Goal
Each member writes the SQL for their **6 tables** and contributes to a single file: **`schemas/his-emergency.sql`**

---

## File Structure & Naming

The final SQL file will be at:
```
schemas/his-emergency.sql
```

### File Structure (in order of execution):
```sql
-- ============================================
-- Hospital Information System - Emergency Dept
-- Phase 1: SQL Schema Implementation
-- Team: Omar Hesham, Ziad Khaled, Youssef Amir
-- ============================================

-- 1. DROP TABLES (if exist) — in reverse dependency order
-- 2. CREATE TABLES — in dependency order (no FK references before table exists)
-- 3. ADD FOREIGN KEYS — for circular dependencies
-- 4. CREATE INDEXES — for performance
-- 5. INSERT SAMPLE DATA — 5-10 rows per table
```

---

## SQL Dialect

We will use **MySQL/MariaDB** syntax (most common for academic projects). If your professor requires PostgreSQL or SQLite, the syntax is similar but with minor differences (noted where applicable).

### Key MySQL Features We'll Use:
| Feature | MySQL Syntax | PostgreSQL Equivalent | SQLite Equivalent |
|---------|-------------|----------------------|-------------------|
| Auto-increment | `AUTO_INCREMENT` | `SERIAL` | `AUTOINCREMENT` |
| ENUM type | `ENUM('A','B','C')` | `CHECK (col IN ('A','B','C'))` | `CHECK (col IN ('A','B','C'))` |
| DATETIME | `DATETIME` | `TIMESTAMP` | `DATETIME` |
| Current timestamp default | `DEFAULT CURRENT_TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` |

---

# Member 1 — Omar Hesham 👑 (Team Leader)
## Focus: Patient Flow & Appointments Tables
### Your 6 Tables: Users · Patient · EmergencyVisit · Bed · Appointment · Payment

---

### Table 1 of 6: Users

**Rules:**
- This is the **first table** to create (no FK dependencies)
- `Username` and `Email` must be UNIQUE
- `Role` is an ENUM

**Full SQL:**
```sql
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Email VARCHAR(100),
    Role ENUM('Patient', 'Doctor', 'Nurse', 'Admin') NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID),
    UNIQUE KEY uk_users_username (Username),
    UNIQUE KEY uk_users_email (Email)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Users (Username, PasswordHash, Email, Role) VALUES
('omar_patient', '$2b$12$hashedpassword1', 'omar@email.com', 'Patient'),
('ziad_doctor', '$2b$12$hashedpassword2', 'ziad@hospital.com', 'Doctor'),
('youssef_nurse', '$2b$12$hashedpassword3', 'youssef@hospital.com', 'Nurse'),
('admin_user', '$2b$12$hashedpassword4', 'admin@hospital.com', 'Admin'),
('patient2', '$2b$12$hashedpassword5', 'patient2@email.com', 'Patient');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Users (Omar)\n-- ============================================`

---

### Table 2 of 6: Patient

**Rules:**
- `UserID` is a **UNIQUE FK** to Users (enforces 1:1)
- `SSN` and `PatientNumber` must be UNIQUE (PDF requirement)
- `Sex` is ENUM('M', 'F')

**Full SQL:**
```sql
CREATE TABLE Patient (
    PatientID INT AUTO_INCREMENT,
    UserID INT NOT NULL,
    SSN VARCHAR(20) NOT NULL,
    PatientNumber VARCHAR(20) NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Address VARCHAR(255),
    Phone VARCHAR(20),
    BirthDate DATE,
    Sex ENUM('M', 'F') NOT NULL,
    MedicalHistory TEXT,
    BloodPressure VARCHAR(10),
    HeartRate INT,
    Temperature DECIMAL(4,1),
    PRIMARY KEY (PatientID),
    UNIQUE KEY uk_patient_userid (UserID),
    UNIQUE KEY uk_patient_ssn (SSN),
    UNIQUE KEY uk_patient_patnum (PatientNumber),
    CONSTRAINT fk_patient_user FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Patient (UserID, SSN, PatientNumber, FirstName, LastName, Address, Phone, BirthDate, Sex, MedicalHistory, BloodPressure, HeartRate, Temperature) VALUES
(1, '123-45-6789', 'P001', 'Omar', 'Hesham', '123 Main St, Cairo', '01012345678', '1995-03-15', 'M', 'No known allergies', '120/80', 72, 37.0),
(5, '987-65-4321', 'P002', 'Ahmed', 'Ali', '456 Nile Ave, Giza', '01098765432', '1988-07-22', 'M', 'Hypertension', '140/90', 85, 37.2),
(6, '111-22-3333', 'P003', 'Sara', 'Mohamed', '789 Pyramids Rd', '01011122333', '2000-01-10', 'F', 'Asthma', '110/70', 68, 36.8),
(7, '444-55-6666', 'P004', 'Mona', 'Hassan', '321 Tahrir Sq', '01044455666', '1992-11-05', 'F', 'Diabetes Type 2', '130/85', 78, 37.5),
(8, '777-88-9999', 'P005', 'Khaled', 'Ibrahim', '654 Dokki St', '01077788999', '1975-06-30', 'M', 'Heart disease history', '150/95', 90, 37.8);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Patient (Omar)\n-- ============================================`

---

### Table 3 of 6: EmergencyVisit

**Rules:**
- `TriageID` is a **UNIQUE FK** to Triage (enforces 1:1)
- `BedID` is **nullable** (bed assigned later)
- `Disposition` is ENUM with 4 values

**Full SQL:**
```sql
CREATE TABLE EmergencyVisit (
    VisitID INT AUTO_INCREMENT,
    PatientID INT NOT NULL,
    TriageID INT NOT NULL,
    BedID INT,
    AdmissionDateTime DATETIME NOT NULL,
    DischargeDateTime DATETIME,
    Disposition ENUM('Admitted', 'Discharged', 'Transferred', 'Left Without Being Seen'),
    PRIMARY KEY (VisitID),
    UNIQUE KEY uk_ev_triageid (TriageID),
    CONSTRAINT fk_ev_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_ev_triage FOREIGN KEY (TriageID) REFERENCES Triage(TriageID),
    CONSTRAINT fk_ev_bed FOREIGN KEY (BedID) REFERENCES Bed(BedID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO EmergencyVisit (PatientID, TriageID, BedID, AdmissionDateTime, DischargeDateTime, Disposition) VALUES
(1, 1, 1, '2026-05-18 08:00:00', '2026-05-18 12:30:00', 'Discharged'),
(2, 2, 2, '2026-05-18 09:15:00', NULL, 'Admitted'),
(3, 3, 3, '2026-05-18 10:30:00', '2026-05-18 14:00:00', 'Discharged'),
(4, 4, 1, '2026-05-18 11:45:00', '2026-05-18 16:00:00', 'Transferred'),
(5, 5, NULL, '2026-05-18 13:00:00', '2026-05-18 13:30:00', 'Left Without Being Seen');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: EmergencyVisit (Omar)\n-- ============================================`

⚠️ **Note:** This table depends on `Triage` (Youssef) and `Bed` (Omar). In the final file, this CREATE TABLE must come **after** both Triage and Bed are created.

---

### Table 4 of 6: Bed

**Rules:**
- `LocationID` is FK to DepartmentLocation (Ziad's table)
- `Status` is ENUM with default 'Available'

**Full SQL:**
```sql
CREATE TABLE Bed (
    BedID INT AUTO_INCREMENT,
    RoomNumber VARCHAR(20),
    LocationID INT NOT NULL,
    BedType VARCHAR(50),
    Status ENUM('Available', 'Occupied', 'Cleaning') NOT NULL DEFAULT 'Available',
    PRIMARY KEY (BedID),
    CONSTRAINT fk_bed_location FOREIGN KEY (LocationID) REFERENCES DepartmentLocation(LocationID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Bed (RoomNumber, LocationID, BedType, Status) VALUES
('ED-101', 1, 'Trauma', 'Occupied'),
('ED-102', 1, 'Observation', 'Occupied'),
('ED-103', 1, 'Resuscitation', 'Available'),
('ED-201', 2, 'Trauma', 'Cleaning'),
('ED-202', 2, 'Observation', 'Available');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Bed (Omar)\n-- ============================================`

⚠️ **Note:** This table depends on `DepartmentLocation` (Ziad). Must come after it in the file.

---

### Table 5 of 6: Appointment

**Rules:**
- `DoctorID` is FK to Doctor (Ziad's table)
- `Status` and `Type` are ENUMs

**Full SQL:**
```sql
CREATE TABLE Appointment (
    AppointmentID INT AUTO_INCREMENT,
    PatientID INT NOT NULL,
    DoctorID INT NOT NULL,
    AppointmentDateTime DATETIME NOT NULL,
    Status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show') NOT NULL DEFAULT 'Scheduled',
    Type ENUM('Walk-in', 'Booked') NOT NULL,
    Notes TEXT,
    PRIMARY KEY (AppointmentID),
    CONSTRAINT fk_appt_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_appt_doctor FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Appointment (PatientID, DoctorID, AppointmentDateTime, Status, Type, Notes) VALUES
(1, 1, '2026-05-19 10:00:00', 'Scheduled', 'Booked', 'Follow-up visit'),
(2, 1, '2026-05-19 11:00:00', 'Scheduled', 'Walk-in', 'Chest pain complaint'),
(3, 2, '2026-05-20 09:00:00', 'Scheduled', 'Booked', 'Regular checkup'),
(4, 1, '2026-05-18 08:00:00', 'Completed', 'Walk-in', 'Minor injury'),
(5, 2, '2026-05-18 14:00:00', 'Cancelled', 'Booked', 'Patient called to cancel');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Appointment (Omar)\n-- ============================================`

⚠️ **Note:** This table depends on `Doctor` (Ziad). Must come after it in the file.

---

### Table 6 of 6: Payment

**Rules:**
- `AppointmentID` is a **UNIQUE FK** to Appointment (enforces 1:1)
- `Amount` is DECIMAL(10,2) for currency

**Full SQL:**
```sql
CREATE TABLE Payment (
    PaymentID INT AUTO_INCREMENT,
    AppointmentID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    PaymentDate DATETIME,
    PaymentMethod ENUM('Cash', 'Card', 'Online'),
    Status ENUM('Paid', 'Refunded', 'Pending') NOT NULL DEFAULT 'Pending',
    PRIMARY KEY (PaymentID),
    UNIQUE KEY uk_payment_apptid (AppointmentID),
    CONSTRAINT fk_payment_appt FOREIGN KEY (AppointmentID) REFERENCES Appointment(AppointmentID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Payment (AppointmentID, Amount, PaymentDate, PaymentMethod, Status) VALUES
(1, 150.00, '2026-05-19 10:30:00', 'Card', 'Paid'),
(2, 200.00, '2026-05-19 11:30:00', 'Cash', 'Paid'),
(3, 150.00, NULL, NULL, 'Pending'),
(4, 100.00, '2026-05-18 08:30:00', 'Online', 'Paid'),
(5, 150.00, '2026-05-18 14:30:00', 'Card', 'Refunded');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Payment (Omar)\n-- ============================================`

---

### ✅ Omar's SQL Work Order (execution order in file)

```
1. Users (no dependencies — create first)
2. Patient (depends on Users)
3. Bed (depends on Ziad's DepartmentLocation — place after it)
4. Appointment (depends on Ziad's Doctor — place after it)
5. EmergencyVisit (depends on Youssef's Triage — place after it)
6. Payment (depends on Appointment — place after it)
```

---

# Member 2 — Ziad Khaled
## Focus: Staff Hierarchy & Location Tables
### Your 7 Tables: Hospital · Employee · Doctor · Nurse · Admin · Department · DepartmentLocation

---

### Table 1 of 7: Hospital

**Rules:**
- This is the **root table** — no FK dependencies. Create it first.
- `Name` and `Email` must be UNIQUE.

**Full SQL:**
```sql
CREATE TABLE Hospital (
    HospitalID INT AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address TEXT,
    Phone VARCHAR(20),
    Email VARCHAR(100),
    EstablishedYear INT,
    PRIMARY KEY (HospitalID),
    UNIQUE KEY uk_hospital_name (Name),
    UNIQUE KEY uk_hospital_email (Email)
);
```

**Sample INSERT Data (2 rows):**
```sql
INSERT INTO Hospital (Name, Address, Phone, Email, EstablishedYear) VALUES
('Cairo General Hospital', '123 Health St, Cairo, Egypt', '02-12345678', 'info@cairogeneral.eg', 1985),
('Nile Medical Center', '456 River Rd, Giza, Egypt', '02-87654321', 'contact@nilemed.eg', 2005);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Hospital (Ziad)\n-- ============================================`

✅ **This is the first table you should create** — no dependencies at all.

---

### Table 2 of 7: Employee (Superclass)

**Rules:**
- `UserID` is a **UNIQUE FK** to Users (Omar's table)
- `SSN` must be UNIQUE (PDF requirement)

**Full SQL:**
```sql
CREATE TABLE Employee (
    EmployeeID INT AUTO_INCREMENT,
    UserID INT NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE,
    Sex ENUM('M', 'F') NOT NULL,
    SSN VARCHAR(20) NOT NULL,
    HireDate DATE,
    JobTitle VARCHAR(100),
    PRIMARY KEY (EmployeeID),
    UNIQUE KEY uk_employee_userid (UserID),
    UNIQUE KEY uk_employee_ssn (SSN),
    CONSTRAINT fk_employee_user FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Employee (UserID, FirstName, LastName, BirthDate, Sex, SSN, HireDate, JobTitle) VALUES
(2, 'Ziad', 'Khaled', '1985-04-12', 'M', '222-33-4444', '2020-01-15', 'ER Physician'),
(3, 'Youssef', 'Amir', '1990-08-20', 'M', '333-44-5555', '2021-06-01', 'Charge Nurse'),
(4, 'Admin', 'User', '1980-01-01', 'M', '444-55-6666', '2019-03-10', 'System Administrator'),
(9, 'Fatma', 'Nabil', '1988-12-15', 'F', '555-66-7777', '2022-02-20', 'ER Nurse'),
(10, 'Tarek', 'Samir', '1975-09-05', 'M', '666-77-8888', '2018-11-01', 'Senior Physician');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Employee (Ziad)\n-- ============================================`

⚠️ **Note:** This table depends on `Users` (Omar). Must come after Users in the file.

---

### Table 3 of 7: Department

**Rules:**
- `Name` and `Code` must be UNIQUE (PDF requirement)
- `HospitalID` is FK to Hospital (Ziad's table)
- `ChairmanDoctorID` is FK to Doctor — but Doctor doesn't exist yet!
- **Solution:** Create Department **without** the ChairmanDoctorID FK constraint first, then add it later with ALTER TABLE

**Full SQL (Part 1 — CREATE without circular FK):**
```sql
CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT,
    HospitalID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Code VARCHAR(20) NOT NULL,
    ChairmanDoctorID INT,
    SupervisionStartDate DATE,
    PRIMARY KEY (DepartmentID),
    UNIQUE KEY uk_dept_name (Name),
    UNIQUE KEY uk_dept_code (Code),
    CONSTRAINT fk_dept_hospital FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
);
```

**Full SQL (Part 2 — ALTER TABLE to add circular FK):**
```sql
-- Add the circular FK after Doctor table is created
ALTER TABLE Department
    ADD CONSTRAINT fk_dept_chairman FOREIGN KEY (ChairmanDoctorID) REFERENCES Doctor(DoctorID);
```

**Sample INSERT Data (2 rows):**
```sql
INSERT INTO Department (HospitalID, Name, Code, SupervisionStartDate) VALUES
(1, 'Emergency Department', 'ED001', '2020-01-15'),
(2, 'Cardiology Unit', 'CARD001', '2021-06-01');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement (Part 1) above
- The ALTER TABLE statement (Part 2) — place it **after** the Doctor CREATE TABLE
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Department (Ziad)\n-- ============================================`

---

### Table 4 of 7: Doctor

**Rules:**
- `EmployeeID` is a **UNIQUE FK** to Employee (ISA inheritance)
- `DepartmentID` is FK to Department

**Full SQL:**
```sql
CREATE TABLE Doctor (
    DoctorID INT AUTO_INCREMENT,
    EmployeeID INT NOT NULL,
    DepartmentID INT NOT NULL,
    MajorScientificArea VARCHAR(100),
    Degree VARCHAR(50),
    JoinDate DATE,
    PRIMARY KEY (DoctorID),
    UNIQUE KEY uk_doctor_empid (EmployeeID),
    CONSTRAINT fk_doctor_employee FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    CONSTRAINT fk_doctor_dept FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);
```

**Sample INSERT Data (3 rows):**
```sql
INSERT INTO Doctor (EmployeeID, DepartmentID, MajorScientificArea, Degree, JoinDate) VALUES
(1, 1, 'Emergency Medicine', 'MD', '2020-01-15'),
(5, 1, 'Trauma Surgery', 'MD, FACS', '2018-11-01'),
(6, 2, 'Cardiology', 'MD, PhD', '2021-06-01');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Doctor (Ziad)\n-- ============================================`

⚠️ **Note:** After this table is created, add the ALTER TABLE statement for Department's ChairmanDoctorID FK.

---

### Table 5 of 7: Nurse

**Rules:**
- `EmployeeID` is a **UNIQUE FK** to Employee (ISA inheritance)
- `DepartmentID` is FK to Department

**Full SQL:**
```sql
CREATE TABLE Nurse (
    NurseID INT AUTO_INCREMENT,
    EmployeeID INT NOT NULL,
    DepartmentID INT NOT NULL,
    JoinDate DATE,
    PRIMARY KEY (NurseID),
    UNIQUE KEY uk_nurse_empid (EmployeeID),
    CONSTRAINT fk_nurse_employee FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
    CONSTRAINT fk_nurse_dept FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);
```

**Sample INSERT Data (3 rows):**
```sql
INSERT INTO Nurse (EmployeeID, DepartmentID, JoinDate) VALUES
(2, 1, '2021-06-01'),
(4, 1, '2022-02-20'),
(7, 1, '2023-01-10');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Nurse (Ziad)\n-- ============================================`

---

### Table 6 of 7: Admin

**Rules:**
- `EmployeeID` is a **UNIQUE FK** to Employee (ISA inheritance)
- Simplest table — just PK and FK

**Full SQL:**
```sql
CREATE TABLE Admin (
    AdminID INT AUTO_INCREMENT,
    EmployeeID INT NOT NULL,
    PRIMARY KEY (AdminID),
    UNIQUE KEY uk_admin_empid (EmployeeID),
    CONSTRAINT fk_admin_employee FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);
```

**Sample INSERT Data (1 row):**
```sql
INSERT INTO Admin (EmployeeID) VALUES
(3);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statement above
- Add a comment header: `-- ============================================\n-- Table: Admin (Ziad)\n-- ============================================`

---

### Table 7 of 7: DepartmentLocation

**Rules:**
- `DepartmentID` is FK to Department
- `Latitude` and `Longitude` are DECIMAL for geo-location

**Full SQL:**
```sql
CREATE TABLE DepartmentLocation (
    LocationID INT AUTO_INCREMENT,
    DepartmentID INT NOT NULL,
    Address TEXT,
    Latitude DECIMAL(10,8),
    Longitude DECIMAL(11,8),
    PRIMARY KEY (LocationID),
    CONSTRAINT fk_deptloc_dept FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);
```

**Sample INSERT Data (2 rows):**
```sql
INSERT INTO DepartmentLocation (DepartmentID, Address, Latitude, Longitude) VALUES
(1, '123 Emergency St, Cairo, Egypt', 30.0444, 31.2357),
(2, '456 Cardiology Ave, Cairo, Egypt', 30.0626, 31.2497);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: DepartmentLocation (Ziad)\n-- ============================================`

---

### ✅ Ziad's SQL Work Order (execution order in file)

```
1. Hospital (no dependencies — create first)
2. Employee (depends on Omar's Users — place after Users)
3. Department (depends on Hospital — place after it)
4. Doctor (depends on Employee and Department)
   → Then add: ALTER TABLE Department ADD CONSTRAINT fk_dept_chairman ...
5. Nurse (depends on Employee and Department)
6. Admin (depends on Employee)
7. DepartmentLocation (depends on Department)
```

---

# Member 3 — Youssef Amir
## Focus: Clinical & Medication Tables
### Your 6 Tables: Triage · Examination · Prescription · PrescriptionDetail · Medication · Document

---

### Table 1 of 6: Triage (Weak Entity)

**Rules:**
- `TriageLevel` has a **CHECK constraint** (1-5)
- `PatientID` and `NurseID` are NOT NULL FKs

**Full SQL:**
```sql
CREATE TABLE Triage (
    TriageID INT AUTO_INCREMENT,
    PatientID INT NOT NULL,
    NurseID INT NOT NULL,
    DateTime DATETIME NOT NULL,
    ChiefComplaint TEXT,
    TriageLevel INT NOT NULL,
    BloodPressure VARCHAR(10),
    HeartRate INT,
    Temperature DECIMAL(4,1),
    PRIMARY KEY (TriageID),
    CONSTRAINT chk_triage_level CHECK (TriageLevel BETWEEN 1 AND 5),
    CONSTRAINT fk_triage_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_triage_nurse FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Triage (PatientID, NurseID, DateTime, ChiefComplaint, TriageLevel, BloodPressure, HeartRate, Temperature) VALUES
(1, 1, '2026-05-18 08:00:00', 'Chest pain', 2, '140/90', 95, 37.8),
(2, 2, '2026-05-18 09:15:00', 'Shortness of breath', 3, '150/95', 88, 37.2),
(3, 1, '2026-05-18 10:30:00', 'Minor laceration', 4, '125/80', 70, 36.8),
(4, 2, '2026-05-18 11:45:00', 'Abdominal pain', 2, '135/85', 82, 37.5),
(5, 1, '2026-05-18 13:00:00', 'Headache', 5, '110/70', 65, 36.5);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Triage (Youssef)\n-- ============================================`

⚠️ **Note:** This table depends on `Patient` (Omar) and `Nurse` (Ziad). Must come after both in the file.

---

### Table 2 of 6: Examination (Associative Entity)

**Rules:**
- Three FKs: DoctorID, PatientID, VisitID — all NOT NULL
- `HoursSpent` is DECIMAL(4,2)

**Full SQL:**
```sql
CREATE TABLE Examination (
    ExaminationID INT AUTO_INCREMENT,
    DoctorID INT NOT NULL,
    PatientID INT NOT NULL,
    VisitID INT NOT NULL,
    ExaminationDate DATETIME NOT NULL,
    HoursSpent DECIMAL(4,2),
    PRIMARY KEY (ExaminationID),
    CONSTRAINT fk_exam_doctor FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    CONSTRAINT fk_exam_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_exam_visit FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Examination (DoctorID, PatientID, VisitID, ExaminationDate, HoursSpent) VALUES
(1, 1, 1, '2026-05-18 08:30:00', 1.50),
(1, 2, 2, '2026-05-18 09:45:00', 2.00),
(2, 3, 3, '2026-05-18 11:00:00', 0.75),
(1, 4, 4, '2026-05-18 12:15:00', 1.25),
(2, 5, 5, '2026-05-18 13:30:00', 0.50);
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Examination (Youssef)\n-- ============================================`

⚠️ **Note:** This table depends on `Doctor` (Ziad), `Patient` (Omar), and `EmergencyVisit` (Omar). Must come after all three.

---

### Table 3 of 6: Prescription

**Rules:**
- Three FKs: DoctorID, PatientID, VisitID — all NOT NULL
- `PrescriptionDate` is DATE (not DATETIME)

**Full SQL:**
```sql
CREATE TABLE Prescription (
    PrescriptionID INT AUTO_INCREMENT,
    DoctorID INT NOT NULL,
    PatientID INT NOT NULL,
    VisitID INT NOT NULL,
    PrescriptionDate DATE NOT NULL,
    PRIMARY KEY (PrescriptionID),
    CONSTRAINT fk_rx_doctor FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),
    CONSTRAINT fk_rx_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_rx_visit FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Prescription (DoctorID, PatientID, VisitID, PrescriptionDate) VALUES
(1, 1, 1, '2026-05-18'),
(1, 2, 2, '2026-05-18'),
(2, 3, 3, '2026-05-18'),
(1, 4, 4, '2026-05-18'),
(2, 5, 5, '2026-05-18');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Prescription (Youssef)\n-- ============================================`

⚠️ **Note:** Same dependencies as Examination. Must come after Doctor, Patient, and EmergencyVisit.

---

### Table 4 of 6: PrescriptionDetail

**Rules:**
- Two FKs: PrescriptionID and MedicationID — both NOT NULL
- `StartDate` and `EndDate` are NOT NULL

**Full SQL:**
```sql
CREATE TABLE PrescriptionDetail (
    PrescriptionDetailID INT AUTO_INCREMENT,
    PrescriptionID INT NOT NULL,
    MedicationID INT NOT NULL,
    Directions TEXT,
    Dosage VARCHAR(50),
    TimesPerDay INT,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    PRIMARY KEY (PrescriptionDetailID),
    CONSTRAINT fk_rxd_rx FOREIGN KEY (PrescriptionID) REFERENCES Prescription(PrescriptionID),
    CONSTRAINT fk_rxd_med FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO PrescriptionDetail (PrescriptionID, MedicationID, Directions, Dosage, TimesPerDay, StartDate, EndDate) VALUES
(1, 1, 'Take with food', '500mg', 3, '2026-05-18', '2026-05-25'),
(2, 2, 'Inject subcutaneously', '10 units', 1, '2026-05-18', '2026-06-01'),
(3, 3, 'Inhale as needed', '2 puffs', 4, '2026-05-18', '2026-05-25'),
(4, 1, 'Take after meals', '250mg', 2, '2026-05-18', '2026-05-22'),
(5, 4, 'Apply topically', '1 tube', 2, '2026-05-18', '2026-05-28');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: PrescriptionDetail (Youssef)\n-- ============================================`

⚠️ **Note:** This table depends on `Prescription` (yours) and `Medication` (yours). Must come after both.

---

### Table 5 of 6: Medication

**Rules:**
- Simple lookup table — no FK dependencies
- `Name` is NOT NULL

**Full SQL:**
```sql
CREATE TABLE Medication (
    MedicationID INT AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Description TEXT,
    PRIMARY KEY (MedicationID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Medication (Name, Description) VALUES
('Amoxicillin', 'Antibiotic for bacterial infections'),
('Insulin', 'Hormone for diabetes management'),
('Albuterol', 'Bronchodilator for asthma'),
('Paracetamol', 'Pain reliever and fever reducer'),
('Hydrocortisone Cream', 'Topical steroid for skin inflammation');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Medication (Youssef)\n-- ============================================`

✅ **This is the first table you should create** — no dependencies at all.

---

### Table 6 of 6: Document

**Rules:**
- `PatientID` is NOT NULL FK
- `VisitID` is **nullable** FK (some documents not linked to a visit)

**Full SQL:**
```sql
CREATE TABLE Document (
    DocumentID INT AUTO_INCREMENT,
    PatientID INT NOT NULL,
    VisitID INT,
    FileName VARCHAR(255),
    FilePath VARCHAR(500),
    UploadDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Description TEXT,
    PRIMARY KEY (DocumentID),
    CONSTRAINT fk_doc_patient FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    CONSTRAINT fk_doc_visit FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
);
```

**Sample INSERT Data (5 rows):**
```sql
INSERT INTO Document (PatientID, VisitID, FileName, FilePath, UploadDate, Description) VALUES
(1, 1, 'xray_chest_001.jpg', '/uploads/patients/1/xray_chest_001.jpg', '2026-05-18 08:15:00', 'Chest X-ray'),
(2, 2, 'ecg_002.pdf', '/uploads/patients/2/ecg_002.pdf', '2026-05-18 09:30:00', 'ECG Report'),
(3, 3, 'blood_test_003.pdf', '/uploads/patients/3/blood_test_003.pdf', '2026-05-18 10:45:00', 'Blood test results'),
(4, 4, 'ct_scan_004.dcm', '/uploads/patients/4/ct_scan_004.dcm', '2026-05-18 12:00:00', 'CT Scan abdomen'),
(5, NULL, 'prior_records_005.pdf', '/uploads/patients/5/prior_records_005.pdf', '2026-05-18 13:10:00', 'Prior medical records');
```

**What to add to `his-emergency.sql`:**
- The CREATE TABLE statement above
- The INSERT statements above
- Add a comment header: `-- ============================================\n-- Table: Document (Youssef)\n-- ============================================`

⚠️ **Note:** This table depends on `Patient` (Omar) and optionally `EmergencyVisit` (Omar). Must come after both.

---

### ✅ Youssef's SQL Work Order (execution order in file)

```
1. Medication (no dependencies — create first among your tables)
2. Triage (depends on Omar's Patient and Ziad's Nurse)
3. Prescription (depends on Ziad's Doctor, Omar's Patient, Omar's EmergencyVisit)
4. PrescriptionDetail (depends on Prescription and Medication — both yours)
5. Examination (depends on Ziad's Doctor, Omar's Patient, Omar's EmergencyVisit)
6. Document (depends on Omar's Patient, optionally Omar's EmergencyVisit)
```

---

## Sample Data (INSERT Statements)

### Complete INSERT Order

The INSERT statements must be executed in this order to avoid FK constraint violations:

```
1. Users (Omar)
2. Hospital (Ziad)
3. Medication (Youssef)
4. Employee (Ziad)
5. Department (Ziad)
6. Doctor (Ziad)
7. Nurse (Ziad)
8. Admin (Ziad)
9. DepartmentLocation (Ziad)
10. Patient (Omar)
11. Bed (Omar)
12. Triage (Youssef)
13. EmergencyVisit (Omar)
14. Appointment (Omar)
15. Payment (Omar)
16. Examination (Youssef)
17. Prescription (Youssef)
18. PrescriptionDetail (Youssef)
19. Document (Youssef)
```

### Why This Order?
Each table's INSERT must come **after** all tables it references via FK. For example:
- `Patient` INSERT needs `Users` to exist (UserID FK)
- `Triage` INSERT needs `Patient` and `Nurse` to exist
- `EmergencyVisit` INSERT needs `Patient`, `Triage`, and `Bed` to exist
- `PrescriptionDetail` INSERT needs `Prescription` and `Medication` to exist

---

## Indexes & Performance

Add these indexes **after** all tables are created. They improve query performance for common lookups.

```sql
-- ============================================
-- INDEXES (Performance)
-- ============================================

-- Patient lookups
CREATE INDEX idx_patient_ssn ON Patient(SSN);
CREATE INDEX idx_patient_patnum ON Patient(PatientNumber);

-- EmergencyVisit lookups
CREATE INDEX idx_ev_patient ON EmergencyVisit(PatientID);
CREATE INDEX idx_ev_admission ON EmergencyVisit(AdmissionDateTime);

-- Appointment lookups
CREATE INDEX idx_appt_doctor ON Appointment(DoctorID);
CREATE INDEX idx_appt_datetime ON Appointment(AppointmentDateTime);

-- Triage lookups
CREATE INDEX idx_triage_patient ON Triage(PatientID);
CREATE INDEX idx_triage_datetime ON Triage(DateTime);

-- Examination lookups
CREATE INDEX idx_exam_doctor ON Examination(DoctorID);
CREATE INDEX idx_exam_visit ON Examination(VisitID);

-- Prescription lookups
CREATE INDEX idx_rx_doctor ON Prescription(DoctorID);
CREATE INDEX idx_rx_patient ON Prescription(PatientID);

-- Document lookups
CREATE INDEX idx_doc_patient ON Document(PatientID);
CREATE INDEX idx_doc_visit ON Document(VisitID);
```

**What to add to `his-emergency.sql`:**
- All the CREATE INDEX statements above
- Add a comment header: `-- ============================================\n-- INDEXES\n-- ============================================`

---

## How to Run & Test the SQL File

### Option 1: MySQL Command Line
```bash
# Create the database first
mysql -u root -p -e "CREATE DATABASE his_emergency;"

# Run the SQL file
mysql -u root -p his_emergency < schemas/his-emergency.sql

# Verify tables were created
mysql -u root -p his_emergency -e "SHOW TABLES;"

# Verify data was inserted
mysql -u root -p his_emergency -e "SELECT COUNT(*) FROM Users;"
mysql -u root -p his_emergency -e "SELECT COUNT(*) FROM Patient;"
mysql -u root -p his_emergency -e "SELECT COUNT(*) FROM Doctor;"
```

### Option 2: MySQL Workbench
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Create a new database: `CREATE DATABASE his_emergency;`
4. Open the SQL file: File → Open SQL Script → select `schemas/his-emergency.sql`
5. Click the lightning bolt icon (⚡) to execute
6. Check the Output tab for errors

### Option 3: phpMyAdmin
1. Open phpMyAdmin in your browser
2. Create a new database named `his_emergency`
3. Select the database
4. Go to the "Import" tab
5. Choose `schemas/his-emergency.sql`
6. Click "Go"

### Option 4: Online SQL Validator (No Installation)
- Use [SQL Fiddle](http://sqlfiddle.com/) or [DB Fiddle](https://www.db-fiddle.com/)
- Select MySQL as the engine
- Paste the entire SQL file content
- Click "Run SQL"

---

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ERROR 1005: Can't create table` | FK references a table that doesn't exist yet | Reorder CREATE TABLE statements so referenced tables come first |
| `ERROR 1452: Cannot add or update a child row` | INSERT references a PK that doesn't exist | Reorder INSERT statements; ensure parent rows exist before child rows |
| `ERROR 1062: Duplicate entry` | UNIQUE constraint violated | Check sample data for duplicate SSN, PatientNumber, Username, etc. |
| `ERROR 1451: Cannot delete or update a parent row` | Trying to DROP a table that's referenced by FK | DROP tables in reverse order (children first, then parents) |
| `ERROR 1064: SQL syntax error` | Typo in SQL syntax | Check for missing commas, parentheses, or semicolons |
| `ERROR 1146: Table doesn't exist` | Table name typo or wrong database | Verify table names match exactly (case-sensitive on Linux) |
| `CHECK constraint not enforced` | MySQL version < 8.0.16 | Upgrade MySQL or use triggers instead of CHECK |
| `ENUM value out of range` | Inserting a value not in ENUM list | Only use values defined in the ENUM |

### Circular Dependency Fix (Department ↔ Doctor)

The `Department.ChairmanDoctorID` references `Doctor.DoctorID`, but `Doctor.DepartmentID` references `Department.DepartmentID`. This creates a circular FK.

**Solution (already included in the SQL above):**
```sql
-- Step 1: Create Department WITHOUT the ChairmanDoctorID FK
CREATE TABLE Department (
    DepartmentID INT AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Code VARCHAR(20) NOT NULL,
    ChairmanDoctorID INT,  -- No FK constraint yet
    SupervisionStartDate DATE,
    PRIMARY KEY (DepartmentID),
    UNIQUE KEY uk_dept_name (Name),
    UNIQUE KEY uk_dept_code (Code)
);

-- Step 2: Create Doctor (which references Department)
CREATE TABLE Doctor (
    DoctorID INT AUTO_INCREMENT,
    EmployeeID INT NOT NULL,
    DepartmentID INT NOT NULL,
    ...
    CONSTRAINT fk_doctor_dept FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Step 3: Now add the circular FK
ALTER TABLE Department
    ADD CONSTRAINT fk_dept_chairman FOREIGN KEY (ChairmanDoctorID) REFERENCES Doctor(DoctorID);
```

---

## Final Checklist

Each member must verify their SQL before merging:

### CREATE TABLE Checklist
- [ ] Table name matches the relational schema
- [ ] All columns from the schema are present
- [ ] Data types match (INT, VARCHAR, DECIMAL, DATE, DATETIME, TEXT, ENUM)
- [ ] Primary key is defined with `PRIMARY KEY`
- [ ] AUTO_INCREMENT is set on surrogate PKs
- [ ] UNIQUE constraints on SSN, PatientNumber, Department Name, Department Code
- [ ] NOT NULL constraints where required
- [ ] DEFAULT values where specified
- [ ] ENUM values match exactly (case-sensitive)
- [ ] CHECK constraints where required (TriageLevel 1-5)
- [ ] Foreign key constraints with correct references
- [ ] FK constraint names are unique (e.g., `fk_patient_user`, not just `fk_user`)

### INSERT Data Checklist
- [ ] At least 5 rows per table
- [ ] All NOT NULL columns have values
- [ ] FK values reference existing PKs (respect the INSERT order)
- [ ] UNIQUE columns have unique values
- [ ] ENUM values are from the allowed list
- [ ] CHECK constraint values are within range (TriageLevel 1-5)
- [ ] Date/datetime formats are correct ('YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS')

### File Structure Checklist
- [ ] File starts with DROP TABLE statements (in reverse dependency order)
- [ ] CREATE TABLE statements are in dependency order
- [ ] ALTER TABLE for circular FK is placed after both tables exist
- [ ] CREATE INDEX statements are after all tables
- [ ] INSERT statements are in dependency order
- [ ] Every statement ends with a semicolon (`;`)
- [ ] Comment headers separate each section

---

## Timeline

| Day | Date | Task |
|-----|------|------|
| **Today** | Mon, May 18 | Each member writes CREATE TABLE + INSERT for their 6 tables |
| **Tonight** | Mon, May 18 | Merge all sections into `schemas/his-emergency.sql` |
| **Tomorrow AM** | Tue, May 19 | Test the SQL file — run it, fix errors |
| **Tomorrow PM** | Tue, May 19 | Final review — verify all 18 tables, constraints, and sample data |
| **Wed** | May 20 | Commit, tag `v1.0-phase1`, and prepare for evaluation |

---

*Let's finish this! 💪*
