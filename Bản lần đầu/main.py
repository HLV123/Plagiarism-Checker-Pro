# main.py
"""
File chính để chạy Plagiarism Checker GUI
"""

import sys
import os
from tkinter import messagebox

def check_requirements():
    """Kiểm tra các thư viện cần thiết"""
    required_packages = ['requests', 'tkinter']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Thiếu các thư viện sau:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n📦 Cài đặt bằng lệnh:")
        print("pip install requests")
        return False
    
    return True

def check_config():
    """Kiểm tra cấu hình API"""
    try:
        from config import API_KEY, SEARCH_ENGINE_ID
        
        if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:
            print("❌ Chưa cấu hình API_KEY trong file config.py")
            return False
            
        if not SEARCH_ENGINE_ID:
            print("❌ Chưa cấu hình SEARCH_ENGINE_ID trong file config.py")
            return False
            
        return True
        
    except ImportError:
        print("❌ Không tìm thấy file config.py")
        return False

def main():
    """Hàm main để khởi chạy ứng dụng"""
    print("🚀 KHỞI ĐỘNG PLAGIARISM CHECKER")
    print("="*50)
    
    # Kiểm tra requirements
    if not check_requirements():
        print("\n❌ Vui lòng cài đặt các thư viện cần thiết trước khi chạy!")
        input("Nhấn Enter để thoát...")
        return
    
    # Kiểm tra config
    if not check_config():
        print("\n❌ Vui lòng cấu hình API key trong file config.py!")
        input("Nhấn Enter để thoát...")
        return
    
    print("✅ Tất cả kiểm tra đều OK!")
    print("🔄 Đang khởi động GUI...")
    
    try:
        from gui import PlagiarismGUI
        
        # Khởi tạo và chạy GUI
        app = PlagiarismGUI()
        print("✅ GUI đã khởi động thành công!")
        app.run()
        
    except Exception as e:
        print(f"❌ Lỗi khi khởi động GUI: {e}")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()