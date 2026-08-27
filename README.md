# Secure Login System

## 1. Project Title

**Secure Login System**

## 2. Project Overview

The Secure Login System is a web-based authentication application developed using Python Flask. It provides secure user registration and login functionality while protecting user accounts against common security threats.

The system uses bcrypt hashing to securely store passwords instead of storing them in plain text. It also implements input validation, parameterized database queries, session management, login attempt protection, and security activity logging.

## 3. Objectives

* To develop a secure user registration and login system.
* To protect passwords using bcrypt hashing.
* To prevent SQL injection using parameterized queries.
* To implement secure session management.
* To restrict unauthorized access to protected pages.
* To detect repeated failed login attempts.
* To maintain security activity logs.

## 4. Technologies Used

| Technology   | Purpose                                      |
| ------------ | -------------------------------------------- |
| Python       | Backend programming                          |
| Flask        | Web framework                                |
| SQLite       | Database                                     |
| HTML         | Web page structure                           |
| CSS          | User interface design                        |
| JavaScript   | Client-side validation and password features |
| Flask-Bcrypt | Password hashing                             |

## 5. Main Features

### User Registration

Users can create an account using a username, email address, and password.

### Password Hashing

Passwords are protected using bcrypt hashing before being stored in the database.

### Password Strength Validation

The registration system checks password length and complexity.

### Confirm Password

The user must enter the same password twice during registration.

### Show/Hide Password

Users can show or hide their password using the eye button.

### Secure Login

The system verifies the entered password against the stored bcrypt hash.

### SQL Injection Protection

Parameterized SQL queries are used to reduce the risk of SQL injection.

### Session Management

A secure session is created after successful login.

### Protected Dashboard

Only authenticated users can access the dashboard.

### Login Attempt Protection

Repeated unsuccessful login attempts trigger temporary login blocking.

### Security Activity Logs

Successful login, failed login, account registration, logout, and blocking events are recorded.

### Logout

The session is cleared when the user logs out.

## 6. System Workflow

```text
User
  ↓
Registration
  ↓
Input Validation
  ↓
Password Strength Check
  ↓
Bcrypt Password Hashing
  ↓
SQLite Database
  ↓
Login
  ↓
Password Verification
  ↓
Session Creation
  ↓
Protected Dashboard
  ↓
Security Activity
  ↓
Logout
  ↓
Session Cleared
```

## 7. Database Structure

### Users Table

* `id`
* `username`
* `email`
* `password`

### Security Logs Table

* `id`
* `email`
* `activity`
* `timestamp`

## 8. Security Measures

The application includes multiple security mechanisms:

1. Bcrypt password hashing.
2. Password complexity validation.
3. Parameterized database queries.
4. Session-based authentication.
5. Protected dashboard.
6. Failed login attempt limitation.
7. Security activity logging.
8. Input validation.

## 9. Expected Outcome

The project provides a functional and secure authentication system that reduces the risk of unauthorized access and protects user credentials from common attacks.

## 10. Testing

| Test Case                             | Expected Result              |
| ------------------------------------- | ---------------------------- |
| Valid registration                    | Account created successfully |
| Existing email                        | Registration rejected        |
| Weak password                         | Registration rejected        |
| Mismatched passwords                  | Registration rejected        |
| Correct login credentials             | Dashboard displayed          |
| Wrong password                        | Login rejected               |
| Repeated failed attempts              | Temporary login block        |
| Direct dashboard access without login | Redirected to login          |
| Logout                                | Session cleared              |
| Security activity                     | Recorded in security logs    |

## 11. How to Run the Project

Activate the virtual environment and run:

```bash
python database.py
python app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

## 12. Project Conclusion

The Secure Login System demonstrates practical implementation of web authentication and cybersecurity concepts. By combining password hashing, input validation, SQL injection protection, session management, login attempt protection, and security logging, the system provides a stronger authentication mechanism than a basic username-password application.

# Project Synopsis

## Problem Statement

Many web applications use login systems to authenticate users. Poorly implemented authentication can expose passwords and user accounts to unauthorized access. A secure authentication system is therefore required to protect user credentials and manage user sessions safely.

## Proposed Solution

The proposed Secure Login System provides user registration, secure password storage, authentication, session management, protected dashboard access, failed login protection, and security activity logging.

## Objectives

The main objective is to develop a secure and user-friendly authentication system using Flask and SQLite while implementing common cybersecurity practices.

## Applications

* Student projects
* Small web applications
* Authentication demonstrations
* Cybersecurity learning projects
* Flask-based web applications

# Screenshot Checklist

Take screenshots of these screens for the report:

1. **Registration Page** — shows username, email, password and confirm password.
2. **Password Strength** — shows Weak/Medium/Strong password indicator.
3. **Login Page** — shows secure login interface.
4. **Successful Login / Dashboard** — shows logged-in username and security status.
5. **Wrong Password** — shows invalid credentials message.
6. **Login Attempt Protection** — shows temporary block message.
7. **Security Activity Logs** — shows recorded login/logout activities.
8. **Logout** — shows return to login page.

# Viva Questions and Answers

### 1. What is the purpose of this project?

The purpose is to create a secure authentication system that protects user accounts from unauthorized access.

### 2. Which technology is used for the backend?

Python Flask is used as the backend framework.

### 3. Why is bcrypt used?

Bcrypt is used to securely hash passwords before storing them in the database.

### 4. Is the original password stored in the database?

No. Only the bcrypt hash of the password is stored.

### 5. What is SQL injection?

SQL injection is an attack where malicious SQL input is used to manipulate database queries.

### 6. How does the project prevent SQL injection?

Parameterized SQL queries are used instead of directly joining user input into SQL statements.

### 7. What is session management?

Session management keeps track of an authenticated user after successful login.

### 8. Why is the dashboard protected?

To prevent users who are not logged in from accessing private account information.

### 9. What happens after logout?

The session is cleared and the user is redirected to the login page.

### 10. What happens after repeated failed login attempts?

The system temporarily blocks further login attempts for that email.

### 11. What is the purpose of security logs?

Security logs record activities such as registration, successful login, failed login, blocking, and logout.

### 12. Which database is used?

SQLite is used as the database.

### 13. What are the main security features?

Bcrypt hashing, password validation, SQL injection protection, session management, login attempt protection, and security logging.

### 14. What is the future scope?

Future improvements can include Two-Factor Authentication (2FA), password reset through email, stronger session security, and an administrator security dashboard.
