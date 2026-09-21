# FMECA Platform Startup Troubleshooting Guide

## Issue: Window closes without showing "Services started successfully!"

If the startup window closes immediately without showing the success message, it means there was an error during the startup process.

## Solution 1: Use the Simple English Version (Recommended)

I've created a simpler version of the startup script that avoids Chinese character encoding issues:

### Steps:
1. Find the file named `start_platform_simple.bat` in the platform directory
2. Double-click this file instead of the original one
3. The window will stay open showing detailed error messages if any issues occur

## Solution 2: Manual Startup (Most Reliable)

If the script still doesn't work, you can start the services manually:

### Step 1: Start Backend Service

1. Press **Win + R** to open the Run dialog
2. Type `cmd` and press Enter to open Command Prompt
3. Enter the following commands one by one:
   ```
   cd c:\FMECA platform test\backend
   python manage.py runserver 0.0.0.0:8000
   ```
4. A window will open showing the backend service is running

### Step 2: Start Frontend Service

1. Press **Win + R** again to open another Run dialog
2. Type `cmd` and press Enter to open another Command Prompt
3. Enter the following commands one by one:
   ```
   cd c:\FMECA platform test\frontend
   npm run dev
   ```
4. A window will open showing the frontend service is running

### Step 3: Access the Platform

After both services are running:
- Open your browser
- Visit: http://localhost:3000

## Common Error Messages and Solutions

### Error 1: "Python not found"

**Problem**: Python is not installed or not in the system PATH

**Solution**:
1. Download and install Python 3.8+ from https://www.python.org/downloads/
2. During installation, make sure to check "Add Python to PATH"
3. Restart your computer and try again

### Error 2: "Node.js not found"

**Problem**: Node.js is not installed or not in the system PATH

**Solution**:
1. Download and install Node.js 16+ from https://nodejs.org/en/download/
2. Restart your computer and try again

### Error 3: "Directory not found"

**Problem**: The script cannot find the backend or frontend directory

**Solution**:
1. Make sure you're running the script from the correct location
2. Verify the backend and frontend directories exist in the platform folder

### Error 4: "npm run dev failed"

**Problem**: Frontend dependencies may not be installed

**Solution**:
1. Open Command Prompt
2. Navigate to the frontend directory: `cd c:\FMECA platform test\frontend`
3. Install dependencies: `npm install`
4. Wait for installation to complete, then try `npm run dev` again

## How to See Detailed Error Messages

1. Right-click on the script file
2. Select "Edit"
3. This will open the script in Notepad
4. Look for the error handling sections
5. Make sure each error condition has a `pause` command

## Contact Support

If you've tried all these solutions and still have issues, please:
1. Take a screenshot of any error messages
2. Note which step you were at when the error occurred
3. Contact the technical support team
