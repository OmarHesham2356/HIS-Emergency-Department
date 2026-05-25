# 🏥 HIS — Emergency Department

A **Hospital Information System** purpose-built for the **Emergency Department**. Streamlit-based web app with role-based access for doctors, nurses, patients, and administrators.

## Features

- **Role-based dashboard** — separate views for Admin, Doctor, Nurse, Patient
- **Patient management** — registration, medical history, triage tracking
- **Emergency visits** — admission, triage (level 1-5), bed assignment, discharge
- **Clinical workflow** — examinations, prescriptions, medication tracking
- **Appointments** — walk-in registration and scheduled bookings
- **Pharmacy** — prescription fulfillment
- **Staff management** — doctor, nurse, employee hierarchy
- **Admin panel** — statistical dashboards and reporting

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io) |
| Backend | Python 3.14 |
| Database | MySQL / MariaDB |
| Container | Docker + Dev Containers |

## Team Members

- **Omar Hesham** — Team Lead, Patient Flow & Appointments
- **Ziad Khaled** — Staff Hierarchy & Locations
- **Youssef Amir** — Clinical & Medication

---

## Development Environment

This project uses **Dev Containers** ([`@devcontainers/cli`](https://github.com/devcontainers/cli)) to provide a consistent, reproducible environment. The container bundles Python 3, MariaDB client, and all dependencies via a virtualenv.

### Prerequisites

- [Docker](https://docs.docker.com/engine/install/)
- [Node.js](https://nodejs.org/) + npm (for the CLI tool)
- [MariaDB](https://mariadb.org/) server running on the host

### Quick Start

```bash
# 1. Install the Dev Containers CLI
sudo npm install -g @devcontainers/cli

# 2. Make sure MariaDB is running
sudo systemctl enable --now mariadb

# 3. Create the database
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS emergency_dept;"

# 4. Build and start the container
devcontainer up --workspace-folder .

# 5. Drop into the container shell
devcontainer exec --workspace-folder . bash
```

### Available Commands (inside the container)

```bash
make run          # Launch the Streamlit app
make seed         # Seed sample data
make reset        # Drop and recreate the database
make reset-full   # Full reset: drop → schema → seed
```

### First Time Setup

Inside the container, initialize the database with sample data:

```bash
make reset-full
make run
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Database Schema

The schema covers 14+ entities for the Emergency Department:

- **Users** — authentication & role-based access (Admin, Doctor, Nurse, Patient)
- **Patient** — medical records (SSN, patient number, vital signs)
- **Employee / Doctor / Nurse** — staff hierarchy
- **Department** — Emergency Department, locations
- **EmergencyVisit** — admission, discharge, bed assignment
- **Triage** — triage level (1-5), vital signs, nurse assignment
- **Examination** — doctor-patient-visit interactions
- **Prescription / PrescriptionDetail / Medication** — clinical orders
- **Bed** — treatment bay tracking
- **Appointment** — walk-in & scheduled visits
- **Payment** — appointment billing
- **Document** — file uploads (scans, reports)

See [`docs/requirements.md`](docs/requirements.md) for the full specification.

---

## Project Structure

```
├── .devcontainer/          # Dev container configuration
├── app/                    # Streamlit application
│   ├── app.py              # Main app entry point
│   ├── db.py               # Database connection layer
│   └── .env.example        # Environment variable template
├── sql/                    # Database scripts
│   ├── merge/full_schema.sql  # Complete schema
│   ├── reset.sql           # Drop all tables
│   ├── seed_data.py        # Sample data seeder
│   └── validate.py         # Data validation
├── diagrams/               # ER diagrams (per member + merged)
├── schemas/                # Relational schema mappings
├── docs/                   # Requirements, plans, meeting notes
├── deliverables/           # Assignment deliverables
├── Dockerfile              # Container image definition
└── Makefile                # Command shortcuts
```
