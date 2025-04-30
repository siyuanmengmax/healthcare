# Healthcare Management System - Build Guide

This document provides instructions for setting up, configuring, and running the Healthcare Management System.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Internet connection (for API integration)
- Virtual environment (recommended)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/siyuanmengmax/healthcare.git
cd healthcare
```

### 2. Create and Activate Virtual Environment (Recommended)

#### For Linux/MacOS:
```bash
python -m venv env
source env/bin/activate
```

#### For Windows:
```bash
python -m venv env
env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

1. Open `healthcare_management/settings.py`
2. Locate the `ANTHROPIC_API_KEY` setting
3. Replace the placeholder with your Claude API key:
   ```python
   ANTHROPIC_API_KEY = 'your-api-key-here'
   ```
   
   You can obtain an API key from the [Anthropic Console](https://console.anthropic.com/).

### 5. Database Setup

The project uses SQLite, which doesn't require separate server installation. To initialize the database:

```bash
# Create migration files for any model changes
python manage.py makemigrations

# Apply migrations to create database schema
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```
Follow the prompts to create an administrator account.

### 7. Run Development Server

```bash
python manage.py runserver
```

The application should now be running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Database Changes

### Current Database Schema

The database schema is defined in the migration files in each app's `migrations` directory. The key models include:

- User (extended Django User model)
- Patient
- Doctor
- MedicalRecord
- MedicalRecordAnalysis
- Conversation
- Message

### Making Database Changes

If you need to modify the database schema:

1. Edit the relevant model in the appropriate `models.py` file
2. Generate migration files:
   ```bash
   python manage.py makemigrations
   ```
3. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

### Database Reset (If Needed)

If you need to reset the database during development:

1. Delete the `db.sqlite3` file
2. Delete all files in the migration folders except `__init__.py`
3. Regenerate migrations:
   ```bash
   python manage.py makemigrations users
   python manage.py makemigrations ehr
   python manage.py makemigrations messaging
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a new superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Media Files

Uploaded files are stored in the `media` directory. Make sure this directory has appropriate permissions:

```bash
# Create media directory if it doesn't exist
mkdir -p media/ehr_attachments
mkdir -p media/message_attachments

# Set permissions (for Linux/MacOS)
chmod 755 media
chmod 755 media/ehr_attachments
chmod 755 media/message_attachments
```

## Testing

Run the test suite to verify the installation:

```bash
python manage.py test
```

## Deployment Considerations

For production deployment:

1. Update `healthcare_management/settings.py`:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS` with your domain
   - Configure a production-ready database (PostgreSQL recommended)
   - Set up proper static file serving

2. Configure a proper web server (Nginx, Apache) with WSGI (Gunicorn, uWSGI)

3. Set up HTTPS with a valid SSL certificate

## Troubleshooting

### Common Issues

**Issue**: Missing dependencies
**Solution**: Run `pip install -r requirements.txt` to ensure all dependencies are installed

**Issue**: Database migration errors
**Solution**: Try resetting the database as described above

**Issue**: API key errors
**Solution**: Double-check your Anthropic API key and ensure it has the necessary permissions

**Issue**: Media files not loading
**Solution**: Check file permissions on the media directory and ensure `MEDIA_URL` and `MEDIA_ROOT` are correctly configured in settings.py

### Support

For additional help, please contact the project maintainers:
- Siyuan (Max) Meng (@siyuanmengmax)
- Yanan (Amy) Zhang (@moonmoonmoonmoon)
- Anushka Agarwal (@anushka17agarwal)
- Talha Mohammed Zakir Chafekar (@talha1503)