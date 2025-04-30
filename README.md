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

## Features
We have successfully implemented the following features:

### User Management
- **Patient Registration & Authentication**: Secure signup process with comprehensive profile creation
- **Doctor Registration & Authentication**: Medical professionals can create accounts with specialization details
- **Profile Management**: Interfaces for users to view and update their personal information

### Electronic Health Records (EHR)
- **Record Upload**: Functionality to upload and manage various types of medical records
- **Record Tagging**: Ability to categorize records with custom tags for easier organization
- **Confidentiality Controls**: Options to mark sensitive records as confidential

### AI-Powered Analysis
- **Medical Document Analysis**: Utilizes Claude AI to extract key information from medical documents
- **Structured Data Extraction**: Automatically identifies diagnoses, medications, treatments, test results, and abnormal values
- **Analysis Review**: User-friendly interface to review AI-generated analysis

### Communication
- **Secure Messaging**: Private conversations between doctors and patients
- **File Sharing**: Ability to share documents through the messaging system
- **Unread Message Notifications**: Real-time notification of new messages

## Technology Stack
### Backend
- **Django (5.1.7)**: For robust security features, ORM capabilities, and built-in admin interface
- **Python**: Core programming language for backend development
- **Anthropic Claude API**: AI service for medical document analysis

### Frontend
- **Django Templates**: For building responsive user interfaces
- **HTML/CSS**: For structure and styling of the application
- **JavaScript**: For interactive elements and real-time notifications

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
- Anthropic API key
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

4. Configure your Anthropic API key
   - Open `healthcare_management/settings.py`
   - Replace the placeholder API key with your own:
     ```python
     ANTHROPIC_API_KEY = 'your-api-key-here'
     ```

5. Apply migrations
   ```bash
   # Generate migration files based on model changes
   python manage.py makemigrations
   
   # Apply migrations to the database
   python manage.py migrate
   ```

6. Create a superuser (admin)
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

## Project Structure
- `healthcare_management/` - Main project directory
- `users/` - User authentication and profile management app
- `ehr/` - Electronic Health Records management app
- `messaging/` - Patient-doctor communication app
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `media/` - User-uploaded files

## AI-Powered Medical Record Analysis
Our system uses the Anthropic Claude AI model to analyze medical documents and extract key information:

1. **Document Upload**: Users can upload medical records through the EHR interface
2. **AI Analysis**: Claude AI analyzes the document content and extracts:
   - Diagnoses
   - Medications with dosages and frequencies
   - Treatments and recommendations
   - Test results with normal ranges
   - Abnormal values requiring attention
3. **Structured Results**: Analysis results are displayed in a user-friendly format
4. **Clinical Decision Support**: The structured data helps healthcare providers make informed decisions

## Team Members
- Siyuan (Max) Meng (@siyuanmengmax)
- Yanan (Amy) Zhang (@moonmoonmoonmoon)
- Anushka Agarwal (@anushka17agarwal)
- Talha Mohammed Zakir Chafekar (@talha1503)

## Project Resources
- [Project Documentation](https://drive.google.com/drive/folders/1CKSTxzOG-uz_qVGkbOr2_3o1p5T_zjmL?usp=sharing)
- [GitHub Repository](https://github.com/siyuanmengmax/healthcare)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Professor and TAs of COMPSCI 520 at UMass Amherst
- Django documentation and community
- Anthropic for providing the Claude AI API