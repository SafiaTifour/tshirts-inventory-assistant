import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import streamlit
        import langchain
        import faiss
        import sentence_transformers
        import pandas
        import yaml
        print("✅ All required packages are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {str(e)}")
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully.")
            return True
        except Exception as e:
            print(f"❌ Failed to install requirements: {str(e)}")
            return False

def check_config():
    """Check if config file exists"""
    if not os.path.exists(os.path.join("config", "config.yaml")):
        print("❌ Config file not found. Please create config/config.yaml based on the example.")
        return False
    print("✅ Config file found.")
    return True

def run_app():
    """Run the Streamlit app"""
    try:
        print("Starting AtliQ T-Shirts SQL Assistant...")
        subprocess.check_call([sys.executable, "-m", "streamlit", "run", "main.py"])
        return True
    except Exception as e:
        print(f"❌ Failed to start app: {str(e)}")
        return False

if __name__ == "__main__":
    print("AtliQ T-Shirts SQL Assistant Setup")
    print("==================================")
    
    if check_requirements() and check_config():
        run_app()
    else:
        print("\nPlease fix the issues above and try again.")