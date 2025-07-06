# Entry Management System

A Django-based web application for managing entries, calculating interest, and tracking releases.

## Features

- User registration and approval system
- Entry management with date, amount, serial number, and weight tracking
- Interest calculation with compound interest
- Release management system
- Admin dashboard with comprehensive statistics and audit logs

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create superuser (admin):
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Default Admin Credentials

- Username: admin
- Password: (set during superuser creation)

**Note:** Change these credentials in production!

## Project Structure

- `entry_management/` - Main project directory
  - `users/` - User management app
  - `entries/` - Entry and release management app
  - `core/` - Core functionality and utilities
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images) 