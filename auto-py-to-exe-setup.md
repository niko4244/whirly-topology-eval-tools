# How to Build Your .exe in 2 Minutes

1. **Install auto-py-to-exe**  
   Open a command prompt and run:
   ```
   pip install auto-py-to-exe
   auto-py-to-exe
   ```
2. **In the GUI:**
   - Script Location: select `start_app.py`
   - Onefile: ✔️
   - Console: ✔️ (or Windowed if you want no console)
   - Add Data:  
     - `frontend/templates;frontend/templates`
     - `api;api`
     - `knowledge;knowledge`
     - Any other folders your app needs
   - Advanced > Hidden Imports:  
     - `flask`, `fastapi`, `requests`, `uvicorn`, `jinja2`
   - Output folder: select where you want the `.exe`

3. Click **Convert .py to .exe**

**Your .exe will appear in the output folder, ready for use!**