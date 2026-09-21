# FMECA Platform Manual Startup Guide

This guide will help you start the FMECA platform on your own when you reopen the program.

## Two Startup Methods

### Method 1: Use Simple Startup Script (Recommended)

I've created a simple startup script that avoids encoding issues:

#### Steps:
1. Find the file `start_platform_simple.bat` in the platform directory
2. Double-click this file to run it
3. The script will:
   - Check Python and Node.js environments
   - Start backend service automatically
   - Build and start frontend service automatically
4. When you see "Services started successfully!", the platform is ready

### Method 2: Manual Startup (Step-by-Step)

If the script doesn't work, you can start services manually:

#### Step 1: Start Backend Service

1. **Open Command Prompt**: Press `Win + R` → type `cmd` → press Enter
2. **Navigate to backend directory**: Type the following command and press Enter:
   ```
   cd c:\FMECA platform test\backend
   ```
3. **Start backend server**: Type the following command and press Enter:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```
4. **Verify backend is running**: You should see:
   ```
   Starting development server at http://0.0.0.0:8000/
   ```

#### Step 2: Build and Deploy Frontend

1. **Open another Command Prompt**: Press `Win + R` → type `cmd` → press Enter
2. **Navigate to frontend directory**: Type the following command and press Enter:
   ```
   cd c:\FMECA platform test\frontend
   ```
3. **Build frontend**: Type the following command and press Enter:
   ```
   npm run build
   ```
4. **Wait for build to complete**: This may take 1-2 minutes
5. **Copy built files to backend**: Type the following command and press Enter:
   ```
   xcopy /E /Y "c:\FMECA platform test\frontend\dist" "c:\FMECA platform test\backend\static\dist"
   ```

## Access the Platform

After completing either method:
- Open your browser
- Visit: http://localhost:8000

## Verify Startup Success

### Check Backend Service
1. Open Command Prompt
2. Type the following command and press Enter:
   ```
   curl -I http://localhost:8000
   ```
3. You should see a response with `HTTP/1.1 200 OK`

### Check Static Resources
1. Open Command Prompt
2. Type the following command and press Enter:
   ```
   curl -I http://localhost:8000/assets/index-5ebaaa76.css
   ```
3. You should see a response with `HTTP/1.1 200 OK`

## Troubleshooting

### If backend fails to start:
- Check if Python is installed: `python --version`
- Check if backend directory exists: `cd c:\FMECA platform test\backend`
- Look for error messages in the Command Prompt

### If frontend build fails:
- Check if Node.js is installed: `npm --version`
- Check if frontend directory exists: `cd c:\FMECA platform test\frontend`
- Try running `npm install` first, then `npm run build`

### If platform doesn't load in browser:
- Check if backend server is still running
- Refresh the browser
- Clear browser cache and try again

## Shutdown Instructions

### To stop backend service:
1. Go to the backend Command Prompt
2. Press `Ctrl + Break` or `Ctrl + C`

### To clean up:
You don't need to do anything special. The next time you start the platform, any changes will be automatically handled.

## Important Notes

- Keep the backend Command Prompt open while using the platform
- If you close the backend window, the platform will stop working
- The first startup may take longer as it builds the frontend
- Subsequent startups will be faster as the build is already done
