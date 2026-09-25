#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    # Automatically switch to venv python if not currently using it
    venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv", "bin", "python3")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        print(f"[*] Switching to virtual environment Python...")
        os.execl(venv_python, venv_python, *sys.argv)

    print("=" * 60)
    print("🚀 CYBERTRACE BACKEND STARTING 🚀")
    print("=" * 60)
    print("Architecture has been upgraded from Streamlit to FastAPI + React.")
    print("\n[STEP 1] This terminal is now running the Backend Capture Engine.")
    print("[STEP 2] To view the User Interface, open a NEW terminal and run:")
    print("         cd frontend")
    print("         npm run dev")
    print("=" * 60)
    
    try:
        import uvicorn
        # Run the FastAPI app programmatically
        uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\nShutting down CyberTrace Backend...")
    except ImportError:
        print("\nError: uvicorn not found. Did you run 'pip install -r requirements.txt'?")
        sys.exit(1)
    except Exception as e:
        print(f"\nError starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
