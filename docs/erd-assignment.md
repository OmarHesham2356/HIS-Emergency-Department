# ERD Design Assignment Plan

This document outlines which team member is responsible for designing each entity and its relationships in the Entity-Relationship Diagram (ERD) for the Emergency Department.

## Team Members

- **Member 1**: [Omar Hesham] (Team Leader)
- **Member 2**: [Ziad Khaled]
- **Member 3**: [Youssef Amir]
- **Member 4**: [Teammate 4 Name]
- **Member 5**: [Teammate 5 Name] *(if applicable)*

## Assignment Table

| Entity / Component          | Responsible Member | Details to Design                                                                 | Notes / Dependencies |
|-----------------------------|--------------------|---------------------------------------------------------------------------------|----------------------|
| **Users**                   | Member 1           | Attributes: UserID (PK), Username (unique, NOT NULL), PasswordHash (NOT NULL), Email (unique), Role ENUM('Patient','Doctor','Nurse','Admin'), CreatedAt<br>Relationships: 1:1 Patient, 1:1 Employee | Foundation for authentication; must be completed before Patient/Employee |
| **Patient**                 | Member 2           | Attributes: PatientID (PK), UserID (FK → Users, UNIQUE, NOT NULL), SSN (UNIQUE, NOT NULL), PatientNumber (UNIQUE, NOT NULL), FirstName, LastName (NOT NULL), Address, Phone, BirthDate, Sex, MedicalHistory (TEXT), BloodPressure (VARCHAR), HeartRate (INT), Temperature (DECIMAL)<br>Relationships: 1:1 User, 1:N Triage, 1:N EmergencyVisit, 1:N Examination (via PatientID), 1:N Prescription, 1:N Appointment, 1:N Document | Depends on Users; SSN and PatientNumber must be unique |
| **Employee** (superclass)   | Member 3           | Attributes: EmployeeID (PK), UserID (FK → Users, UNIQUE, NOT NULL), FirstName, LastName, BirthDate, Sex, SSN (UNIQUE, NOT NULL), HireDate, JobTitle<br>Relationships: 1:1 User, specialization to Doctor/Nurse/Admin via unique EmployeeID FK | Must be defined before subclasses; SSN unique |
| **Doctor**                  | Member 4           | Attributes: DoctorID (PK), EmployeeID (FK → Employee, UNIQUE, NOT NULL), DepartmentID (FK → Department, NOT NULL), MajorScientificArea (VARCHAR), Degree (VARCHAR), JoinDate (DATE)<br>Relationships: 1:1 Employee, N:1 Department (works in), 1:N Examination, 1:N Prescription, 1:N Appointment | Depends on Employee and Department |
| **Nurse**                   | Member 5 (or Member 2 if only 4 members) | Attributes: NurseID (PK), EmployeeID (FK → Employee, UNIQUE, NOT NULL), DepartmentID (FK → Department, NOT NULL), JoinDate<br>Relationships: 1:1 Employee, N:1 Department, 1:N Triage (performs triage) | Depends on Employee and Department |
| **Admin**                   | Member 1 (or assign as needed) | Attributes: AdminID (PK), EmployeeID (FK → Employee, UNIQUE, NOT NULL)<br>Relationships: 1:1 Employee | Simple subclass; can be paired with another task |
| **Department**              | Member 2           | Attributes: DepartmentID (PK), Name (UNIQUE, NOT NULL), Code (UNIQUE, NOT NULL), ChairmanDoctorID (FK → Doctor, UNIQUE), SupervisionStartDate (DATE)<br>Relationships: 1:N Doctor, 1:N Nurse, 1:1 Chairman (Doctor), 1:N DepartmentLocation | Must define unique Name and Code; ChairmanDoctorID is a unique FK to Doctor |
| **DepartmentLocation**      | Member 3           | Attributes: LocationID (PK), DepartmentID (FK → Department, NOT NULL), Address (TEXT), Latitude (DECIMAL), Longitude (DECIMAL)<br>Relationships: N:1 Department, 1:N Bed | Depends on Department |
| **Bed**                     | Member 4           | Attributes: BedID (PK), RoomNumber (VARCHAR), LocationID (FK → DepartmentLocation, NOT NULL), BedType (VARCHAR, e.g., ‘Trauma’, ‘Observation’, ‘Resuscitation’), Status ENUM('Available','Occupied','Cleaning') NOT NULL DEFAULT 'Available'<br>Relationships: N:1 DepartmentLocation, 1:N EmergencyVisit (bed assigned) | Depends on DepartmentLocation |
| **Triage** (weak entity)    | Member 5           | Attributes: TriageID (PK), PatientID (FK → Patient, NOT NULL), NurseID (FK → Nurse, NOT NULL), DateTime (DATETIME, NOT NULL), ChiefComplaint (TEXT), TriageLevel (INT, CHECK 1–5, NOT NULL), BloodPressure (VARCHAR), HeartRate (INT), Temperature (DECIMAL)<br>Relationships: N:1 Patient, N:1 Nurse, 1:1 EmergencyVisit (via unique TriageID in EmergencyVisit) | Weak entity; depends on Patient and Nurse; TriageID PK |
| **EmergencyVisit**          | Member 1           | Attributes: VisitID (PK), PatientID (FK → Patient, NOT NULL), TriageID (FK → Triage, UNIQUE, NOT NULL), BedID (FK → Bed), AdmissionDateTime (DATETIME, NOT NULL), DischargeDateTime (DATETIME), Disposition ENUM('Admitted','Discharged','Transferred','Left Without Being Seen')<br>Relationships: N:1 Patient, 1:1 Triage (unique), N:1 Bed (nullable), N:1 Examination (via VisitID), N:1 Prescription (via VisitID) | Central visit entity; TriageID unique ensures one triage per visit |
| **Examination**             | Member 2           | Attributes: ExaminationID (PK), DoctorID (FK → Doctor, NOT NULL), PatientID (FK → Patient, NOT NULL), VisitID (FK → EmergencyVisit, NOT NULL), ExaminationDate (DATETIME, NOT NULL), HoursSpent (DECIMAL(4,2))<br>Relationships: N:1 Doctor, N:1 Patient, N:1 Visit | Associative entity for doctor-patient-visit interaction; allows multiple doctors per patient per visit |
| **Prescription**            | Member 3           | Attributes: PrescriptionID (PK), DoctorID (FK → Doctor, NOT NULL), PatientID (FK → Patient, NOT NULL), VisitID (FK → EmergencyVisit, NOT NULL), PrescriptionDate (DATE, NOT NULL)<br>Relationships: N:1 Doctor, N:1 Patient, N:1 Visit, 1:N PrescriptionDetail | Links doctor, patient, visit; header for meds |
| **PrescriptionDetail**      | Member 4           | Attributes: PrescriptionDetailID (PK), PrescriptionID (FK → Prescription, NOT NULL), MedicationID (FK → Medication, NOT NULL), Directions (TEXT), Dosage (VARCHAR), TimesPerDay (INT), StartDate (DATE, NOT NULL), EndDate (DATE, NOT NULL)<br>Relationships: N:1 Prescription, N:1 Medication | Detail lines for each medication |
| **Medication**              | Member 5           | Attributes: MedicationID (PK), Name (VARCHAR, NOT NULL), Description (TEXT)<br>Relationships: 1:N PrescriptionDetail | Simple lookup |
| **Appointment**             | Member 1           | Attributes: AppointmentID (PK), PatientID (FK → Patient, NOT NULL), DoctorID (FK → Doctor, NOT NULL), AppointmentDateTime (DATETIME, NOT NULL), Status ENUM('Scheduled','Completed','Cancelled','No‑Show'), Type ENUM('Walk‑in','Booked'), Notes (TEXT)<br>Relationships: N:1 Patient, N:1 Doctor, 1:1 Payment | Supports both walk‑in and booked appointments |
| **Payment**                 | Member 2           | Attributes: PaymentID (PK), AppointmentID (FK → Appointment, UNIQUE, NOT NULL), Amount (DECIMAL(10,2), NOT NULL), PaymentDate (DATETIME), PaymentMethod ENUM('Cash','Card','Online'), Status ENUM('Paid','Refunded','Pending') NOT NULL DEFAULT 'Pending'<br>Relationships: 1:1 Appointment (unique) | One payment per appointment |
| **Document**                | Member 3           | Attributes: DocumentID (PK), PatientID (FK → Patient, NOT NULL), VisitID (FK → EmergencyVisit, NULLABLE), FileName (VARCHAR), FilePath (VARCHAR), UploadDate (DATETIME), Description (TEXT)<br>Relationships: N:1 Patient, N:1 Visit (optional) | File uploads for scans/reports |

## Assignment Guidelines

1. **Complete your assigned entity** including:
   - All attributes with correct data types and constraints (NOT NULL, UNIQUE, CHECK, ENUM, etc.)
   - Primary key designation
   - Foreign key references (to already-defined entities where applicable)
   - Relationship cardinalities (as listed in the “Relationships” column)
2. **Draw your entity** in the ERD tool (draw.io/Lucidchart) using standard notation:
   - Rectangles for entities
   - Ovals for attributes (optional; can list inside rectangle)
   - Diamonds for relationships (or use lines with cardinality labels)
   - Underline primary keys
   - Bold or underline attributes that must be unique (per PDF: SSN, PatientNumber, Department.Name, Department.Code)
3. **Label relationships** clearly with:
   - Cardinality (e.g., 1:1, 1:N, N:M)
   - Participation (total/partial) where evident from NOT NULL FKs
4. **Add brief notes** in the ERD (as comments or a separate text box) for any design decisions (e.g., why Triage is a weak entity, why HoursSpent is per session).
5. **Review dependencies**: Ensure that any entity you reference (via FK) has been assigned to another member and that you coordinate on the referenced entity’s primary key name and type.
6. **Integrate into the master ERD**: After all members complete their parts, the team will convene to combine individual pieces into a single coherent ERD, checking for:
   - Consistency of attribute names and types across FK/PK pairs
   - Correct relationship directions and cardinalities
   - No missing entities or attributes from the specification
   - Proper handling of weak entities and specialization (Employee → Doctor/Nurse/Admin)

## Timeline (aligned with Phase 1 Plan)

- **Mon, May 11**: Each member works on their assigned entity draft (based on this assignment).
- **Tue, May 12 AM**: Share individual entity drafts in a team meeting; discuss dependencies and resolve conflicts.
- **Tue, May 12 PM**: Begin integrating entities into a master ERD.
- **Wed, May 13**: Review and refine the master ERD; ensure all relationships are correct.
- **Thu, May 14**: Finalize ERD, export as `diagrams/erd.png`, and verify against the specification.

## Contact

For questions about this assignment, contact the Team Leader (Member 1).
