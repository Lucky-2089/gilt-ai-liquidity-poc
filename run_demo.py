import subprocess
import sys
import webbrowser
import time
import threading
import os
from importlib import import_module


def install_dependencies():
    """Install required Python packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")


def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = ['fastapi', 'uvicorn', 'pydantic', 'sklearn', 'pandas', 'numpy']
    missing = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    return missing


def start_server():
    """Start the FastAPI server"""
    print("Starting AI Liquidity Provider API server...")

    # Add the backend directory to Python path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

    try:
        from app import app
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure app.py is in the backend folder")
    except Exception as e:
        print(f"Error starting server: {e}")


def open_browser():
    """Open the browser after a short delay"""
    time.sleep(3)
    webbrowser.open("http://localhost:8000")
    print("Demo page opened in browser at http://localhost:8000")


if __name__ == "__main__":
    print("=== AI Liquidity Provider Demo ===")

    # Check for missing dependencies
    missing = check_dependencies()
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Installing dependencies...")
        install_dependencies()

    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    # Start the server
    start_server()