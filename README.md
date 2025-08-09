# WHIRLY

**WHIRLY** is a brand-filtered, gamified tech sheet system for Whirlpool, Maytag, KitchenAid, and Jenn-Air.  
Technician/admin dashboards, secure CSV reports, achievements, and feedback.  
Built with Python (Flask+FastAPI) and ready for installer packaging.

## Features
- Brand-filtered tech sheet upload
- Achievements and badge events
- Leaderboard
- Feedback and analytics
- Admin dashboard with secure CSV download
- Authentication (technician/admin roles)
- One-click installer for Windows

## How to Run (Developer Mode)
1. Install Python 3.9+
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the app:
   ```
   python start_app.py
   ```
   Your browser will open to the dashboard.

## How to Build Standalone EXE
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Build the executable:
   ```
   pyinstaller --onefile --add-data "frontend/templates;frontend/templates" start_app.py
   ```
   The output will be in `dist/WHIRLY.exe`

## How to Build the Installer (Windows)
1. Download and install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Use the provided `installer.iss` script
3. Build `WHIRLYSetup.exe`—your users can install with one click!

## Uninstall
Remove via Control Panel > Programs > Uninstall "WHIRLY"

## Branding
Includes a retro 1950s-style Whirlpool logo (`assets/logo_whirlpool_50s.png`) for use in installer and dashboard.

## License
Copyright 2025 niko4244. All rights reserved.