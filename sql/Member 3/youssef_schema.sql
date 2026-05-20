-- ============================================================
-- Member 3 — Youssef Amir
-- Focus: Clinical & Medication
-- Tables: Medication, Prescription, PrescriptionDetail, Triage,
--         Examination, Document
-- Lab 4 DDL Syntax — MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS emergency_dept;
USE emergency_dept;

-- ============================================================
-- 1. MEDICATION
-- Lookup list of available drugs. No FK dependencies.
-- ============================================================
CREATE TABLE Medication (
    MedicationID    INT AUTO_INCREMENT,
    Name            VARCHAR(100)    NOT NULL,
    Description     TEXT,
    PRIMARY KEY (MedicationID)
);

-- ============================================================
-- 2. PRESCRIPTION
-- Header record linking a Doctor's order to a Patient visit.
-- DoctorID → Doctor (Ziad), PatientID → Patient (Omar),
-- VisitID → EmergencyVisit (Omar) — cross-team FKs deferred.
-- ============================================================
CREATE TABLE Prescription (
    PrescriptionID      INT AUTO_INCREMENT,
    DoctorID            INT             NOT NULL,
    PatientID           INT             NOT NULL,
    VisitID             INT             NOT NULL,
    PrescriptionDate    DATE            NOT NULL,
    PRIMARY KEY (PrescriptionID)
    -- FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)          [Ziad]
    -- FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)      [Omar]
    -- FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)   [Omar]
);

-- ============================================================
-- 3. PRESCRIPTION_DETAIL
-- Individual drug lines inside a prescription.
-- ============================================================
CREATE TABLE PrescriptionDetail (
    PrescriptionDetailID    INT AUTO_INCREMENT,
    PrescriptionID          INT             NOT NULL,
    MedicationID            INT             NOT NULL,
    Directions              TEXT,
    Dosage                  VARCHAR(50),
    TimesPerDay             INT,
    StartDate               DATE            NOT NULL,
    EndDate                 DATE            NOT NULL,
    PRIMARY KEY (PrescriptionDetailID),
    FOREIGN KEY (PrescriptionID) REFERENCES Prescription(PrescriptionID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK (EndDate >= StartDate),
    CHECK (TimesPerDay > 0)
);

-- ============================================================
-- 4. TRIAGE (Weak Entity)
-- Nurse's first assessment. Composite PK (PatientID, TriageID).
-- PatientID → Patient (Omar), NurseID → Nurse (Ziad) — deferred.
-- ============================================================
CREATE TABLE Triage (
    PatientID       INT             NOT NULL,
    TriageID        INT             NOT NULL AUTO_INCREMENT UNIQUE,
    NurseID         INT             NOT NULL,
    DateTime        DATETIME        NOT NULL,
    ChiefComplaint  TEXT,
    TriageLevel     INT             NOT NULL,
    BloodPressure   VARCHAR(10),
    HeartRate       INT,
    Temperature     DECIMAL(4,1),
    PRIMARY KEY (PatientID, TriageID),
    CHECK (TriageLevel BETWEEN 1 AND 5),
    CHECK (HeartRate > 0)
    -- FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)      [Omar]
    -- FOREIGN KEY (NurseID) REFERENCES Nurse(EmployeeID)            [Ziad]
);

-- ============================================================
-- 5. EXAMINATION
-- A doctor examines a patient during a visit.
-- DoctorID → Doctor (Ziad), PatientID → Patient (Omar),
-- VisitID → EmergencyVisit (Omar) — deferred.
-- ============================================================
CREATE TABLE Examination (
    ExaminationID       INT AUTO_INCREMENT,
    DoctorID            INT             NOT NULL,
    PatientID           INT             NOT NULL,
    VisitID             INT             NOT NULL,
    ExaminationDate     DATETIME        NOT NULL,
    HoursSpent          DECIMAL(4,2),
    PRIMARY KEY (ExaminationID),
    CHECK (HoursSpent > 0)
    -- FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)          [Ziad]
    -- FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)      [Omar]
    -- FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)   [Omar]
);

-- ============================================================
-- 6. DOCUMENT
-- File metadata (X-rays, scans) linked to a Patient
-- and optionally to a Visit.
-- PatientID → Patient (Omar), VisitID → EmergencyVisit (Omar) — deferred.
-- ============================================================
CREATE TABLE Document (
    DocumentID      INT AUTO_INCREMENT,
    PatientID       INT             NOT NULL,
    VisitID         INT             NULL,
    FileName        VARCHAR(255),
    FilePath        VARCHAR(500),
    UploadDate      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    Description     TEXT,
    PRIMARY KEY (DocumentID)
    -- FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)      [Omar]
    -- FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)   [Omar]
);

-- ============================================================
-- SAMPLE DATA
-- ============================================================

INSERT INTO Medication (Name, Description) VALUES
    ('Paracetamol',  'Pain reliever and fever reducer'),
    ('Ibuprofen',    'Anti-inflammatory pain reliever'),
    ('Amoxicillin',  'Broad-spectrum antibiotic'),
    ('Omeprazole',   'Reduces stomach acid'),
    ('Metformin',    'Controls blood sugar in Type 2 diabetes');

INSERT INTO Prescription (DoctorID, PatientID, VisitID, PrescriptionDate) VALUES
    (1, 1, 1, '2025-05-11');

INSERT INTO PrescriptionDetail
    (PrescriptionID, MedicationID, Directions, Dosage, TimesPerDay, StartDate, EndDate)
VALUES
    (1, 1, 'Take after meals', '500mg', 3, '2025-05-11', '2025-05-18'),
    (1, 3, 'Take with water on empty stomach', '250mg', 2, '2025-05-11', '2025-05-18');

INSERT INTO Triage
    (PatientID, NurseID, DateTime, ChiefComplaint, TriageLevel,
     BloodPressure, HeartRate, Temperature)
VALUES
    (1, 1, '2025-05-11 08:30:00', 'Chest pain and shortness of breath',
     2, '140/90', 98, 37.2);

INSERT INTO Examination (DoctorID, PatientID, VisitID, ExaminationDate, HoursSpent)
VALUES
    (1, 1, 1, '2025-05-11 09:00:00', 1.50);

INSERT INTO Document (PatientID, VisitID, FileName, FilePath, Description)
VALUES
    (1, NULL, 'chest_xray.png', '/uploads/patient_1/chest_xray.png',
     'Chest X-Ray taken on arrival — no fractures detected');

-- ============================================================
-- CROSS-TEAM FOREIGN KEY CONSTRAINTS (deferred)
-- Prescription.DoctorID        → Doctor(EmployeeID)           [Ziad]
-- Prescription.PatientID       → Patient(PatientID)         [Omar]
-- Prescription.VisitID         → EmergencyVisit(VisitID)    [Omar]
-- Triage.PatientID             → Patient(PatientID)         [Omar]
-- Triage.NurseID               → Nurse(NurseID)             [Ziad]
-- Examination.DoctorID         → Doctor(DoctorID)           [Ziad]
-- Examination.PatientID        → Patient(PatientID)         [Omar]
-- Examination.VisitID          → EmergencyVisit(VisitID)    [Omar]
-- Document.PatientID           → Patient(PatientID)         [Omar]
-- Document.VisitID             → EmergencyVisit(VisitID)    [Omar]
-- ============================================================
-- ALTER TABLE Prescription
--     ADD FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Prescription
--     ADD FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Prescription
--     ADD FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Triage
--     ADD FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Triage
--     ADD FOREIGN KEY (NurseID) REFERENCES Nurse(EmployeeID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Examination
--     ADD FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Examination
--     ADD FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Examination
--     ADD FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Document
--     ADD FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
--         ON DELETE RESTRICT ON UPDATE CASCADE;
-- ALTER TABLE Document
--     ADD FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
--         ON DELETE SET NULL ON UPDATE CASCADE;
