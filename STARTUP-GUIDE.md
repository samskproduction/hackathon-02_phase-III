# Full Stack Application Startup Guide

This guide explains how to start both the backend and frontend applications for the Todo application.

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm
- Ensure you have installed all dependencies for both backend and frontend

## Installation

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

## Starting the Applications

### Windows Batch Scripts (Recommended)

We provide convenient batch scripts to start the applications:

1. **Start Backend Only**:
   ```cmd
   start-backend.bat
   ```
   This starts the backend server on `http://localhost:8000`

2. **Start Frontend Only**:
   ```cmd
   start-frontend.bat
   ```
   This starts the frontend server on `http://localhost:3000`

3. **Start Both Applications** (Recommended):
   ```cmd
   start-applications.bat
   ```
   This opens separate command prompts for both backend and frontend servers.

### Manual Startup

#### Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate your virtual environment:
   ```bash
   # On Windows:
   venv\Scripts\activate
   ```

3. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the frontend development server:
   ```bash
   npm run dev
   ```

## Application URLs

- **Backend API**: `http://localhost:8000`
  - Health check: `http://localhost:8000/health`
  - API endpoints: `http://localhost:8000/api/*`
  - Swagger docs: `http://localhost:8000/docs`

- **Frontend**: `http://localhost:3000` (usually)
  - Login: `http://localhost:3000/auth/login`
  - Signup: `http://localhost:3000/auth/signup`
  - Dashboard: `http://localhost:3000/dashboard`

## Better Auth Integration

The frontend now uses Better Auth for authentication instead of the previous custom auth system. The backend API expects JWT tokens in the Authorization header for protected endpoints.

## Troubleshooting

1. **Port already in use**: If you get port binding errors, make sure no other instances are running.

2. **Dependency issues**: Make sure you've installed all dependencies for both backend and frontend.

3. **Environment variables**: Ensure your `.env` files are properly configured in both directories.

4. **Cross-origin issues**: The backend is configured to allow requests from `http://localhost:3000` by default.

## Stopping the Servers

To stop either server, go to its respective command prompt/terminal and press `Ctrl+C`.