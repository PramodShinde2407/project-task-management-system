# Mini Jira - Task Management System

A lightweight task management system built with FastAPI, designed as a simplified version of Jira for managing projects and tasks efficiently.

## Overview

Mini Jira is a RESTful API-based task management application that allows users to create, update, delete, and track tasks and projects. It provides a minimal but functional implementation of core project management features.

## Features

- **Project Management**: Create and manage multiple projects
- **Task Management**: Add, update, and track tasks within projects
- **Task Status Tracking**: Track task progress through different states (TODO, In Progress, Done, etc.)
- **User Assignment**: Assign tasks to users
- **Comments & Activity**: Add comments and track activity on tasks
- **REST API**: Full REST API for all operations

## Tech Stack

- **Framework**: FastAPI
- **Python**: 3.8+
- **Database**: SQLite (or configurable)
- **Server**: Uvicorn

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Mini_Jira
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the development server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
Mini_Jira/
├── main.py              # Main application entry point
├── requirements.txt     # Project dependencies
├── models/              # Database models
├── schemas/             # Pydantic schemas for request/response
├── routes/              # API routes
├── database.py          # Database configuration
└── README.md            # This file
```

## API Endpoints

### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create a new project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update a project
- `DELETE /projects/{id}` - Delete a project

### Tasks
- `GET /tasks` - List all tasks
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get task details
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues, please create an issue in the repository.
