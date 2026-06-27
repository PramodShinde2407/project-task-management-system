# Mini Jira - Task Management Backend System

A lightweight Jira-inspired task management backend built with FastAPI and PostgreSQL. The system enables organizations to manage projects, tasks, team collaboration, notifications, activity tracking, and reporting through a secure REST API.

## Project Overview

Mini Jira is a backend service designed to support project and task management workflows. It provides authentication, role-based authorization, project management, task assignment, comments, notifications, activity tracking, and reporting features.

### Supported Roles

* **Admin**

  * Manage users
  * Manage project managers
  * Access all projects and tasks
  * Access reports

* **Project Manager**

  * Create and manage projects
  * Add project members
  * Create and assign tasks
  * Track project progress
  * Generate reports

* **Team Member**

  * View assigned projects and tasks
  * Update task status
  * Add comments
  * Track personal progress

---

## Features

### Authentication & Authorization

* JWT-based authentication
* Secure password hashing using bcrypt
* Role-based access control (RBAC)
* Protected API routes

### Project Management

* Create, update, and delete projects
* Assign members to projects
* Manage project lifecycle
* Generate project reports

### Task Management

* Create and manage tasks
* Assign tasks to team members
* Track task status and priority
* Due date management

### Collaboration

* Task comments
* User mentions in comments
* Team-based project access

### Notifications

* Task assignment notifications
* User notification center
* Mark notifications as read

### Activity Tracking

* Project timeline tracking
* Task activity history
* Audit trail for major actions

### Reporting & Dashboard

* Project reports
* User productivity reports
* Dashboard statistics
* Recent activity tracking

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migration Tool:** Alembic
* **Authentication:** JWT
* **Password Hashing:** Passlib (bcrypt)
* **Validation:** Pydantic
* **ASGI Server:** Uvicorn

---

## Database Design

### Core Tables

* Users
* Projects
* Tasks
* Comments
* Timeline
* Notifications

### Association Tables

* Project_Assigned
* Task_Assigned
* Comment_Mentions
* Notification_Assigned

### Key Relationships

* One Manager → Many Projects
* One Project → Many Tasks
* One Task → Many Comments
* Many Users ↔ Many Projects
* Many Users ↔ Many Tasks
* Many Users ↔ Many Notifications

---

## Project Structure

```text
MINI_JIRA/
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── Backend/
│   ├── core/
│   ├── database/
│   │   ├── base.py
│   │   ├── connection.py
│   │   └── session.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   ├── dependencies/
│   └── utils/
│
├── .env
├── alembic.ini
├── requirements.txt
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd MINI_JIRA
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/project_task_management_system

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Migration

Initialize Alembic:

```bash
alembic init alembic
```

Generate Migration:

```bash
alembic revision --autogenerate -m "initial migration"
```

Apply Migration:

```bash
alembic upgrade head
```

---

## Running the Application

```bash
uvicorn main:app --reload
```

Application URL:

```text
http://localhost:8000
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Main API Modules

### Authentication

* Signup
* Login
* Logout

### Projects

* Create Project
* Update Project
* Delete Project
* Add/Remove Members
* Project Reports

### Tasks

* Create Task
* Assign Task
* Update Status
* Delete Task

### Comments

* Add Comment
* Edit Comment
* Delete Comment
* Mention Users

### Notifications

* View Notifications
* Mark as Read

### Timeline

* Project Activity History
* Task Activity History

### Dashboard

* Statistics
* Recent Activities

### Reports

* Project Reports
* User Productivity Reports
* Task Statistics Reports

---

## Business Rules

* Only Admin can create users.
* Only Admin can assign Project Managers.
* Project Managers can manage only their projects.
* Team Members cannot create projects.
* Team Members cannot assign tasks.
* Tasks must belong to a project.
* Users must be project members before task assignment.
* Completed tasks cannot be reassigned.
* Deleting a project removes related tasks.
* Notifications are generated on task assignment.

---

## Future Improvements

* Email notifications
* File attachments
* WebSocket-based real-time updates
* Project analytics dashboard
* Docker deployment
* CI/CD integration
* Unit and Integration Testing

---

## Author

Pramod Shinde

Backend Assessment Project – Mini Jira Task Management System
