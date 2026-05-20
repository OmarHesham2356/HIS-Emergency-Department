-- ============================================================
-- Member 1 — Omar Hesham (Team Leader)
-- Focus: Patient Flow & Appointments
-- Tables: Patient, Payment, Patient_Phone, Users, Bed,
--         Appointment, EmergencyVisit
-- Lab 4 DDL Syntax — MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS emergency_dept;
USE emergency_dept;

-- ============================================================
-- 1. PATIENT
-- Strong entity. No internal FK dependencies.
-- SSN and PatientNumber are UNIQUE per PDF spec.
-- ============================================================
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

-- ============================================================
-- 2. PAYMENT
-- Strong entity. No internal FK dependencies.
-- ============================================================
CREATE TABLE Payment (
    PaymentID       INT AUTO_INCREMENT,
    Amount          DECIMAL(10,2)   NOT NULL,
    PaymentDate     DATETIME        DEFAULT CURRENT_TIMESTAMP,
    PaymentMethod   ENUM('Cash','Card','Online'),
    Status          ENUM('Paid','Refunded','Pending') DEFAULT 'Pending',
    PRIMARY KEY (PaymentID)
);

-- ============================================================
-- 3. PATIENT_PHONE
-- Multivalued attribute mapping (Lab 3 rule 2a).
-- Composite PK: (PatientID, Phone)
-- ============================================================
CREATE TABLE Patient_Phone (
    PatientID       INT             NOT NULL,
    Phone           VARCHAR(20)     NOT NULL,
    PRIMARY KEY (PatientID, Phone),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ============================================================
-- 4. BED
-- LocationID FK → DepartmentLocation (Ziad — cross-team,
--    added via ALTER TABLE after this file)
-- ============================================================
CREATE TABLE Bed (
    BedID           INT AUTO_INCREMENT,
    RoomNumber      VARCHAR(20),
    LocationID      INT             NOT NULL,
    BedType         VARCHAR(50),
    Status          ENUM('Available','Occupied','Cleaning') DEFAULT 'Available',
    PRIMARY KEY (BedID)
);

-- ============================================================
-- 5. USERS
-- Authentication foundation.
-- PatientID FK → Patient (1:1, optional → mandatory side).
-- EmployeeID FK → Employee (Ziad — cross-team, deferred).
-- ============================================================
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

-- ============================================================
-- 6. APPOINTMENT
-- PatientID FK → Patient (N:1).
-- DoctorID FK → Doctor (Ziad — cross-team, deferred).
-- PaymentID FK → Payment (1:1, UNIQUE).
-- ============================================================
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
    FOREIGN KEY (PaymentID) REFERENCES Payment(PaymentID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ============================================================
-- 7. EMERGENCY_VISIT
-- PatientID FK → Patient (N:1).
-- TriageID FK → Triage (Youssef — cross-team, deferred).
-- BedID FK → Bed (N:1, nullable — optional bed assignment).
-- ============================================================
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
-- CROSS-TEAM FOREIGN KEY CONSTRAINTS
-- These reference tables owned by other members:
--   Employee, Doctor          → Ziad Khaled
--   Triage, DepartmentLocation → Youssef Amir / Ziad Khaled
-- Run these AFTER the respective member's tables exist.
-- ============================================================

-- Users → Employee (Ziad)
-- ALTER TABLE Users
--     ADD FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
--         ON DELETE SET NULL
--         ON UPDATE CASCADE;

-- Bed → DepartmentLocation (Ziad)
-- ALTER TABLE Bed
--     ADD FOREIGN KEY (LocationID) REFERENCES DepartmentLocation(LocationID)
--         ON DELETE RESTRICT
--         ON UPDATE CASCADE;

-- Appointment → Doctor (Ziad)
-- ALTER TABLE Appointment
--     ADD FOREIGN KEY (DoctorID) REFERENCES Doctor(EmployeeID)
--         ON DELETE RESTRICT
--         ON UPDATE CASCADE;

-- EmergencyVisit → Triage (Youssef)
-- ALTER TABLE EmergencyVisit
--     ADD FOREIGN KEY (TriageID) REFERENCES Triage(TriageID)
--         ON DELETE RESTRICT
--         ON UPDATE CASCADE;
