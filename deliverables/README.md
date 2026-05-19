# 🏥 ERD Deliverables — Emergency Department

## 👥 Team Members
| Member | Role |
|--------|------|
| **Omar Hesham** | Team Leader — Patient Flow & Appointments |
| **Ziad Khaled** | Staff Hierarchy & Locations |
| **Youssef Amir** | Clinical & Medication |

---

## 📋 Table of Contents
1. [How to Use This Document](#how-to-use-this-document)
2. [ERD Notation Reference (Cheat Sheet)](#erd-notation-reference-cheat-sheet)
3. [Member 1 — Omar Hesham](#member-1--omar-hesham-team-leader)
   - Users · Patient · EmergencyVisit · Bed · Appointment · Payment
4. [Member 2 — Ziad Khaled](#member-2--ziad-khaled)
   - Hospital · Employee · Doctor · Nurse · Admin · Department · DepartmentLocation
5. [Member 3 — Youssef Amir](#member-3--youssef-amir)
   - Triage · Examination · Prescription · PrescriptionDetail · Medication · Document
6. [Dependency Map (Who to Coordinate With)](#dependency-map)
7. [Timeline & Milestones](#timeline--milestones)

---

## How to Use This Document

### Your Mission
Each member must design **6 entities** in an ERD tool (**draw.io** or **Lucidchart**). These will be combined into one master ERD by Tuesday.

### For Each of Your 6 Entities, You Must:
| Step | Action | ERD Notation |
|------|--------|-------------|
| 1️⃣ | Draw a **rectangle** for the entity | ▭ EntityName |
| 2️⃣ | List all **attributes** inside (or as ovals) | Attribute1, Attribute2, ... |
| 3️⃣ | **Underline** the Primary Key(s) | <u>PK</u> |
| 4️⃣ | **Bold + Underline** unique attributes | **<u>SSN</u>** |
| 5️⃣ | Mark Foreign Keys with **(FK)** and draw a line to the referenced entity | → ReferencedEntity |
| 6️⃣ | Label relationship **cardinalities** on the connecting lines | 1, N, or M |
| 7️⃣ | Add **constraints** as notes (ENUM values, CHECK bounds) | Note: Level 1-5 |

### Relationship Line Symbols
```
   1 —————— N        One-to-Many
   1 —————— 1        One-to-One
   N —————— M        Many-to-Many (rare — use associative table)
   ═══ thick line ═══ Total participation (every instance must participate)
```

---

## ERD Notation Reference (Cheat Sheet)

Keep this open while drawing:

| Symbol | Meaning | Example |
|--------|---------|---------|
| `▭ Rectangle` | Entity (a table) | `▭ Patient` |
| `▭▭ Double Rectangle` | Weak Entity (depends on another) | `▭▭ Triage` |
| `◊ Diamond` | Relationship | `◊ Examines` |
| `<u>underline</u>` | Primary Key | `<u>PatientID</u>` |
| **`<u>bold+underline</u>`** | **Unique** (bold in PDF) | **`<u>SSN</u>`** |
| `(FK)` | Foreign Key | `DepartmentID (FK)` |
| `1`, `N`, `M` on lines | Cardinality | `Patient —1—N— EmergencyVisit` |
| `[A, B, C]` | ENUM values | `Status [Available, Occupied]` |
| `(min, max)` | Min/Max participation | `(1,1)` or `(0,N)` |

---

# Member 1 — Omar Hesham 👑 (Team Leader)
## Focus: Patient Flow & Appointments
### Your 6 Entities: Users · Patient · EmergencyVisit · Bed · Appointment · Payment

---

### Entity 1 of 6: Users

**What it represents:** Every person who logs into the system — patients, doctors, nurses, and admins. This is the **authentication foundation**. All other people-entities will reference this table.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| UserID | INT | **PRIMARY KEY** | <u>UserID</u> |
| Username | VARCHAR(50) | **UNIQUE, NOT NULL** | Username |
| PasswordHash | VARCHAR(255) | **NOT NULL** | PasswordHash |
| Email | VARCHAR(100) | **UNIQUE** | Email |
| Role | ENUM('Patient','Doctor','Nurse','Admin') | **NOT NULL** | Role [Patient,Doctor,Nurse,Admin] |
| CreatedAt | DATETIME | DEFAULT CURRENT_TIMESTAMP | CreatedAt |

**Relationships (how to draw them):**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Has (login) | Patient | 1:1 | Line from Users to Patient, label `1` on Users side, `1` on Patient side. Put `◊ Has` diamond in between. Add a note: *"Each User is optionally one Patient"* |
| Has (login) | Employee | 1:1 | Line from Users to Employee, label `1` on Users side, `1` on Employee side. Put `◊ Has` diamond. |

**Drawing instructions:**
- Users is an **independent entity** — no FK dependencies. Draw it first.
- The two `1:1` relationships mean: one User record can belong to **either** a Patient **or** an Employee (not both, but the ERD shows both lines).
- In the actual database, this is implemented by putting a `UNIQUE` FK in Patient and Employee tables that references UserID.

**📌 Dependencies:**
- Ziad needs UserID from you **before** he can create Employee (Employee has FK → Users).
- Youssef doesn't directly depend on Users for his entities.
- ⚠️ **Deadline for this entity: Monday morning** — others are waiting on it!

---

### Entity 2 of 6: Patient

**What it represents:** A patient's complete medical record. This is the **most detailed entity** with medical history and vitals. Each patient links to exactly one User account.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| PatientID | INT | **PRIMARY KEY** | <u>PatientID</u> |
| UserID | INT | **UNIQUE, FOREIGN KEY → Users(UserID), NOT NULL** | UserID (FK) → Users |
| SSN | VARCHAR(20) | **UNIQUE, NOT NULL** | **<u>SSN</u>** 🔴 |
| PatientNumber | VARCHAR(20) | **UNIQUE, NOT NULL** | **<u>PatientNumber</u>** 🔴 |
| FirstName | VARCHAR(50) | **NOT NULL** | FirstName |
| LastName | VARCHAR(50) | **NOT NULL** | LastName |
| Address | VARCHAR(255) | — | Address |
| Phone | VARCHAR(20) | — | Phone |
| BirthDate | DATE | — | BirthDate |
| Sex | ENUM('M','F') | **NOT NULL** | Sex [M,F] |
| MedicalHistory | TEXT | — | MedicalHistory |
| BloodPressure | VARCHAR(10) | — | BloodPressure (e.g., "120/80") |
| HeartRate | INT | — | HeartRate |
| Temperature | DECIMAL(4,1) | — | Temperature |

🔴 **Bold+Underline** = These are the **unique attributes** required by the PDF specification (SSN and PatientNumber). The evaluator will check these!

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Has (login) | Users | 1:1 (total on Patient side) | Line with `1` on both ends. Use thick line from Patient side (NOT NULL FK means mandatory). |
| Registered by Triage | Triage | 1:N | Line from Patient `1` to Triage `N`. Label `◊ Undergoes`. |
| Makes Visit | EmergencyVisit | 1:N | Line from Patient `1` to EmergencyVisit `N`. Label `◊ Makes`. |
| Examined in | Examination | 1:N | Line from Patient `1` to Examination `N`. |
| Receives Prescription | Prescription | 1:N | Line from Patient `1` to Prescription `N`. |
| Books Appointment | Appointment | 1:N | Line from Patient `1` to Appointment `N`. |
| Has Document | Document | 1:N | Line from Patient `1` to Document `N`. |

**Drawing instructions:**
- Patient is a **strong entity** with its own PK (PatientID).
- The UserID FK is **UNIQUE** — this enforces the 1:1 relationship with Users.
- **Do NOT list the relationship attributes inside Patient** — just show the relationship line.
- You can draw Patient's attributes in a list inside the rectangle, or as ovals attached.

**📌 Dependencies:**
- **You must finish Users first** (Patient.UserID references Users.UserID).
- Youssef needs PatientID from you **before** he can do Triage, Examination, Prescription, and Document.
- ⚠️ **Deadline: Monday** — Youssef is waiting on Triage!

---

### Entity 3 of 6: EmergencyVisit

**What it represents:** A patient's stay in the Emergency Department — from admission (after triage) to discharge. This is the **central entity** of the whole system. Almost every other clinical entity links back to it.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| VisitID | INT | **PRIMARY KEY** | <u>VisitID</u> |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| TriageID | INT | **FOREIGN KEY → Triage(TriageID), UNIQUE, NOT NULL** | TriageID (FK) → Triage |
| BedID | INT | **FOREIGN KEY → Bed(BedID), NULLABLE** | BedID (FK) → Bed (optional) |
| AdmissionDateTime | DATETIME | **NOT NULL** | AdmissionDateTime |
| DischargeDateTime | DATETIME | — (nullable) | DischargeDateTime |
| Disposition | ENUM('Admitted','Discharged','Transferred','Left Without Being Seen') | — | Disposition [Admitted,Discharged,Transferred,Left Without Being Seen] |

**Important design note:** The **TriageID is UNIQUE** in this table. This enforces the rule: **one triage produces exactly one emergency visit**. In ERD terms, this is a 1:1 relationship between Triage and EmergencyVisit.

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Belongs to | Patient | N:1 | Line from EmergencyVisit N to Patient 1. |
| Results from | Triage | 1:1 | Line from EmergencyVisit `1` to Triage `1`. TriageID is UNIQUE here. |
| Assigned to | Bed | N:1 (optional) | Line from EmergencyVisit N to Bed 1. Use dashed line or add `(optional)` because BedID can be NULL. |
| Has Examination | Examination | 1:N | Line from EmergencyVisit `1` to Examination `N`. |
| Has Prescription | Prescription | 1:N | Line from EmergencyVisit `1` to Prescription `N`. |
| Has Document | Document | 1:N | Line from EmergencyVisit `1` to Document `N`. |

**Drawing instructions:**
- Draw EmergencyVisit as a strong entity (single rectangle).
- The relationship to Triage is **1:1** — a unique constraint. Add a note on the line: *"One triage → one visit"*.
- The relationship to Bed is **optional**. Show this with a `(0,1)` on the Bed side or a dashed line.

**📌 Dependencies:**
- Needs **PatientID** from you (Patient).
- Needs **TriageID** from Youssef (Triage).
- Needs **BedID** from you (Bed — but Bed is also your entity, so define Bed before this).
- Youssef needs VisitID from you **before** he can do Examination and Prescription.
- ⚠️ **Order:** Users → Patient → Bed → Triage (Youssef) → **EmergencyVisit** → then Youssef can do Examination & Prescription.

---

### Entity 4 of 6: Bed

**What it represents:** A specific treatment bay, bed, or room in the Emergency Department where a patient stays during their visit.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| BedID | INT | **PRIMARY KEY** | <u>BedID</u> |
| RoomNumber | VARCHAR(20) | — | RoomNumber |
| LocationID | INT | **FOREIGN KEY → DepartmentLocation(LocationID), NOT NULL** | LocationID (FK) → DepartmentLocation |
| BedType | VARCHAR(50) | — (e.g., 'Trauma', 'Observation', 'Resuscitation') | BedType |
| Status | ENUM('Available','Occupied','Cleaning') | **NOT NULL, DEFAULT 'Available'** | Status [Available,Occupied,Cleaning] |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Located in | DepartmentLocation | N:1 | Line from Bed N to DepartmentLocation 1. |
| Assigned to | EmergencyVisit | 1:N | Line from Bed `1` to EmergencyVisit `N`. |

**Drawing instructions:**
- Bed is a strong entity.
- The `LocationID` FK links to **DepartmentLocation** — Ziad's entity. Coordinate with him on the exact attribute name and type.
- Draw a line from Bed to DepartmentLocation with `N` on Bed side and `1` on DepartmentLocation side.

**📌 Dependencies:**
- Needs **LocationID** from **Ziad** (DepartmentLocation).
- ⚠️ **Coordinate with Ziad:** Ask him what he's naming the PK in DepartmentLocation (should be `LocationID` INT).

---

### Entity 5 of 6: Appointment

**What it represents:** A scheduled (booked) or walk-in appointment between a patient and a doctor. ER walk-ins are treated as appointments created on arrival.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| AppointmentID | INT | **PRIMARY KEY** | <u>AppointmentID</u> |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| DoctorID | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | DoctorID (FK) → Doctor |
| AppointmentDateTime | DATETIME | **NOT NULL** | AppointmentDateTime |
| Status | ENUM('Scheduled','Completed','Cancelled','No-Show') | **NOT NULL, DEFAULT 'Scheduled'** | Status [Scheduled,Completed,Cancelled,No-Show] |
| Type | ENUM('Walk-in','Booked') | **NOT NULL** | Type [Walk-in,Booked] |
| Notes | TEXT | — | Notes |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Books | Patient | N:1 | Line from Appointment N to Patient 1. |
| Performs | Doctor | N:1 | Line from Appointment N to Doctor 1. |
| Has Payment | Payment | 1:1 | Line from Appointment `1` to Payment `1`. |

**Drawing instructions:**
- Strong entity with its own PK.
- Two `N:1` relationships to Patient and Doctor — both mandatory (NOT NULL FK).
- 1:1 relationship to Payment — implemented as UNIQUE FK on the Payment side.

**📌 Dependencies:**
- Needs **PatientID** from you (Patient).
- Needs **DoctorID** from **Ziad** (Doctor).
- ⚠️ **Coordinate with Ziad:** Ask him what he's naming the PK in Doctor (should be `DoctorID` INT).

---

### Entity 6 of 6: Payment

**What it represents:** A financial transaction for an appointment — either a payment or a refund. One appointment has exactly one payment.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| PaymentID | INT | **PRIMARY KEY** | <u>PaymentID</u> |
| AppointmentID | INT | **FOREIGN KEY → Appointment(AppointmentID), UNIQUE, NOT NULL** | AppointmentID (FK) → Appointment |
| Amount | DECIMAL(10,2) | **NOT NULL** | Amount |
| PaymentDate | DATETIME | — (default NOW) | PaymentDate |
| PaymentMethod | ENUM('Cash','Card','Online') | — | PaymentMethod [Cash,Card,Online] |
| Status | ENUM('Paid','Refunded','Pending') | **NOT NULL, DEFAULT 'Pending'** | Status [Paid,Refunded,Pending] |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Pays for | Appointment | 1:1 | Line from Payment `1` to Appointment `1`. The UNIQUE constraint on AppointmentID in Payment enforces this. |

**Drawing instructions:**
- Payment is a strong entity.
- The `AppointmentID` FK is **UNIQUE** — this makes the relationship 1:1. Add a note on the line: *"One payment per appointment"*.

**📌 Dependencies:**
- Needs **AppointmentID** from you (Appointment).
- This is the last entity in your chain. By the time you draw this, you should have all your other entities ready.

---

### ✅ Omar's Step-by-Step Work Order

Follow this exact order to avoid circular dependencies:

```
Day 1 (Mon):  Users → Patient → Bed → (coordinate with Ziad for LocationID)
Day 2 (Tue):  EmergencyVisit (once Youssef gives you TriageID)
Day 2 (Tue):  Appointment (once Ziad gives you DoctorID)
Day 2 (Tue):  Payment (once Appointment is done)
```

---

# Member 2 — Ziad Khaled
## Focus: Staff Hierarchy & Locations
### Your 7 Entities: Hospital · Employee · Doctor · Nurse · Admin · Department · DepartmentLocation

---

### Entity 1 of 7: Hospital

**What it represents:** The parent organization that contains multiple departments. This satisfies the explicit project requirement: *"Model hospitals including regular rooms, . etc"* and *"Model work relationship between doctor and hospital"*. Every department belongs to exactly one hospital.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| HospitalID | INT | **PRIMARY KEY** | <u>HospitalID</u> |
| Name | VARCHAR(100) | **UNIQUE, NOT NULL** | **<u>Name</u>** |
| Address | TEXT | — | Physical address |
| Phone | VARCHAR(20) | — | Contact number |
| Email | VARCHAR(100) | **UNIQUE** | Admin email |
| EstablishedYear | INT | — | Year founded |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Contains | Department | 1:N | Line from Hospital `1` to Department `N`. Label `◊ Contains`. |

**Drawing instructions:**
- Hospital is a **strong, independent entity** — no FK dependencies.
- Draw it at the top of your hierarchy since it's the highest-level entity.
- The 1:N relationship to Department means: one hospital has many departments, but each department belongs to exactly one hospital.
- Add a note: *"Hospital is the parent organization"*.

**📌 Dependencies:**
- None! Hospital is completely independent.
- ⚠️ **Draw this FIRST** — it's the root of the entire schema.
- Department needs HospitalID from you.

---

### Entity 2 of 7: Employee (Superclass)

**What it represents:** The **superclass** for all hospital staff — doctors, nurses, and administrators. Every employee has a User account for login. This uses the **ER specialization** pattern: Employee is the parent/general entity, and Doctor/Nurse/Admin are child/specific entities that inherit from it.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| EmployeeID | INT | **PRIMARY KEY** | <u>EmployeeID</u> |
| UserID | INT | **FOREIGN KEY → Users(UserID), UNIQUE, NOT NULL** | UserID (FK) → Users |
| FirstName | VARCHAR(50) | **NOT NULL** | FirstName |
| LastName | VARCHAR(50) | **NOT NULL** | LastName |
| BirthDate | DATE | — | BirthDate |
| Sex | ENUM('M','F') | **NOT NULL** | Sex [M,F] |
| SSN | VARCHAR(20) | **UNIQUE, NOT NULL** | **<u>SSN</u>** 🔴 |
| HireDate | DATE | — | HireDate |
| JobTitle | VARCHAR(100) | — | JobTitle |

🔴 **SSN must be bold+underlined** — it's one of the unique attributes from the PDF specification.

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Has (login) | Users | 1:1 | Line from Employee `1` to Users `1`. |
| Is a (specialization) | Doctor | 1:1 | Line from Employee `1` to Doctor `1`. Use **ISA triangle** notation (triangle labeled `ISA` between Employee and Doctor). |
| Is a (specialization) | Nurse | 1:1 | Same as above — Employee `1` → ISA → Nurse `1`. |
| Is a (specialization) | Admin | 1:1 | Same as above — Employee `1` → ISA → Admin `1`. |

**How to draw the ISA hierarchy (specialization):**
```
         ┌──────────┐
         │ Employee │  ← superclass
         └────▲─────┘
              │
            ◁ISA▷      ← triangle
         ┌────┴─────┐
         │          │
    ┌────┴───┐ ┌───┴────┐ ┌────┴───┐
    │ Doctor │ │ Nurse  │ │ Admin  │   ← subclasses
    └────────┘ └────────┘ └────────┘
```

**📌 Dependencies:**
- Needs **UserID** from **Omar** (Users).
- ⚠️ **This is the first entity you should draw** (after getting UserID from Omar).

---

### Entity 3 of 7: Doctor

**What it represents:** A doctor who works in the Emergency Department. Each doctor is a specialization of Employee (IS-A relationship).

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| DoctorID | INT | **PRIMARY KEY** | <u>DoctorID</u> |
| EmployeeID | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | EmployeeID (FK) → Employee |
| DepartmentID | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | DepartmentID (FK) → Department |
| MajorScientificArea | VARCHAR(100) | — | MajorScientificArea |
| Degree | VARCHAR(50) | — | Degree |
| JoinDate | DATE | — (date joined the department) | JoinDate |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Is a | Employee | 1:1 | Via ISA triangle (see above). |
| Works in | Department | N:1 | Line from Doctor N to Department 1. |
| Chairs | Department | 1:1 | Line from Doctor `1` to Department `1` (as Chairman). Add note: *"Doctor chairs one department"*. |
| Performs Examination | Examination | 1:N | Line from Doctor `1` to Examination `N`. |
| Writes Prescription | Prescription | 1:N | Line from Doctor `1` to Prescription `N`. |
| Has Appointment | Appointment | 1:N | Line from Doctor `1` to Appointment `N`. |

**Drawing instructions:**
- Doctor is a **subclass** — connected to Employee via ISA triangle.
- `EmployeeID` is both PK (DoctorID) and FK — and it's **UNIQUE** (enforces 1:1 with Employee).
- The **Chairman** relationship with Department is special: one doctor chairs at most one department, and one department has exactly one chairman.
- ⚠️ **Circular dependency:** Department.ChairmanDoctorID references Doctor.DoctorID, but Doctor.DepartmentID references Department.DepartmentID. **Solution:** First create both tables in your ERD without the Chairman FK, then add the Chairman line after both exist.

**📌 Dependencies:**
- Needs **EmployeeID** from you (Employee).
- Needs **DepartmentID** from you (Department — but you can define Department first).
- ⚠️ **Omar** needs DoctorID for Appointment.
- ⚠️ **Youssef** needs DoctorID for Examination and Prescription.

---

### Entity 4 of 7: Nurse

**What it represents:** A nurse who works in the Emergency Department, primarily responsible for performing triage assessments.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| NurseID | INT | **PRIMARY KEY** | <u>NurseID</u> |
| EmployeeID | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | EmployeeID (FK) → Employee |
| DepartmentID | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | DepartmentID (FK) → Department |
| JoinDate | DATE | — | JoinDate |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Is a | Employee | 1:1 | Via ISA triangle with Employee. |
| Works in | Department | N:1 | Line from Nurse N to Department 1. |
| Performs | Triage | 1:N | Line from Nurse `1` to Triage `N`. |

**Drawing instructions:**
- Same ISA pattern as Doctor.
- `EmployeeID` is UNIQUE — enforces 1:1 with Employee.
- Simpler than Doctor — only 3 relationships.

**📌 Dependencies:**
- Needs **EmployeeID** from you (Employee).
- Needs **DepartmentID** from you (Department).
- **Youssef** needs NurseID for Triage.

---

### Entity 5 of 7: Admin

**What it represents:** An administrative staff member who manages the system (e.g., handles reports, manages users, accesses the admin dashboard).

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| AdminID | INT | **PRIMARY KEY** | <u>AdminID</u> |
| EmployeeID | INT | **FOREIGN KEY → Employee(EmployeeID), UNIQUE, NOT NULL** | EmployeeID (FK) → Employee |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Is a | Employee | 1:1 | Via ISA triangle with Employee. |

**Drawing instructions:**
- The simplest entity in the whole system.
- Just AdminID (PK) and EmployeeID (FK, UNIQUE).
- Connected to Employee via ISA triangle.

**📌 Dependencies:**
- Needs **EmployeeID** from you (Employee).

---

### Entity 6 of 7: Department

**What it represents:** The Emergency Department itself — its identity, code, and who chairs it. Note: this system could have multiple departments, but we are focusing on the Emergency Department. Each department belongs to exactly one hospital.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| DepartmentID | INT | **PRIMARY KEY** | <u>DepartmentID</u> |
| HospitalID | INT | **FOREIGN KEY → Hospital(HospitalID), NOT NULL** | HospitalID (FK) → Hospital |
| Name | VARCHAR(100) | **UNIQUE, NOT NULL** | **<u>Name</u>** 🔴 |
| Code | VARCHAR(20) | **UNIQUE, NOT NULL** | **<u>Code</u>** 🔴 |
| ChairmanDoctorID | INT | **FOREIGN KEY → Doctor(DoctorID), UNIQUE** | ChairmanDoctorID (FK) → Doctor |
| SupervisionStartDate | DATE | — | SupervisionStartDate |

🔴 **Name and Code must be bold+underlined** — these are the unique attributes from the PDF requirement.

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Belongs to | Hospital | N:1 | Line from Department N to Hospital 1. Thick line on Department side (every dept belongs to a hospital). |
| Has Doctor | Doctor | 1:N | Line from Department `1` to Doctor `N`. |
| Has Nurse | Nurse | 1:N | Line from Department `1` to Nurse `N`. |
| Chaired by | Doctor | 1:1 | Line from Department `1` to Doctor `1` (Chairman). |
| Has Location | DepartmentLocation | 1:N | Line from Department `1` to DepartmentLocation `N`. |

**Drawing instructions:**
- Department is a strong entity with two UNIQUE attributes (Name, Code).
- The **ChairmanDoctorID** is a FK and is also UNIQUE — this enforces the 1:1 relationship (one department has one chairman, one doctor chairs at most one department).
- ⚠️ **Circular dependency:** Department.ChairmanDoctorID references Doctor.DoctorID. Solution: define Department first **without** the chairman, define Doctor (which references Department.DepartmentID), then go back and add the ChairmanDoctorID relationship line.

**📌 Dependencies:**
- Needs **HospitalID** from you (Hospital — define Hospital first, it's independent).
- Needs **DoctorID** for ChairmanDoctorID (circular — resolve after Doctor is created).
- Omar needs DepartmentID for nothing directly, but your DepartmentLocation feeds into Omar's Bed.
- Youssef doesn't directly need Department.

---

### Entity 7 of 7: DepartmentLocation

**What it represents:** A physical location where the department operates. A department can have multiple locations (e.g., main ER building, satellite urgent care). This also stores **geo-coordinates** for the "find nearest place" requirement.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| LocationID | INT | **PRIMARY KEY** | <u>LocationID</u> |
| DepartmentID | INT | **FOREIGN KEY → Department(DepartmentID), NOT NULL** | DepartmentID (FK) → Department |
| Address | TEXT | — | Address |
| Latitude | DECIMAL(10,8) | — (for geo-location queries) | Latitude |
| Longitude | DECIMAL(11,8) | — (for geo-location queries) | Longitude |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Belongs to | Department | N:1 | Line from DepartmentLocation N to Department 1. |
| Contains | Bed | 1:N | Line from DepartmentLocation `1` to Bed `N`. |

**Drawing instructions:**
- Strong entity.
- The Latitude/Longitude attributes support the "geo-location" requirement from the project spec.

**📌 Dependencies:**
- Needs **DepartmentID** from you (Department).
- **Omar** needs LocationID from you **before** he can complete Bed.
- ⚠️ **Coordinate with Omar:** Agree on naming — your PK is `LocationID` (INT).

---

### ✅ Ziad's Step-by-Step Work Order

```
Day 1 (Mon):  Hospital (independent — draw FIRST) → Employee (after Omar gives you UserID)
Day 1 (Mon):  Department (first draft without chairman, with HospitalID FK)
Day 1 (Mon):  Doctor → Nurse → Admin (all subclass entities)
Day 1 (Mon):  DepartmentLocation (after Department is done)
Day 1 (Mon):  Go back to Department and add ChairmanDoctorID relationship line
Day 2 (Tue):  Coordinate with Omar on LocationID for Bed
Day 2 (Tue):  Give DoctorID to Omar (for Appointment) and Youssef (for Examination, Prescription)
Day 2 (Tue):  Give NurseID to Youssef (for Triage)
```

---

# Member 3 — Youssef Amir
## Focus: Clinical & Medication
### Your 6 Entities: Triage · Examination · Prescription · PrescriptionDetail · Medication · Document

---

### Entity 1 of 6: Triage (Weak Entity)

**What it represents:** The **initial assessment** performed on a patient when they arrive at the Emergency Department. A triage is done by a nurse and assigns a severity level (1-5). Each triage results in exactly one emergency visit.

**Why is Triage a Weak Entity?** A triage record cannot exist without a Patient and a Nurse (it depends on both). However, we give it its own TriageID as PK — think of it as a **weak entity with a synthetic key**. In the ERD, mark it with a **double border** to show it depends on Patient and Nurse.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| TriageID | INT | **PRIMARY KEY** | <u>TriageID</u> |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| NurseID | INT | **FOREIGN KEY → Nurse(NurseID), NOT NULL** | NurseID (FK) → Nurse |
| DateTime | DATETIME | **NOT NULL** | DateTime |
| ChiefComplaint | TEXT | — (e.g., "Chest pain", "Difficulty breathing") | ChiefComplaint |
| TriageLevel | INT | **CHECK (1-5), NOT NULL** | TriageLevel [1-5] 🔴 |
| BloodPressure | VARCHAR(10) | — (measured at triage, e.g., "140/90") | BloodPressure |
| HeartRate | INT | — | HeartRate |
| Temperature | DECIMAL(4,1) | — | Temperature |

🔴 **TriageLevel** must have a CHECK constraint for values 1-5. Add this as a note in the ERD.

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Performed on | Patient | N:1 | Line from Triage N to Patient 1. Thick line on Triage side (total participation — every triage needs a patient). |
| Performed by | Nurse | N:1 | Line from Triage N to Nurse 1. Thick line on Triage side. |
| Results in | EmergencyVisit | 1:1 | Line from Triage `1` to EmergencyVisit `1`. The UNIQUE constraint on TriageID in EmergencyVisit enforces this. |

**Drawing instructions:**
- Use a **double rectangle** for Triage (weak entity notation).
- Draw thick lines (total participation) from Triage to Patient and Nurse — because a triage MUST have both.
- The relationship to EmergencyVisit is 1:1 — add a note: *"One triage → one visit"*.

**📌 Dependencies:**
- Needs **PatientID** from **Omar** (Patient).
- Needs **NurseID** from **Ziad** (Nurse).
- **Omar** needs TriageID for EmergencyVisit.
- ⚠️ **This should be your FIRST entity** but you need PatientID and NurseID first. Coordinate with Omar and Ziad on Monday morning.

---

### Entity 2 of 6: Examination

**What it represents:** A record that a doctor examined a patient during a specific emergency visit. This is an **associative entity** that resolves the M:N relationship between Doctor and Patient (many doctors can examine many patients) and links it to a specific visit.

**This satisfies the PDF requirement:** *"Many doctors may investigate one patient at the same time, each doctor should keep track of the number of hours per week spent on each patient."*

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| ExaminationID | INT | **PRIMARY KEY** | <u>ExaminationID</u> |
| DoctorID | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | DoctorID (FK) → Doctor |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| VisitID | INT | **FOREIGN KEY → EmergencyVisit(VisitID), NOT NULL** | VisitID (FK) → EmergencyVisit |
| ExaminationDate | DATETIME | **NOT NULL** | ExaminationDate |
| HoursSpent | DECIMAL(4,2) | — (e.g., 1.5 = 1 hour 30 min) | HoursSpent |

**Design note:** The `HoursSpent` stores the duration of this specific examination session. The system can **aggregate** these per week to satisfy the "hours per week" PDF requirement.

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Performed by | Doctor | N:1 | Line from Examination N to Doctor 1. |
| Performed on | Patient | N:1 | Line from Examination N to Patient 1. |
| During | EmergencyVisit | N:1 | Line from Examination N to EmergencyVisit 1. |

**Drawing instructions:**
- Examination is an associative entity. You can draw it as a **rectangle inside a diamond** or as a regular rectangle connected to Doctor, Patient, and EmergencyVisit.
- All three relationships are mandatory (N:1 with NOT NULL FKs).

**📌 Dependencies:**
- Needs **DoctorID** from **Ziad** (Doctor).
- Needs **PatientID** from **Omar** (Patient).
- Needs **VisitID** from **Omar** (EmergencyVisit).

---

### Entity 3 of 6: Prescription

**What it represents:** A prescription header — a doctor prescribes medications to a patient during an emergency visit. One prescription can have multiple medications (via PrescriptionDetail).

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| PrescriptionID | INT | **PRIMARY KEY** | <u>PrescriptionID</u> |
| DoctorID | INT | **FOREIGN KEY → Doctor(DoctorID), NOT NULL** | DoctorID (FK) → Doctor |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| VisitID | INT | **FOREIGN KEY → EmergencyVisit(VisitID), NOT NULL** | VisitID (FK) → EmergencyVisit |
| PrescriptionDate | DATE | **NOT NULL** | PrescriptionDate |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Written by | Doctor | N:1 | Line from Prescription N to Doctor 1. |
| Given to | Patient | N:1 | Line from Prescription N to Patient 1. |
| During | EmergencyVisit | N:1 | Line from Prescription N to EmergencyVisit 1. |
| Contains | PrescriptionDetail | 1:N | Line from Prescription `1` to PrescriptionDetail `N`. |

**Drawing instructions:**
- Strong entity. Like Examination, it connects Doctor, Patient, and Visit.
- The key difference from Examination: Prescription has the additional `1:N` relationship to PrescriptionDetail.

**📌 Dependencies:**
- Needs **DoctorID** from **Ziad** (Doctor).
- Needs **PatientID** from **Omar** (Patient).
- Needs **VisitID** from **Omar** (EmergencyVisit).

---

### Entity 4 of 6: PrescriptionDetail

**What it represents:** The specific medication line items within a prescription. One prescription can have multiple medications, each with its own dosage, directions, and duration.

**This satisfies the PDF requirement:** *"The doctor should give the directions for each medication (how many times per day and dose) in the prescription. We keep track of both the start and end dates of getting each medication."*

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| PrescriptionDetailID | INT | **PRIMARY KEY** | <u>PrescriptionDetailID</u> |
| PrescriptionID | INT | **FOREIGN KEY → Prescription(PrescriptionID), NOT NULL** | PrescriptionID (FK) → Prescription |
| MedicationID | INT | **FOREIGN KEY → Medication(MedicationID), NOT NULL** | MedicationID (FK) → Medication |
| Directions | TEXT | — (e.g., "Take with food", "Before bedtime") | Directions |
| Dosage | VARCHAR(50) | — (e.g., "500mg", "1 tablet", "2 puffs") | Dosage |
| TimesPerDay | INT | — (e.g., 1, 2, 3) | TimesPerDay |
| StartDate | DATE | **NOT NULL** | StartDate |
| EndDate | DATE | **NOT NULL** | EndDate |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Part of | Prescription | N:1 | Line from PrescriptionDetail N to Prescription 1. |
| References | Medication | N:1 | Line from PrescriptionDetail N to Medication 1. |

**Drawing instructions:**
- Strong entity with its own PK.
- Two N:1 relationships to Prescription and Medication.

**📌 Dependencies:**
- Needs **PrescriptionID** from you (Prescription).
- Needs **MedicationID** from you (Medication — define Medication first).
- ⚠️ **Order:** Medication → Prescription → PrescriptionDetail.

---

### Entity 5 of 6: Medication

**What it represents:** A simple lookup table of all available medications/drugs that can be prescribed.

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| MedicationID | INT | **PRIMARY KEY** | <u>MedicationID</u> |
| Name | VARCHAR(100) | **NOT NULL** | Name |
| Description | TEXT | — | Description |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Prescribed in | PrescriptionDetail | 1:N | Line from Medication `1` to PrescriptionDetail `N`. |

**Drawing instructions:**
- **Simple lookup** — the simplest entity in the system.
- Can be drawn quickly. Do this first among your entities.

**📌 Dependencies:**
- None! Medication is independent.
- ✅ **This should be the first entity you draw** — no waiting needed.

---

### Entity 6 of 6: Document

**What it represents:** Uploaded files associated with a patient — such as medical scans, lab reports, or X-ray images. This satisfies the requirement for "Static file serving and file uploads (e.g., patient scans)."

**Attributes:**

| Attribute | Data Type | Constraints | ERD Notation |
|-----------|-----------|-------------|--------------|
| DocumentID | INT | **PRIMARY KEY** | <u>DocumentID</u> |
| PatientID | INT | **FOREIGN KEY → Patient(PatientID), NOT NULL** | PatientID (FK) → Patient |
| VisitID | INT | **FOREIGN KEY → EmergencyVisit(VisitID), NULLABLE** | VisitID (FK) → EmergencyVisit (optional) |
| FileName | VARCHAR(255) | — (the original file name) | FileName |
| FilePath | VARCHAR(500) | — (storage path on server) | FilePath |
| UploadDate | DATETIME | — (default NOW) | UploadDate |
| Description | TEXT | — | Description |

**Relationships:**

| Relationship | With Entity | Cardinality | How to Draw |
|-------------|-------------|-------------|-------------|
| Belongs to | Patient | N:1 | Line from Document N to Patient 1. Thick line (every document belongs to a patient). |
| Relates to | EmergencyVisit | N:1 (optional) | Line from Document N to EmergencyVisit 1. Use dashed line because VisitID can be NULL. |

**Drawing instructions:**
- Strong entity.
- The relationship to EmergencyVisit is **optional** (some documents may be uploaded before a visit is created).
- Show optionality with `(0,N)` on Document side or dashed line.

**📌 Dependencies:**
- Needs **PatientID** from **Omar** (Patient).
- Needs **VisitID** from **Omar** (EmergencyVisit, optional).

---

### ✅ Youssef's Step-by-Step Work Order

```
Day 1 (Mon):  Medication (independent — start here!)
Day 1 (Mon):  Triage (once Omar gives you PatientID and Ziad gives you NurseID)
Day 2 (Tue):  Prescription (once Omar gives you VisitID and Ziad gives you DoctorID)
Day 2 (Tue):  PrescriptionDetail (once Prescription and Medication are done)
Day 2 (Tue):  Examination (once Omar gives you VisitID and Ziad gives you DoctorID)
Day 2 (Tue):  Document (once Omar gives you PatientID)
Day 2 (Tue):  Give TriageID to Omar (for EmergencyVisit)
```

---

## Dependency Map

This shows who depends on whom and in what order:

```
                         ┌─────────────────────────────────────────────┐
                         │             Omar's Entities                │
                         │  ┌──────┐   ┌─────────┐   ┌─────────────┐ │
                         │  │ Users│──>│ Patient │──>│EmergencyVisit│ │
                         │  └──┬───┘   └────┬────┘   └──────┬──────┘ │
                         │     │            │               │        │
                         │     │       ┌────┴────┐     ┌────┴─────┐  │
                         │     │       │   Bed   │     │Appointment│  │
                         │     │       └────▲────┘     └────┬─────┘  │
                         │     │            │               │        │
                         │     │            │          ┌────┴─────┐  │
                         │     │            │          │ Payment  │  │
                         │     │            │          └──────────┘  │
                         └─────┼────────────┼────────────────────────┘
                               │            │
          ┌────────────────────┼────────────┼────────────────────────┐
          │          Ziad's    │            │                        │
          │          Entities  │            │                        │
          │     ┌──────────┐   │       ┌────┴────┐                   │
          │     │ Hospital │   │       │Departm't│                   │
          │     └────┬─────┘   │       │Location │                   │
          │          │         │       └────┬─────┘                   │
          │     ┌────┴─────┐   │            │                         │
          │     │ Employee │<──┘            │  (Bed needs LocationID)  │
          │     └────┬─────┘                │                         │
          │          │                      │                         │
          │     ┌────┴────┐                 │                         │
          │     │ ISA ▷   │                 │                         │
          │  ┌──┴──┐ ┌───┴───┐ ┌─────┐     │                         │
          │  │Doctor│ │ Nurse │ │Admin│     │                         │
          │  └──┬───┘ └───┬───┘ └─────┘     │                         │
          │     │         │                 │                         │
          └─────┼─────────┼─────────────────┘                         │
                │         │                                           │
          ┌─────┼─────────┼───────────────────────────────────────────┘
          │     │         │           Youssef's Entities
          │     │    ┌────┴────┐  ┌──────────────┐
          │     │    │ Triage  │  │  Examination  │
          │     │    └────┬────┘  └──────┬───────┘
          │     │         │              │
          │     │    ┌────┴────┐  ┌──────┴───────┐
          │     │    │Prescript│  │ PrescriptDetl │
          │     │    └────┬────┘  └──────┬───────┘
          │     │         │              │
          │     │    ┌────┴────┐         │
          │     │    │Medicatn│          │
          │     │    └─────────┘         │
          │     │    ┌──────────┐        │
          │     │    │ Document │        │
          │     │    └──────────┘        │
          └─────┼────────────────────────┘
                │
     Legend: ──> "depends on" (FK reference)
```

### Critical Coordination Points

| What | Who Gives | Who Needs | When |
|------|-----------|-----------|------|
| HospitalID | Ziad (Hospital) | Ziad (Department) | Mon AM |
| UserID | Omar (Users) | Ziad (Employee) | Mon AM |
| PatientID | Omar (Patient) | Youssef (Triage, etc.) | Mon |
| NurseID | Ziad (Nurse) | Youssef (Triage) | Mon |
| DoctorID | Ziad (Doctor) | Omar (Appointment), Youssef (Exam, Prescription) | Mon-Tue |
| LocationID | Ziad (DeptLocation) | Omar (Bed) | Mon |
| TriageID | Youssef (Triage) | Omar (EmergencyVisit) | Tue AM |
| VisitID | Omar (EmergencyVisit) | Youssef (Exam, Prescription) | Tue |
| AppointmentID | Omar (Appointment) | Omar (Payment) | Tue |

---

## Timeline & Milestones

| Day | Date | Morning (AM) | Afternoon (PM) |
|-----|------|-------------|----------------|
| **Sun** | May 10 | ✅ **Kick-off** — Roles assigned, repo set up | ✅ Document created — review this file |
| **Mon** | May 11 | **Draft independent entities** (Users, Employee, Medication, etc.) | **Draft dependent entities** (Patient requires Users, Doctor requires Employee, etc.) |
| **Tue** | May 12 AM | **Share drafts** — each member shows their 6 entities. Resolve cross-dependencies (DoctorID, PatientID, etc.) | **Integrate** — combine all 18 entities into one master ERD (Omar leads) |
| **Wed** | May 13 | **Review master ERD** — check all attributes, constraints, cardinalities | **Refine** — fix any issues found during review |
| **Thu** | May 14 | **Finalize ERD** — export as `diagrams/erd.png` | **Validate** — verify all 18 entities are correct and complete |
| **Fri** | May 15 | **Final review with team** — close issues, update Kanban board | **Tag v1.0-phase1** and prepare for evaluation |
| **Sat** | May 16 | 🎯 **Lab evaluation** — present ERD to TA/Doctor | |

---

## Common Mistakes to Avoid

| ❌ Mistake | ✅ Correct Approach |
|-----------|-------------------|
| Forgetting to **underline PKs** | Every entity must have its PK underlined |
| Forgetting to **bold+underline** unique attrs (SSN, PatientNumber, Name, Code) | These are what evaluators check first! |
| Not labeling cardinalities on relationship lines | Every line must have `1`, `N`, or `M` labels |
| Using different attribute names for the same FK | If Omar names it `PatientID`, Youssef must use `PatientID` too |
| Making Triage a strong entity | Use double rectangle for Triage (weak) |
| Not showing the ISA hierarchy for Employee→Doctor/Nurse/Admin | Use the ISA triangle! |
| Leaving out CHECK constraints | TriageLevel 1-5 must have a note |
| Drawing circular dependencies without a plan | Follow the work orders above |
| Forgetting the **optional** relationships | BedID in EmergencyVisit is nullable. VisitID in Document is nullable. Show this. |

---

## Final Checklist (for each member)

Before submitting your part, check all of these:

- [ ] **Entity rectangle** drawn with correct name
- [ ] **All attributes** listed (refer to your tables above)
- [ ] **Primary Key** underlined
- [ ] **Unique attributes** (SSN, PatientNumber, Name, Code) **bold+underlined**
- [ ] **Foreign Keys** marked with (FK) and connected to the referenced entity
- [ ] **Relationship lines** have correct cardinality labels (1, N, M)
- [ ] **Total participation** shown with thick lines where FK is NOT NULL
- [ ] **Optional participation** shown with dashed lines where FK is nullable
- [ ] **ENUM values** noted on the attribute (e.g., [Available, Occupied])
- [ ] **CHECK constraints** noted (e.g., TriageLevel 1-5)
- [ ] **ISA hierarchy** drawn correctly for Employee → Doctor/Nurse/Admin
- [ ] **Weak entity** (Triage) has double border

---

*Good luck team! Let's get an A+ on this evaluation. 💪*
