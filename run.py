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
    print(f"Starting EVOLUTION TRACKER 2.0 Backend...")
    print(f"Project root: {ROOT_DIR}")
    print(f"Listening at: http://127.0.0.1:8000")
    print(f"API Documentation: http://127.0.0.1:8000/docs")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
