import sys
import os
import traceback
from tkinter import messagebox
import tkinter as tk

def check_python_version():
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_required_modules():
    required_modules = {
        'tkinter': 'tkinter',
        'requests': 'requests',
        'typing': 'typing',
        'threading': 'threading',
        'time': 'time',
        'json': 'json',
        'webbrowser': 'webbrowser'
    }
    
    missing_modules = []
    
    for module_name, import_name in required_modules.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_modules.append(module_name)
    
    if missing_modules:
        print("❌ Missing required modules:")
        for module in missing_modules:
            print(f"   • {module}")
        print("\n📦 Install missing modules with:")
        print("pip install requests")
        return False
    
    return True

def check_configuration():
    try:
        from config import API_KEY, SEARCH_ENGINE_ID, BASE_URL
        
        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            print("❌ API_KEY not configured in config.py")
            return False
            
        if not SEARCH_ENGINE_ID:
            print("❌ SEARCH_ENGINE_ID not configured in config.py")
            return False
            
        if not BASE_URL:
            print("❌ BASE_URL not configured in config.py")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected configuration error: {e}")
        return False

def check_file_structure():
    required_files = [
        'config.py',
        'api.py', 
        'analyzer.py',
        'checker.py',
        'gui.py'
    ]
    
    missing_files = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_name in required_files:
        file_path = os.path.join(current_dir, file_name)
        if not os.path.exists(file_path):
            missing_files.append(file_name)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_name in missing_files:
            print(f"   • {file_name}")
        return False
    
    return True

def test_api_connection():
    try:
        from api import GoogleSearchAPI
        
        print("🔍 Testing API connection...")
        api = GoogleSearchAPI()
        
        if api.test_connection():
            print("✅ API connection successful!")
            return True
        else:
            print("❌ API connection failed!")
            print("   Please check your API key and internet connection")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def run_system_checks():
    print("🚀 PLAGIARISM CHECKER PRO - SYSTEM CHECK")
    print("=" * 55)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Modules", check_required_modules),
        ("File Structure", check_file_structure),
        ("Configuration", check_configuration),
        ("API Connection", test_api_connection)
    ]
    
    all_passed = True
    
    for check_name, check_function in checks:
        print(f"\n🔧 {check_name}...")
        try:
            if not check_function():
                all_passed = False
                print(f"❌ {check_name} check failed!")
            else:
                print(f"✅ {check_name} check passed!")
        except Exception as e:
            print(f"❌ {check_name} check error: {e}")
            all_passed = False
    
    return all_passed

def show_startup_error(message):
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Startup Error", message)
        root.destroy()
    except:
        print(f"❌ STARTUP ERROR: {message}")

def main():
    try:
        if not run_system_checks():
            error_msg = ("System checks failed!\n\n"
                        "Please check the console output for details and fix any issues before running the application.\n\n"
                        "Common solutions:\n"
                        "• Install missing modules: pip install requests\n"
                        "• Configure API keys in config.py\n"
                        "• Check internet connection")
            show_startup_error(error_msg)
            input("\nPress Enter to exit...")
            return
        
        print("\n🎉 All system checks passed!")
        print("🚀 Starting Plagiarism Checker Pro...")
        print("=" * 40)
        
        from gui import ModernPlagiarismGUI
        
        app = ModernPlagiarismGUI()
        
        print("✅ Application started successfully!")
        print("💡 Close this console window will also close the application")
        
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        
    except ImportError as e:
        error_msg = f"Import Error: {e}\n\nMake sure all required files are present and dependencies are installed."
        show_startup_error(error_msg)
        print(f"❌ Import Error: {e}")
        
    except Exception as e:
        error_msg = f"Unexpected Error: {e}\n\nPlease check the console for more details."
        show_startup_error(error_msg)
        print(f"❌ Unexpected error: {e}")
        print("\n📋 Full error trace:")
        traceback.print_exc()
        
    finally:
        print("\n👋 Thank you for using Plagiarism Checker Pro!")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()