# Phase 1 Plan: Database Design & Implementation (Emergency Department)

## Overview
This document outlines the step-by-step plan for Phase 1 of the project, which focuses on database design and implementation for the Emergency Department. The plan spans from May 10 to May 16, 2026.

## Step-by-step Plan with Deadlines

| Date       | Task                                                                 | Owner(s)      | Deliverable                                                                 |
|------------|----------------------------------------------------------------------|---------------|-----------------------------------------------------------------------------|
| Sun, May 10| Finalize entity list, attributes, and relationships. Define cardinalities. | Role 1, whole team input | Raw list in docs/meeting-notes/meeting-2026-05-10.md |
| Mon, May 11| Draw the ERD (use draw.io or Lucidchart). Incorporate all PDF constraints. | Role 1        | First draft of ERD image in diagrams/erd-draft.png |
| Tue, May 12| Team review of ERD. Check if all 10 requirements from pages 2-3 are covered. | All           | Feedback in a GitHub Issue; final ERD agreed. |
| Tue, May 12| Start Mapping to Relational Schema. For each entity/relationship, produce a table definition with primary keys, foreign keys, and all attributes. Handle M:N relationships. Normalize to 3NF. | Role 2        | Draft schema in schemas/relational-schema.md |
| Wed, May 13| Review relational schema with the team. Ensure it matches ERD and no missing attributes. | Role 1, Role 2| Finalized schema. |
| Wed, May 13| Begin SQL coding: CREATE TABLE statements with all constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK for triage level 1-5, NOT NULL). | Role 3        | schemas/his-emergency.sql started |
| Thu, May 14| Finish all tables in SQL. Add at least 5-10 sample INSERT rows per table. | Role 3, with sample data ideas from all | SQL file ready for testing |
| Thu, May 14| Documentation and validation: Write a clean README.md describing the project, how to run the SQL file, team members, department choice justification. Validate SQL by running it in a local DB (SQLite/PostgreSQL) or using an online SQL validator. Check that all unique constraints, foreign keys are correct. | Role 4        | Updated README, docs/requirements.md, validation report (a markdown note) |
| Fri, May 15| Final review. Merge all work into main via pull request. Ensure the Kanban board is up to date, all issues closed. Prepare a 2-minute summary (who did what, key design decisions) for the evaluation. | You (Team Leader) | Repo ready, tag v1.0-phase1. |
| Sat, May 16| Lab evaluation week starts. Be ready to walk through the ERD, show SQL code running, explain normalization. | Whole team    | Presentation to TA/Doctor. |

## Notes
- Role 1: Team Leader (responsible for initial entity list, ERD draft, team coordination, final review).
- Role 2: Responsible for mapping ERD to relational schema.
- Role 3: Responsible for SQL coding and sample data.
- Role 4: Responsible for documentation, validation, and README.

## Emergency ERD Hints (from the plan)
- Patient (PatientID, Name, SSN(unique), PatientNumber(unique), Address, Phone, Birthdate, Sex, MedicalHistory, BloodPressure, HeartRate, Temperature)
- Employee (EmployeeID, Name, …) – superclass for Doctor, Nurse, Admin
- Doctor (DoctorID, EmployeeID (FK), DepartmentID (FK), MajorScientificArea, Degree, JoinDate)
- Nurse (NurseID, EmployeeID (FK))
- Triage (TriageID, PatientID (FK), NurseID (FK), DateTime, ChiefComplaint, TriageLevel, BP, HR, Temp)
- EmergencyVisit (VisitID, PatientID (FK), TriageID (FK, unique – one triage per visit), BedID (FK), AdmissionDateTime, DischargeDateTime, Disposition)
- Bed (BedID, RoomNumber, Location, Status)
- Examination (DoctorID, PatientID, VisitID, Date, HoursPerWeek)
- Prescription (PrescriptionID, DoctorID, PatientID, VisitID, Date)
- PrescriptionDetail (PrescriptionID, MedicationID, Directions, Dosage, TimesPerDay, StartDate, EndDate)
- Medication (MedicationID, Name, Description)
- Appointment (AppointmentID, PatientID, DoctorID, DateTime, Status, Type (walk-in, booked))
- Payment (PaymentID, AppointmentID, Amount, Date, Status (paid, refunded))

## Pro Tips for Evaluation
- Justify every design choice in the documentation.
- Use the PDF bold attributes: All bold attributes must have UNIQUE constraints in SQL and be underlined in the ERD.
- Run the SQL and screenshot the tables (for proof, but not required for Phase 1 deliverables).
- Keep the Kanban board moving – it’s a visible proof of teamwork.
