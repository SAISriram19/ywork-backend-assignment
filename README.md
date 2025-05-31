# Django Order Management System with Google OAuth

## Overview
This project implements a comprehensive order management system with Google OAuth 2.0 authentication and REST API endpoints using Django Rest Framework.

## Project Structure
```
django-order-management/
├── data_api/         # Main application code
├── ordermanagement/  # Django project configuration
├── google_credentials.json  # Google OAuth credentials
├── manage.py         # Django management script
├── requirements.txt  # Project dependencies
└── README.md        # Project documentation
```

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- virtualenv (for creating isolated Python environments)

## Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/SAISriram19/ywork-backend-assignment.git
cd ywork-backend-assignment
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google OAuth
1. Go to Google Cloud Console (https://console.cloud.google.com)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Go to "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Select "Web application"
   - Add authorized redirect URI:
     ```
     http://localhost:8000/accounts/google/login/callback/
     ```
5. Download the credentials JSON file and save it as `google_credentials.json` in the project root directory

### 5. Database Setup
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
The application will be available at `http://localhost:8000`

## API Documentation

### Authentication Endpoints
- Google Login: `GET /accounts/google/login/`
- Google Login Callback: `GET /accounts/google/login/callback/`
- OAuth Token: `GET /api/oauth-token/` (returns access and refresh tokens)

### Data Management Endpoints
- Create Item: `POST /api/items/`
  ```json
  {
      "title": "string",
      "description": "string"
  }
  ```

- List Items: `GET /api/items/`
  - Filter by title: `GET /api/items/?title=your_search_term`
  - Returns only items owned by the authenticated user

- Get Item: `GET /api/items/<id>/`
- Update Item: `PUT /api/items/<id>/`
- Delete Item: `DELETE /api/items/<id>/`

## Data Models

1. **GoogleOAuthToken**
   - Stores OAuth tokens for authenticated users
   - Contains access and refresh tokens
   - Tracks token expiration

2. **Item**
   - Represents user-owned items
   - Includes title and description
   - Each item is associated with an owner

## Security Features

1. **Authentication**:
   - Google OAuth 2.0 for user authentication
   - Access and refresh tokens stored securely
   - Session-based authentication
   - Token-based authentication for API endpoints

2. **API Protection**:
   - All API endpoints require authentication
   - User-specific data isolation
   - Rate limiting
   - CSRF protection

## Testing with Postman

1. First authenticate through browser:
   - Visit `http://localhost:8000/accounts/google/login/`
   - Complete Google OAuth flow
   - Copy session cookie from browser

2. In Postman:
   - Add header: `Cookie: your_session_cookie`
   - Use endpoints as documented above
   - All endpoints require authentication

## Configuration Notes

1. **Google OAuth Configuration**:
   - The application reads OAuth credentials from `google_credentials.json`
   - Ensure the JSON file contains valid credentials
   - Verify redirect URI is correctly configured in Google Cloud Console
   - Keep credentials secure and never commit them to version control

2. **Authentication Flow**:
   - Always initiate OAuth flow through browser first
   - Use browser session cookies for Postman testing
   - All API endpoints require authentication

3. **Security Best Practices**:
   - Never expose your `google_credentials.json` file
   - Regularly rotate your OAuth credentials
   - Keep your Django SECRET_KEY secure

4. **Development Tips**:
   - Use DEBUG=True during development
   - Check Django logs for detailed error messages
   - Test API endpoints using both browser and Postman


