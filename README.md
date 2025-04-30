# Healthcare Management System

## Project Overview
The Healthcare Management System is a comprehensive digital platform aimed at modernizing healthcare record-keeping by transitioning from paper-based methods to a secure digital platform. Our system leverages advanced AI and Large Language Models (LLMs) to intelligently process medical documents, extract meaningful insights, and provide clinical decision support.

### Primary Goals
- Improve the accuracy and accessibility of patient records
- Enhance communication between doctors and patients
- Reduce administrative workload through AI-assisted automation
- Ensure data security and privacy compliance with healthcare regulations

### Target Audience
Our intended audience includes healthcare facilities of various sizes, from individual practices to clinics and hospitals, as well as their patients who will benefit from improved access to their healthcare information and more efficient communication with their providers.

## Implemented Features (Midpoint Milestone)
We have successfully implemented the following core features:

- **Patient Registration**: Secure signup process for patients with comprehensive profile creation
- **Patient Authentication**: Secure login system with session management
- **Patient Profile Management**: Interface for patients to view and update their personal information
- **Electronic Health Records (EHR) Upload**: Functionality for patients to upload and manage their medical records

## Upcoming Features
- **Doctor Registration and Authentication**
- **AI-Powered Medical Data Analysis**
- **Secure Messaging between Doctors and Patients**
- **Advanced Search and Filtering**
- **Appointment Management**
- **Medication Tracking and Reminders**

## Technology Stack
### Backend
- **Django (5.1.7)**: For robust security features, ORM capabilities, and built-in admin interface
- **Python**: Core programming language for backend development

### Frontend
- **Django Templates**: For building responsive user interfaces
- **HTML/CSS**: For structure and styling of the application

### Database
- **SQLite**: A reliable and secure relational database management system for development

### Security
- **Django Authentication System**: For secure user authentication and authorization
- **CSRF Protection**: Built-in protection against Cross-Site Request Forgery
- **Password Hashing**: Secure storage of user credentials

## Getting Started

### Prerequisites
- Python 3.8+
- Django 5.1.7+
- Virtual environment (recommended)

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/siyuanmengmax/healthcare.git
   cd healthcare
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   # Generate migration files based on model changes
   python manage.py makemigrations
   
   # Apply migrations to the database
   python manage.py migrate

5. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure
- `healthcare_management/` - Main project directory
- `users/` - User authentication and profile management app
- `ehr/` - Electronic Health Records management app
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `media/` - User-uploaded files

## Project Status
This project is currently in development by Team20_HealthManagement at the University of Massachusetts Amherst (Spring 2025). The current implementation represents the Midpoint Milestone of our development process.

## Team Members
- Siyuan (Max) Meng (@siyuanmengmax)
- Yanan (Amy) Zhang (@moonmoonmoonmoon)
- Anushka Agarwal (@anushka17agarwal)
- Talha Mohammed Zakir Chafekar (@talha1503)

## Project Resources
- [Project Documentation](https://drive.google.com/drive/folders/1CKSTxzOG-uz_qVGkbOr2_3o1p5T_zjmL?usp=sharing)
- [GitHub Repository](https://github.com/siyuanmengmax/healthcare)

## License
This project is for educational purposes as part of the CS 520 course at UMass Amherst.

## Acknowledgements
- Professor and TAs of COMPSCI 520 at UMass Amherst
- Django documentation and community