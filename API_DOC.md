# Healthcare Management System API Documentation

This document outlines the internal APIs for the Healthcare Management System. These APIs enable programmatic interaction with the system's core functionality.

## Authentication API

### User Authentication

#### Login

- **URL**: `/login/`
- **Method**: POST
- **Description**: Authenticates a user and creates a session
- **Request Parameters**:
  - `username`: User's username
  - `password`: User's password
- **Response**:
  - Success: Redirects to appropriate dashboard
  - Error: Returns login page with error message
- **Implementation**: `UserLoginView` in `users/views.py`

#### Logout

- **URL**: `/logout/`
- **Method**: POST
- **Description**: Ends user session
- **Response**: Redirects to login page
- **Implementation**: Django's `LogoutView`

## User Management API

### Patient Registration

- **URL**: `/signup/`
- **Method**: POST
- **Description**: Creates a new patient account
- **Request Parameters**:
  - `username`: Desired username
  - `email`: Email address
  - `password1`: Password
  - `password2`: Password confirmation
  - `name`: Patient's full name
  - `date_of_birth`: Date of birth (optional)
  - `address`: Address (optional)
  - `phone`: Phone number (optional)
  - `emergency_contact`: Emergency contact information (optional)
- **Response**:
  - Success: Redirects to login page
  - Error: Returns signup page with validation errors
- **Implementation**: `PatientSignUpView` in `users/views.py`

### Doctor Registration

- **URL**: `/doctor/signup/`
- **Method**: POST
- **Description**: Creates a new doctor account
- **Request Parameters**:
  - `username`: Desired username
  - `email`: Email address
  - `password1`: Password
  - `password2`: Password confirmation
  - `name`: Doctor's full name
  - `specialization`: Medical specialization
  - `license_number`: Professional license number
  - `contact_number`: Contact number (optional)
  - `bio`: Professional biography (optional)
  - `office_address`: Office address (optional)
  - `office_hours`: Office hours (optional)
- **Response**:
  - Success: Redirects to login page
  - Error: Returns signup page with validation errors
- **Implementation**: `DoctorSignUpView` in `users/views.py`

## Electronic Health Records API

### List Medical Records

- **URL**: `/ehr/list/`
- **Method**: GET
- **Description**: Retrieves list of medical records for the current user
- **Query Parameters**:
  - `record_type`: Filter by record type (optional)
  - `tag`: Filter by tag ID (optional)
- **Response**: HTML page with list of records
- **Implementation**: `PatientEHRListView` in `ehr/views.py`

### Upload Medical Record

- **URL**: `/ehr/upload/`
- **Method**: POST
- **Description**: Creates a new medical record
- **Request Parameters**:
  - `record_type`: Type of medical record
  - `description`: Brief description of the record
  - `content`: Textual content of the record (optional)
  - `attachments`: File attachment
  - `tags`: Selected tags (optional)
  - `is_confidential`: Confidentiality flag (optional)
- **Response**:
  - Success: Redirects to record list page
  - Error: Returns upload form with validation errors
- **Implementation**: `upload_ehr` in `ehr/views.py`

### View Medical Record

- **URL**: `/ehr/record/<id>/`
- **Method**: GET
- **Description**: Retrieves detailed view of a specific medical record
- **Path Parameters**:
  - `id`: Record ID
- **Response**: HTML page with record details
- **Implementation**: `EHRDetailView` in `ehr/views.py`

### Update Medical Record

- **URL**: `/ehr/record/<id>/update/`
- **Method**: POST
- **Description**: Updates an existing medical record
- **Path Parameters**:
  - `id`: Record ID
- **Request Parameters**: Same as upload endpoint
- **Response**:
  - Success: Redirects to record detail page
  - Error: Returns update form with validation errors
- **Implementation**: `update_ehr` in `ehr/views.py`

### Delete Medical Record

- **URL**: `/ehr/record/<id>/delete/`
- **Method**: POST
- **Description**: Deletes a medical record
- **Path Parameters**:
  - `id`: Record ID
- **Response**: Redirects to record list page
- **Implementation**: `delete_ehr` in `ehr/views.py`

### Add Record Tag

- **URL**: `/ehr/add-tag/`
- **Method**: POST
- **Description**: Creates a new tag for medical records
- **Request Parameters**:
  - `tag_name`: Name of the tag
- **Response**: JSON response indicating success/failure
- **Implementation**: `add_tag` in `ehr/views.py`

## AI Analysis API

### Analyze Medical Record

- **URL**: `/ehr/record/<id>/analyze/`
- **Method**: GET
- **Description**: Analyzes a medical record using Claude AI
- **Path Parameters**:
  - `id`: Record ID
- **Response**: Redirects to analysis result page
- **Implementation**: `analyze_medical_record` in `ehr/views.py`

### View Analysis Results

- **URL**: `/ehr/record/<id>/analysis/`
- **Method**: GET
- **Description**: Displays AI analysis results for a medical record
- **Path Parameters**:
  - `id`: Record ID
- **Response**: HTML page with structured analysis data
- **Implementation**: `view_analysis` in `ehr/views.py`

## Messaging API

### List Conversations

- **URL**: `/messages/`
- **Method**: GET
- **Description**: Lists all conversations for the current user
- **Response**: HTML page with conversation list
- **Implementation**: `conversation_list` in `messaging/views.py`

### View Conversation

- **URL**: `/messages/<conversation_id>/`
- **Method**: GET
- **Description**: Displays a specific conversation thread
- **Path Parameters**:
  - `conversation_id`: Conversation ID
- **Response**: HTML page with message thread and reply form
- **Implementation**: `conversation_detail` in `messaging/views.py`

### Send Message

- **URL**: `/messages/<conversation_id>/`
- **Method**: POST
- **Description**: Adds a message to a conversation
- **Path Parameters**:
  - `conversation_id`: Conversation ID
- **Request Parameters**:
  - `content`: Message text
  - `attachment`: Optional file attachment
- **Response**: Redirects back to conversation page with new message
- **Implementation**: `conversation_detail` in `messaging/views.py`

### Start Conversation

- **URL**: `/messages/start/<user_id>/`
- **Method**: GET
- **Description**: Creates a new conversation with specified user
- **Path Parameters**:
  - `user_id`: User ID to start conversation with
- **Response**: Redirects to new conversation page
- **Implementation**: `start_conversation` in `messaging/views.py`

### Get Unread Message Count

- **URL**: `/messages/unread/count/`
- **Method**: GET
- **Description**: Returns count of unread messages for current user
- **Response**: JSON with unread message count
- **Implementation**: `unread_message_count` in `messaging/views.py`

### List Available Doctors

- **URL**: `/messages/doctors/`
- **Method**: GET
- **Description**: Lists all doctors available for messaging (patient only)
- **Response**: HTML page with doctor list
- **Implementation**: `doctor_list` in `messaging/views.py`

## Implementation Notes

### API Error Handling

- All APIs implement appropriate error handling
- Authentication is required for all endpoints except login and registration
- Role-based access control is enforced for each endpoint
- Invalid requests return appropriate HTTP status codes with error messages

### API Security Considerations

- CSRF protection is enabled for all POST endpoints
- Session-based authentication is used for all protected endpoints
- File uploads are validated for type and size
- Role-based permission checks prevent unauthorized access

### Future API Enhancements

- RESTful JSON API endpoints for mobile integration
- Pagination support for list endpoints
- More advanced filtering and search capabilities
- OAuth2 authentication for third-party application integration