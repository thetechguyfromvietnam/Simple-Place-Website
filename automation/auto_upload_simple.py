#!/usr/bin/env python3
"""
SIMPLE AUTO UPLOAD SCRIPT
=========================
Tự động hóa upload hóa đơn lên website https://ehd.smartsign.com.vn/

Flow:
1. Mở website, đợi user đăng nhập thủ công (10 giây)
2. Click "Quản lý hóa đơn" → "Tạo hóa đơn"
3. Điền thông tin khách hàng (3 trường)
4. Click "Upload file excel" → Modal mở → Upload file → Click "Đồng ý" → Click icon X
5. Click "Lưu lại"
6. Lặp lại cho tất cả files

Sử dụng:
    python3 auto_upload_simple.py
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import platform
import subprocess

# Resolve project root for shared directories
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent

# ============================================================================
# CẤU HÌNH
# ============================================================================

WEBSITE_URL = "https://ehd.smartsign.com.vn/"
INVOICE_DIR = PROJECT_ROOT / "tax_files"

# Thông tin khách hàng mặc định (điền vào 3 trường bắt buộc)
# - Họ tên người mua hàng (Buyer's name)
CUSTOMER_FULLNAME = "Khách Hàng Không Cung Cấp Thông Tin"
# - Tên đơn vị (Company)
CUSTOMER_COMPANY = "Khách Hàng Không Cung Cấp Thông Tin"
# - Địa chỉ (Address)
CUSTOMER_ADDRESS = "Khách Hàng Không Cung Cấp Thông Tin"

# ============================================================================
# SETUP
# ============================================================================

def setup_driver():
    """Setup Chrome với options tối ưu"""
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# ============================================================================
# MAIN ACTIONS
# ============================================================================

def wait_and_find(driver, by, value, timeout=20, description=""):
    """Tìm element và chờ nó xuất hiện"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        if description:
            print(f"✓ Tìm thấy: {description}")
        return element
    except Exception as e:
        print(f"❌ Không tìm thấy: {description or value} - {e}")
        return None

def wait_and_click(driver, by, value, timeout=20, description=""):
    """Click vào element"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        if description:
            print(f"✓ Clicked: {description}")
        return True
    except Exception as e:
        print(f"❌ Không click được: {description or value} - {e}")
        return False

def wait_and_input(driver, by, value, text, timeout=20, description=""):
    """Nhập text vào element"""
    try:
        element = wait_and_find(driver, by, value, timeout, description)
        if element:
            element.clear()
            element.send_keys(text)
            if description:
                print(f"✓ Nhập text: {description}")
            return True
        return False
    except Exception as e:
        print(f"❌ Không nhập được: {description or value} - {e}")
        return False

# ============================================================================
# LOGIN
# ============================================================================

def login(driver):
    """Đăng nhập vào website (thủ công)"""
    print("\n🔐 Bước 1: Đăng nhập...")
    
    driver.get(WEBSITE_URL)
    print(f"✓ Đã mở: {WEBSITE_URL}")
    
    # Đợi user đăng nhập thủ công
    print("⏳ Vui lòng đăng nhập thủ công...")
    print("✓ Đã đợi đăng nhập xong")
    return True

# ============================================================================
# UPLOAD INVOICE
# ============================================================================

def upload_one_invoice(driver, file_path):
    """Upload một file hóa đơn"""
    print(f"\n📄 Uploading: {file_path.name}")
    
    # Step 1: Click vào dropdown "Quản lý hóa đơn"
    menu_dropdown = wait_and_click(driver, By.XPATH, "//a[contains(@class, 'dropdown-toggle') and contains(text(), 'Quản lý hóa đơn')]", description="Quản lý hóa đơn dropdown")
    
    # Step 2: Click "Tạo hóa đơn" trong dropdown
    new_invoice_btn = wait_and_click(driver, By.XPATH, "//a[text()='Tạo hóa đơn']", description="New invoice button")
    
    # Step 3: Điền thông tin khách hàng (3 trường bắt buộc)
    print("📝 Điền thông tin khách hàng...")
    
    # Điền Họ tên người mua hàng (Buyer's name)
    wait_and_input(driver, By.ID, "txtFullname", CUSTOMER_FULLNAME, description="Họ tên người mua hàng")
    
    # Điền Tên đơn vị (Company)
    wait_and_input(driver, By.ID, "txtCompanyName", CUSTOMER_COMPANY, description="Tên đơn vị")
    
    # Điền Địa chỉ (Address)
    wait_and_input(driver, By.ID, "txtAddress", CUSTOMER_ADDRESS, description="Địa chỉ")
    
    # Step 4: Click button "Upload file excel" để mở modal
    upload_btn = wait_and_click(driver, By.XPATH, "//button[contains(text(), 'Upload file excel')]", description="Upload file excel button")
    if not upload_btn:
        print("⚠️  Không tìm thấy button Upload file excel")
        return False
    
    absolute_file_path = file_path.resolve()
    print(f"📂 Đường dẫn file: {absolute_file_path}")
    
    # Tìm file input trong modal (có thể là #fileUploader hoặc input type="file")
    file_input = wait_and_find(driver, By.ID, "fileUploader", description="File input #fileUploader")
    if file_input:
        file_input.send_keys(str(absolute_file_path))
        print(f"✓ Uploaded: {file_path.name}")
    else:
        # Fallback: Tìm file input khác
        file_input = wait_and_find(driver, By.XPATH, "//input[@type='file']", description="File input")
        if file_input:
            file_input.send_keys(str(absolute_file_path))
            print(f"✓ Uploaded: {file_path.name}")
        else:
            print("⚠️  Không tìm thấy input file upload")
            return False
    
    # Click button "Đồng ý" trong modal để xác nhận upload
    confirm_btn = wait_and_click(driver, By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'Đồng ý')]", description="Đồng ý button")
    if not confirm_btn:
        # Fallback: thử tìm button "Đồng ý" khác
        confirm_btn = wait_and_click(driver, By.XPATH, "//button[text()='Đồng ý']", description="Đồng ý button")
    
    if confirm_btn:
        print("✓ Đã xác nhận upload")
    
    # Đợi user tự ấn nút "Đóng"
    print("\n👉 Vui lòng tự ấn nút 'Đóng' trong modal...")
    
    # Step 5: Tự động click "Lưu lại" button
    save_button = wait_and_click(driver, By.ID, "btnSave", description="Lưu lại button")
    if not save_button:
        # Fallback: thử các selectors khác
        save_selectors = [
            ("By.XPATH", "//input[@value='Lưu lại']"),
            ("By.XPATH", "//button[contains(text(), 'Lưu lại')]"),
        ]
        
        for selector_type, selector_value in save_selectors:
            if selector_type == "By.XPATH":
                save_button = wait_and_click(driver, By.XPATH, selector_value, description="Lưu lại")
            
            if save_button:
                break
    
    if not save_button:
        print("⚠️  Không tìm thấy button Lưu lại")
        return False
    
    print("✓ Đã click Lưu lại")
    
    # Click button "Đồng ý" sau khi lưu lại
    confirm_after_save = wait_and_click(driver, By.XPATH, "//button[contains(@class, 'swal2-confirm') and contains(text(), 'Đồng ý')]", description="Đồng ý button sau khi lưu")
    if not confirm_after_save:
        # Fallback: thử tìm button "Đồng ý" khác
        confirm_after_save = wait_and_click(driver, By.XPATH, "//button[text()='Đồng ý']", description="Đồng ý button")
    
    if confirm_after_save:
        print("✓ Đã click Đồng ý sau khi lưu")
    
    return True

def upload_all_invoices(driver):
    """Upload tất cả files"""
    if not INVOICE_DIR.exists():
        print(f"❌ Không tìm thấy folder: {INVOICE_DIR}")
        return
    
    files = sorted(INVOICE_DIR.glob("*.xlsx"), key=lambda x: x.name)
    if not files:
        print(f"❌ Không tìm thấy file .xlsx nào trong {INVOICE_DIR}")
        return
    
    print(f"\n📁 Tìm thấy {len(files)} file(s)")
    print("📋 Thứ tự upload:")
    for i, file_path in enumerate(files, 1):
        print(f"   {i}. {file_path.name}")
    
    # Login một lần
    if not login(driver):
        print("❌ Không thể đăng nhập")
        return
    
    # Upload từng file
    for i, file_path in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] Processing...")
        if upload_one_invoice(driver, file_path):
            print(f"✅ Thành công: {file_path.name}")
        else:
            print(f"❌ Thất bại: {file_path.name}")
    
    print("\n✅ Hoàn thành upload tất cả files!")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main function"""
    print("="*70)
    print("🤖 SIMPLE AUTO UPLOAD")
    print("="*70)
    
    # Check files
    if not INVOICE_DIR.exists():
        print(f"\n❌ Không tìm thấy folder: {INVOICE_DIR}")
        print("   Chạy process_invoices.py trước để tạo files")
        return
    
    files = sorted(INVOICE_DIR.glob("*.xlsx"), key=lambda x: x.name)
    if not files:
        print(f"\n❌ Không tìm thấy file .xlsx trong {INVOICE_DIR}")
        return
    
    print(f"\n📁 Sẵn sàng upload {len(files)} file(s) theo thứ tự")
    
    driver = None
    try:
        driver = setup_driver()
        upload_all_invoices(driver)
    except KeyboardInterrupt:
        print("\n⚠️  Đã dừng")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

