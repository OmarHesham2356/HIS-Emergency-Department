-- ============================================================
-- RESET — Drop all 20 tables in reverse dependency order
-- Run from: mysql -u root < sql/reset.sql
-- ============================================================

USE emergency_dept;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS Document;
DROP TABLE IF EXISTS Examination;
DROP TABLE IF EXISTS Triage;
DROP TABLE IF EXISTS PrescriptionDetail;
DROP TABLE IF EXISTS Prescription;
DROP TABLE IF EXISTS EmergencyVisit;
DROP TABLE IF EXISTS Appointment;
DROP TABLE IF EXISTS Bed;
DROP TABLE IF EXISTS DepartmentLocation;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Nurse;
DROP TABLE IF EXISTS Doctor;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Patient_Phone;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Medication;
DROP TABLE IF EXISTS Hospital;

SET FOREIGN_KEY_CHECKS = 1;
