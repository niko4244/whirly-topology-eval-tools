import requests

def check_backend_health(url="http://localhost:8000/health"):
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200 and resp.json().get("status") == "ok":
            print("Backend healthy.")
            return True
        else:
            print("Backend unhealthy:", resp.text)
            return False
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    check_backend_health()