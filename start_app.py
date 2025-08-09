import os
import threading
import webbrowser
from threading import Timer

def run_backend():
    os.system("uvicorn api.brand_report_api:app --port 8000")

def run_frontend():
    def open_browser():
        webbrowser.open("http://localhost:5000")
    Timer(1.5, open_browser).start()
    os.system("flask run --port 5000")

if __name__ == "__main__":
    threading.Thread(target=run_backend, daemon=True).start()
    run_frontend()