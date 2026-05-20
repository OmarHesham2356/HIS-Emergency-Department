-- ============================================================
-- Member 2 — Ziad Khaled
-- Focus: Staff Hierarchy & Locations
-- Tables: Hospital, Employee, Department, Doctor, Nurse, Admin,
--         DepartmentLocation
-- Lab 4 DDL Syntax — MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS emergency_dept;
USE emergency_dept;

-- ============================================================
-- 1. HOSPITAL
-- Strong entity. Root of the location hierarchy.
-- ============================================================
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

-- ============================================================
-- 2. EMPLOYEE
-- Superclass in the ISA hierarchy (Doctor / Nurse / Admin).
-- UserID FK → Users (Omar — cross-team, added in ALTER below).
-- ============================================================
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
    UNIQUE (SSN)
    -- CONSTRAINT fk_employee_user FOREIGN KEY (UserID) REFERENCES Users(UserID)
    --   (cross-team — enabled in merged schema)
);

-- ============================================================
-- 3. DEPARTMENT
-- Belongs to one Hospital. ChairmanDoctorID is circular
-- (references Doctor) and is added via ALTER below.
-- ============================================================
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

-- ============================================================
-- 4. DOCTOR
-- Subclass of Employee. Belongs to one Department.
-- ============================================================
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

-- ============================================================
-- Circular Dependency Fix: Department.ChairmanDoctorID → Doctor
-- ============================================================
ALTER TABLE Department
    ADD CONSTRAINT fk_dept_chairman
    FOREIGN KEY (ChairmanDoctorID) REFERENCES Doctor(EmployeeID)
        ON DELETE SET NULL
        ON UPDATE CASCADE;

-- ============================================================
-- 5. NURSE
-- Subclass of Employee. Belongs to one Department.
-- ============================================================
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

-- ============================================================
-- 6. ADMIN
-- Subclass of Employee.
-- ============================================================
CREATE TABLE Admin (
    EmployeeID      INT             NOT NULL,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================
-- 7. DEPARTMENT_LOCATION
-- A Department may have multiple physical locations.
-- ============================================================
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

-- ============================================================
-- SAMPLE DATA
-- Requires UserIDs from Omar's Users table to already exist.
-- ============================================================

INSERT INTO Hospital (Name, Address, Phone, Email, EstablishedYear) VALUES
('Cairo General Hospital', '123 Health St, Cairo, Egypt', '02-12345678', 'info@cairogeneral.eg', 1985),
('Nile Medical Center', '456 River Rd, Giza, Egypt', '02-87654321', 'contact@nilemed.eg', 2005);

INSERT INTO Employee (UserID, FirstName, LastName, BirthDate, Sex, SSN, HireDate, JobTitle, EmployeeType) VALUES
(2, 'Ziad', 'Khaled', '1985-04-12', 'M', '222-33-4444', '2020-01-15', 'ER Physician', 'Doctor'),
(3, 'Youssef', 'Amir', '1990-08-20', 'M', '333-44-5555', '2021-06-01', 'Charge Nurse', 'Nurse'),
(4, 'Admin', 'User', '1980-01-01', 'M', '444-55-6666', '2019-03-10', 'System Administrator', 'Admin'),
(9, 'Fatma', 'Nabil', '1988-12-15', 'F', '555-66-7777', '2022-02-20', 'ER Nurse', 'Nurse'),
(10, 'Tarek', 'Samir', '1975-09-05', 'M', '666-77-8888', '2018-11-01', 'Senior Physician', 'Doctor'),
(11, 'Ahmed', 'Mansour', '1978-03-22', 'M', '777-88-9991', '2017-05-12', 'Cardiologist', 'Doctor'),
(12, 'Sara', 'Ali', '1993-11-04', 'F', '888-99-0002', '2023-08-19', 'Triage Nurse', 'Nurse');

INSERT INTO Department (HospitalID, Name, Code, SupervisionStartDate) VALUES
(1, 'Emergency Department', 'ED001', '2020-01-15'),
(2, 'Cardiology Unit', 'CARD001', '2021-06-01');

INSERT INTO Doctor (EmployeeID, DepartmentID, MajorScientificArea, Degree, JoinDate) VALUES
(1, 1, 'Emergency Medicine', 'MD', '2020-01-15'),
(5, 1, 'Trauma Surgery', 'MD, FACS', '2018-11-01'),
(6, 2, 'Cardiology', 'MD, PhD', '2021-06-01');

UPDATE Department SET ChairmanDoctorID = 1 WHERE DepartmentID = 1;
UPDATE Department SET ChairmanDoctorID = 6 WHERE DepartmentID = 2;

INSERT INTO Nurse (EmployeeID, DepartmentID, JoinDate) VALUES
(2, 1, '2021-06-01'),
(4, 1, '2022-02-20'),
(7, 1, '2023-01-10');

INSERT INTO Admin (EmployeeID) VALUES (3);

INSERT INTO DepartmentLocation (DepartmentID, Address, Latitude, Longitude) VALUES
(1, '123 Emergency St, Cairo, Egypt', 30.04440000, 31.23570000),
(2, '456 Cardiology Ave, Cairo, Egypt', 30.06260000, 31.24970000);

-- ============================================================
-- CROSS-TEAM FOREIGN KEY CONSTRAINTS (deferred)
-- Employee.UserID → Users(UserID)  [Omar]
-- ============================================================
-- ALTER TABLE Employee
--     ADD FOREIGN KEY (UserID) REFERENCES Users(UserID)
--         ON DELETE RESTRICT
--         ON UPDATE CASCADE;
