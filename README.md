# Role-Based Management System

## Overview
This project is a full-stack Role-Based Management System that implements authentication and authorization using Role-Based Access Control (RBAC).

It enables administrators to manage users, assign roles, and control access to different parts of the application based on permissions. The system is designed to be lightweight, scalable, and suitable for real-world applications such as admin dashboards, SaaS platforms, and enterprise systems.

---

## Features

- User authentication (login and registration)
- User management (create, update, delete users)
- Role management (Admin, Manager, User)
- Permission-based access control (RBAC)
- RESTful API built with Flask
- Dynamic frontend using Vue.js
- Secure route protection (frontend and backend)
- Lightweight database using SQLite

---

## Architecture

The system follows a standard RBAC structure:

- Users are assigned to roles  
- Roles are associated with permissions  
- Permissions control access to system features  

Application flow:

Frontend (Vue.js) communicates with Backend (Flask API), which interacts with the SQLite database.

---

## Tech Stack

### Backend
- Flask (Python)
- RESTful APIs
- SQLite

### Frontend
- Vue.js
- Axios
- HTML, CSS, JavaScript

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/niyibizimadeit/role-based-management-system.git
cd role-based-management-system
