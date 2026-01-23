#!/usr/bin/env python3
"""
Automate Fabi report navigation
===============================

This helper uses Selenium to:
1. Log into https://fabi.ipos.vn/ with the supplied credentials
2. Dismiss the license reminder popup (if present)
3. Open the Báo cáo section
4. Expand the "Báo cáo phân tích - B" accordion
5. Open report B07 - Phương thức thanh toán
6. (Optional) Click the "Transfer" filter if it exists on the page

Usage:
    python3 auto_fetch_fabi.py --username <email> --password <password>

Environment variables (fallbacks):
    FABI_USERNAME
    FABI_PASSWORD

Flags:
    --headless          Run Chrome in headless mode (disabled by default because
                        Fabi blocks standard headless fingerprints).
    --no-click-transfer Skip the attempt to click the transfer filter.

Note:
    - webdriver-manager caches the ChromeDriver binary inside ./.wdm/
    - If the site changes CSS selectors, update the XPaths below.
"""

import argparse
import os
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Ensure webdriver cache lives inside the project folder
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
DOWNLOAD_DIR = PROJECT_ROOT / "data"

DOWNLOAD_DIR.mkdir(exist_ok=True)
os.environ.setdefault("WDM_LOCAL", "1")
os.environ.setdefault("WDM_LOG_LEVEL", "0")

LOGIN_URL = "https://fabi.ipos.vn/login"
DEFAULT_USERNAME = "tranmy077@gmail.com"
DEFAULT_PASSWORD = "nguyenvanhuong99@"

# Selectors
EMAIL_INPUT = (By.NAME, "email_input")
PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "button.btn-primary")
REPORT_TILE = (
    By.XPATH,
    "//div[contains(@class,'list-menu-item__icon') and contains(@class,'cursor-pointer')]//img[@alt='Báo cáo']/..",
)
REPORT_TEXT_TILE = (
    By.XPATH,
    "//p[contains(@class,'menu-label') and normalize-space()='Báo cáo'] | //*[contains(text(),'Báo cáo') and contains(@class,'menu')]",
)
REPORT_IMG_DIRECT = (
    By.XPATH,
    "//div[contains(@class,'list-menu-item__icon')]//img[@alt='Báo cáo' and contains(@class,'icon')]",
)
REPORT_DIV_WRAPPER = (
    By.XPATH,
    "//div[contains(@class,'list-menu-item__icon') and contains(@class,'cursor-pointer') and .//img[@alt='Báo cáo']]",
)
ANALYSIS_ACCORDION = (
    By.XPATH,
    "//div[@data-toggle='collapse' and @data-target='#collapse-menu-1' and contains(@class,'menu-item')]",
)
ANALYSIS_ACCORDION_BY_SPAN = (
    By.XPATH,
    "//span[normalize-space()='Báo cáo phân tích - B']/ancestor::div[@data-toggle='collapse' and @data-target='#collapse-menu-1' and contains(@class,'menu-item')]",
)
ANALYSIS_ACCORDION_TEXT = (
    By.XPATH,
    "//div[contains(@class,'menu-item__title') and .//span[normalize-space()='Báo cáo phân tích - B']]/ancestor::div[@data-toggle='collapse']",
)
ANALYSIS_ACCORDION_BY_TITLE = (
    By.XPATH,
    "//span[text()='Báo cáo phân tích - B']/ancestor::div[contains(@class,'menu-item') and @data-toggle='collapse']",
)
B07_LINK = (
    By.XPATH,
    "//a[contains(., 'B07 - Phương thức thanh toán')]",
)
TRANSFER_FILTER = (
    By.XPATH,
    "//tr[.//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'transfer')]]",
)
TRANSFER_TD = (
    By.XPATH,
    "//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'transfer')]",
)
# More specific selector based on HTML structure: row with TRANSFER text in second td
TRANSFER_ROW_SPECIFIC = (
    By.XPATH,
    "//tr[td[@scope='row']/span[text()='2']][td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'transfer')]]",
)
TRANSFER_FILTER_FALLBACK = (
    By.XPATH,
    "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'transfer') "
    "or contains(., 'Chuyển khoản')]",
)
ATM_FILTER = (
    By.XPATH,
    "//tr[.//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'atm')]]",
)
ATM_TD = (
    By.XPATH,
    "//td[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'atm')]",
)
ATM_FILTER_FALLBACK = (
    By.XPATH,
    "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'atm')]",
)
EXPORT_BUTTON = (
    By.XPATH,
    "//div[contains(@class,'modal-footer')]//button[contains(@class,'btn-outline-blue') and contains(., 'Xuất hoá đơn')]",
)
EXPORT_BUTTON_BY_MODAL = (
    By.XPATH,
    "//div[@class='modal-footer']//button[.//i[contains(@class,'fa-download')] and contains(., 'Xuất hoá đơn')]",
)
EXPORT_BUTTON_BY_ICON = (
    By.XPATH,
    "//button[.//i[contains(@class,'fa-download')] and contains(., 'Xuất hoá đơn')]",
)
EXPORT_BUTTON_FALLBACK = (
    By.XPATH,
    "//button[contains(@class,'btn-outline-blue') and contains(., 'Xuất hoá đơn')]",
)
EXPORT_BUTTON_GENERIC = (
    By.XPATH,
    "//*[self::button or self::a][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'xuất hóa đơn')]",
)
MODAL_CLOSE_BUTTONS = (
    By.CSS_SELECTOR,
    ".modal.show button.btn_close, .modal.show button.close, .modal.show i.fa-times-circle",
)
MODAL_CLOSE_X_BUTTON = (
    By.CSS_SELECTOR,
    "button.close[data-dismiss='modal'], button.close.close__btn, .modal.show button.close",
)
OVERLAY_ELEMENTS = (By.CSS_SELECTOR, ".modal-backdrop, .fixed-background")
SPINNER_ELEMENTS = (
    By.CSS_SELECTOR,
    ".spinner-border, .skeleton-loader, [role='status'].spinner-border",
)


def configure_driver(headless: bool) -> webdriver.Chrome:
    """Create and return a configured Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1440,900")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "download.default_directory": str(DOWNLOAD_DIR.resolve()),
            "safebrowsing.enabled": False,  # Disable safebrowsing to allow downloads
            "safebrowsing.disable_download_protection": True,  # Allow potentially unsafe downloads
            "profile.default_content_setting_values.automatic_downloads": 1,  # Allow automatic downloads
            "profile.content_settings.exceptions.automatic_downloads": {
                "*": {
                    "setting": 1
                }
            },
        },
    )
    
    # Additional arguments to allow downloads
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=DownloadBubble,DownloadBubbleV2")  # Disable download bubble

    if headless:
        # Fabi blocks default headless fingerprints; using the latest headless mode with
        # automation tweaks improves the odds but visible mode is still more reliable.
        chrome_options.add_argument("--headless=new")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Hide webdriver flag as early as possible
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"},
    )
    
    # Enable automatic downloads using Chrome DevTools Protocol
    # This helps bypass browser security restrictions on downloads
    try:
        # Set download behavior to allow automatic downloads
        driver.execute_cdp_cmd("Page.setDownloadBehavior", {
            "behavior": "allow",
            "downloadPath": str(DOWNLOAD_DIR.resolve())
        })
        print(f"✅ Download behavior set to allow automatic downloads to: {DOWNLOAD_DIR}")
    except Exception as e:
        # CDP command might not be available in all Chrome versions
        # The preferences should still work
        print(f"⚠️  Could not set download behavior via CDP (may not be supported): {e}")
        print(f"   Using preferences instead. Download directory: {DOWNLOAD_DIR}")
    
    return driver


def wait_and_click(driver: webdriver.Chrome, locator, timeout: int = 30):
    """Wait for an element to be clickable, scroll it into view, and click via JS."""
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        driver.execute_script("arguments[0].click();", element)
    except ElementClickInterceptedException:
        clear_overlays(driver)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", element)
    return element


def wait_and_type(driver: webdriver.Chrome, locator, text: str, timeout: int = 30):
    """Wait for an input, clear it, then type text."""
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    element.clear()
    element.send_keys(text)
    return element


def dismiss_popups(driver: webdriver.Chrome, timeout: int = 5):
    """Close the license reminder popup if it appears."""
    end_time = time.time() + timeout
    while time.time() < end_time:
        buttons = driver.find_elements(*MODAL_CLOSE_BUTTONS)
        if not buttons:
            break
        for btn in buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.2)
            except Exception:
                continue
        time.sleep(0.2)
    clear_overlays(driver)


def close_modal(driver: webdriver.Chrome, wait: WebDriverWait) -> bool:
    """Close the modal dialog by clicking outside the modal (on backdrop) or X button ONCE.
    
    Per instructions: "click anywhere is not in the model to escape the model"
    """
    try:
        # Check if modal is already closed
        try:
            modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
            if not modal.is_displayed():
                print("ℹ️ Modal is already closed")
                return True
        except Exception:
            # Modal not found, assume it's already closed
            print("ℹ️ Modal not found, already closed")
            return True
        
        # First, try clicking outside the modal (on the backdrop) as per instructions
        # "click anywhere is not in the model to escape the model"
        try:
            # Find the modal backdrop
            backdrop = driver.find_element(By.CSS_SELECTOR, ".modal-backdrop, .fade.show.modal-backdrop")
            if backdrop.is_displayed():
                # Click on the backdrop (outside the modal) to close it
                driver.execute_script("arguments[0].click();", backdrop)
                print("✅ Closed modal by clicking outside (on backdrop)")
                time.sleep(1)
                
                # Verify modal is closed
                try:
                    modal_check = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
                    if not modal_check.is_displayed():
                        return True
                except Exception:
                    # Modal not found, it's closed successfully
                    return True
        except Exception:
            # Backdrop not found or click didn't work, try X button instead
            pass
        
        # Fallback: Find the close button (X) - only get the first one
        close_buttons = driver.find_elements(*MODAL_CLOSE_X_BUTTON)
        if not close_buttons:
            print("⚠️ Could not find modal close button or backdrop")
            return False
        
        # Get the first visible close button
        close_button = None
        for btn in close_buttons:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    close_button = btn
                    break
            except Exception:
                continue
        
        if not close_button:
            print("⚠️ No visible close button found")
            return False
        
        # Click the close button ONCE
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_button)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", close_button)
        print("✅ Closed modal by clicking X button (1 lần)")
        
        # Wait for modal to close and verify it's closed
        time.sleep(1)
        try:
            modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
            if modal.is_displayed():
                print("⚠️ Modal still visible after clicking close")
                return False
        except Exception:
            # Modal not found, it's closed successfully
            pass
        
        return True
    except TimeoutException:
        print("⚠️ Timeout while closing modal")
        return False
    except Exception as e:
        print(f"⚠️ Error closing modal: {e}")
        return False


def clear_overlays(driver: webdriver.Chrome):
    """Remove remaining overlays/backdrops if they obscure clicks."""
    overlays = driver.find_elements(*OVERLAY_ELEMENTS)
    for overlay in overlays:
        try:
            driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", overlay)
        except Exception:
            continue


def wait_for_loading(driver: webdriver.Chrome, timeout: int = 40):
    """Wait until loading indicators disappear."""
    end_time = time.time() + timeout
    while time.time() < end_time:
        spinners = driver.find_elements(*SPINNER_ELEMENTS)
        visible = [s for s in spinners if s.is_displayed()]
        if not visible:
            return
        time.sleep(0.5)
    # soft timeout, log but don't raise
    print("⚠️  Loading indicators still visible after timeout.")


def navigate_to_b07(driver: webdriver.Chrome, wait: WebDriverWait):
    """Carry out navigation steps until the B07 report is open."""
    wait.until(lambda d: "dashboard" in d.current_url)
    dismiss_popups(driver)

    # Try multiple selectors to click the "Báo cáo" button
    # Order: wrapper div (most reliable) -> direct img -> text fallback
    clicked = False
    for selector in [REPORT_DIV_WRAPPER, REPORT_TILE, REPORT_IMG_DIRECT, REPORT_TEXT_TILE]:
        try:
            wait_and_click(driver, selector)
            clicked = True
            print(f"✅ Clicked 'Báo cáo' button using selector: {selector[1][:50]}...")
            break
        except (TimeoutException, NoSuchElementException):
            continue
    
    if not clicked:
        raise TimeoutException("Could not find or click the 'Báo cáo' button after login")

    wait.until(lambda d: "/report/" in d.current_url)
    time.sleep(1)  # Give page time to fully load
    dismiss_popups(driver)

    # Wait for the collapse element to exist first
    try:
        collapse = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "collapse-menu-1")))
        is_expanded = "show" in collapse.get_attribute("class")
        print(f"ℹ️ Accordion initial state - expanded: {is_expanded}")
    except TimeoutException:
        print("⚠️ Collapse element not found yet, will try to click accordion anyway")
        collapse = None
        is_expanded = False

    # Try multiple selectors to click the "Báo cáo phân tích - B" accordion
    accordion_clicked = False
    selectors_to_try = [ANALYSIS_ACCORDION_BY_SPAN, ANALYSIS_ACCORDION_BY_TITLE, ANALYSIS_ACCORDION, ANALYSIS_ACCORDION_TEXT]
    
    for selector in selectors_to_try:
        try:
            # Wait for element to be present and visible
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(selector)
            )
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            time.sleep(0.5)
            
            # Clear any overlays
            clear_overlays(driver)
            time.sleep(0.3)
            
            # Try clicking
            try:
                element.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", element)
            
            accordion_clicked = True
            print(f"✅ Clicked 'Báo cáo phân tích - B' accordion")
            time.sleep(1)  # Wait for accordion animation
            break
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"⚠️ Selector failed: {type(e).__name__}")
            continue
    
    if not accordion_clicked:
        raise TimeoutException("Could not find or click the 'Báo cáo phân tích - B' accordion")

    # Verify the accordion is expanded
    collapse = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "collapse-menu-1")))
    if "show" not in collapse.get_attribute("class"):
        print("⚠️ Accordion not expanded after click, trying again...")
        time.sleep(1)
        # Try clicking one more time
        for selector in [ANALYSIS_ACCORDION_BY_SPAN, ANALYSIS_ACCORDION]:
            try:
                element = driver.find_element(*selector)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                driver.execute_script("arguments[0].click();", element)
                time.sleep(1)
                break
            except Exception:
                continue

    WebDriverWait(driver, 10).until(EC.visibility_of(collapse))

    wait_and_click(driver, B07_LINK)

    wait.until(lambda d: "payment-method" in d.current_url.lower())
    wait_for_loading(driver)


def click_transfer_filter(driver: webdriver.Chrome, wait: WebDriverWait) -> bool:
    """Attempt to click the 'Transfer' row/button on the B07 report page - ONLY ONCE."""
    # Check if modal is already open (don't click again if modal is open)
    try:
        modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
        if modal.is_displayed():
            print("ℹ️ Modal is already open, skipping TRANSFER row click")
            return True
    except Exception:
        pass
    
    # Wait for the B07 report table to load
    time.sleep(2)  # Give table time to render
    
    # Scroll down to find the report table as per instructions
    # The instructions say "From now on this part will be scrol down Find"
    try:
        # First, try to find the report table container
        report_table = driver.find_element(By.CSS_SELECTOR, ".report-table, table.table")
        driver.execute_script("arguments[0].scrollIntoView({block: 'start', behavior: 'smooth'});", report_table)
        time.sleep(1)  # Wait for scroll to complete
        print("✅ Scrolled to report table")
    except Exception:
        # If table not found, scroll down the page to reveal content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(1)
        print("ℹ️ Scrolled down page to find table")
    
    # Try multiple selectors to find the TRANSFER row - but only click ONCE
    # Order: specific structure > general row > td > fallback
    selectors_to_try = [TRANSFER_ROW_SPECIFIC, TRANSFER_FILTER, TRANSFER_TD, TRANSFER_FILTER_FALLBACK]
    element = None
    
    for selector in selectors_to_try:
        try:
            # Wait for element to be present
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(selector)
            )
            break  # Found element, stop trying other selectors
        except TimeoutException:
            continue
    
    if not element:
        print("⚠️ Could not find TRANSFER row")
        return False
    
    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
    time.sleep(0.5)
    
    # Clear any overlays
    clear_overlays(driver)
    time.sleep(0.3)
    
    # Click ONCE - prefer clicking the row (tr) if available
    try:
        # If we found a td element, try to click the parent tr instead
        if element.tag_name.lower() == 'td':
            try:
                tr_element = element.find_element(By.XPATH, "./ancestor::tr")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tr_element)
                driver.execute_script("arguments[0].click();", tr_element)
            except Exception:
                # If can't find tr, click the td itself
                driver.execute_script("arguments[0].click();", element)
        elif element.tag_name.lower() == 'tr':
            # Already a row, click it directly ONCE
            driver.execute_script("arguments[0].click();", element)
        else:
            # Other element types, use JavaScript click
            driver.execute_script("arguments[0].click();", element)
    except Exception:
        # Fallback to JavaScript click
        driver.execute_script("arguments[0].click();", element)
    
    print(f"✅ Clicked TRANSFER row (1 lần)")
    wait_for_loading(driver)
    # Wait for modal to appear and load data
    time.sleep(3)  # Increased wait time for modal to load data
    return True



def click_atm_filter(driver: webdriver.Chrome, wait: WebDriverWait, keep_modal_open: bool = False) -> bool:
    """Attempt to click the 'ATM' row/button on the B07 report page.
    
    Args:
        keep_modal_open: If True, ensure modal stays open when clicking row
    """
    # Check if modal is already open
    modal_open = False
    if keep_modal_open:
        try:
            modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
            if modal.is_displayed():
                modal_open = True
                print("ℹ️ Modal is already open, will update content instead of opening new one")
        except Exception:
            pass
    
    # Wait for the B07 report table to load
    time.sleep(2)  # Give table time to render
    
    # Try multiple selectors to find and click the ATM row
    selectors_to_try = [ATM_FILTER, ATM_TD, ATM_FILTER_FALLBACK]
    
    for selector in selectors_to_try:
        try:
            # Wait for element to be present
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(selector)
            )
            
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            time.sleep(0.5)
            
            # Don't clear overlays if modal should stay open
            if not keep_modal_open:
                clear_overlays(driver)
            time.sleep(0.3)
            
            # Try clicking - prefer clicking the row (tr) if available
            try:
                # If we found a td element, try to click the parent tr instead
                if element.tag_name.lower() == 'td':
                    try:
                        tr_element = element.find_element(By.XPATH, "./ancestor::tr")
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tr_element)
                        # Use JavaScript click to avoid closing modal
                        driver.execute_script("arguments[0].click();", tr_element)
                    except Exception:
                        # If can't find tr, click the td itself
                        driver.execute_script("arguments[0].click();", element)
                elif element.tag_name.lower() == 'tr':
                    # Already a row, use JavaScript click to keep modal open
                    driver.execute_script("arguments[0].click();", element)
                else:
                    # Other element types, use JavaScript click
                    driver.execute_script("arguments[0].click();", element)
            except Exception:
                # Fallback to JavaScript click
                driver.execute_script("arguments[0].click();", element)
            
            print(f"✅ Clicked ATM row using selector")
            wait_for_loading(driver)
            # Wait for modal content to update (not open new modal)
            time.sleep(2)
            return True
            
        except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"⚠️ Selector failed: {type(e).__name__}")
            continue
    
    return False


def wait_for_download(new_files_before, timeout: int = 60):
    """Poll the download directory until a new file (not .crdownload) appears."""
    deadline = time.time() + timeout
    previous = set(new_files_before)

    while time.time() < deadline:
        current_files = set(DOWNLOAD_DIR.glob("*"))
        added = [f for f in current_files - previous if not f.name.endswith(".crdownload")]
        if added:
            # Wait for any temporary .crdownload to disappear for these files
            complete = []
            for file_path in added:
                # if companion .crdownload exists, continue waiting
                cr_file = file_path.with_suffix(file_path.suffix + ".crdownload")
                if cr_file.exists():
                    break
                complete.append(file_path)
            if complete:
                return complete
        time.sleep(1)
    return []


def export_report(driver: webdriver.Chrome, wait: WebDriverWait, timeout: int = 60, keep_modal_open: bool = False) -> list[Path]:
    """Click the 'Xuất Hóa Đơn' button and wait for the downloaded files.
    
    Args:
        keep_modal_open: If True, don't dismiss popups to keep modal open for reuse
    """

    files_before = list(DOWNLOAD_DIR.glob("*"))
    
    # Wait a moment for the page to fully load
    time.sleep(1)
    
    # Only dismiss popups if we're not keeping modal open (to reuse existing modal)
    if not keep_modal_open:
        # Don't dismiss popups for TRANSFER modal - it might trigger blank modals
        print("ℹ️ Skipping dismiss_popups to prevent blank modals")
    else:
        print("ℹ️ Keeping modal open for reuse")

    # Wait for modal to be visible if it exists (increased timeout since modal appears after row click)
    # IMPORTANT: Only proceed if modal has data, not blank
    modal = None
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block'], .modal:not([style*='display: none'])"))
        )
        # Ensure modal is visible
        WebDriverWait(driver, 5).until(EC.visibility_of(modal))
        
        # Check if modal has content (not blank) - wait up to 3 seconds
        has_content = False
        for check in range(3):
            try:
                modal_content = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content")
                text_content = modal_content.text.strip()
                if text_content and len(text_content) > 10:  # Has meaningful content
                    print("✅ Modal dialog detected with content")
                    has_content = True
                    break
            except Exception:
                pass
            time.sleep(1)
        
        if not has_content:
            print("⚠️ Modal detected but appears blank, waiting...")
            time.sleep(2)
            # Re-check modal
            try:
                modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
                modal_content = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content")
                text_content = modal_content.text.strip()
                if not text_content or len(text_content) <= 10:
                    print("⚠️ Modal is still blank, may download empty file")
            except Exception:
                print("⚠️ Could not verify modal content")
        
        time.sleep(1)  # Give modal time to fully render/update content
    except TimeoutException:
        print("ℹ️ No modal detected, trying to find button directly on page")
    
    # Try multiple selectors to find and click the export button
    # Priority: modal footer button > button with icon > generic button
    # IMPORTANT: Only click ONCE - find the first button in modal footer
    selectors_to_try = [EXPORT_BUTTON, EXPORT_BUTTON_BY_MODAL, EXPORT_BUTTON_BY_ICON, EXPORT_BUTTON_FALLBACK, EXPORT_BUTTON_GENERIC]
    button = None
    
    for selector in selectors_to_try:
        try:
            # Wait for element to be visible and clickable
            # Use find_elements to get all matches, then take the first one
            elements = WebDriverWait(driver, 5).until(
                lambda d: d.find_elements(*selector)
            )
            if elements:
                # Get the first clickable button
                for elem in elements:
                    try:
                        if elem.is_displayed() and elem.is_enabled():
                            button = elem
                            print(f"✅ Found export button (first match in modal)")
                            break
                    except Exception:
                        continue
                if button:
                    break
        except TimeoutException:
            continue
    
    if not button:
        print("⚠️  Không tìm thấy nút 'Xuất Hóa Đơn'.")
        return []

    # Final check: Ensure modal still has content before clicking export
    try:
        if modal:
            modal_content = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content")
            text_content = modal_content.text.strip()
            if not text_content or len(text_content) <= 10:
                print("⚠️ Modal appears blank, waiting for content...")
                time.sleep(2)
                # Re-check
                modal_content = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content")
                text_content = modal_content.text.strip()
                if not text_content or len(text_content) <= 10:
                    print("⚠️ Modal is still blank, aborting export to prevent empty download")
                    return []
    except Exception:
        pass

    # Scroll into view and click ONCE
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)
        time.sleep(0.5)
        
        # Don't clear overlays - might trigger modal close
        # clear_overlays(driver)
        time.sleep(0.3)
        
        # Click ONCE - use JavaScript click to ensure it's treated as user action
        # Only click if button is still visible and enabled
        if button.is_displayed() and button.is_enabled():
            try:
                # Use JavaScript click to bypass some security restrictions
                driver.execute_script("arguments[0].click();", button)
                print("✅ Clicked 'Xuất hoá đơn' button (1 lần)")
                
                # Immediately disable button to prevent multiple clicks
                try:
                    driver.execute_script("arguments[0].disabled = true;", button)
                except Exception:
                    pass
            except Exception:
                # Fallback to regular click
                try:
                    button.click()
                    print("✅ Clicked 'Xuất hoá đơn' button (1 lần)")
                    # Disable button
                    try:
                        driver.execute_script("arguments[0].disabled = true;", button)
                    except Exception:
                        pass
                except ElementClickInterceptedException:
                    driver.execute_script("arguments[0].click();", button)
                    print("✅ Clicked 'Xuất hoá đơn' button (1 lần)")
        else:
            print("⚠️ Button không còn visible/enabled, không thể click")
            return []
        
        # Wait a moment for download dialog/confirmation if any
        time.sleep(2)
        
        # Check if there's a download confirmation dialog and handle it
        try:
            # Try to find and accept any download confirmation dialogs
            alert = driver.switch_to.alert
            alert.accept()
            print("✅ Accepted download confirmation dialog")
        except Exception:
            # No alert dialog, continue
            pass
        
        wait_for_loading(driver, timeout=timeout // 2 or 10)
    except Exception as e:
        print(f"⚠️  Lỗi khi click nút export: {e}")
        return []

    downloaded = wait_for_download(files_before, timeout=timeout)
    if downloaded:
        print(f"✅ Đã tải {len(downloaded)} file(s):")
        for path in downloaded:
            print(f"   • {path.name}")
    else:
        print("⚠️  Không phát hiện file mới sau khi bấm 'Xuất Hóa Đơn'.")
    return downloaded


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Automate Fabi report navigation.")
    parser.add_argument("--username", help="Fabi username (email). Defaults to $FABI_USERNAME.")
    parser.add_argument("--password", help="Fabi password. Defaults to $FABI_PASSWORD.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chrome in headless mode (less reliable for Fabi).",
    )
    parser.add_argument(
        "--no-click-transfer",
        action="store_true",
        help="Skip clicking the Transfer filter after opening B07.",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=40,
        help="Maximum wait time (seconds) for each step. Default: 40.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    username = args.username or os.getenv("FABI_USERNAME") or DEFAULT_USERNAME
    password = args.password or os.getenv("FABI_PASSWORD") or DEFAULT_PASSWORD

    if not username or not password:
        print("❌ Missing credentials. Provide --username/--password or set FABI_USERNAME/FABI_PASSWORD.")
        sys.exit(1)

    driver = configure_driver(headless=args.headless)
    wait = WebDriverWait(driver, args.wait)

    try:
        driver.get(LOGIN_URL)
        wait_and_type(driver, EMAIL_INPUT, username)
        wait_and_type(driver, PASSWORD_INPUT, password)
        wait_and_click(driver, LOGIN_BUTTON)

        navigate_to_b07(driver, wait)
        print(f"✅ Opened B07 report: {driver.current_url}")

        if args.no_click_transfer:
            print("ℹ️ Skipping transfer filter as requested.")
        else:
            # Step 1: Click TRANSFER and download
            clicked = click_transfer_filter(driver, wait)
            if clicked:
                print("✅ Transfer filter clicked.")
                
                # Wait for modal to appear and ensure it has data loaded
                print("⏳ Waiting for modal to appear and load data...")
                try:
                    # Wait for modal to be visible
                    modal = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']"))
                    )
                    WebDriverWait(driver, 5).until(EC.visibility_of(modal))
                    print("✅ Modal appeared")
                    
                    # Prevent modal from auto-closing by disabling event listeners
                    try:
                        driver.execute_script("""
                            // Disable auto-close on backdrop click
                            var modals = document.querySelectorAll('.modal');
                            modals.forEach(function(modal) {
                                if (modal.style.display !== 'none' && modal.classList.contains('show')) {
                                    // Remove backdrop click handler
                                    modal.setAttribute('data-backdrop', 'static');
                                    modal.setAttribute('data-keyboard', 'false');
                                    
                                    // Prevent ESC key from closing
                                    var originalRemove = modal.remove;
                                    modal.remove = function() {};
                                    
                                    // Disable all close button handlers temporarily
                                    var closeBtns = modal.querySelectorAll('[data-dismiss="modal"], .close, button.close');
                                    closeBtns.forEach(function(btn) {
                                        btn.onclick = null;
                                        btn.addEventListener('click', function(e) {
                                            e.stopPropagation();
                                        }, true);
                                    });
                                }
                            });
                        """)
                        print("ℹ️ Disabled auto-close handlers on modal")
                    except Exception as e:
                        print(f"⚠️ Could not disable auto-close: {e}")
                    
                    # Wait for data to load in modal (check multiple times)
                    data_loaded = False
                    for attempt in range(5):  # Check up to 5 times
                        time.sleep(1)
                        try:
                            modal_content = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content")
                            # Check if modal has actual content (not just empty)
                            text_content = modal_content.text.strip()
                            if text_content and len(text_content) > 10:  # Has meaningful content
                                print(f"✅ Modal has data loaded (attempt {attempt + 1})")
                                data_loaded = True
                                break
                        except Exception:
                            pass
                    
                    if not data_loaded:
                        print("⚠️ Modal content not fully loaded, but proceeding...")
                    
                    # Verify modal is still open before proceeding
                    try:
                        modal_check = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
                        if not modal_check.is_displayed():
                            print("⚠️ Modal closed unexpectedly, waiting for it to reopen...")
                            time.sleep(2)
                            modal = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']"))
                            )
                    except Exception:
                        print("⚠️ Could not verify modal state")
                except TimeoutException:
                    print("⚠️ Modal did not appear after clicking TRANSFER")
                
                # Export TRANSFER data
                print("\n📥 Downloading TRANSFER data...")
                transfer_files = export_report(driver, wait, keep_modal_open=False)
                if transfer_files:
                    print(f"✅ Downloaded {len(transfer_files)} file(s) for TRANSFER")
                else:
                    print("⚠️ No files downloaded for TRANSFER")
                
                # Close TRANSFER modal by clicking X button ONCE
                print("\n🔒 Closing TRANSFER modal...")
                close_modal(driver, wait)
                
                # Verify modal is closed before continuing
                time.sleep(1)
                try:
                    modal = driver.find_element(By.CSS_SELECTOR, ".modal.show, .modal[style*='display: block']")
                    if modal.is_displayed():
                        print("⚠️ Modal still open, trying to close again...")
                        close_modal(driver, wait)
                        time.sleep(1)
                except Exception:
                    print("✅ Modal is closed")
            else:
                print("⚠️ Transfer filter not found. Please adjust the SELECTOR or verify UI state.")
            
            # Step 2: Click ATM row to open new modal
            print("\n🔄 Switching to ATM filter...")
            atm_clicked = click_atm_filter(driver, wait, keep_modal_open=False)
            if atm_clicked:
                print("✅ ATM filter clicked.")
                print("⏳ Waiting for modal content to update with ATM data...")
                time.sleep(2)  # Wait for modal content to update with ATM data
                
                # Export ATM data - reuse the same modal
                print("\n📥 Downloading ATM data...")
                atm_files = export_report(driver, wait, keep_modal_open=True)
                if atm_files:
                    print(f"✅ Downloaded {len(atm_files)} file(s) for ATM")
                    # Rename ATM files to add "(1)" to avoid overwriting TRANSFER files
                    # Both TRANSFER and ATM downloads have the same filename (e.g., sale_by_payment_method.xls)
                    # So we rename ATM file to sale_by_payment_method (1).xls
                    for file_path in atm_files:
                        try:
                            # Get file name and extension
                            stem = file_path.stem  # filename without extension (e.g., "sale_by_payment_method")
                            suffix = file_path.suffix  # extension (e.g., ".xls")
                            
                            # Create new filename with "(1)" before extension
                            # Example: sale_by_payment_method.xls → sale_by_payment_method (1).xls
                            new_name = f"{stem} (1){suffix}"
                            new_path = file_path.parent / new_name
                            
                            # Check if new name already exists, if so use (2), (3), etc.
                            counter = 1
                            while new_path.exists():
                                counter += 1
                                new_name = f"{stem} ({counter}){suffix}"
                                new_path = file_path.parent / new_name
                            
                            # Rename the file
                            file_path.rename(new_path)
                            print(f"   • Renamed ATM file: {file_path.name} → {new_path.name}")
                            print(f"     (TRANSFER: {file_path.name}, ATM: {new_path.name})")
                        except Exception as e:
                            print(f"⚠️ Could not rename {file_path.name}: {e}")
                else:
                    print("⚠️ No files downloaded for ATM")
            else:
                print("⚠️ ATM filter not found. Please adjust the SELECTOR or verify UI state.")

        # Keep the browser open for manual inspection unless headless mode is used.
        if not args.headless:
            print("ℹ️ Leaving browser window open for manual actions. Press Ctrl+C to quit.")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Interrupted by user.")
    except TimeoutException as err:
        print(f"❌ Timeout while waiting for page element: {err}")
    except NoSuchElementException as err:
        print(f"❌ Could not locate element: {err}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

