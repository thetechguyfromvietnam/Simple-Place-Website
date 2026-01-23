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

def close_modal(driver, timeout=10):
    """Tự động đóng modal sau khi upload xong.
    Thử các cách: tìm nút Đóng/X, hoặc click vào overlay để đóng.
    """
    print("🔒 Đang đóng modal...")
    time.sleep(1)  # Đợi một chút để modal xuất hiện hoàn toàn
    
    # Danh sách các selector để tìm nút Đóng/X (ưu tiên data-dismiss="modal")
    close_selectors = [
        # Icon X trong modal-header (ưu tiên nhất - từ HTML được cung cấp)
        (By.XPATH, "//i[contains(@class, 'fa-times') and @data-dismiss='modal']"),
        (By.CSS_SELECTOR, "i.fa-times[data-dismiss='modal']"),
        # Nút Đóng trong modal-footer (ưu tiên thứ hai)
        (By.XPATH, "//button[@data-dismiss='modal' and contains(text(), 'Đóng')]"),
        (By.XPATH, "//div[@class='modal-footer']//button[@data-dismiss='modal']"),
        # Bootstrap modal close button
        (By.XPATH, "//button[@data-dismiss='modal']"),
        # SweetAlert2 close button
        (By.CSS_SELECTOR, ".swal2-close"),
        (By.CSS_SELECTOR, "button.swal2-close"),
        # Nút Đóng thông thường
        (By.XPATH, "//button[contains(@class, 'btn-default') and contains(text(), 'Đóng')]"),
        (By.XPATH, "//button[contains(text(), 'Đóng')]"),
        (By.XPATH, "//button[contains(@class, 'close')]"),
        (By.XPATH, "//span[contains(@class, 'close')]"),
        # Icon X khác
        (By.XPATH, "//*[contains(@class, 'fa-times')]"),
        (By.XPATH, "//*[contains(@class, 'fa-close')]"),
        (By.XPATH, "//button[@aria-label='Close']"),
        (By.XPATH, "//span[@aria-label='Close']"),
    ]
    
    # Thử tìm và click nút Đóng/X
    for by, selector in close_selectors:
        try:
            element = driver.find_element(by, selector)
            if element and element.is_displayed():
                element.click()
                print("✓ Đã click nút Đóng/X để đóng modal")
                time.sleep(0.5)  # Đợi modal đóng
                return True
        except Exception:
            continue
    
    # Nếu không tìm thấy nút Đóng, thử click vào overlay/backdrop để đóng modal
    overlay_selectors = [
        (By.CSS_SELECTOR, ".swal2-overlay"),
        (By.CSS_SELECTOR, ".modal-backdrop"),
        (By.CSS_SELECTOR, ".modal-overlay"),
        (By.CSS_SELECTOR, "[class*='overlay']"),
        (By.XPATH, "//div[contains(@class, 'overlay')]"),
    ]
    
    print("ℹ️  Không tìm thấy nút Đóng, thử click vào overlay...")
    for by, selector in overlay_selectors:
        try:
            element = driver.find_element(by, selector)
            if element and element.is_displayed():
                # Click vào overlay để đóng modal
                driver.execute_script("arguments[0].click();", element)
                print("✓ Đã click vào overlay để đóng modal")
                time.sleep(0.5)  # Đợi modal đóng
                return True
        except Exception:
            continue
    
    # Fallback: Thử ESC key
    try:
        from selenium.webdriver.common.keys import Keys
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        print("✓ Đã nhấn ESC để đóng modal")
        time.sleep(0.5)
        return True
    except Exception:
        pass
    
    print("⚠️  Không thể đóng modal tự động, nhưng sẽ tiếp tục...")
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
    
    # Reset trạng thái pressed của nút "Upload file excel" ngay lập tức (không delay)
    try:
        # Tìm và reset nút upload file excel bằng JavaScript (nhanh nhất)
        driver.execute_script("""
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var btn = buttons[i];
                if (btn.textContent && btn.textContent.includes('Upload file excel')) {
                    btn.blur();
                    btn.classList.remove('active', 'pressed', 'focus', 'btn-active');
                    btn.removeAttribute('aria-pressed');
                    break;
                }
            }
        """)
        print("✓ Đã reset trạng thái nút Upload file excel")
    except Exception as e:
        print(f"⚠️  Không thể reset trạng thái nút: {e}")
    
    # Click vào input field để blur nút (không delay)
    try:
        name_input = driver.find_element(By.ID, "txtFullname")
        driver.execute_script("arguments[0].click();", name_input)
    except Exception:
        pass
    
    # Đợi modal đóng tự động (giảm thời gian đợi)
    time.sleep(0.5)  # Giảm từ 1 giây xuống 0.5 giây
    
    # Kiểm tra xem modal có còn mở không, nếu có thì mới đóng
    try:
        # Kiểm tra xem có modal nào còn hiển thị không
        modal_elements = driver.find_elements(By.CSS_SELECTOR, ".swal2-show, .modal.show, .modal.in")
        if modal_elements:
            # Nếu modal vẫn còn mở, mới gọi close_modal
            close_modal(driver)
        else:
            print("✓ Modal đã đóng tự động")
    except Exception:
        # Nếu không kiểm tra được, đợi thêm một chút rồi tiếp tục
        time.sleep(0.5)
    
    # Click nút "Đóng" trong modal (tìm bất kỳ nút nào có text "Đóng")
    print("🔒 Đang tìm và click nút Đóng trong modal...")
    close_btn = False
    try:
        # Tìm tất cả các nút có text "Đóng" trong modal
        close_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Đóng')]")
        for btn in close_buttons:
            if btn.is_displayed():
                btn.click()
                print("✓ Đã click nút Đóng")
                close_btn = True
                time.sleep(0.5)  # Đợi modal đóng hoàn toàn
                break
    except Exception as e:
        print(f"⚠️  Không tìm thấy nút Đóng: {e}")
    
    if not close_btn:
        print("⚠️  Không tìm thấy nút Đóng, có thể modal đã đóng")
    
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

