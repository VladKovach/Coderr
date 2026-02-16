# Coderr - Services Marketplace API

A Django REST Framework-based backend for a services marketplace platform that allows users to create service offers, manage orders, track reviews, and build extended profiles.

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/)
- **pip** - Usually comes with Python
- **Virtual Environment** - Built-in with Python

Verify installations:

```bash
python --version
git --version
pip --version
```

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/VladKovach/Coderr.git
cd Coderr
```

### Step 2: Create and Activate a Virtual Environment

#### On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

## 💾 Database Setup

### Apply Migrations

Create the database tables and apply all migrations:

```bash
# Create any pending migrations
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate
```

### Create a Superuser (Admin)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:

- Username
- Email
- Password

## 🏃 Running the Application

### Start the Development Server

```bash
python manage.py runserver
```

The server will run at: **http://127.0.0.1:8000/**

### Access Key URLs

| URL                            | Purpose               |
| ------------------------------ | --------------------- |
| `http://127.0.0.1:8000/api/`   | API Root              |
| `http://127.0.0.1:8000/admin/` | Django Admin Panel    |
| `http://127.0.0.1:8000/media/` | Media Files (uploads) |

### API Endpoints Overview

The API is organized by feature modules:

```
/api/auth/           # Authentication endpoints
/api/profiles/       # Profiles specific info
/api/profile/        # Profiles management
/api/offers/         # Service offers
/api/offerdetails/   # Offer details
/api/orders/         # Order management
/api/order-count/    # Order statistics
/api/reviews/        # Review system
/api/base-info/      # Dashboard analytics
```

## 🧪 Running Tests

The project uses **pytest** and **pytest-django** for testing.

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov
```

### Run Tests for a Specific App

```bash
pytest auth_app/
pytest offers_app/
pytest orders_app/
```

## 🔐 Authentication

The API uses **Token Authentication**. To obtain a token:

1. Register or login via the auth endpoints
2. Include the token in request headers:
   ```
   Authorization: Token your-token-here
   ```

**Happy coding! 🚀**
