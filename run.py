import os
import sys

# Ensure project root directory is always the first entry in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Set PYTHONPATH environment variable for uvicorn reloader subprocesses
os.environ["PYTHONPATH"] = ROOT_DIR + os.pathsep + os.environ.get("PYTHONPATH", "")

if __name__ == "__main__":
    import uvicorn
    import socket
    from backend.app.config import settings

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    local_ip = get_local_ip()
    host = settings.HOST or "0.0.0.0"
    port = settings.PORT or 8000

    print("===================================================")
    print("  EVOLUTION TRACKER 2.0 - VISION X BACKEND SERVER")
    print("  VERIFY BEFORE YOU SHARE")
    print("===================================================")
    print(f"Project root   : {ROOT_DIR}")
    print(f"Local Host     : http://localhost:{port}")
    print(f"Network (LAN)  : http://{local_ip}:{port}")
    print(f"API Docs (LAN) : http://{local_ip}:{port}/docs")
    print("---------------------------------------------------")
    print(f"Access Web App from any device on the same Wi-Fi:")
    print(f"👉 http://{local_ip}:5173")
    print("===================================================")

    uvicorn.run("backend.app.main:app", host=host, port=port, reload=True)
