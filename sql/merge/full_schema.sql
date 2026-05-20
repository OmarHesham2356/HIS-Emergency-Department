-- ============================================================
-- FULL MERGED SCHEMA — All 3 Members
-- Members: Omar Hesham, Ziad Khaled, Youssef Amir
-- Total: 20 tables
-- Lab 4 DDL Syntax — MySQL
-- All cross-team FOREIGN KEY constraints ACTIVE.
-- ============================================================

CREATE DATABASE IF NOT EXISTS emergency_dept;
USE emergency_dept;

-- ============================================================
-- PHASE 1 — No-dependency tables
-- ============================================================

-- 1. HOSPITAL (Ziad — Member 2)
CREATE TABLE Hospital (
    HospitalID      INT AUTO_INCREMENT,
    Name            VARCHAR(100)    NOT NULL,
    Address         TEXT,
    Phone           VARCHAR(20),
    Email           VARCHAR(100),
    EstablishedYear INT,
    PRIMARY KEY (HospitalID),
    UNIQUE (Name),
    UNIQUE (Email)
);

-- 2. PATIENT (Omar — Member 1)
CREATE TABLE Patient (
    PatientID       INT AUTO_INCREMENT,
    SSN             VARCHAR(20)     NOT NULL,
    PatientNumber   VARCHAR(20)     NOT NULL,
    FirstName       VARCHAR(50)     NOT NULL,
    LastName        VARCHAR(50)     NOT NULL,
    Address         VARCHAR(255),
    BirthDate       DATE,
    Sex             ENUM('M','F')   NOT NULL,
    MedicalHistory  TEXT,
    BloodPressure   VARCHAR(10),
    HeartRate       INT,
    Temperature     DECIMAL(4,1),
    PRIMARY KEY (PatientID),
    UNIQUE (SSN),
    UNIQUE (PatientNumber)
);

-- 3. PAYMENT (Omar — Member 1)
CREATE TABLE Payment (
    PaymentID       INT AUTO_INCREMENT,
    Amount          DECIMAL(10,2)   NOT NULL,
    PaymentDate     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod   ENUM('Cash','Card','Online'),
    Status          ENUM('Paid','Refunded','Pending') DEFAULT 'Pending',
    PRIMARY KEY (PaymentID)
);

-- 4. MEDICATION (Youssef — Member 3)
CREATE TABLE Medication (
    MedicationID    INT AUTO_INCREMENT,
    Name            VARCHAR(100)    NOT NULL,
    Description     TEXT,
    PRIMARY KEY (MedicationID)
);

-- ============================================================
-- PHASE 2 — Tables referencing Phase 1
-- ============================================================

-- 5. PATIENT_PHONE (Omar — Member 1)
-- FK → Patient (active)
CREATE TABLE Patient_Phone (
    PatientID       INT             NOT NULL,
    Phone           VARCHAR(20)     NOT NULL,
    PRIMARY KEY (PatientID, Phone),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 6. USERS (Omar — Member 1)
-- FK → Patient (active). EmployeeID FK → Employee deferred to Phase 3.
CREATE TABLE Users (
    UserID          INT AUTO_INCREMENT,
    PatientID       INT             UNIQUE,
    EmployeeID      INT             UNIQUE,
    Username        VARCHAR(50)     NOT NULL,
    PasswordHash    VARCHAR(255)    NOT NULL,
    Email           VARCHAR(100),
    Role            ENUM('Patient','Doctor','Nurse','Admin') NOT NULL,
    CreatedAt       DATETIME        DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (UserID),
    UNIQUE (Username),
    UNIQUE (Email),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 7. EMPLOYEE (Ziad — Member 2)
-- FK → Users (active). Total specialization (every employee is a Doctor/Nurse/Admin).
CREATE TABLE Employee (
    EmployeeID      INT AUTO_INCREMENT,
    UserID          INT             NOT NULL,
    FirstName       VARCHAR(50)     NOT NULL,
    LastName        VARCHAR(50)     NOT NULL,
    BirthDate       DATE,
    Sex             ENUM('M','F')   NOT NULL,
    SSN             VARCHAR(20)     NOT NULL,
    HireDate        DATE,
    JobTitle        VARCHAR(100),
    EmployeeType    ENUM('Doctor','Nurse','Admin') NOT NULL,
    PRIMARY KEY (EmployeeID),
    UNIQUE (UserID),
    UNIQUE (SSN),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 8. DEPARTMENT (Ziad — Member 2)
-- FK → Hospital (active). ChairmanDoctorID FK → Doctor deferred.
CREATE TABLE Department (
    DepartmentID        INT AUTO_INCREMENT,
    HospitalID          INT             NOT NULL,
    Name                VARCHAR(100)    NOT NULL,
    Code                VARCHAR(20)     NOT NULL,
    ChairmanDoctorID    INT,
    SupervisionStartDate DATE,
    PRIMARY KEY (DepartmentID),
    UNIQUE (Name),
    UNIQUE (Code),
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 9. DOCTOR (Ziad — Member 2)
-- ISA: PK inherited from Employee (Supertype). No separate DoctorID.
CREATE TABLE Doctor (
    EmployeeID          INT             NOT NULL,
    DepartmentID        INT             NOT NULL,
    MajorScientificArea VARCHAR(100),
    Degree              VARCHAR(50),
    JoinDate            DATE,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Circular dep resolved: Department.ChairmanDoctorID → Doctor(EmployeeID)
ALTER TABLE Department
    ADD CONSTRAINT fk_dept_chairman
    FOREIGN KEY (ChairmanDoctorID) REFERENCES Doctor(EmployeeID)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

-- 10. NURSE (Ziad — Member 2)
-- ISA: PK inherited from Employee (Supertype). No separate NurseID.
CREATE TABLE Nurse (
    EmployeeID      INT             NOT NULL,
    DepartmentID    INT             NOT NULL,
    JoinDate        DATE,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 11. ADMIN (Ziad — Member 2)
-- ISA: PK inherited from Employee (Supertype). No separate AdminID.
CREATE TABLE Admin (
    EmployeeID      INT             NOT NULL,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 12. DEPARTMENT_LOCATION (Ziad — Member 2)
CREATE TABLE DepartmentLocation (
    LocationID      INT AUTO_INCREMENT,
    DepartmentID    INT             NOT NULL,
    Address         TEXT,
    Latitude        DECIMAL(10,8),
    Longitude       DECIMAL(11,8),
    PRIMARY KEY (LocationID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 13. BED (Omar — Member 1)
-- FK → DepartmentLocation (active — Ziad)
CREATE TABLE Bed (
    BedID           INT AUTO_INCREMENT,
    RoomNumber      VARCHAR(20),
    LocationID      INT             NOT NULL,
    BedType         VARCHAR(50),
    Status          ENUM('Available','Occupied','Cleaning') DEFAULT 'Available',
    PRIMARY KEY (BedID),
    FOREIGN KEY (LocationID) REFERENCES DepartmentLocation(LocationID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Resolve circular: Users.EmployeeID → Employee
ALTER TABLE Users
    ADD FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

-- 14. APPOINTMENT (Omar — Member 1)
-- FK → Patient, Payment (active). DoctorID FK → Doctor (active — Ziad).
CREATE TABLE Appointment (
    AppointmentID       INT AUTO_INCREMENT,
    PatientID           INT             NOT NULL,
    DoctorID            INT             NOT NULL,
    PaymentID           INT             UNIQUE,
    AppointmentDateTime DATETIME        NOT NULL,
    Status              ENUM('Scheduled','Completed','Cancelled','No-Show')
                            DEFAULT 'Scheduled',
    Type                ENUM('Walk-in','Booked') NOT NULL,
    Notes               TEXT,
    PRIMARY KEY (AppointmentID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- 15. EMERGENCY_VISIT (Omar — Member 1)
-- FK → Patient, Bed (active). TriageID FK → Triage deferred.
CREATE TABLE EmergencyVisit (
    VisitID             INT AUTO_INCREMENT,
    PatientID           INT             NOT NULL,
    TriageID            INT             UNIQUE,
    BedID               INT,
    AdmissionDateTime   DATETIME        NOT NULL,
    DischargeDateTime   DATETIME,
    Disposition         ENUM('Admitted','Discharged','Transferred','Left Without Being Seen'),
    PRIMARY KEY (VisitID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (BedID) REFERENCES Bed(BedID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ============================================================
-- PHASE 3 — Youssef's tables with all cross-team FKs active
-- ============================================================

-- 16. PRESCRIPTION (Youssef — Member 3)
-- FK → Doctor (Ziad), Patient (Omar), EmergencyVisit (Omar) — all active
CREATE TABLE Prescription (
    PrescriptionID      INT AUTO_INCREMENT,
    DoctorID            INT             NOT NULL,
    PatientID           INT             NOT NULL,
    VisitID             INT             NOT NULL,
    PrescriptionDate    DATE            NOT NULL,
    PRIMARY KEY (PrescriptionID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 17. PRESCRIPTION_DETAIL (Youssef — Member 3)
-- FK → Prescription, Medication (both active)
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

-- 18. TRIAGE (Youssef — Member 3) — Weak Entity
-- FK → Patient (Omar), Nurse (Ziad) — both active
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
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (NurseID) REFERENCES Nurse(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK (TriageLevel BETWEEN 1 AND 5),
    CHECK (HeartRate > 0)
);

-- 19. EXAMINATION (Youssef — Member 3)
-- M:N junction: Doctor examines Patient. Composite PK (DoctorID, PatientID, ExaminationDate).
-- FK → Doctor(EmployeeID) (Ziad), Patient (Omar), EmergencyVisit (Omar) — all active
CREATE TABLE Examination (
    DoctorID            INT             NOT NULL,
    PatientID           INT             NOT NULL,
    ExaminationDate     DATETIME        NOT NULL,
    VisitID             INT             NOT NULL,
    HoursSpent          DECIMAL(4,2),
    PRIMARY KEY (DoctorID, PatientID, ExaminationDate),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CHECK (HoursSpent > 0)
);

-- 20. DOCUMENT (Youssef — Member 3)
-- FK → Patient (Omar), EmergencyVisit (Omar, nullable) — both active
CREATE TABLE Document (
    DocumentID      INT AUTO_INCREMENT,
    PatientID       INT             NOT NULL,
    VisitID         INT             NULL,
    FileName        VARCHAR(255),
    FilePath        VARCHAR(500),
    UploadDate      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    Description     TEXT,
    PRIMARY KEY (DocumentID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (VisitID) REFERENCES EmergencyVisit(VisitID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ============================================================
-- FINAL DEFERRED FK
-- EmergencyVisit.TriageID → Triage
-- (Triage was created after EmergencyVisit, so ALTER is needed)
-- ============================================================
ALTER TABLE EmergencyVisit
    ADD CONSTRAINT fk_ev_triage
    FOREIGN KEY (TriageID) REFERENCES Triage(TriageID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE;
