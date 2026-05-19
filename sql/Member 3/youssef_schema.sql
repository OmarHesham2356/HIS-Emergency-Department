-- ============================================================
--  Emergency Department Database
--  Member 3: Youssef Amir — Clinical & Medication
--  Entities: Medication, Prescription, PrescriptionDetail,
--             Triage, Examination, Document
--
--  DATABASE: MySQL
--  SCOPE: Youssef's 6 tables ONLY — no cross-team FKs yet.
--         Foreign key constraints to teammates' tables are
--         commented out with a TODO tag. Omar or Ziad will
--         uncomment them once the master schema is merged.
--
--  WORK ORDER (safest creation order — no circular deps):
--    1. Medication          (no FKs at all — fully independent)
--    2. Prescription        (needs Doctor, Patient, Visit — stubbed)
--    3. PrescriptionDetail  (needs Prescription + Medication)
--    4. Triage              (needs Patient, Nurse — stubbed)
--    5. Examination         (needs Doctor, Patient, Visit — stubbed)
--    6. Document            (needs Patient, Visit — stubbed)
-- ============================================================

-- ============================================================
-- Drop tables in reverse order to avoid FK conflicts
-- (run this block when resetting during development)
-- ============================================================
DROP TABLE IF EXISTS Document;
DROP TABLE IF EXISTS Examination;
DROP TABLE IF EXISTS Triage;
DROP TABLE IF EXISTS PrescriptionDetail;
DROP TABLE IF EXISTS Prescription;
DROP TABLE IF EXISTS Medication;


-- ============================================================
-- TABLE 1: Medication
-- What it does: A simple lookup list of all available drugs
--               that can be prescribed. Fully independent —
--               no FK references to any other table.
-- ============================================================
CREATE TABLE Medication (
    MedicationID    INT             NOT NULL AUTO_INCREMENT,
    Name            VARCHAR(100)    NOT NULL,
    Description     TEXT,

    -- ── Primary Key ──────────────────────────────────────────
    CONSTRAINT pk_Medication PRIMARY KEY (MedicationID)
);


-- ============================================================
-- TABLE 2: Prescription
-- What it does: A "header" record — one doctor gives one
--               patient a prescription during a specific visit.
--               The actual drug details live in PrescriptionDetail.
--
-- TODO (Omar):  Uncomment the FK lines for PatientID and VisitID
--               once the Patient and EmergencyVisit tables exist.
-- TODO (Ziad):  Uncomment the FK line for DoctorID
--               once the Doctor table exists.
-- ============================================================
CREATE TABLE Prescription (
    PrescriptionID      INT     NOT NULL AUTO_INCREMENT,

    -- FK → Doctor (Ziad's table)
    -- TODO Ziad: uncomment when Doctor table is merged
    DoctorID            INT     NOT NULL,
    -- CONSTRAINT fk_Prescription_Doctor
    --     FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),

    -- FK → Patient (Omar's table)
    -- TODO Omar: uncomment when Patient table is merged
    PatientID           INT     NOT NULL,
    -- CONSTRAINT fk_Prescription_Patient
    --     FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),

    -- FK → EmergencyVisit (Omar's table)
    -- TODO Omar: uncomment when EmergencyVisit table is merged
    VisitID             INT     NOT NULL,
    -- CONSTRAINT fk_Prescription_Visit
    --     FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID),

    PrescriptionDate    DATE    NOT NULL,

    -- ── Primary Key ──────────────────────────────────────────
    CONSTRAINT pk_Prescription PRIMARY KEY (PrescriptionID)
);


-- ============================================================
-- TABLE 3: PrescriptionDetail
-- What it does: The individual drug lines inside a prescription.
--               One prescription can have many of these rows
--               (e.g. one row for Paracetamol, one for Ibuprofen).
--               Stores dosage, how many times per day, and the
--               start/end dates for taking each drug.
--               This satisfies the PDF requirement:
--               "directions for each medication (how many times
--                per day and dose) + start and end dates"
-- ============================================================
CREATE TABLE PrescriptionDetail (
    PrescriptionDetailID    INT             NOT NULL AUTO_INCREMENT,

    -- FK → Prescription (Youssef's own table — active now)
    PrescriptionID          INT             NOT NULL,
    CONSTRAINT fk_PrescDetail_Prescription
        FOREIGN KEY (PrescriptionID)
        REFERENCES Prescription(PrescriptionID)
        ON DELETE CASCADE,   -- if the prescription is deleted, its lines go too

    -- FK → Medication (Youssef's own table — active now)
    MedicationID            INT             NOT NULL,
    CONSTRAINT fk_PrescDetail_Medication
        FOREIGN KEY (MedicationID)
        REFERENCES Medication(MedicationID),

    Directions              TEXT,                   -- e.g. "Take with food"
    Dosage                  VARCHAR(50),             -- e.g. "500mg", "2 tablets"
    TimesPerDay             INT,                     -- e.g. 1, 2, 3
    StartDate               DATE            NOT NULL,
    EndDate                 DATE            NOT NULL,

    -- ── Primary Key ──────────────────────────────────────────
    CONSTRAINT pk_PrescriptionDetail PRIMARY KEY (PrescriptionDetailID),

    -- ── Check Constraints ────────────────────────────────────
    CONSTRAINT chk_PrescDetail_Dates
        CHECK (EndDate >= StartDate),        -- end can't be before start
    CONSTRAINT chk_PrescDetail_TimesPerDay
        CHECK (TimesPerDay > 0)              -- must take it at least once a day
);


-- ============================================================
-- TABLE 4: Triage  *** WEAK ENTITY ***
-- What it does: The nurse's first assessment of a patient when
--               they walk into the ER. Assigns a severity level
--               1 (most critical) to 5 (least critical).
--               One triage always leads to exactly one
--               EmergencyVisit (Omar links that side).
--
-- Why WEAK ENTITY? A triage record cannot exist without
--               a Patient. In the ERD it has a double border.
--               The composite PK is (PatientID, TriageID).
--
-- TODO (Omar):  Uncomment the FK for PatientID once Patient exists.
-- TODO (Ziad):  Uncomment the FK for NurseID once Nurse exists.
-- ============================================================
CREATE TABLE Triage (

    -- Part 1 of composite PK — also FK to Patient (Omar)
    -- TODO Omar: uncomment FK when Patient table is merged
    PatientID       INT         NOT NULL,
    -- CONSTRAINT fk_Triage_Patient
    --     FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),

    -- Part 2 of composite PK — the partial key (unique per patient)
    TriageID        INT         NOT NULL AUTO_INCREMENT UNIQUE,
    -- Note: AUTO_INCREMENT requires a KEY, added below.
    -- TriageID is also referenced by EmergencyVisit (Omar's table)
    -- as a UNIQUE FK to enforce the 1:1 relationship.

    -- FK → Nurse (Ziad's table)
    -- TODO Ziad: uncomment when Nurse table is merged
    NurseID         INT         NOT NULL,
    -- CONSTRAINT fk_Triage_Nurse
    --     FOREIGN KEY (NurseID) REFERENCES Nurse(NurseID),

    DateTime        DATETIME    NOT NULL,
    ChiefComplaint  TEXT,                       -- e.g. "Chest pain"
    TriageLevel     INT         NOT NULL,        -- 1 = critical, 5 = minor
    BloodPressure   VARCHAR(10),                 -- e.g. "140/90"
    HeartRate       INT,
    Temperature     DECIMAL(4,1),               -- e.g. 37.5

    -- ── Composite Primary Key (Weak Entity rule) ─────────────
    CONSTRAINT pk_Triage PRIMARY KEY (PatientID, TriageID),

    -- ── Check Constraints ────────────────────────────────────
    CONSTRAINT chk_Triage_Level
        CHECK (TriageLevel BETWEEN 1 AND 5),    -- PDF spec: levels 1-5 only

    CONSTRAINT chk_Triage_HeartRate
        CHECK (HeartRate > 0)
);


-- ============================================================
-- TABLE 5: Examination
-- What it does: Records one doctor examining one patient during
--               a specific visit. Many doctors can examine the
--               same patient (N:M resolved by this table).
--               HoursSpent tracks how long — satisfies the PDF
--               requirement: "keep track of hours per week
--               spent on each patient."
--
-- TODO (Omar):  Uncomment FKs for PatientID and VisitID.
-- TODO (Ziad):  Uncomment FK for DoctorID.
-- ============================================================
CREATE TABLE Examination (
    ExaminationID       INT             NOT NULL AUTO_INCREMENT,

    -- FK → Doctor (Ziad's table)
    -- TODO Ziad: uncomment when Doctor table is merged
    DoctorID            INT             NOT NULL,
    -- CONSTRAINT fk_Examination_Doctor
    --     FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID),

    -- FK → Patient (Omar's table)
    -- TODO Omar: uncomment when Patient table is merged
    PatientID           INT             NOT NULL,
    -- CONSTRAINT fk_Examination_Patient
    --     FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),

    -- FK → EmergencyVisit (Omar's table)
    -- TODO Omar: uncomment when EmergencyVisit table is merged
    VisitID             INT             NOT NULL,
    -- CONSTRAINT fk_Examination_Visit
    --     FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID),

    ExaminationDate     DATETIME        NOT NULL,
    HoursSpent          DECIMAL(4,2),            -- e.g. 1.50 = 1 hour 30 min

    -- ── Primary Key ──────────────────────────────────────────
    CONSTRAINT pk_Examination PRIMARY KEY (ExaminationID),

    -- ── Check Constraints ────────────────────────────────────
    CONSTRAINT chk_Examination_Hours
        CHECK (HoursSpent > 0)
);


-- ============================================================
-- TABLE 6: Document
-- What it does: Stores metadata about uploaded files (X-rays,
--               lab results, scan images) attached to a patient.
--               VisitID is NULLABLE — a document may be uploaded
--               before a visit is formally created in the system.
--               Satisfies the PDF requirement:
--               "Static file serving and file uploads (patient scans)"
--
-- TODO (Omar):  Uncomment FKs for PatientID and VisitID.
-- ============================================================
CREATE TABLE Document (
    DocumentID      INT             NOT NULL AUTO_INCREMENT,

    -- FK → Patient (Omar's table) — NOT NULL (every doc needs a patient)
    -- TODO Omar: uncomment when Patient table is merged
    PatientID       INT             NOT NULL,
    -- CONSTRAINT fk_Document_Patient
    --     FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),

    -- FK → EmergencyVisit (Omar's table) — NULLABLE (optional link)
    -- TODO Omar: uncomment when EmergencyVisit table is merged
    VisitID         INT             NULL,         -- NULL = not yet linked to a visit
    -- CONSTRAINT fk_Document_Visit
    --     FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID),

    FileName        VARCHAR(255),                 -- original file name e.g. "xray_chest.png"
    FilePath        VARCHAR(500),                 -- server storage path e.g. "/uploads/p42/xray.png"
    UploadDate      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    Description     TEXT,

    -- ── Primary Key ──────────────────────────────────────────
    CONSTRAINT pk_Document PRIMARY KEY (DocumentID)
);


-- ============================================================
-- SAMPLE DATA — for testing your tables independently
-- (remove or comment out before submitting the final schema)
-- ============================================================

-- Medication samples
INSERT INTO Medication (Name, Description) VALUES
    ('Paracetamol',  'Pain reliever and fever reducer'),
    ('Ibuprofen',    'Anti-inflammatory pain reliever'),
    ('Amoxicillin',  'Broad-spectrum antibiotic'),
    ('Omeprazole',   'Reduces stomach acid'),
    ('Metformin',    'Controls blood sugar in Type 2 diabetes');

-- Prescription sample
-- (PatientID=1, DoctorID=1, VisitID=1 are placeholders — teammates fill these)
INSERT INTO Prescription (DoctorID, PatientID, VisitID, PrescriptionDate) VALUES
    (1, 1, 1, '2025-05-11');

-- PrescriptionDetail samples
INSERT INTO PrescriptionDetail
    (PrescriptionID, MedicationID, Directions, Dosage, TimesPerDay, StartDate, EndDate)
VALUES
    (1, 1, 'Take after meals', '500mg', 3, '2025-05-11', '2025-05-18'),
    (1, 3, 'Take with water on empty stomach', '250mg', 2, '2025-05-11', '2025-05-18');

-- Triage sample
-- (PatientID=1, NurseID=1 are placeholders — teammates fill these)
INSERT INTO Triage
    (PatientID, NurseID, DateTime, ChiefComplaint, TriageLevel,
     BloodPressure, HeartRate, Temperature)
VALUES
    (1, 1, '2025-05-11 08:30:00', 'Chest pain and shortness of breath',
     2, '140/90', 98, 37.2);

-- Examination sample
-- (DoctorID=1, PatientID=1, VisitID=1 are placeholders — teammates fill these)
INSERT INTO Examination (DoctorID, PatientID, VisitID, ExaminationDate, HoursSpent)
VALUES
    (1, 1, 1, '2025-05-11 09:00:00', 1.50);

-- Document sample
-- (PatientID=1 is placeholder — VisitID left NULL intentionally to show nullable)
INSERT INTO Document (PatientID, VisitID, FileName, FilePath, Description)
VALUES
    (1, NULL, 'chest_xray.png', '/uploads/patient_1/chest_xray.png',
     'Chest X-Ray taken on arrival — no fractures detected');


-- ============================================================
-- USEFUL QUERIES — to verify everything works
-- ============================================================

-- See all medications
SELECT * FROM Medication;

-- See a full prescription with its drug details
SELECT
    p.PrescriptionID,
    p.PrescriptionDate,
    m.Name          AS DrugName,
    pd.Dosage,
    pd.TimesPerDay,
    pd.StartDate,
    pd.EndDate,
    pd.Directions
FROM Prescription p
JOIN PrescriptionDetail pd ON p.PrescriptionID = pd.PrescriptionID
JOIN Medication m          ON pd.MedicationID  = m.MedicationID;

-- See all triage records with level
SELECT
    PatientID,
    TriageID,
    DateTime,
    ChiefComplaint,
    TriageLevel,
    BloodPressure,
    HeartRate,
    Temperature
FROM Triage
ORDER BY TriageLevel ASC;   -- most critical (level 1) first

-- See examinations with hours
SELECT
    ExaminationID,
    DoctorID,
    PatientID,
    VisitID,
    ExaminationDate,
    HoursSpent
FROM Examination;

-- Total hours a doctor spent on a patient (satisfies PDF requirement)
-- Replace 1s with actual IDs when testing
SELECT
    DoctorID,
    PatientID,
    SUM(HoursSpent)                         AS TotalHours,
    WEEK(ExaminationDate)                   AS WeekNumber
FROM Examination
GROUP BY DoctorID, PatientID, WEEK(ExaminationDate);

-- See all documents for a patient
SELECT * FROM Document WHERE PatientID = 1;
