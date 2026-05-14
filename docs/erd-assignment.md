# ERD Design Assignment — 3-Member Team

> **Last Updated:** May 10, 2026
> **Team:** Omar Hesham, Ziad Khaled, Youssef Amir

> ⚠️ **This file is a summary. The full detailed assignment with attributes, constraints, and dependencies is in [`deliverables/README.md`](../deliverables/README.md). Please go there for your complete task list.**

---

## Quick Overview

| Member | Role | Entities Assigned |
|--------|------|-------------------|
| **Omar Hesham** | Team Leader — Patient Flow & Appointments | Users, Patient, EmergencyVisit, Bed, Appointment, Payment |
| **Ziad Khaled** | Staff Hierarchy & Locations | Employee, Doctor, Nurse, Admin, Department, DepartmentLocation |
| **Youssef Amir** | Clinical & Medication | Triage, Examination, Prescription, PrescriptionDetail, Medication, Document |

Each member has **6 entities** to design. See [`deliverables/README.md`](../deliverables/README.md) for the full specification of attributes, constraints, cardinalities, and dependencies.

---

## What Each Member Must Deliver

### Omar Hesham — Patient Flow & Appointments
1. **Users** — authentication & profiles
2. **Patient** — medical records (SSN, PatientNumber unique)
3. **EmergencyVisit** — ER stay record
4. **Bed** — treatment bays / rooms
5. **Appointment** — walk-in & booked
6. **Payment** — appointment payments & refunds

### Ziad Khaled — Staff Hierarchy & Locations
1. **Employee** — superclass (SSN unique)
2. **Doctor** — subclass
3. **Nurse** — subclass
4. **Admin** — subclass
5. **Department** — department info (Name & Code unique)
6. **DepartmentLocation** — geo-locations

### Youssef Amir — Clinical & Medication
1. **Triage** — weak entity (triage level 1-5)
2. **Examination** — doctor-patient-visit interaction
3. **Prescription** — prescription header
4. **PrescriptionDetail** — medication lines
5. **Medication** — drug lookup
6. **Document** — file uploads (scans/reports)

---

## Dependencies Map

```
Omar (Users) ──> Ziad (Employee needs UserID)
Omar (Patient) ──> Youssef (Triage needs PatientID)
Omar (EmergencyVisit) ──> Youssef (needs TriageID)
Youssef (Triage) ──> Ziad (needs NurseID)
Youssef (Examination) ──> Ziad (needs DoctorID) + Omar (needs PatientID, VisitID)
Youssef (Prescription) ──> Ziad (needs DoctorID) + Omar (needs PatientID, VisitID)
Ziad (Doctor) ──> Ziad (needs DepartmentID)
Ziad (Department) ──> Ziad (needs ChairmanDoctorID — circular, set after Doctor)
Omar (Bed) ──> Ziad (needs LocationID from DepartmentLocation)
```

---

## Timeline

| Date | Task |
|------|------|
| **Mon, May 11** | Each member drafts their 6 entities |
| **Tue, May 12 AM** | Share drafts & resolve dependencies |
| **Tue, May 12 PM** | Combine into master ERD (Omar leads) |
| **Wed, May 13** | Review & refine master ERD |
| **Thu, May 14** | Finalize & export `diagrams/erd.png` |

---

## ERD Notation Reminders
- **Primary Keys** → underline
- **Unique Attributes** → bold + underline (SSN, PatientNumber, Department.Name, Department.Code)
- **CHECK constraints** → note on the attribute (e.g., TriageLevel 1-5)
- **Weak entities** → double border (Triage)
- **1:1, 1:N, N:M** → label all relationship lines

---

**👉 For full details (all attributes, data types, FKs, constraints, and cardinalities), open [`deliverables/README.md`](../deliverables/README.md).**
