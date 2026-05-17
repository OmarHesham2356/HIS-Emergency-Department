# 🗃️ Relational Schema Mapping — Phase 1 Deliverable 2

## 👥 Team Members
| Member | Role |
|--------|------|
| **Omar Hesham** | Team Leader — Patient Flow & Appointments Tables |
| **Ziad Khaled** | Staff Hierarchy & Location Tables |
| **Youssef Amir** | Clinical & Medication Tables |

---

## 📋 Table of Contents
1. [What Is Relational Schema Mapping?](#what-is-relational-schema-mapping)
2. [Mapping Rules (Quick Reference)](#mapping-rules-quick-reference)
3. [Member 1 — Omar Hesham](#member-1--omar-hesham-team-leader)
   - Users · Patient · EmergencyVisit · Bed · Appointment · Payment
4. [Member 2 — Ziad Khaled](#member-2--ziad-khaled)
   - Employee · Doctor · Nurse · Admin · Department · DepartmentLocation
5. [Member 3 — Youssef Amir](#member-3--youssef-amir)
   - Triage · Examination · Prescription · PrescriptionDetail · Medication · Document
6. [Cross-Table Relationship Mapping](#cross-table-relationship-mapping)
7. [Normalization Checklist (3NF)](#normalization-checklist-3nf)
8. [Final Output Format](#final-output-format)
9. [Timeline](#timeline)

---

## What Is Relational Schema Mapping?

This is the process of converting your **ERD (Entity-Relationship Diagram)** into **relational database tables**. Each entity becomes a table, each attribute becomes a column, and each relationship becomes a foreign key or a separate junction table.

### Your Goal
Produce a complete markdown file (`schemas/relational-schema.md`) that lists **all 18 tables** with:
- Table name
- Column names with data types
- Primary keys (PK)
- Foreign keys (FK) with references
- Unique constraints
- CHECK / ENUM constraints
- NOT NULL constraints
- Default values

---

## Mapping Rules (Quick Reference)

| ERD Concept | Relational Mapping Rule | Example |
|-------------|------------------------|---------|
| **Strong Entity** | Becomes its own table with PK | `Patient` → `Patient` table |
| **Weak Entity** | Becomes its own table; PK includes FK to owner | `Triage` → `Triage` table with `PatientID` as part of key |
| **1:1 Relationship** | FK goes in **either** table (usually the one with total participation) | `Patient.UserID` (UNIQUE FK → Users) |
| **1:N Relationship** | FK goes in the **N-side** table | `EmergencyVisit.PatientID` → Patient |
| **M:N Relationship** | Create a **new junction table** with composite PK | `Examination` (DoctorID + PatientID + VisitID) |
| **ISA / Specialization** | Subclass tables have FK to superclass PK | `Doctor.EmployeeID` → Employee |
| **Multi-valued Attribute** | Becomes a separate table (not applicable in our design) | — |
| **Composite Attribute** | Split into individual columns | `Name` → `FirstName`, `LastName` |

---

# Member 1 — Omar Hesham 👑 (Team Leader)
## Focus: Patient Flow & Appointments Tables
### Your 6 Tables: Users · Patient · EmergencyVisit · Bed · Appointment · Payment

---

### Table 1 of 6: Users

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `UserID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `Username` | VARCHAR(50) | **UNIQUE, NOT NULL** | Login identifier |
| `PasswordHash` | VARCHAR(255) | **NOT NULL** | Store hashed password (bcrypt) |
| `Email` | VARCHAR(100) | **UNIQUE** | For notifications |
| `Role` | ENUM('Patient','Doctor','Nurse','Admin') | **NOT NULL** | Determines access level |
| `CreatedAt` | DATETIME | **DEFAULT CURRENT_TIMESTAMP** | Registration timestamp |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:1 with Patient | FK in Patient table | `Patient.UserID` → `Users.UserID` (UNIQUE) |
| 1:1 with Employee | FK in Employee table | `Employee.UserID` → `Users.UserID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF: All columns are atomic (no repeating groups)
- ✅ 2NF: No partial dependencies (single-column PK)
- ✅ 3NF: No transitive dependencies (all non-key columns depend only on UserID)

**What to write in `relational-schema.md`:**
```markdown
### Table: Users
| Column | Type | Constraints |
|--------|------|-------------|
| UserID | INT | PK, AUTO_INCREMENT |
| Username | VARCHAR(50) | UNIQUE, NOT NULL |
| PasswordHash | VARCHAR(255) | NOT NULL |
| Email | VARCHAR(100) | UNIQUE |
| Role | ENUM('Patient','Doctor','Nurse','Admin') | NOT NULL |
| CreatedAt | DATETIME | DEFAULT CURRENT_TIMESTAMP |
```

---

### Table 2 of 6: Patient

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `PatientID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `UserID` | INT | **FOREIGN KEY → Users(UserID), UNIQUE, NOT NULL** | 1:1 with Users |
| `SSN` | VARCHAR(20) | **UNIQUE, NOT NULL** | 🔴 PDF unique attribute |
| `PatientNumber` | VARCHAR(20) | **UNIQUE, NOT NULL** | 🔴 PDF unique attribute |
| `FirstName` | VARCHAR(50) | **NOT NULL** | Split from composite Name |
| `LastName` | VARCHAR(50) | **NOT NULL** | Split from composite Name |
| `Address` | VARCHAR(255) | — | Can be NULL |
| `Phone` | VARCHAR(20) | — | Can be NULL |
| `BirthDate` | DATE | — | Can be NULL |
| `Sex` | ENUM('M','F') | **NOT NULL** | Binary for simplicity |
| `MedicalHistory` | TEXT | — | Can be NULL |
| `BloodPressure` | VARCHAR(10) | — | Format: "120/80" |
| `HeartRate` | INT | — | Beats per minute |
| `Temperature` | DECIMAL(4,1) | — | e.g., 98.6 |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:1 with Users | FK here (Patient side) | `Patient.UserID` → `Users.UserID` (UNIQUE) |
| 1:N with EmergencyVisit | FK in EmergencyVisit | `EmergencyVisit.PatientID` → `Patient.PatientID` |
| 1:N with Triage | FK in Triage | `Triage.PatientID` → `Patient.PatientID` |
| 1:N with Examination | FK in Examination | `Examination.PatientID` → `Patient.PatientID` |
| 1:N with Prescription | FK in Prescription | `Prescription.PatientID` → `Patient.PatientID` |
| 1:N with Appointment | FK in Appointment | `Appointment.PatientID` → `Patient.PatientID` |
| 1:N with Document | FK in Document | `Document.PatientID` → `Patient.PatientID` |

**Normalization Notes:**
- ✅ 1NF: All atomic values
- ✅ 2NF: All non-key attributes depend on PatientID (single PK)
- ✅ 3NF: No transitive dependencies
- ⚠️ Note: `BloodPressure`, `HeartRate`, `Temperature` are **current** vitals. Historical vitals are stored in Triage and Examination tables. This is intentional — Patient stores the latest snapshot, Triage/Examination store historical records.

**What to write in `relational-schema.md`:**
```markdown
### Table: Patient
| Column | Type | Constraints |
|--------|------|-------------|
| PatientID | INT | PK, AUTO_INCREMENT |
| UserID | INT | FK → Users(UserID), UNIQUE, NOT NULL |
| SSN | VARCHAR(20) | UNIQUE, NOT NULL |
| PatientNumber | VARCHAR(20) | UNIQUE, NOT NULL |
| FirstName | VARCHAR(50) | NOT NULL |
| LastName | VARCHAR(50) | NOT NULL |
| Address | VARCHAR(255) | |
| Phone | VARCHAR(20) | |
| BirthDate | DATE | |
| Sex | ENUM('M','F') | NOT NULL |
| MedicalHistory | TEXT | |
| BloodPressure | VARCHAR(10) | |
| HeartRate | INT | |
| Temperature | DECIMAL(4,1) | |
```

---

### Table 3 of 6: EmergencyVisit

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `VisitID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | Which patient |
| `TriageID` | INT | **FOREIGN KEY → Triage(TriageID), UNIQUE, NOT NULL** | 1:1 with Triage |
| `BedID` | INT | **FOREIGN KEY → Bed(BedID)** | NULLABLE — bed assigned later |
| `AdmissionDateTime` | DATETIME | **NOT NULL** | When visit started |
| `DischargeDateTime` | DATETIME | — | NULL until discharge |
| `Disposition` | ENUM('Admitted','Discharged','Transferred','Left Without Being Seen') | — | Visit outcome |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Patient | FK here | `EmergencyVisit.PatientID` → `Patient.PatientID` |
| 1:1 with Triage | FK here (UNIQUE) | `EmergencyVisit.TriageID` → `Triage.TriageID` (UNIQUE) |
| N:1 with Bed | FK here | `EmergencyVisit.BedID` → `Bed.BedID` (nullable) |
| 1:N with Examination | FK in Examination | `Examination.VisitID` → `EmergencyVisit.VisitID` |
| 1:N with Prescription | FK in Prescription | `Prescription.VisitID` → `EmergencyVisit.VisitID` |
| 1:N with Document | FK in Document | `Document.VisitID` → `EmergencyVisit.VisitID` (nullable) |

**Normalization Notes:**
- ✅ 1NF: All atomic
- ✅ 2NF: All depend on VisitID
- ✅ 3NF: No transitive dependencies
- ⚠️ The UNIQUE constraint on `TriageID` enforces the 1:1 relationship (one triage → one visit)

**What to write in `relational-schema.md`:**
```markdown
### Table: EmergencyVisit
| Column | Type | Constraints |
|--------|------|-------------|
| VisitID | INT | PK, AUTO_INCREMENT |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| TriageID | INT | FK → Triage(TriageID), UNIQUE, NOT NULL |
| BedID | INT | FK → Bed(BedID) |
| AdmissionDateTime | DATETIME | NOT NULL |
| DischargeDateTime | DATETIME | |
| Disposition | ENUM('Admitted','Discharged','Transferred','Left Without Being Seen') | |
```

---

### Table 4 of 6: Bed

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `BedID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `RoomNumber` | VARCHAR(20) | — | e.g., "ED-101" |
| `LocationID` | INT | **FOREIGN KEY → DepartmentLocation(LocationID), NOT NULL** | Which location |
| `BedType` | VARCHAR(50) | — | 'Trauma', 'Observation', 'Resuscitation' |
| `Status` | ENUM('Available','Occupied','Cleaning') | **NOT NULL, DEFAULT 'Available'** | Current status |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with DepartmentLocation | FK here | `Bed.LocationID` → `DepartmentLocation.LocationID` |
| 1:N with EmergencyVisit | FK in EmergencyVisit | `EmergencyVisit.BedID` → `Bed.BedID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean single-table design
- ⚠️ Coordinate with Ziad: `LocationID` references his `DepartmentLocation` table

**What to write in `relational-schema.md`:**
```markdown
### Table: Bed
| Column | Type | Constraints |
|--------|------|-------------|
| BedID | INT | PK, AUTO_INCREMENT |
| RoomNumber | VARCHAR(20) | |
| LocationID | INT | FK → DepartmentLocation(LocationID), NOT NULL |
| BedType | VARCHAR(50) | |
| Status | ENUM('Available','Occupied','Cleaning') | NOT NULL, DEFAULT 'Available' |
```

---

### Table 5 of 6: Appointment

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `AppointmentID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | Who booked |
| `DoctorID` | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | With which doctor |
| `AppointmentDateTime` | DATETIME | **NOT NULL** | Scheduled time |
| `Status` | ENUM('Scheduled','Completed','Cancelled','No-Show') | **NOT NULL, DEFAULT 'Scheduled'** | Current status |
| `Type` | ENUM('Walk-in','Booked') | **NOT NULL** | How it was created |
| `Notes` | TEXT | — | Additional info |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Patient | FK here | `Appointment.PatientID` → `Patient.PatientID` |
| N:1 with Doctor | FK here | `Appointment.DoctorID` → `Doctor.DoctorID` |
| 1:1 with Payment | FK in Payment | `Payment.AppointmentID` → `Appointment.AppointmentID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ Coordinate with Ziad: `DoctorID` references his `Doctor` table

**What to write in `relational-schema.md`:**
```markdown
### Table: Appointment
| Column | Type | Constraints |
|--------|------|-------------|
| AppointmentID | INT | PK, AUTO_INCREMENT |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| DoctorID | INT | FK → Doctor(DoctorID), NOT NULL |
| AppointmentDateTime | DATETIME | NOT NULL |
| Status | ENUM('Scheduled','Completed','Cancelled','No-Show') | NOT NULL, DEFAULT 'Scheduled' |
| Type | ENUM('Walk-in','Booked') | NOT NULL |
| Notes | TEXT | |
```

---

### Table 6 of 6: Payment

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `PaymentID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `AppointmentID` | INT | **FOREIGN KEY → Appointment(AppointmentID), UNIQUE, NOT NULL** | 1:1 with Appointment |
| `Amount` | DECIMAL(10,2) | **NOT NULL** | e.g., 150.00 |
| `PaymentDate` | DATETIME | — | When payment was made |
| `PaymentMethod` | ENUM('Cash','Card','Online') | — | How paid |
| `Status` | ENUM('Paid','Refunded','Pending') | **NOT NULL, DEFAULT 'Pending'** | Payment status |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:1 with Appointment | FK here (UNIQUE) | `Payment.AppointmentID` → `Appointment.AppointmentID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ The UNIQUE constraint on `AppointmentID` enforces 1:1 (one payment per appointment)
- ⚠️ `Amount` is DECIMAL(10,2) to handle currency precisely (up to 99,999,999.99)

**What to write in `relational-schema.md`:**
```markdown
### Table: Payment
| Column | Type | Constraints |
|--------|------|-------------|
| PaymentID | INT | PK, AUTO_INCREMENT |
| AppointmentID | INT | FK → Appointment(AppointmentID), UNIQUE, NOT NULL |
| Amount | DECIMAL(10,2) | NOT NULL |
| PaymentDate | DATETIME | |
| PaymentMethod | ENUM('Cash','Card','Online') | |
| Status | ENUM('Paid','Refunded','Pending') | NOT NULL, DEFAULT 'Pending' |
```

---

### ✅ Omar's Step-by-Step Work Order

```
1. Users (independent — start here)
2. Patient (depends on Users)
3. Bed (depends on Ziad's DepartmentLocation — coordinate first)
4. Appointment (depends on Ziad's Doctor — coordinate first)
5. EmergencyVisit (depends on Youssef's Triage — coordinate first)
6. Payment (depends on Appointment — do last)
```

**Coordination checkpoints:**
- Before Bed: Ask Ziad for `DepartmentLocation.LocationID` data type and name
- Before Appointment: Ask Ziad for `Doctor.DoctorID` data type and name
- Before EmergencyVisit: Ask Youssef for `Triage.TriageID` data type and name

---

# Member 2 — Ziad Khaled
## Focus: Staff Hierarchy & Location Tables
### Your 6 Tables: Employee · Doctor · Nurse · Admin · Department · DepartmentLocation

---

### Table 1 of 6: Employee (Superclass)

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `EmployeeID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `UserID` | INT | **FOREIGN KEY → Users(UserID), UNIQUE, NOT NULL** | 1:1 with Users |
| `FirstName` | VARCHAR(50) | **NOT NULL** | Split from composite Name |
| `LastName` | VARCHAR(50) | **NOT NULL** | Split from composite Name |
| `BirthDate` | DATE | — | Can be NULL |
| `Sex` | ENUM('M','F') | **NOT NULL** | Binary |
| `SSN` | VARCHAR(20) | **UNIQUE, NOT NULL** | 🔴 PDF unique attribute |
| `HireDate` | DATE | — | When hired |
| `JobTitle` | VARCHAR(100) | — | e.g., "ER Physician", "Charge Nurse" |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:1 with Users | FK here | `Employee.UserID` → `Users.UserID` (UNIQUE) |
| ISA → Doctor | FK in Doctor | `Doctor.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |
| ISA → Nurse | FK in Nurse | `Nurse.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |
| ISA → Admin | FK in Admin | `Admin.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF: All atomic
- ✅ 2NF: Single-column PK, no partial dependencies
- ✅ 3NF: No transitive dependencies
- ⚠️ The ISA hierarchy is implemented via **subclass tables with FK to superclass**. This is the "class table inheritance" pattern.

**What to write in `relational-schema.md`:**
```markdown
### Table: Employee
| Column | Type | Constraints |
|--------|------|-------------|
| EmployeeID | INT | PK, AUTO_INCREMENT |
| UserID | INT | FK → Users(UserID), UNIQUE, NOT NULL |
| FirstName | VARCHAR(50) | NOT NULL |
| LastName | VARCHAR(50) | NOT NULL |
| BirthDate | DATE | |
| Sex | ENUM('M','F') | NOT NULL |
| SSN | VARCHAR(20) | UNIQUE, NOT NULL |
| HireDate | DATE | |
| JobTitle | VARCHAR(100) | |
```

---

### Table 2 of 6: Doctor

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `DoctorID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key (also used as FK target) |
| `EmployeeID` | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | ISA inheritance |
| `DepartmentID` | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | Works in which dept |
| `MajorScientificArea` | VARCHAR(100) | — | e.g., "Emergency Medicine", "Cardiology" |
| `Degree` | VARCHAR(50) | — | e.g., "MD", "DO", "MBBS" |
| `JoinDate` | DATE | — | Date joined the department |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| ISA from Employee | FK here | `Doctor.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |
| N:1 with Department | FK here | `Doctor.DepartmentID` → `Department.DepartmentID` |
| 1:1 Chairman with Department | FK in Department | `Department.ChairmanDoctorID` → `Doctor.DoctorID` (UNIQUE) |
| 1:N with Examination | FK in Examination | `Examination.DoctorID` → `Doctor.DoctorID` |
| 1:N with Prescription | FK in Prescription | `Prescription.DoctorID` → `Doctor.DoctorID` |
| 1:N with Appointment | FK in Appointment | `Appointment.DoctorID` → `Doctor.DoctorID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ **Circular dependency alert:** `Doctor.DepartmentID` references `Department`, and `Department.ChairmanDoctorID` references `Doctor`. In SQL, create both tables first without the circular FK, then `ALTER TABLE` to add it.
- ⚠️ `EmployeeID` is UNIQUE — enforces that each employee can be a doctor at most once.

**What to write in `relational-schema.md`:**
```markdown
### Table: Doctor
| Column | Type | Constraints |
|--------|------|-------------|
| DoctorID | INT | PK, AUTO_INCREMENT |
| EmployeeID | INT | FK → Employee(EmployeeID), UNIQUE, NOT NULL |
| DepartmentID | INT | FK → Department(DepartmentID), NOT NULL |
| MajorScientificArea | VARCHAR(100) | |
| Degree | VARCHAR(50) | |
| JoinDate | DATE | |
```

---

### Table 3 of 6: Nurse

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `NurseID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `EmployeeID` | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | ISA inheritance |
| `DepartmentID` | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | Works in which dept |
| `JoinDate` | DATE | — | Date joined the department |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| ISA from Employee | FK here | `Nurse.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |
| N:1 with Department | FK here | `Nurse.DepartmentID` → `Department.DepartmentID` |
| 1:N with Triage | FK in Triage | `Triage.NurseID` → `Nurse.NurseID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- Simpler than Doctor — fewer attributes and relationships

**What to write in `relational-schema.md`:**
```markdown
### Table: Nurse
| Column | Type | Constraints |
|--------|------|-------------|
| NurseID | INT | PK, AUTO_INCREMENT |
| EmployeeID | INT | FK → Employee(EmployeeID), UNIQUE, NOT NULL |
| DepartmentID | INT | FK → Department(DepartmentID), NOT NULL |
| JoinDate | DATE | |
```

---

### Table 4 of 6: Admin

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `AdminID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `EmployeeID` | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | ISA inheritance |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| ISA from Employee | FK here | `Admin.EmployeeID` → `Employee.EmployeeID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Minimal table — just PK and FK
- This is the simplest table in the entire schema

**What to write in `relational-schema.md`:**
```markdown
### Table: Admin
| Column | Type | Constraints |
|--------|------|-------------|
| AdminID | INT | PK, AUTO_INCREMENT |
| EmployeeID | INT | FK → Employee(EmployeeID), UNIQUE, NOT NULL |
```

---

### Table 5 of 6: Department

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `DepartmentID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `Name` | VARCHAR(100) | **UNIQUE, NOT NULL** | 🔴 PDF unique attribute |
| `Code` | VARCHAR(20) | **UNIQUE, NOT NULL** | 🔴 PDF unique attribute |
| `ChairmanDoctorID` | INT | **FOREIGN KEY → Doctor(DoctorID), UNIQUE** | Who chairs the dept |
| `SupervisionStartDate` | DATE | — | When chairman started |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:N with Doctor | FK in Doctor | `Doctor.DepartmentID` → `Department.DepartmentID` |
| 1:N with Nurse | FK in Nurse | `Nurse.DepartmentID` → `Department.DepartmentID` |
| 1:1 Chairman with Doctor | FK here | `Department.ChairmanDoctorID` → `Doctor.DoctorID` (UNIQUE) |
| 1:N with DepartmentLocation | FK in DepartmentLocation | `DepartmentLocation.DepartmentID` → `Department.DepartmentID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ **Circular dependency:** `ChairmanDoctorID` references `Doctor.DoctorID`, but `Doctor.DepartmentID` references `Department.DepartmentID`. Handle this in SQL by:
  1. Create `Department` table **without** the `ChairmanDoctorID` FK constraint
  2. Create `Doctor` table with `DepartmentID` FK
  3. `ALTER TABLE Department ADD CONSTRAINT fk_chairman FOREIGN KEY (ChairmanDoctorID) REFERENCES Doctor(DoctorID);`

**What to write in `relational-schema.md`:**
```markdown
### Table: Department
| Column | Type | Constraints |
|--------|------|-------------|
| DepartmentID | INT | PK, AUTO_INCREMENT |
| Name | VARCHAR(100) | UNIQUE, NOT NULL |
| Code | VARCHAR(20) | UNIQUE, NOT NULL |
| ChairmanDoctorID | INT | FK → Doctor(DoctorID), UNIQUE |
| SupervisionStartDate | DATE | |
```

---

### Table 6 of 6: DepartmentLocation

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `LocationID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `DepartmentID` | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | Which department |
| `Address` | TEXT | — | Full address |
| `Latitude` | DECIMAL(10,8) | — | For geo-location queries |
| `Longitude` | DECIMAL(11,8) | — | For geo-location queries |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Department | FK here | `DepartmentLocation.DepartmentID` → `Department.DepartmentID` |
| 1:N with Bed | FK in Bed | `Bed.LocationID` → `DepartmentLocation.LocationID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ Latitude/Longitude support the "find nearest place" requirement. DECIMAL precision: 10,8 gives ~1cm accuracy.

**What to write in `relational-schema.md`:**
```markdown
### Table: DepartmentLocation
| Column | Type | Constraints |
|--------|------|-------------|
| LocationID | INT | PK, AUTO_INCREMENT |
| DepartmentID | INT | FK → Department(DepartmentID), NOT NULL |
| Address | TEXT | |
| Latitude | DECIMAL(10,8) | |
| Longitude | DECIMAL(11,8) | |
```

---

### ✅ Ziad's Step-by-Step Work Order

```
1. Employee (depends on Omar's Users — coordinate first)
2. Department (independent of others — can start anytime)
3. Doctor (depends on Employee and Department)
4. Nurse (depends on Employee and Department)
5. Admin (depends on Employee)
6. DepartmentLocation (depends on Department)
```

**Coordination checkpoints:**
- Before Employee: Ask Omar for `Users.UserID` data type
- Before Doctor: Make sure Department is created first
- After all 6: Tell Omar your `Doctor.DoctorID` type and `DepartmentLocation.LocationID` type

---

# Member 3 — Youssef Amir
## Focus: Clinical & Medication Tables
### Your 6 Tables: Triage · Examination · Prescription · PrescriptionDetail · Medication · Document

---

### Table 1 of 6: Triage (Weak Entity)

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `TriageID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | Which patient |
| `NurseID` | INT | **FOREIGN KEY → Nurse(NurseID), NOT NULL** | Who performed triage |
| `DateTime` | DATETIME | **NOT NULL** | When triage occurred |
| `ChiefComplaint` | TEXT | — | e.g., "Chest pain" |
| `TriageLevel` | INT | **CHECK (TriageLevel BETWEEN 1 AND 5), NOT NULL** | Severity 1-5 |
| `BloodPressure` | VARCHAR(10) | — | Measured at triage |
| `HeartRate` | INT | — | Measured at triage |
| `Temperature` | DECIMAL(4,1) | — | Measured at triage |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Patient | FK here | `Triage.PatientID` → `Patient.PatientID` |
| N:1 with Nurse | FK here | `Triage.NurseID` → `Nurse.NurseID` |
| 1:1 with EmergencyVisit | FK in EmergencyVisit | `EmergencyVisit.TriageID` → `Triage.TriageID` (UNIQUE) |

**Normalization Notes:**
- ✅ 1NF: All atomic
- ✅ 2NF: All non-key attributes depend on TriageID (single PK)
- ✅ 3NF: No transitive dependencies
- ⚠️ Even though Triage is a **weak entity** in the ERD, we use a surrogate `TriageID` as PK. The "weak" nature is enforced by the NOT NULL FKs to Patient and Nurse — a triage record cannot exist without both.

**What to write in `relational-schema.md`:**
```markdown
### Table: Triage
| Column | Type | Constraints |
|--------|------|-------------|
| TriageID | INT | PK, AUTO_INCREMENT |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| NurseID | INT | FK → Nurse(NurseID), NOT NULL |
| DateTime | DATETIME | NOT NULL |
| ChiefComplaint | TEXT | |
| TriageLevel | INT | CHECK (TriageLevel BETWEEN 1 AND 5), NOT NULL |
| BloodPressure | VARCHAR(10) | |
| HeartRate | INT | |
| Temperature | DECIMAL(4,1) | |
```

---

### Table 2 of 6: Examination (Associative Entity)

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `ExaminationID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `DoctorID` | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | Who examined |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | Who was examined |
| `VisitID` | INT | **FOREIGN KEY → EmergencyVisit(VisitID), NOT NULL** | During which visit |
| `ExaminationDate` | DATETIME | **NOT NULL** | When examination occurred |
| `HoursSpent` | DECIMAL(4,2) | — | Duration (e.g., 1.50 = 1h 30m) |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Doctor | FK here | `Examination.DoctorID` → `Doctor.DoctorID` |
| N:1 with Patient | FK here | `Examination.PatientID` → `Patient.PatientID` |
| N:1 with EmergencyVisit | FK here | `Examination.VisitID` → `EmergencyVisit.VisitID` |

**Normalization Notes:**
- ✅ 1NF: All atomic
- ✅ 2NF: All depend on ExaminationID (surrogate PK)
- ✅ 3NF: No transitive dependencies
- ⚠️ This is an **associative entity** that resolves the M:N relationship between Doctor and Patient. The `VisitID` FK adds context — which visit did this examination happen during?
- ⚠️ The PDF says "hours per week spent on each patient" — we store `HoursSpent` per examination session. The application can SUM these per week to get weekly totals.

**What to write in `relational-schema.md`:**
```markdown
### Table: Examination
| Column | Type | Constraints |
|--------|------|-------------|
| ExaminationID | INT | PK, AUTO_INCREMENT |
| DoctorID | INT | FK → Doctor(DoctorID), NOT NULL |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| VisitID | INT | FK → EmergencyVisit(VisitID), NOT NULL |
| ExaminationDate | DATETIME | NOT NULL |
| HoursSpent | DECIMAL(4,2) | |
```

---

### Table 3 of 6: Prescription

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `PrescriptionID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `DoctorID` | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | Who prescribed |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | For which patient |
| `VisitID` | INT | **FOREIGN KEY → EmergencyVisit(VisitID), NOT NULL** | During which visit |
| `PrescriptionDate` | DATE | **NOT NULL** | When prescribed |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Doctor | FK here | `Prescription.DoctorID` → `Doctor.DoctorID` |
| N:1 with Patient | FK here | `Prescription.PatientID` → `Patient.PatientID` |
| N:1 with EmergencyVisit | FK here | `Prescription.VisitID` → `EmergencyVisit.VisitID` |
| 1:N with PrescriptionDetail | FK in PrescriptionDetail | `PrescriptionDetail.PrescriptionID` → `Prescription.PrescriptionID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- This is the **header** table — it links doctor, patient, and visit. The actual medications are in `PrescriptionDetail`.

**What to write in `relational-schema.md`:**
```markdown
### Table: Prescription
| Column | Type | Constraints |
|--------|------|-------------|
| PrescriptionID | INT | PK, AUTO_INCREMENT |
| DoctorID | INT | FK → Doctor(DoctorID), NOT NULL |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| VisitID | INT | FK → EmergencyVisit(VisitID), NOT NULL |
| PrescriptionDate | DATE | NOT NULL |
```

---

### Table 4 of 6: PrescriptionDetail

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `PrescriptionDetailID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `PrescriptionID` | INT | **FOREIGN KEY → Prescription(PrescriptionID), NOT NULL** | Which prescription |
| `MedicationID` | INT | **FOREIGN KEY → Medication(MedicationID), NOT NULL** | Which medication |
| `Directions` | TEXT | — | e.g., "Take with food" |
| `Dosage` | VARCHAR(50) | — | e.g., "500mg" |
| `TimesPerDay` | INT | — | e.g., 1, 2, 3 |
| `StartDate` | DATE | **NOT NULL** | When to start |
| `EndDate` | DATE | **NOT NULL** | When to stop |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Prescription | FK here | `PrescriptionDetail.PrescriptionID` → `Prescription.PrescriptionID` |
| N:1 with Medication | FK here | `PrescriptionDetail.MedicationID` → `Medication.MedicationID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ `StartDate` and `EndDate` are NOT NULL — every medication must have a defined treatment period
- ⚠️ This table satisfies the PDF requirement: *"The doctor should give the directions for each medication (how many times per day and dose). We keep track of both the start and end dates."*

**What to write in `relational-schema.md`:**
```markdown
### Table: PrescriptionDetail
| Column | Type | Constraints |
|--------|------|-------------|
| PrescriptionDetailID | INT | PK, AUTO_INCREMENT |
| PrescriptionID | INT | FK → Prescription(PrescriptionID), NOT NULL |
| MedicationID | INT | FK → Medication(MedicationID), NOT NULL |
| Directions | TEXT | |
| Dosage | VARCHAR(50) | |
| TimesPerDay | INT | |
| StartDate | DATE | NOT NULL |
| EndDate | DATE | NOT NULL |
```

---

### Table 5 of 6: Medication

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `MedicationID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `Name` | VARCHAR(100) | **NOT NULL** | Drug name |
| `Description` | TEXT | — | What it's used for |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| 1:N with PrescriptionDetail | FK in PrescriptionDetail | `PrescriptionDetail.MedicationID` → `Medication.MedicationID` |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Simple lookup table
- This is the simplest table — just a drug catalog

**What to write in `relational-schema.md`:**
```markdown
### Table: Medication
| Column | Type | Constraints |
|--------|------|-------------|
| MedicationID | INT | PK, AUTO_INCREMENT |
| Name | VARCHAR(100) | NOT NULL |
| Description | TEXT | |
```

---

### Table 6 of 6: Document

**ERD Entity → Relational Table**

| Column Name | Data Type | Constraints | Notes |
|-------------|-----------|-------------|-------|
| `DocumentID` | INT | **PRIMARY KEY, AUTO_INCREMENT** | Surrogate key |
| `PatientID` | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | Which patient |
| `VisitID` | INT | **FOREIGN KEY → EmergencyVisit(VisitID)** | NULLABLE — may not be linked to a visit |
| `FileName` | VARCHAR(255) | — | Original file name |
| `FilePath` | VARCHAR(500) | — | Server storage path |
| `UploadDate` | DATETIME | **DEFAULT CURRENT_TIMESTAMP** | When uploaded |
| `Description` | TEXT | — | What the document is |

**Relationships Mapped:**
| Relationship | Mapping | Where FK Lives |
|-------------|---------|----------------|
| N:1 with Patient | FK here | `Document.PatientID` → `Patient.PatientID` |
| N:1 with EmergencyVisit | FK here | `Document.VisitID` → `EmergencyVisit.VisitID` (nullable) |

**Normalization Notes:**
- ✅ 1NF, 2NF, 3NF: Clean design
- ⚠️ `VisitID` is nullable — some documents may be uploaded before a visit is created (e.g., prior medical records)
- ⚠️ This table satisfies the requirement: *"Static file serving and file uploads (e.g., patient scans)"*

**What to write in `relational-schema.md`:**
```markdown
### Table: Document
| Column | Type | Constraints |
|--------|------|-------------|
| DocumentID | INT | PK, AUTO_INCREMENT |
| PatientID | INT | FK → Patient(PatientID), NOT NULL |
| VisitID | INT | FK → EmergencyVisit(VisitID) |
| FileName | VARCHAR(255) | |
| FilePath | VARCHAR(500) | |
| UploadDate | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| Description | TEXT | |
```

---

### ✅ Youssef's Step-by-Step Work Order

```
1. Medication (independent — start here)
2. Triage (depends on Omar's Patient and Ziad's Nurse)
3. Prescription (depends on Ziad's Doctor, Omar's Patient, Omar's EmergencyVisit)
4. PrescriptionDetail (depends on Prescription and Medication — both yours)
5. Examination (depends on Ziad's Doctor, Omar's Patient, Omar's EmergencyVisit)
6. Document (depends on Omar's Patient, optionally Omar's EmergencyVisit)
```

**Coordination checkpoints:**
- Before Triage: Ask Omar for `Patient.PatientID` type, ask Ziad for `Nurse.NurseID` type
- Before Prescription: Ask Ziad for `Doctor.DoctorID` type, ask Omar for `Patient.PatientID` and `EmergencyVisit.VisitID` types
- Before Examination: Same coordination as Prescription

---

## Cross-Table Relationship Mapping

This section shows how all relationships between the 18 tables are implemented via foreign keys.

### 1:1 Relationships

| Table A | Table B | FK Column | Where FK Lives | Constraint |
|---------|---------|-----------|----------------|------------|
| Users | Patient | UserID | Patient.UserID | UNIQUE, NOT NULL |
| Users | Employee | UserID | Employee.UserID | UNIQUE, NOT NULL |
| Triage | EmergencyVisit | TriageID | EmergencyVisit.TriageID | UNIQUE, NOT NULL |
| Appointment | Payment | AppointmentID | Payment.AppointmentID | UNIQUE, NOT NULL |
| Employee | Doctor | EmployeeID | Doctor.EmployeeID | UNIQUE, NOT NULL |
| Employee | Nurse | EmployeeID | Nurse.EmployeeID | UNIQUE, NOT NULL |
| Employee | Admin | EmployeeID | Admin.EmployeeID | UNIQUE, NOT NULL |
| Department | Doctor (Chairman) | ChairmanDoctorID | Department.ChairmanDoctorID | UNIQUE |

### 1:N Relationships

| Table 1 (1-side) | Table N (N-side) | FK Column | Where FK Lives |
|------------------|------------------|-----------|----------------|
| Patient | Triage | PatientID | Triage.PatientID |
| Patient | EmergencyVisit | PatientID | EmergencyVisit.PatientID |
| Patient | Examination | PatientID | Examination.PatientID |
| Patient | Prescription | PatientID | Prescription.PatientID |
| Patient | Appointment | PatientID | Appointment.PatientID |
| Patient | Document | PatientID | Document.PatientID |
| Nurse | Triage | NurseID | Triage.NurseID |
| Bed | EmergencyVisit | BedID | EmergencyVisit.BedID |
| Department | Doctor | DepartmentID | Doctor.DepartmentID |
| Department | Nurse | DepartmentID | Nurse.DepartmentID |
| Department | DepartmentLocation | DepartmentID | DepartmentLocation.DepartmentID |
| DepartmentLocation | Bed | LocationID | Bed.LocationID |
| Doctor | Examination | DoctorID | Examination.DoctorID |
| Doctor | Prescription | DoctorID | Prescription.DoctorID |
| Doctor | Appointment | DoctorID | Appointment.DoctorID |
| EmergencyVisit | Examination | VisitID | Examination.VisitID |
| EmergencyVisit | Prescription | VisitID | Prescription.VisitID |
| EmergencyVisit | Document | VisitID | Document.VisitID |
| Prescription | PrescriptionDetail | PrescriptionID | PrescriptionDetail.PrescriptionID |
| Medication | PrescriptionDetail | MedicationID | PrescriptionDetail.MedicationID |

---

## Normalization Checklist (3NF)

Each member must verify their tables pass 3NF. Here's the checklist:

### 1NF (First Normal Form)
- [ ] All columns contain **atomic** (indivisible) values
- [ ] No repeating groups or arrays in any column
- [ ] Each row is unique (enforced by PK)

### 2NF (Second Normal Form)
- [ ] Already in 1NF
- [ ] No **partial dependencies** — all non-key columns depend on the **entire** PK
- [ ] Since all our tables use single-column surrogate PKs, 2NF is automatically satisfied

### 3NF (Third Normal Form)
- [ ] Already in 2NF
- [ ] No **transitive dependencies** — non-key columns don't depend on other non-key columns
- [ ] Example violation (NOT in our design): If we had `DepartmentName` in Doctor table, that would be transitive (Doctor → DepartmentID → DepartmentName). We avoid this by putting DepartmentName only in Department table.

### Verification Table

| Table | 1NF | 2NF | 3NF | Notes |
|-------|-----|-----|-----|-------|
| Users | ✅ | ✅ | ✅ | Clean |
| Patient | ✅ | ✅ | ✅ | Vitals are current snapshot; historical in Triage |
| Employee | ✅ | ✅ | ✅ | Superclass — clean |
| Doctor | ✅ | ✅ | ✅ | ISA pattern |
| Nurse | ✅ | ✅ | ✅ | ISA pattern |
| Admin | ✅ | ✅ | ✅ | ISA pattern |
| Department | ✅ | ✅ | ✅ | Circular FK handled via ALTER TABLE |
| DepartmentLocation | ✅ | ✅ | ✅ | Clean |
| Bed | ✅ | ✅ | ✅ | Clean |
| Triage | ✅ | ✅ | ✅ | Weak entity with surrogate PK |
| EmergencyVisit | ✅ | ✅ | ✅ | Clean |
| Examination | ✅ | ✅ | ✅ | Associative entity |
| Prescription | ✅ | ✅ | ✅ | Header table |
| PrescriptionDetail | ✅ | ✅ | ✅ | Detail table |
| Medication | ✅ | ✅ | ✅ | Lookup table |
| Appointment | ✅ | ✅ | ✅ | Clean |
| Payment | ✅ | ✅ | ✅ | 1:1 via UNIQUE FK |
| Document | ✅ | ✅ | ✅ | Nullable VisitID |

---

## Final Output Format

Each member writes their section in `schemas/relational-schema.md` using this format:

```markdown
## Table: TableName

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| ColumnName | TYPE | PK/FK/UNIQUE/NOT NULL/etc. | What it stores |

**Foreign Keys:**
- `ColumnName` → ReferencedTable(ReferencedColumn)

**Indexes:**
- (list any additional indexes beyond PK/FK)

**Normalization:**
- 1NF: [reason]
- 2NF: [reason]
- 3NF: [reason]
```

### Example (from Omar's Users table):

```markdown
## Table: Users

| Column | Data Type | Constraints | Description |
|--------|-----------|-------------|-------------|
| UserID | INT | PK, AUTO_INCREMENT | Unique user identifier |
| Username | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| PasswordHash | VARCHAR(255) | NOT NULL | Bcrypt-hashed password |
| Email | VARCHAR(100) | UNIQUE | User email address |
| Role | ENUM('Patient','Doctor','Nurse','Admin') | NOT NULL | Access role |
| CreatedAt | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Foreign Keys:**
- None (referenced by Patient.UserID and Employee.UserID)

**Normalization:**
- 1NF: All columns atomic
- 2NF: Single-column PK, no partial dependencies
- 3NF: No transitive dependencies
```

---

## Timeline

| Day | Date | Task |
|-----|------|------|
| **Today** | Mon, May 18 | Each member writes their 6 table definitions in `schemas/relational-schema.md` |
| **Tonight** | Mon, May 18 | Cross-check FK references between members (coordinate data types and names) |
| **Tomorrow AM** | Tue, May 19 | Merge all sections into one complete `relational-schema.md` |
| **Tomorrow PM** | Tue, May 19 | Review for normalization violations, missing constraints, circular dependencies |
| **Wed** | May 20 | Finalize and commit |

---

*Let's get this done! 💪*
