#!/usr/bin/env python3
import sys
import subprocess
import os

def main():
    print("Starting CyberTrace Dashboard...")
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard", "app.py")
    
    try:
        subprocess.run(["streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nShutting down CyberTrace...")
    except Exception as e:
        print(f"Error starting dashboard: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
