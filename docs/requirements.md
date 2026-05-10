# Project Requirements for Emergency Department

## Overview
This document summarizes the project requirements from the provided guidelines and email, specifically tailored for the Emergency Department.

## Essential Functionalities (from guidelines)
1. Home page for visitors.
2. Different users can use the application, and each category can do different staff (e.g. Doctors, Patients, nurses, employees, etc.)
3. User registration and login for secure access
4. Each user has his own profile (Think about the doctor and patient profiles)
5. Static file serving and file uploads (e.g., patient scans)
6. Appointments model between doctors and patients.
7. Contact forms for user inquiries and requests
8. Statistical analysis dashboard for administrative users (admin dashboard)

## Specific Requirements for Hospital Database (from PDF)
### Patient Information
- The hospital keeps track of each patient’s:
  - Name
  - Patient-number (unique)
  - Social security number (unique)
  - Address
  - Phone
  - Birth date
  - Sex
  - Medical history
  - Medical status (blood pressure, heart rate, temperature)
- Date of admission to the department is tracked.

### Department Information
- Each department is described by:
  - Name (unique)
  - Department-code (unique)
  - Chairman (a doctor)
- Date the chairman started department supervision is tracked.
- A department may have several locations at the same time.

### Doctor Information
- Each doctor is described by:
  - Personal data (name, sex, birth-date, social security number)
  - Major scientific area
  - Degree
- Each doctor joins only one department in a specific date.
- Each doctor examines and checks one patient or more on regular basis.
- Many doctors may investigate one patient at the same time.
- Each doctor should track the number of hours per week spent on each patient.

### Prescription Information
- A doctor may write a prescription of the necessary medication(s) for each patient.
- Prescription date is recorded.
- Doctor gives directions for each medication (how many times per day and dose) in the prescription.
- Track both start and end dates of getting each medication.
- A doctor may write several prescriptions for many patients.
- Many doctors may write many prescriptions for one patient.

### Additional Requirements from Plan
1. Model patients, with complete info
2. Model hospitals including regular rooms, etc.
3. Model doctor info
4. Model work relationship between doctor and hospital
5. Model treatment relationship between doctor and patient
6. Model geo locations, (to find nearest place)
7. Allow patients to register/pay for doctor appointment
8. Allow patients to cancel/get refund for doctor appointment
9. Allow doctor to reserve different rooms for patient treatment
10. Generate reports for doctor appointments, room allocation ...

## Emergency Department Specific Additions
Based on the plan, we add the following Emergency-specific entities and attributes:

### Patient
- Emergency-specific: triage arrival time, chief complaint.

### Doctor
- (emergency physicians) – personal data, degree, department assignment date.

### Department
- (Emergency Department) – name, code, chairman, locations, start date.

### Nurse
- Treat as a category of Employee; a Nurse can assist in triage.

### Triage (weak entity)
- Triage level (1-5)
- Timestamp
- Vital signs at triage
- Nurse who performed it

### Emergency Visit
- Admission date/time
- Discharge date/time
- Result (admitted, transferred, discharged)
- Bed assigned

### Bed / Treatment Bay
- Room number
- Location
- Status (occupied/available)
- Type

### Prescription
- Written during emergency visit, by a doctor, for a patient
- Includes date, directions

### Medication
- Drug name
- Dosage form

### Examination/Treatment
- Captures the “doctor examines patient” relationship
- Number of hours per week spent (might be simplified to per-visit duration in ER, but keep the weekly attribute as required)

### Appointment
- ER typically walk-in, but model a “quick book” for minor emergencies, or use it to satisfy the appointment requirement.
- Treat walk-in registration as an appointment created on arrival.
- Appointment table with date/time, status, type.

### Payment/Invoice
- For appointment registration and refunds (requirements 7-8).

## Unique Constraints (Bold attributes in PDF)
- Patient: social security number, patient-number
- Department: name, code
- (Note: The plan does not specify other unique attributes, but we will ensure uniqueness where required by the PDF.)

## Notes
- All bold attributes from the PDF must have UNIQUE constraints in SQL and be underlined in the ERD.
- We will normalize to 3NF.