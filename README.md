Task Management Application

This is a Django-based Task Management System that allows admins to assign tasks to users, track their progress, and manage task completion reports. It also includes authentication using Django’s user model and JWT tokens for API access.

Features
- Role-based access:
  - SuperAdmin: Manage admins and users.
  - Admin: Manage users assigned to them and assign tasks.
  - User: View and update assigned tasks, add completion report and worked hours.
- CRUD operations for tasks (Create, Read, Update, Delete) for admins and users.
- Track task status: Pending, In Progress, Completed.
- JWT-based API authentication for secure access.
- Separate web views and API endpoints.
- Responsive and clean HTML templates with a consistent layout.

Technologies Used
- Python 3.13
- Django 5.2.6
- Django REST Framework
- djangorestframework-simplejwt
- SQLite (default) or any other database configured in settings
- HTML/CSS for front-end templates

Installation

1. Clone the repository:
   bash
   git clone https://github.com/muneerrahman/Task-Management-Application.git
   cd Task-Management-Application
