# 🏢 Karnesh Technology HR Portal

A modern **Human Resource Management System (HRMS)** built using
**Flask, SQLite, HTML, CSS, and JavaScript**. This project provides a
complete solution for managing employees, attendance, leave requests,
departments, payroll, dashboards, and reports through a responsive web
interface.

------------------------------------------------------------------------

## ✨ Features

### 🔐 Authentication

-   Secure Login & Logout
-   Session-Based Authentication
-   Role-Based Access Control (HR/Admin)

### 👨‍💼 Employee Management

-   Add, Edit, Delete Employees
-   Employee Search
-   Department Assignment
-   Employee Status Management
-   Duplicate Employee Code & User ID Validation

### 📅 Attendance Management

-   Mark Attendance
-   Edit Attendance
-   Attendance History
-   Attendance Reports

### 📝 Leave Management

-   Apply Leave
-   Approve / Reject Leave
-   Leave History
-   Pending Leave Tracking

### 🏢 Department Management

-   Add, Edit, Delete Departments
-   Department-wise Employee Count

### 💰 Payroll Management

-   Salary Records
-   Payroll Reports

### 📊 Dashboard & Reports

-   Dashboard Statistics
-   Employee Distribution Charts
-   Attendance Reports
-   Leave Status Charts
-   Salary Reports
-   Export CSV
-   Print Reports

------------------------------------------------------------------------

## 🛠 Tech Stack

### Backend

-   Python
-   Flask
-   SQLite3

### Frontend

-   HTML5
-   CSS3
-   JavaScript (ES6)
-   Chart.js
-   Font Awesome

------------------------------------------------------------------------

## 📂 Project Structure

``` text
Karnesh_Technology_HR_Portal/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── middleware/
│   └── hr_portal.db
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── login.html
│   ├── dashboard.html
│   ├── employee.html
│   ├── attendance.html
│   ├── leave.html
│   ├── reports.html
│   └── profile.html
│
└── README.md
```

------------------------------------------------------------------------

## 🚀 Installation

``` bash
git clone https://github.com/yourusername/Karnesh_Technology_HR_Portal.git
cd Karnesh_Technology_HR_Portal
pip install -r requirements.txt
cd backend
python app.py
```

Open the frontend using **VS Code Live Server** and browse to:

``` text
frontend/login.html
```

------------------------------------------------------------------------

## 🗄 Database

SQLite database:

``` text
backend/hr_portal.db
```

Tables: - users - employees - departments - attendance -
leave_requests - payroll

------------------------------------------------------------------------

## 🔒 Security Features

-   Session Authentication
-   Role-Based Authorization
-   Protected REST APIs
-   Input Validation
-   Duplicate Employee Validation
-   Exception Handling

------------------------------------------------------------------------

## 🚀 Future Enhancements

-   Email Notifications
-   JWT Authentication
-   Face Recognition Attendance
-   Employee Self-Service Portal
-   Cloud Database Support
-   Audit Logs
-   Dark Mode
-   Excel & PDF Export

------------------------------------------------------------------------

## 👨‍💻 Author

**Karnesh E J**

B.E. Computer Science Engineering\
S.A. Engineering College, Chennai

------------------------------------------------------------------------

## 📄 License

This project is licensed under the **MIT License**.

------------------------------------------------------------------------

## ⭐ Support

If you found this project useful, consider giving it a **⭐ Star** on
GitHub!
