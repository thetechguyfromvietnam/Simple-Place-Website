#!/usr/bin/env python3
"""
PHẦN MỀM XỬ LÝ HÓA ĐƠN TỔNG HỢP
==================================
Kết hợp và tách file XLS (sale_by_payment_method) thành nhiều file Excel riêng lẻ
Hoặc tạo hóa đơn Grab với menu random

- Mỗi file = 1 hóa đơn
- Tên món: Tiếng Việt / Tiếng Anh (từ menu)
- Xử lý: Giảm giá + Chiết khấu thanh toán (trừ vào giá món)
- Thay thế: Rượu/Bia → Đồ ăn (điều chỉnh giá cho thuế)

Sử dụng:
    python3 process_invoices.py
    
    Chương trình sẽ hiển thị menu để chọn:
    1. Process sale_by_payment_method (combine và split)
    2. Process single file
    3. Create Grab invoice
"""

import re
import xlsxwriter
import sys
import os
import random
from datetime import datetime
from pathlib import Path

# Resolve project root so sibling packages (Menu, etc.) remain importable
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import parse_menu
script_dir = PROJECT_ROOT
from Menu.parse_menu import parse_excel_menu

# ============================================================================
# HÀM TIỆN ÍCH CHUẨN HÓA KEY TÊN MÓN
# ============================================================================

def normalize_menu_key(s):
    """
    Chuẩn hóa chuỗi để dùng làm key so sánh tên món:
    - Đưa về lowercase
    - Bỏ ký tự đặc biệt (giữ lại chữ, số, khoảng trắng)
    - Gom nhiều khoảng trắng thành 1
    
    Ví dụ:
        'V - Bruschetta'  -> 'v bruschetta'
        'V-Bruschetta'    -> 'v bruschetta'
    """
    if not s:
        return ''
    s = s.lower().strip()
    # Bỏ ký tự không phải chữ/số/khoảng trắng (bao gồm '-', '/', ',', ...)
    s = re.sub(r'[^\w\s]', ' ', s)
    # Gom nhiều khoảng trắng liên tiếp thành 1
    s = re.sub(r'\s+', ' ', s)
    return s

# ============================================================================
# CẤU HÌNH
# ============================================================================

MENU_FILES = [
    'Menu/simple-place-menu.xlsx',
    'Menu/taco-place-menu.xlsx'
]

OUTPUT_DIR = 'tax_files'

# Default files for combining
DEFAULT_FILE1 = 'sale_by_payment_method.xls'  # transfer
DEFAULT_FILE2 = 'sale_by_payment_method (1).xls'  # atm

# ============================================================================
# CẤU HÌNH PHÍ DỊCH VỤ (CHỈ ÁP DỤNG HÔM NAY - NGÀY LỄ)
# ============================================================================
# Phí dịch vụ = 8% của tổng bill, được thêm vào mỗi hóa đơn như một món ăn với số lượng 1.
# 
# Cách sử dụng:
# - Để bật phí dịch vụ: Đặt SERVICE_FEE_ENABLED = True
# - Để tắt phí dịch vụ: Đặt SERVICE_FEE_ENABLED = False
# 
# Phí dịch vụ sẽ được tính = 8% của tổng giá trị các món ăn (trước khi thêm phí dịch vụ)
# ============================================================================
SERVICE_FEE_ENABLED = False  # Bật/tắt phí dịch vụ. True = bật, False = tắt
SERVICE_FEE_PERCENTAGE = 0.08  # 8% của tổng bill
SERVICE_FEE_NAME = "Phí dịch vụ"  # Tên phí dịch vụ (không cần phần tiếng Anh)
SERVICE_FEE_UNIT = ""  # Để trống, không cần đơn vị

# ============================================================================
# LOAD MENU VÀ TẠO MAPPING
# ============================================================================

def load_menus():
    """Load tất cả menu và tạo mapping"""
    all_items = []
    
    for menu_file in MENU_FILES:
        menu_path = script_dir / menu_file
        if menu_path.exists():
            items = parse_excel_menu(str(menu_path))
            # Track source menu for each item
            menu_type = 'simple' if 'simple-place' in menu_file.lower() else 'taco'
            for item in items:
                item['menu_source'] = menu_type
                all_items.append(item)
    
    # Tạo mapping: English name (lowercase) -> Full name (Vietnamese / English)
    name_mapping = {}
    price_to_items = {}
    
    # Nhóm được xem là bia/rượu: chỉ các nhóm sau trong menu
    alcohol_groups = {'BEER & CRAFT BEERS', 'SANGRIA', 'RED', 'WHITE'}
    
    for item in all_items:
        full_name = item['name']
        price = item['price']
        
        # Extract English part (sau dấu /)
        if ' / ' in full_name:
            parts = full_name.split(' / ')
            english_name = parts[-1].strip()
            eng_key = normalize_menu_key(english_name)
            # If duplicate, prefer the first one found (Simple Place takes precedence)
            if eng_key and eng_key not in name_mapping:
                name_mapping[eng_key] = full_name
        
        # Map cả tên đầy đủ (prefer Simple Place if duplicate)
        full_name_key = normalize_menu_key(full_name)
        if full_name_key and full_name_key not in name_mapping:
            name_mapping[full_name_key] = full_name
        
        # Tạo price mapping cho món không phải bia/rượu và không phải Coke
        group_name = str(item.get('group', '')).strip().upper()
        is_alcohol = group_name in alcohol_groups
        
        # Kiểm tra tên món có chứa từ khóa bia/rượu không (bao gồm cả Coke thường, nhưng KHÔNG bao gồm Coke Light/Zero)
        if not is_alcohol:
            item_name_lower = full_name.lower()
            alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 'whisky', 'vodka']
            is_alcohol = any(keyword in item_name_lower for keyword in alcohol_keywords)
            
            # Kiểm tra Coke thường (KHÔNG phải Light/Zero)
            if not is_alcohol and ('coke' in item_name_lower or 'coca' in item_name_lower):
                exclude_keywords = ['light', 'zero', 'ít đường', 'không đường', 'it duong', 'khong duong']
                is_coke_light_or_zero = any(exclude_kw in item_name_lower for exclude_kw in exclude_keywords)
                if not is_coke_light_or_zero:
                    is_alcohol = True
        
        # Chỉ thêm món không phải bia/rượu vào price_to_items
        if not is_alcohol:
            if price not in price_to_items:
                price_to_items[price] = []
            price_to_items[price].append(item)
    
    return all_items, name_mapping, price_to_items

# ============================================================================
# XỬ LÝ THAY THẾ RƯỢU/BIA
# ============================================================================

def find_replacement_for_alcohol(alcohol_name, alcohol_price, price_to_items):
    """
    Tìm món thay thế không cồn và điều chỉnh giá cho thuế.
    
    Logic: Món thay thế sẽ được thêm số tiền bằng với thuế 10% của bia
    để tổng số tiền ra đủ sau khi đã áp thuế 8%.
    
    Công thức:
    - Giá bia gốc: P
    - Thuế 10% của bia: P * 0.10
    - Giá món thay thế = P + (P * 0.10) = P * 1.10
    - Sau thuế 8%: P * 1.10 * 1.08 = P * 1.188
    - Để tổng bằng P * 1.10 (như bia với thuế 10%): F * 1.08 = P * 1.10
    - Vậy: F = P * 1.10 / 1.08
    
    QUAN TRỌNG: Không bao giờ thay thế bia/rượu bằng bia/rượu khác.
    """
    import random
    
    # Nhóm được xem là bia/rượu: chỉ các nhóm sau trong menu
    alcohol_groups = {'BEER & CRAFT BEERS', 'SANGRIA', 'RED', 'WHITE'}
    
    # Từ khóa để nhận diện bia/rượu trong tên món (KHÔNG bao gồm Coke Light/Zero)
    alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 'whisky', 'vodka']
    
    def is_alcohol_item(item):
        """Kiểm tra xem món có phải là bia/rượu không"""
        # Kiểm tra nhóm
        group_name = str(item.get('group', '')).strip().upper()
        if group_name in alcohol_groups:
            return True
        
        # Kiểm tra tên món
        item_name_lower = str(item.get('name', '')).lower()
        if any(keyword in item_name_lower for keyword in alcohol_keywords):
            return True
        
        # Kiểm tra Coke thường (KHÔNG phải Light/Zero)
        if 'coke' in item_name_lower or 'coca' in item_name_lower:
            exclude_keywords = ['light', 'zero', 'ít đường', 'không đường', 'it duong', 'khong duong']
            is_coke_light_or_zero = any(exclude_kw in item_name_lower for exclude_kw in exclude_keywords)
            if not is_coke_light_or_zero:
                return True
        
        return False
    
    # Tính số tiền thuế 10% (áp dụng cho bia/rượu và Coke 10% đường)
    tax_10_percent = alcohol_price * 0.10
    
    # Giá món thay thế = giá gốc (bia/rượu hoặc Coke) + thuế 10%, sau đó điều chỉnh để sau thuế 8% vẫn đủ
    # Công thức: adjusted_price = (alcohol_price + tax_10_percent) / 1.08 * 1.08 / 1.08
    # Đơn giản hóa: adjusted_price = alcohol_price * 1.10 / 1.08
    # Áp dụng cho cả bia/rượu và Coke 10% đường (cùng tính thuế 10%)
    # Làm tròn thành số nguyên (không có phần thập phân)
    adjusted_price = round(alcohol_price * 1.10 / 1.08)
    
    # Tìm món có giá gần với giá gốc, đảm bảo không phải bia/rượu
    for delta in [0, 5000, -5000, 10000, -10000, 15000, -15000, 20000, -20000]:
        nearby_price = alcohol_price + delta
        if nearby_price in price_to_items and len(price_to_items[nearby_price]) > 0:
            # Lọc ra các món không phải bia/rượu
            non_alcohol_items = [item for item in price_to_items[nearby_price] if not is_alcohol_item(item)]
            
            if len(non_alcohol_items) > 0:
                best_replacement = random.choice(non_alcohol_items)
                return best_replacement['name'], best_replacement['unit'], adjusted_price
    
    # Fallback: chọn random từ tất cả món, nhưng đảm bảo không phải bia/rượu
    if price_to_items:
        # Thu thập tất cả món không phải bia/rượu
        all_non_alcohol_items = []
        for price, items in price_to_items.items():
            for item in items:
                if not is_alcohol_item(item):
                    all_non_alcohol_items.append(item)
        
        if len(all_non_alcohol_items) > 0:
            replacement = random.choice(all_non_alcohol_items)
            return replacement['name'], replacement['unit'], adjusted_price
    
    return alcohol_name, 'Lon', alcohol_price

# ============================================================================
# TỰ ĐỘNG SỬA FORMAT TÊN MÓN
# ============================================================================

def fix_item_name_format(item_name):
    """
    Tự động sửa format tên món thành 'Tên Tiếng Việt / Tên Tiếng Anh'
    """
    if not item_name or ' / ' in item_name:
        return item_name
    
    item_name = item_name.strip()
    
    # Mapping các món thường gặp không đúng format
    format_fixes = {
        'Avocado Smothie (Sinh tố bơ)': 'Sinh tố bơ / Avocado Smoothie',
        'Mango Smothie (Sinh tố xoài)': 'Sinh tố xoài / Mango Smoothie',
        'Strawberry Smothie (Sinh tố dâu)': 'Sinh tố dâu / Strawberry Smoothie',
        'Lamb Stew': 'Lamb Stew / Lamb Stew',
        # V - Bruschetta: ép về format Tiếng Việt / Tiếng Anh chuẩn trong menu
        'V - Bruschetta': 'Bruschetta Ý Chay (Bánh Mì Nướng Phủ Cà Chua Tươi, Dầu Ôliu) / V-Bruschetta',
    }
    
    # Kiểm tra trong mapping
    if item_name in format_fixes:
        return format_fixes[item_name]
    
    # Nếu có dấu ngoặc đơn với tiếng Việt bên trong: "English (Vietnamese)"
    if '(' in item_name and ')' in item_name:
        match = re.match(r'^(.+?)\s*\((.+?)\)\s*$', item_name)
        if match:
            english_part = match.group(1).strip()
            vietnamese_part = match.group(2).strip()
            # Kiểm tra xem phần trong ngoặc có phải tiếng Việt không
            if any(ord(char) > 127 for char in vietnamese_part):
                return f"{vietnamese_part} / {english_part}"
    
    # Nếu chỉ có tiếng Anh, thêm lại chính nó làm phần tiếng Anh
    # (giữ nguyên để có format đúng, nhưng sẽ được match với menu sau)
    if not any(ord(char) > 127 for char in item_name):
        return f"{item_name} / {item_name}"
    
    # Nếu chỉ có tiếng Việt, thêm lại chính nó
    return f"{item_name} / {item_name}"

# ============================================================================
# MATCH TÊN MÓN VỚI MENU
# ============================================================================

def match_menu_name(raw_name, all_menu_items, name_mapping):
    """Match tên món từ file với tên trong menu"""
    raw_lower = raw_name.lower().strip()
    
    # Loại bỏ variations
    raw_normalized = re.sub(r'\s*\(spicy\)\s*', '', raw_lower).strip()
    raw_without_extra = re.sub(r'\s+extra\s*$', '', raw_normalized).strip()
    raw_without_s = re.sub(r's\s+extra', ' extra', raw_normalized)
    
    # Direct match với key đã chuẩn hóa
    candidates = [raw_normalized, raw_without_s, raw_without_extra, raw_lower]
    for candidate in candidates:
        key = normalize_menu_key(candidate)
        if key in name_mapping:
            return name_mapping[key]
    
    # Partial match
    best_match = None
    best_score = 0
    
    # Handle singular/plural variations
    raw_normalized_singular = raw_normalized.rstrip('s')
    raw_normalized_plural = raw_normalized + 's' if not raw_normalized.endswith('s') else raw_normalized
    candidates_to_try = [raw_normalized, raw_normalized_singular, raw_normalized_plural]
    
    for item in all_menu_items:
        full_name = item['name']
        
        if ' / ' in full_name:
            english_part = full_name.split(' / ')[-1].strip().lower()
        else:
            english_part = full_name.lower()
        
        # Try each candidate variation
        for raw_candidate in candidates_to_try:
            raw_clean = re.sub(r'[^\w\s]', '', raw_candidate)
            eng_clean = re.sub(r'[^\w\s]', '', english_part)
            
            raw_words = set(raw_clean.split())
            eng_words = set(eng_clean.split())
            
            if raw_words and eng_words:
                common_words = raw_words & eng_words
                
                if len(raw_words) == 1:
                    score = len(common_words) / len(eng_words) if len(common_words) > 0 else 0
                    if eng_clean.startswith(raw_clean):
                        score += 0.2
                else:
                    score = len(common_words) / max(len(raw_words), len(eng_words))
                
                if raw_clean in eng_clean or eng_clean in raw_clean:
                    score += 0.3
                
                threshold = 0.3 if len(raw_words) == 1 else 0.5
                
                if score >= threshold and score > best_score:
                    best_score = score
                    best_match = full_name
                    break
    
    return best_match if best_match else raw_name

# ============================================================================
# KẾT HỢP FILES
# ============================================================================

def combine_files(file1_path, file2_path):
    """Kết hợp 2 file HTML thành 1, xử lý trực tiếp trong memory"""
    
    with open(file1_path, 'r', encoding='utf-8', errors='ignore') as f:
        content1 = f.read()
    
    with open(file2_path, 'r', encoding='utf-8', errors='ignore') as f:
        content2 = f.read()
    
    # Extract rows from both files
    parts1 = content1.split('<tr>')
    header = parts1[0] if parts1 else ''
    rows1 = ['<tr>' + part for part in parts1[1:] if part.strip()]
    
    parts2 = content2.split('<tr>')
    rows2 = ['<tr>' + part for part in parts2[1:] if part.strip()]
    
    # Extract footer
    footer_pos = max(
        content1.rfind('</table>'),
        content1.rfind('</tbody>'),
        content1.rfind('</html>')
    )
    footer = ''
    if footer_pos >= 0:
        tag_end = content1.find('>', footer_pos)
        footer = content1[tag_end + 1:] if tag_end >= 0 else content1[footer_pos:]
    
    # Combine
    combined_content = header + '\n'.join(rows1 + rows2) + footer
    
    return combined_content, len(rows1)

# ============================================================================
# PARSE FILE XLS
# ============================================================================

def parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined=False):
    """
    Parse HTML content và group theo hóa đơn
    Returns list of invoices
    """
    
    # Count total invoices if combined
    total_invoice_count = 0
    if is_combined:
        rows_temp = content.split('<tr>')
        for temp_row in rows_temp:
            if re.search(r'rowspan="\d+">(\d{6})</td>', temp_row):
                total_invoice_count += 1
    
    invoices = []
    current_invoice = None
    invoice_counter = 0
    alcohol_items_found = []  # Track alcohol items for reporting
    
    rows = content.split('<tr>')
    
    for row in rows:
        invoice_match = re.search(r'rowspan="\d+">(\d{6})</td>', row)
        
        if invoice_match:
            invoice_num = invoice_match.group(1)
            invoice_counter += 1
            
            date_match = re.search(r'>(\d{2}/\d{2}/\d{4})</td>', row)
            invoice_date = date_match.group(1) if date_match else datetime.now().strftime('%d/%m/%Y')
            
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row)
            cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
            
            discount = 0
            payment_discount = 0
            total_amount_pos = -1
            
            for i, cell in enumerate(cells):
                if 15 <= i <= 25:
                    cell_clean = cell.replace(' ', '').replace(',', '').replace('.', '')
                    if cell_clean.isdigit() and len(cell_clean) >= 4:
                        value = float(cell_clean)
                        if value >= 50000 and total_amount_pos == -1:
                            total_amount_pos = i
                            break
            
            if total_amount_pos >= 0:
                if total_amount_pos + 1 < len(cells):
                    cell_clean = cells[total_amount_pos + 1].replace(' ', '').replace(',', '').replace('.', '')
                    if cell_clean.isdigit():
                        discount = float(cell_clean)
                
                if total_amount_pos + 5 < len(cells):
                    cell_clean = cells[total_amount_pos + 5].replace(' ', '').replace(',', '').replace('.', '').replace('-', '')
                    if cell_clean.isdigit():
                        payment_discount = float(cell_clean)
            
            final_total = 0
            if len(cells) > 0:
                last_cell_clean = cells[-1].replace(' ', '').replace(',', '').replace('.', '')
                if last_cell_clean.isdigit() and len(last_cell_clean) >= 4:
                    final_total = float(last_cell_clean)
            
            # Detect payment method
            payment_method = None
            for cell in cells:
                cell_upper = cell.upper()
                if 'ATM (' in cell_upper or cell_upper.startswith('ATM'):
                    payment_method = 'atm'
                    break
                elif 'TRANSFER (' in cell_upper or cell_upper.startswith('TRANSFER'):
                    payment_method = 'transfer'
                    break
            
            if payment_method is None:
                row_upper = row.upper()
                if 'ATM (' in row_upper:
                    payment_method = 'atm'
                elif 'TRANSFER (' in row_upper:
                    payment_method = 'transfer'
            
            # Default for combined files: first half = transfer, second half = atm
            if payment_method is None and is_combined and total_invoice_count > 0:
                boundary = total_invoice_count // 2
                payment_method = 'transfer' if invoice_counter <= boundary else 'atm'
            
            current_invoice = {
                'number': len(invoices) + 1,
                'invoice_id': invoice_num,
                'date': invoice_date,
                'items': [],
                'discount': discount,
                'payment_discount': payment_discount,
                'final_total': final_total,
                'payment_method': payment_method
            }
            invoices.append(current_invoice)
        
        # Extract items
        if current_invoice is not None:
            if current_invoice.get('payment_method') is None:
                row_upper = row.upper()
                if 'ATM (' in row_upper:
                    current_invoice['payment_method'] = 'atm'
                elif 'TRANSFER (' in row_upper:
                    current_invoice['payment_method'] = 'transfer'
            
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row)
            cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
            
            # Track items đã parse trong row này để tránh duplicate
            parsed_in_row = set()
            
            # Parse tất cả các món có thể trong row
            # Bắt đầu từ đầu row và parse đến khi không còn đủ 4 cells (name, qty, unit, price)
            for i in range(len(cells) - 3):
                try:
                    name = cells[i]
                    qty_candidate = cells[i + 1]
                    unit_candidate = cells[i + 2]
                    price_candidate = cells[i + 3]
                    
                    # Mở rộng điều kiện số lượng để không bỏ sót món
                    # Cho phép số lượng từ 1 đến 200
                    if not (qty_candidate.isdigit() and 1 <= int(qty_candidate) <= 200):
                        continue
                    
                    qty = int(qty_candidate)
                    price_clean = price_candidate.replace(' ', '').replace(',', '').replace('.', '')
                    if not price_clean.isdigit():
                        continue
                    
                    price_value = float(price_clean)
                    unit = unit_candidate if unit_candidate and not unit_candidate.isdigit() else 'Phần'
                    
                    # Bỏ qua các tên không hợp lệ
                    # LƯU Ý: Cho phép tên là số (như "333" là tên bia) nếu có giá và số lượng hợp lệ
                    if (len(name) < 1 or 
                        name in ['', 'STT', 'Mã hoá đơn', 'Simple Place']):
                        continue
                    
                    # Chỉ bỏ qua tên là số nếu không có context hợp lệ (giá và số lượng)
                    # Nếu có giá và số lượng hợp lệ, có thể là tên món đặc biệt (như "333" là bia)
                    if name.isdigit() and (not price_clean.isdigit() or not qty_candidate.isdigit()):
                        continue
                    
                    skip_patterns = [
                        r'\bcrispy\b', r'\bsoft\b', r'cut in 4', r'- edit\s*$',
                        r'đổi phương thức', r'\bpayment\b', r'\btransfer\b',
                        r'\bcod\b', r'\batm\b', 'background-color', 'vertical-align',
                        'ghi chú', 'giảm sốt'
                    ]
                    if any(re.search(pattern, name.lower()) for pattern in skip_patterns):
                        continue
                    
                    # Mở rộng điều kiện để không bỏ sót món
                    # Cho phép giá từ 500 VND (có thể có món rẻ) đến 2,000,000 VND (có thể có món đắt)
                    # Cho phép số lượng từ 1 đến 200 (có thể có món order nhiều)
                    if (price_value >= 500 and price_value <= 2000000 and 
                        qty >= 1 and qty <= 200 and len(name) > 2):
                        
                        raw_unit = unit.strip() if unit else ''
                        raw_unit_lower = raw_unit.lower()
                        if not raw_unit or raw_unit.isdigit():
                            clean_unit = 'Phần'
                        elif raw_unit_lower in {'món', 'mon', 'dish'}:
                            clean_unit = 'Phần'
                        else:
                            clean_unit = raw_unit
                        
                        # Lưu tên gốc để check từ khóa bia/rượu trước khi match menu
                        original_name = name.strip()
                        original_name_lower = original_name.lower()
                        
                        # Match với menu
                        matched_name = match_menu_name(original_name, all_menu_items, name_mapping)
                        
                        # Tự động sửa format nếu không đúng
                        full_name = fix_item_name_format(matched_name)
                        
                        # Đảm bảo format cuối cùng luôn có " / "
                        if ' / ' not in full_name:
                            full_name = f"{full_name} / {full_name}"
                        
                        # Tạo key để check duplicate dựa trên VỊ TRÍ CELL trong row này
                        # Tránh parse cùng 1 cell nhiều lần (do logic loop có thể parse lại)
                        # Sử dụng vị trí cell (i) thay vì nội dung món để tránh bỏ sót món giống nhau
                        cell_position_key = i
                        
                        # CHỈ kiểm tra duplicate dựa trên vị trí cell trong row này
                        # Cho phép có nhiều món giống nhau (cùng tên, giá, số lượng) trong cùng row hoặc khác row
                        # Vì có thể là các món riêng biệt được order ở các thời điểm khác nhau
                        if cell_position_key in parsed_in_row:
                            continue
                        
                        # Đánh dấu đã parse cell ở vị trí này trong row này
                        parsed_in_row.add(cell_position_key)
                        
                        # KHÔNG kiểm tra duplicate trong invoice nữa
                        # Cho phép có nhiều món giống nhau (cùng tên, giá, số lượng) trong cùng hóa đơn
                        # Vì có thể là các món riêng biệt được order ở các thời điểm khác nhau
                        
                        # Xác định bia/rượu và Coke (thuế 10%) dựa trên Tên nhóm của menu
                        # Chỉ các nhóm: BEER & CRAFT BEERS, SANGRIA, RED, WHITE mới bị coi là bia/rượu (tính thuế 10%)
                        # Ngoài ra, Coke (Coca-Cola) THƯỜNG có 10% đường nên cũng tính thuế 10% (giống bia/rượu)
                        # LƯU Ý: Coke Light và Coke Zero có lượng đường < 10g nên tính thuế 8%, KHÔNG phải 10%
                        alcohol_groups = {'BEER & CRAFT BEERS', 'SANGRIA', 'RED', 'WHITE'}
                        matched_item = next((m for m in all_menu_items if m['name'] == full_name), None)
                        group_name = str(matched_item.get('group', '')).strip().upper() if matched_item else ''
                        is_alcohol = group_name in alcohol_groups
                        
                        # QUAN TRỌNG: Check từ khóa bia/rượu trong CẢ tên gốc (original_name) VÀ tên đã match (full_name)
                        # Để phát hiện các món như "333", "Saigon" ngay cả khi không match được với menu
                        if not is_alcohol:
                            # Danh sách từ khóa bia/rượu
                            alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 'whisky', 'vodka', 'sapporo', 'craft']
                            
                            # Check trong tên gốc (trước khi match menu)
                            is_alcohol = any(keyword in original_name_lower for keyword in alcohol_keywords)
                            
                            # Nếu chưa phát hiện, check trong tên đã match (sau khi match menu)
                            if not is_alcohol:
                                full_name_lower = full_name.lower()
                                is_alcohol = any(keyword in full_name_lower for keyword in alcohol_keywords)
                        
                        # Kiểm tra nếu là Coke (Coca-Cola) THƯỜNG - có 10% đường nên tính thuế 10% (giống bia/rượu)
                        # LƯU Ý: Chỉ Coke thường (có 10% đường) tính thuế 10%, Coke Light và Coke Zero (ít đường) tính thuế 8%
                        if not is_alcohol:
                            # Check trong cả tên gốc và tên đã match
                            if ('coke' in original_name_lower or 'coca' in original_name_lower) or ('coke' in full_name.lower() or 'coca' in full_name.lower()):
                                # Loại trừ Coke Light và Coke Zero (có lượng đường < 10g)
                                exclude_keywords = ['light', 'zero', 'ít đường', 'không đường', 'it duong', 'khong duong', 'less sugar', 'no sugar']
                                # Check trong cả tên gốc và tên đã match
                                is_coke_light_or_zero = (any(exclude_kw in original_name_lower for exclude_kw in exclude_keywords) or
                                                         any(exclude_kw in full_name.lower() for exclude_kw in exclude_keywords))
                                if not is_coke_light_or_zero:
                                    is_alcohol = True
                                    # Log để rõ ràng
                                    print(f"⚠️  PHÁT HIỆN COKE (10% đường) - Mã HĐ: {current_invoice.get('invoice_id', 'N/A')} | Món: {full_name} | Tính thuế 10% (giống bia/rượu)")
                        
                        if is_alcohol:
                            # Log alcohol/beverage detection (bao gồm bia/rượu và Coke 10% đường)
                            original_amount = price_value * qty
                            invoice_id = current_invoice.get('invoice_id', 'N/A')
                            
                            # Xác định loại: bia/rượu hay Coke
                            item_name_lower = full_name.lower()
                            is_coke = ('coke' in item_name_lower or 'coca' in item_name_lower) and group_name not in alcohol_groups
                            item_type = "COKE (10% đường)" if is_coke else "BIA/RƯỢU"
                            
                            alcohol_items_found.append({
                                'invoice_id': invoice_id,
                                'alcohol_name': full_name,
                                'quantity': qty,
                                'unit': clean_unit,
                                'price': price_value,
                                'total_amount': original_amount
                            })
                            
                            # Tính thuế 10% (áp dụng cho cả bia/rượu và Coke 10% đường)
                            tax_10_percent = price_value * 0.10
                            total_with_10_tax = price_value * 1.10
                            
                            print(f"⚠️  PHÁT HIỆN {item_type} - Mã HĐ: {invoice_id} | Món: {full_name} | SL: {qty} | Giá: {price_value:,.0f}đ | Tổng: {original_amount:,.0f}đ")
                            print(f"   Thuế 10%: {tax_10_percent:,.0f}đ | Tổng với thuế 10%: {total_with_10_tax:,.0f}đ")
                            
                            # Replace with food item: thêm số tiền bằng thuế 10% để tổng đủ sau thuế 8%
                            # Áp dụng cho cả bia/rượu và Coke 10% đường
                            full_name, clean_unit, adjusted_price = find_replacement_for_alcohol(
                                full_name, price_value, price_to_items)
                            price_value = adjusted_price
                            
                            # Tính lại để kiểm tra
                            replacement_total_with_8_tax = adjusted_price * 1.08
                            print(f"   → Đã thay bằng: {full_name} | Giá mới: {price_value:,.0f}đ (đã thêm {tax_10_percent:,.0f}đ = thuế 10% của {item_type.lower()})")
                            print(f"   → Tổng sau thuế 8%: {replacement_total_with_8_tax:,.0f}đ (bằng tổng {item_type.lower()} với thuế 10%: {total_with_10_tax:,.0f}đ)")
                        
                        current_invoice['items'].append({
                            'name': full_name,
                            'quantity': qty,
                            'unit': clean_unit,
                            'price': price_value
                        })
                        
                except (ValueError, IndexError):
                    continue
    
    # Apply discounts
    for invoice in invoices:
        if len(invoice['items']) == 0:
            continue
            
        total_discount = invoice['discount'] + invoice['payment_discount']
        
        # Bỏ qua giảm giá quá nhỏ (có thể là parse sai)
        if total_discount > 0 and total_discount < 1000:
            # Giảm giá < 1000đ có thể là parse sai, bỏ qua
            continue
        
        if total_discount > 0 and len(invoice['items']) > 0:
            # Tính tổng giá trị tất cả các món
            total_items_value = sum(item['quantity'] * item['price'] for item in invoice['items'])
            
            if total_items_value > 0:
                # VALIDATION: Chỉ áp dụng giảm giá nếu hợp lý
                # - Giảm giá không được vượt quá 50% tổng giá trị (tránh parse sai)
                # - Giảm giá phải nhỏ hơn tổng giá trị
                max_reasonable_discount = total_items_value * 0.5  # Tối đa 50%
                
                if total_discount > max_reasonable_discount:
                    # Nếu giảm giá quá lớn, có thể là parse sai - bỏ qua
                    print(f"⚠️  Cảnh báo: Hóa đơn {invoice['invoice_id']} có giảm giá bất thường ({total_discount:,.0f}đ > 50% tổng {total_items_value:,.0f}đ). Bỏ qua phân bổ giảm giá.")
                    continue
                
                if total_discount >= total_items_value:
                    # Giảm giá >= tổng giá trị là không hợp lý
                    print(f"⚠️  Cảnh báo: Hóa đơn {invoice['invoice_id']} có giảm giá >= tổng giá trị. Bỏ qua phân bổ giảm giá.")
                    continue
                
                # CHỈ ÁP DỤNG GIẢM GIÁ CHO 1 MÓN (món có giá trị cao nhất)
                # Tìm món có giá trị cao nhất để áp dụng giảm giá
                target_item = max(invoice['items'], 
                                key=lambda x: x['quantity'] * x['price'])
                
                target_item_total = target_item['quantity'] * target_item['price']
                
                # Đảm bảo giảm giá không vượt quá 90% giá trị món (để giá > 0)
                max_discount_for_item = min(total_discount, target_item_total * 0.9)
                
                # Tính giá mới cho món được chọn
                new_item_total = target_item_total - max_discount_for_item
                new_price = max(new_item_total / target_item['quantity'], 1.0)  # Giá tối thiểu là 1 đồng
                
                # Áp dụng giá mới
                old_price = target_item['price']
                target_item['price'] = new_price
                
                # Log thông tin
                print(f"   💰 HĐ {invoice['invoice_id']}: Áp dụng giảm giá {max_discount_for_item:,.0f}đ cho món '{target_item['name']}' (giá: {old_price:,.0f}đ → {new_price:,.0f}đ)")
                
                # Nếu giảm giá còn thừa (do giới hạn 90%), cảnh báo
                remaining_discount = total_discount - max_discount_for_item
                if remaining_discount > 1:
                    print(f"   ⚠️  Cảnh báo: Còn {remaining_discount:,.0f}đ giảm giá chưa được áp dụng (do giới hạn 90% giá trị món)")
                
                # Validation: Kiểm tra tổng sau giảm giá có hợp lý không
                final_total_after_discount = sum(item['quantity'] * item['price'] for item in invoice['items'])
                # Tính expected_final dựa trên giảm giá thực tế đã áp dụng (có thể nhỏ hơn total_discount nếu bị giới hạn)
                actual_discount_applied = total_items_value - final_total_after_discount
                expected_final = total_items_value - max_discount_for_item
                diff = abs(final_total_after_discount - expected_final)
                
                if diff > 1000:  # Chênh lệch > 1000đ là bất thường
                    print(f"⚠️  Cảnh báo: Hóa đơn {invoice['invoice_id']} sau giảm giá có chênh lệch lớn ({diff:,.0f}đ). Có thể giảm giá bị parse sai.")
    
    # Filter empty invoices
    invoices = [inv for inv in invoices if len(inv['items']) > 0]
    
    # Print summary of alcohol items found
    if alcohol_items_found:
        print("\n" + "=" * 70)
        print("📋 TỔNG HỢP BIA/RƯỢU ĐÃ PHÁT HIỆN VÀ THAY THẾ")
        print("=" * 70)
        total_alcohol_amount = 0
        for item in alcohol_items_found:
            print(f"   Mã HĐ: {item['invoice_id']:<10} | {item['alcohol_name']:<40} | SL: {item['quantity']:<3} | Tổng: {item['total_amount']:>12,.0f}đ")
            total_alcohol_amount += item['total_amount']
        print("-" * 70)
        print(f"   Tổng số hóa đơn có bia/rượu: {len(set(item['invoice_id'] for item in alcohol_items_found))}")
        print(f"   Tổng số món bia/rượu: {len(alcohol_items_found)}")
        print(f"   Tổng tiền bia/rượu: {total_alcohol_amount:,.0f}đ")
        print("=" * 70)
        print("💡 Vui lòng kiểm tra lại các hóa đơn trên hệ thống!\n")
    
    return invoices, alcohol_items_found

# ============================================================================
# GRAB INVOICE FUNCTIONS
# ============================================================================

def generate_random_items_with_target(menu_items, target_amount_before_tax, min_items=20, max_items=30):
    """Generate random menu items với INTEGER quantities để match target amount"""
    
    # Filter out alcoholic beverages
    alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 'whisky', 'vodka']
    menu_items = [item for item in menu_items 
                  if not any(keyword in item['name'].lower() for keyword in alcohol_keywords)]
    
    # Check menu size to adjust parameters
    menu_size = len(menu_items)
    is_small_menu = menu_size < 150  # Taco Place has ~123 items
    
    # Adjust parameters based on target amount and menu size
    if target_amount_before_tax > 5000000:
        if is_small_menu:
            min_items = max(20, min_items)  # Reduce min for small menus
            max_items = min(30, menu_size - 5)  # Cap max_items based on menu size
        else:
            min_items = max(25, min_items)
            max_items = min(40, len(menu_items))
        num_attempts = 200
    elif target_amount_before_tax > 2000000:
        if is_small_menu:
            min_items = max(18, min_items)
            max_items = min(28, menu_size - 5)
        else:
            min_items = max(20, min_items)
            max_items = 35
        num_attempts = 100
    else:
        if is_small_menu:
            min_items = max(18, min_items)
            max_items = min(25, menu_size - 5)
        else:
            min_items = max(20, min_items)
            max_items = 30
        num_attempts = 50
    
    best_result = None
    best_diff = float('inf')
    
    # Find tacos and burritos to ensure they're always included
    required_items = []
    tacos = [item for item in menu_items if 'taco' in item['name'].lower()]
    burritos = [item for item in menu_items if 'burrito' in item['name'].lower()]
    
    if tacos:
        required_items.append(random.choice(tacos))
    if burritos:
        required_items.append(random.choice(burritos))
    
    required_items = list({item['name']: item for item in required_items}.values())
    num_required = len(required_items)
    num_attempts = num_attempts * 5
    
    for attempt in range(num_attempts):
        num_additional_items = random.randint(min_items - num_required, max_items - num_required)
        avg_price_needed = target_amount_before_tax / (num_additional_items + num_required)
        available_items = [item for item in menu_items if item not in required_items]
        
        if target_amount_before_tax > 3000000:
            sorted_by_price = sorted(available_items, key=lambda x: x['price'], reverse=True)
            if is_small_menu:
                # For small menus, use larger pool (up to 70% instead of 50%)
                pool_size = max(num_additional_items * 3, int(len(available_items) * 0.7))
            else:
                pool_size = max(num_additional_items * 3, len(available_items) // 2)
            pool = sorted_by_price[:pool_size]
            if len(pool) < num_additional_items:
                # If pool too small, use all available items
                selected_additional = random.sample(available_items, min(num_additional_items, len(available_items)))
            else:
                selected_additional = random.sample(pool, min(num_additional_items, len(pool)))
        elif target_amount_before_tax > 1000000:
            # For medium invoices, use more flexible price range for small menus
            if is_small_menu:
                # Wider price range for small menus: 0.2x to 3x instead of 0.3x to 2.5x
                suitable_items = [item for item in available_items 
                                if avg_price_needed * 0.2 <= item['price'] <= avg_price_needed * 3.0]
            else:
                suitable_items = [item for item in available_items 
                                if avg_price_needed * 0.3 <= item['price'] <= avg_price_needed * 2.5]
            if len(suitable_items) >= num_additional_items:
                selected_additional = random.sample(suitable_items, num_additional_items)
            else:
                selected_additional = suitable_items.copy()
                remaining_needed = num_additional_items - len(suitable_items)
                remaining_pool = [item for item in available_items if item not in suitable_items]
                if remaining_needed > 0 and remaining_pool:
                    selected_additional.extend(random.sample(remaining_pool, min(remaining_needed, len(remaining_pool))))
                # If still not enough, use all available items
                if len(selected_additional) < num_additional_items:
                    remaining_needed = num_additional_items - len(selected_additional)
                    if remaining_needed > 0 and len(available_items) > len(selected_additional):
                        additional = random.sample([item for item in available_items if item not in selected_additional], 
                                                  min(remaining_needed, len(available_items) - len(selected_additional)))
                        selected_additional.extend(additional)
        else:
            sorted_by_price = sorted(available_items, key=lambda x: x['price'])
            if is_small_menu:
                pool_size = max(num_additional_items * 2, int(len(available_items) * 0.6))
            else:
                pool_size = max(num_additional_items * 3, len(available_items) // 2)
            pool = sorted_by_price[:pool_size]
            if len(pool) < num_additional_items:
                selected_additional = random.sample(available_items, min(num_additional_items, len(available_items)))
            else:
                selected_additional = random.sample(pool, min(num_additional_items, len(pool)))
        
        selected_items = required_items + selected_additional
        result = []
        remaining = target_amount_before_tax
        sorted_items = sorted(selected_items, key=lambda x: x['price'], reverse=True)
        
        avg_price = sum(item['price'] for item in sorted_items) / len(sorted_items)
        estimated_avg_qty = target_amount_before_tax / (len(sorted_items) * avg_price)
        default_max_qty = min(5, max(2, int(estimated_avg_qty * 1.5))) if len(sorted_items) >= 20 else 9
        
        # Calculate max price adjustment based on target amount
        # For large invoices, allow larger adjustments
        if target_amount_before_tax > 9000000:
            max_price_adjustment = min(200000, target_amount_before_tax * 0.02)  # Up to 2% or 200k
        elif target_amount_before_tax > 5000000:
            max_price_adjustment = min(100000, target_amount_before_tax * 0.015)  # Up to 1.5% or 100k
        elif target_amount_before_tax > 2000000:
            max_price_adjustment = min(50000, target_amount_before_tax * 0.01)  # Up to 1% or 50k
        elif target_amount_before_tax > 1000000:
            max_price_adjustment = 30000
        else:
            max_price_adjustment = 10000
        
        for i, item in enumerate(sorted_items):
            if i == len(sorted_items) - 1:
                # Last item: không điều chỉnh giá, chỉ điều chỉnh số lượng để đạt chính xác 100%
                # Giữ nguyên giá gốc (hoặc điều chỉnh tối đa 10,000 VND nếu cần)
                original_price = item['price']
                
                # Tính số lượng chính xác cần thiết
                ideal_quantity = remaining / original_price
                
                # Nếu số lượng là số nguyên hoặc gần số nguyên, dùng số lượng đó
                if abs(ideal_quantity - round(ideal_quantity)) < 0.0001:
                    quantity = round(ideal_quantity)
                    adjusted_price = original_price
                else:
                    # Nếu không phải số nguyên, điều chỉnh giá nhỏ nhất có thể (tối đa 10,000 VND)
                    # hoặc làm tròn số lượng và tính lại giá
                    rounded_qty = max(1, round(ideal_quantity))
                    adjusted_price_per_item = remaining / rounded_qty
                    price_diff = abs(adjusted_price_per_item - original_price)
                    
                    # Nếu điều chỉnh giá <= 10,000 VND thì được phép
                    if price_diff <= 10000:
                        adjusted_price = adjusted_price_per_item
                        quantity = rounded_qty
                    else:
                        # Nếu cần điều chỉnh > 10,000 VND, thử tăng số lượng để giảm điều chỉnh giá
                        best_qty = rounded_qty
                        best_price = original_price
                        best_diff = abs(remaining - (original_price * rounded_qty))
                        
                        # Thử với số lượng lớn hơn để giảm điều chỉnh giá
                        max_qty_to_try = min(100, int(remaining / original_price) + 10)
                        for qty_try in range(rounded_qty + 1, max_qty_to_try + 1):
                            price_per_item = remaining / qty_try
                            price_adjustment = abs(price_per_item - original_price)
                            total_with_qty = price_per_item * qty_try
                            diff = abs(remaining - total_with_qty)
                            
                            # Ưu tiên giải pháp có điều chỉnh giá <= 10,000 VND
                            if price_adjustment <= 10000:
                                if diff < best_diff or best_price == original_price:
                                    best_qty = qty_try
                                    best_price = price_per_item
                                    best_diff = diff
                                    if diff < 0.01:  # Đạt chính xác 100%
                                        break
                        
                        # Nếu không tìm được giải pháp với điều chỉnh <= 10,000 VND
                        # thì dùng giải pháp tốt nhất (vẫn điều chỉnh giá nhưng cố gắng giảm thiểu)
                        if best_price == original_price:
                            # Nếu không tìm được, giữ nguyên giá và làm tròn số lượng
                            quantity = max(1, round(ideal_quantity))
                            adjusted_price = original_price
                        else:
                            quantity = best_qty
                            adjusted_price = best_price
                
                # Đảm bảo giá tối thiểu là 1000 VND
                if adjusted_price < 1000:
                    adjusted_price = 1000
                
                # Đảm bảo số lượng >= 1
                quantity = max(1, quantity)
                
                result.append({
                    'name': item['name'],
                    'unit': item['unit'],
                    'price': adjusted_price,
                    'quantity': quantity
                })
                remaining = 0
            else:
                items_left = len(sorted_items) - i
                
                # For second-to-last item, reserve budget for last item more accurately
                if i == len(sorted_items) - 2:
                    last_item = sorted_items[-1]
                    last_item_base_price = last_item['price']
                    # Reserve enough for last item with potential adjustment and quantity
                    # For large invoices, last item might need quantity up to 10-15
                    max_last_item_total = last_item_base_price * 15 + max_price_adjustment * 15
                    # But don't reserve more than 40% of remaining
                    target_remaining_for_last = min(max_last_item_total, remaining * 0.4)
                    # Ensure at least enough for base price + max adjustment
                    target_remaining_for_last = max(target_remaining_for_last, last_item_base_price + max_price_adjustment)
                    this_item_budget = remaining - target_remaining_for_last
                    
                    if this_item_budget > item['price']:
                        max_affordable = min(int(this_item_budget / item['price']), default_max_qty)
                    else:
                        max_affordable = 1
                else:
                    avg_per_item = remaining / items_left
                    target_qty = avg_per_item / item['price']
                    max_qty = min(default_max_qty, max(1, int(target_qty * 2)))
                    max_affordable = min(max_qty, int(remaining / item['price']))
                
                if max_affordable >= 1:
                    if i == len(sorted_items) - 2:
                        # For second-to-last, be more conservative
                        avg_per_item = this_item_budget / max(1, max_affordable)
                        target_qty = avg_per_item / item['price']
                        quantity = min(max_affordable, max(1, int(target_qty)))
                    else:
                        avg_per_item = remaining / items_left
                        target_qty = avg_per_item / item['price']
                        if target_qty >= 1:
                            quantity = min(max_affordable, max(1, int(target_qty)))
                        else:
                            quantity = min(max_affordable, random.randint(1, 2))
                else:
                    quantity = 1
                
                item_total = quantity * item['price']
                remaining -= item_total
                
                result.append({
                    'name': item['name'],
                    'unit': item['unit'],
                    'price': item['price'],
                    'quantity': quantity
                })
        
        actual_total = sum(item['price'] * item['quantity'] for item in result)
        diff = abs(target_amount_before_tax - actual_total)
        
        if len(result) > 0:
            last_item_original_price = sorted_items[-1]['price']
            last_item_adjusted_price = result[-1]['price']
            last_item_adjustment = abs(last_item_adjusted_price - last_item_original_price)
            # Không được điều chỉnh giá món cuối quá 10,000 VND
            # Ưu tiên điều chỉnh số lượng để đạt chính xác 100%
            within_adjustment_limit = last_item_adjustment <= 10000
        else:
            within_adjustment_limit = False
        
        if within_adjustment_limit:
            if diff < best_diff or best_diff == float('inf'):
                best_diff = diff
                best_result = result
                if diff < 0.01:  # Đạt chính xác 100%
                    break
        else:
            # Nếu vượt quá giới hạn, vẫn lưu nhưng đánh dấu để tìm giải pháp tốt hơn
            if best_result is None or (best_diff > 50000 and diff < best_diff):
                best_diff = diff
                best_result = result
    
    return best_result

def create_grab_invoice(total_with_tax, menu_items, date_str=None, invoice_number=None):
    """Tạo file hóa đơn Grab với món ăn random từ menu"""
    
    try:
        total_with_tax = float(total_with_tax)
        if total_with_tax <= 0:
            raise ValueError("Tổng tiền phải lớn hơn 0")
    except (ValueError, TypeError) as e:
        print(f"❌ Lỗi: Số tiền không hợp lệ - {e}")
        return None
    
    if date_str is None:
        date_str = datetime.now().strftime("%d/%m/%Y")
    
    if invoice_number is None:
        invoice_number = f"GRAB_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    amount_before_tax = total_with_tax / 1.08
    vat_amount = total_with_tax - amount_before_tax
    
    print(f"\n💰 Phân tích doanh thu Grab:")
    print(f"   Tổng tiền (có thuế 8%):  {total_with_tax:,.0f} VND")
    print(f"   Tiền trước thuế:         {amount_before_tax:,.2f} VND")
    print(f"   Thuế VAT (8%):           {vat_amount:,.2f} VND")
    
    max_retries = 20
    items = None
    
    # Không được điều chỉnh giá món cuối quá 10,000 VND
    # Ưu tiên điều chỉnh số lượng để đạt chính xác 100%
    max_price_adjustment = 10000
    
    for retry in range(max_retries):
        items = generate_random_items_with_target(menu_items, amount_before_tax)
        if items and len(items) > 0:
            last_item_name = items[-1]['name']
            last_item_original = [m for m in menu_items if m['name'] == last_item_name]
            if last_item_original:
                last_item_original_price = last_item_original[0]['price']
                last_item_actual_price = items[-1]['price']
                adjustment = abs(last_item_actual_price - last_item_original_price)
                actual_total = sum(item['price'] * item['quantity'] for item in items)
                diff = abs(amount_before_tax - actual_total)
                # Kiểm tra: điều chỉnh giá <= 10,000 VND và chênh lệch < 1 VND (chính xác 100%)
                if diff < 1 and adjustment <= max_price_adjustment:
                    break
    
    print(f"\n📋 Món ăn được chọn ({len(items)} món):")
    total_check = 0
    for item in items:
        item_total = item['price'] * item['quantity']
        total_check += item_total
        print(f"   • {item['name']}")
        print(f"     {item['quantity']} {item['unit']} × {item['price']:,.0f} = {item_total:,.2f} VND")
    
    print(f"\n   Tổng kiểm tra: {total_check:,.2f} VND")
    print(f"   Chênh lệch:    {abs(total_check - amount_before_tax):,.2f} VND")
    
    output_dir = script_dir / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    date_for_filename = date_str.replace('/', '-')
    output_file = output_dir / f"Grab - {date_for_filename} - {invoice_number}.xlsx"
    
    # Create workbook using existing function
    invoice_data = {
        'invoice_id': invoice_number,
        'date': date_str,
        'items': items
    }
    
    # Thêm phí dịch vụ vào hóa đơn Grab (nếu được bật)
    add_service_fee_to_invoice(invoice_data)
    
    create_invoice_file(invoice_data, str(output_file))
    
    return str(output_file)

def process_grab_invoice():
    """Interactive function để tạo Grab invoice"""
    print("\n" + "=" * 70)
    print("🏪 TẠO HÓA ĐƠN GRAB")
    print("=" * 70)
    
    # Load menus
    print("\n📚 Đang load menu...")
    all_menu_items, _, _ = load_menus()
    
    # Separate Simple Place and Taco Place based on source menu
    simple_menu_items = []
    taco_menu_items = []
    for item in all_menu_items:
        menu_source = item.get('menu_source', 'simple')  # Default to simple if not set
        if menu_source == 'taco':
            taco_menu_items.append(item)
        else:
            simple_menu_items.append(item)
    
    print(f"   ✓ Simple Place: {len(simple_menu_items)} món")
    print(f"   ✓ Taco Place: {len(taco_menu_items)} món")
    
    # Choose menu
    print("\n📋 Chọn menu:")
    print("   1. Simple Place")
    print("   2. Taco Place")
    
    while True:
        menu_choice = input("\nChọn menu (1 hoặc 2): ").strip()
        if menu_choice == '1':
            menu_items = simple_menu_items
            menu_name = "Simple Place"
            break
        elif menu_choice == '2':
            menu_items = taco_menu_items
            menu_name = "Taco Place"
            break
        else:
            print("❌ Vui lòng chọn 1 hoặc 2")
    
    # Get total amount
    while True:
        try:
            total_input = input("\n💵 Nhập tổng doanh thu Grab (đã bao gồm thuế 8%): ")
            if total_input.lower() in ['exit', 'quit', 'q']:
                print("👋 Quay lại menu chính...")
                return
            total_input = total_input.replace(',', '').replace('.', '').strip()
            total_with_tax = float(total_input)
            if total_with_tax <= 0:
                print("❌ Số tiền phải lớn hơn 0. Vui lòng thử lại.")
                continue
            break
        except ValueError:
            print("❌ Số tiền không hợp lệ. Vui lòng nhập lại (VD: 1080000)")
    
    # Get date (optional)
    date_input = input("📅 Nhập ngày (DD/MM/YYYY) hoặc Enter để dùng hôm nay: ").strip()
    date_str = date_input if date_input else None
    
    # Get invoice number (optional)
    invoice_input = input("🔢 Nhập số hóa đơn hoặc Enter để tự động: ").strip()
    invoice_number = invoice_input if invoice_input else None
    
    # Create invoice
    print("\n⏳ Đang tạo file...")
    output_file = create_grab_invoice(total_with_tax, menu_items, date_str, invoice_number)
    
    if output_file:
        print(f"\n✅ THÀNH CÔNG!")
        print(f"📁 File đã được tạo: {output_file}")
        print(f"\n💡 File sẵn sàng để upload lên website thuế!")

def process_sale_by_payment_method():
    """Process sale_by_payment_method files (combine and split)"""
    print("\n" + "=" * 70)
    print("🔄 XỬ LÝ SALE BY PAYMENT METHOD")
    print("=" * 70)
    
    file1 = DEFAULT_FILE1
    file2 = DEFAULT_FILE2
    
    file1_path = script_dir / file1
    file2_path = script_dir / file2
    
    if not file1_path.exists():
        print(f"\n❌ File không tồn tại: {file1}")
        return
    
    if not file2_path.exists():
        print(f"\n❌ File không tồn tại: {file2}")
        return
    
    print(f"\n📂 File 1 (transfer): {file1}")
    print(f"📂 File 2 (atm): {file2}")
    
    print(f"\n🔗 Đang kết hợp files...")
    content, _ = combine_files(str(file1_path), str(file2_path))
    print(f"   ✓ Đã kết hợp files")
    
    is_combined = True
    source_type = 'combined'
    
    # Load menus
    print(f"\n📚 Đang load menu...")
    all_menu_items, name_mapping, price_to_items = load_menus()
    print(f"   ✓ Tổng số món: {len(all_menu_items)}")
    
    # Parse invoices
    print(f"\n📖 Đang phân tích dữ liệu...")
    invoices, alcohol_items_found = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
    print(f"   ✓ Tìm thấy {len(invoices)} hóa đơn")
    
    if len(invoices) == 0:
        print("\n⚠️  Không tìm thấy hóa đơn nào!")
        return
    
    # Process invoices
    _process_and_save_invoices(invoices, source_type, alcohol_items_found)

def process_single_file():
    """Process single file"""
    print("\n" + "=" * 70)
    print("📄 XỬ LÝ FILE ĐƠN")
    print("=" * 70)
    
    input_file = input("\n📂 Nhập tên file (hoặc đường dẫn): ").strip()
    if not input_file:
        print("❌ Tên file không được để trống!")
        return
    
    input_path = script_dir / input_file
    
    if not input_path.exists():
        print(f"\n❌ File không tồn tại: {input_file}")
        print(f"   Đường dẫn đầy đủ: {input_path}")
        return
    
    print(f"\n📂 File input: {input_file}")
    
    # Detect source type
    input_basename = input_path.name.lower()
    if 'atm' in input_basename:
        source_type = 'atm'
    elif 'transfer' in input_basename:
        source_type = 'transfer'
    else:
        source_type = input_path.stem
    
    print(f"📋 Source type: {source_type}")
    
    # Load content
    with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    is_combined = 'sale_by_payment_method' in input_path.name.lower()
    
    # Load menus
    print(f"\n📚 Đang load menu...")
    all_menu_items, name_mapping, price_to_items = load_menus()
    print(f"   ✓ Tổng số món: {len(all_menu_items)}")
    
    # Parse invoices
    print(f"\n📖 Đang phân tích dữ liệu...")
    invoices, alcohol_items_found = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
    print(f"   ✓ Tìm thấy {len(invoices)} hóa đơn")
    
    if len(invoices) == 0:
        print("\n⚠️  Không tìm thấy hóa đơn nào!")
        return
    
    # Process invoices
    _process_and_save_invoices(invoices, source_type, alcohol_items_found)

def _process_and_save_invoices(invoices, source_type, alcohol_items_found=None):
    """Helper function để process và save invoices"""
    output_dir = script_dir / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📝 Đang tạo file cho từng hóa đơn...")
    print(f"    {'ID':<10} {'Món':<5} {'Tổng tiền':<15} {'Giảm giá':<30} {'Validate':<10}")
    print("   " + "-" * 80)
    
    total_created = 0
    validation_warnings = []
    alcohol_invoices_info = []  # Track invoices with alcohol for summary file
    
    # Kiểm tra và thông báo về phí dịch vụ
    if SERVICE_FEE_ENABLED:
        print(f"\n💰 Phí dịch vụ đã được bật: {SERVICE_FEE_PERCENTAGE * 100:.0f}% của tổng bill")
    
    for invoice in invoices:
        # Bước 1: Thêm phí dịch vụ vào hóa đơn (nếu được bật)
        # Phí dịch vụ = 8% của tổng bill TRƯỚC khi có phí dịch vụ (chưa có VAT)
        add_service_fee_to_invoice(invoice)
        
        # Bước 2: Tính tổng bill sau khi đã có phí dịch vụ (chưa có VAT)
        total = sum(item['quantity'] * item['price'] for item in invoice['items'])
        
        # Bước 3: Tính VAT 8% trên tổng bill đã có phí dịch vụ
        final_with_tax = total * 1.08
        total_str = f"{int(final_with_tax):,}".replace(',', '.')
        
        invoice_source_type = invoice.get('payment_method') or source_type
        
        filename = output_dir / f"{invoice['invoice_id']} - {invoice_source_type} - {total_str}đ.xlsx"
        create_invoice_file(invoice, str(filename))
        
        # Track if this invoice has alcohol
        if alcohol_items_found:
            invoice_has_alcohol = any(item['invoice_id'] == invoice['invoice_id'] for item in alcohol_items_found)
            if invoice_has_alcohol:
                alcohol_invoices_info.append({
                    'invoice_id': invoice['invoice_id'],
                    'date': invoice.get('date', ''),
                    'filename': filename.name,
                    'total_amount': final_with_tax,
                    'payment_method': invoice_source_type
                })
        
        expected_final = total * 1.08
        validation_status = "✓"
        if invoice['final_total'] > 0:
            diff = abs(expected_final - invoice['final_total'])
            if diff > 10:
                validation_status = f"⚠️ ±{diff:,.0f}"
                validation_warnings.append({
                    'id': invoice['invoice_id'],
                    'calculated': expected_final,
                    'actual': invoice['final_total'],
                    'diff': diff
                })
        else:
            validation_status = "N/A"
        
        discount_info = ""
        if invoice['discount'] > 0 or invoice['payment_discount'] > 0:
            discount_info = f"GG: {invoice['discount']:>7,.0f} + CK: {invoice['payment_discount']:>7,.0f}"
        
        print(f"   #{invoice['invoice_id']:<10} {len(invoice['items']):>3}  {total:>13,.0f}đ  {discount_info:<30} {validation_status}")
        total_created += 1
    
    # Show warnings
    if validation_warnings:
        print("\n" + "⚠️  " + "=" * 68)
        print("   CẢNH BÁO: Một số hóa đơn có chênh lệch:")
        print("   " + "-" * 68)
        for warn in validation_warnings:
            print(f"   Invoice #{warn['id']}: Tính = {warn['calculated']:,.0f}đ | Data = {warn['actual']:,.0f}đ | Chênh = {warn['diff']:,.0f}đ")
        print("   " + "=" * 68)
    
    # Không tạo file Excel tổng hợp bia/rượu nữa - chỉ hiển thị trên web
    if alcohol_invoices_info:
        print(f"\n📋 Tổng hợp: {len(alcohol_invoices_info)} hóa đơn có bia/rượu đã được thay thế")
        print(f"   💡 Thông tin chi tiết xem trên trang web")
    
    print("\n" + "=" * 70)
    print(f"✅ HOÀN THÀNH!")
    print(f"📁 Thư mục: {OUTPUT_DIR}/")
    print(f"📊 Tổng số file: {total_created}")
    print("=" * 70)

# ============================================================================
# TẠO FILE EXCEL TỔNG HỢP BIA/RƯỢU
# ============================================================================

def create_alcohol_summary_file(alcohol_invoices_info, alcohol_items_found, output_dir):
    """Tạo file Excel tổng hợp các hóa đơn có bia/rượu đã được thay thế - ĐÃ BỎ"""
    # Function này đã được bỏ - không tạo file Excel nữa, chỉ hiển thị trên web
    return None
    
    # Create filename with current date - đặt ở thư mục gốc, không phải trong tax_files
    date_str = datetime.now().strftime("%Y%m%d")
    summary_filename = PROJECT_ROOT / f"TONG_HOP_BIARUOU_{date_str}.xlsx"
    
    workbook = xlsxwriter.Workbook(str(summary_filename))
    worksheet = workbook.add_worksheet("Danh sách hóa đơn")
    
    # Formats
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#4472C4',
        'font_color': '#FFFFFF',
        'border': 1,
        'align': 'center',
        'valign': 'vcenter'
    })
    cell_format = workbook.add_format({'border': 1, 'align': 'left'})
    number_format = workbook.add_format({'border': 1, 'num_format': '#,##0', 'align': 'right'})
    date_format = workbook.add_format({'border': 1, 'num_format': 'dd/mm/yyyy', 'align': 'center'})
    
    # Set column widths
    worksheet.set_column('A:A', 12)  # Mã HĐ
    worksheet.set_column('B:B', 12)  # Ngày
    worksheet.set_column('C:C', 50)  # Tên file
    worksheet.set_column('D:D', 15)  # Tổng tiền
    worksheet.set_column('E:E', 15)  # Phương thức
    worksheet.set_column('F:F', 40)  # Món bia/rượu
    worksheet.set_column('G:G', 8)   # Số lượng
    worksheet.set_column('H:H', 15)  # Giá
    worksheet.set_column('I:I', 15)  # Tổng món
    
    # Headers
    headers = [
        'Mã Hóa Đơn',
        'Ngày',
        'Tên File',
        'Tổng Tiền HĐ',
        'Phương Thức',
        'Món Bia/Rượu',
        'Số Lượng',
        'Đơn Giá',
        'Tổng Tiền Món'
    ]
    
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    # Write data
    row = 1
    for invoice_info in alcohol_invoices_info:
        invoice_id = invoice_info['invoice_id']
        # Find all alcohol items for this invoice
        invoice_alcohol_items = [item for item in alcohol_items_found if item['invoice_id'] == invoice_id]
        
        if invoice_alcohol_items:
            # First row with invoice info
            worksheet.write(row, 0, invoice_id, cell_format)
            worksheet.write(row, 1, invoice_info.get('date', ''), date_format)
            worksheet.write(row, 2, invoice_info['filename'], cell_format)
            worksheet.write(row, 3, invoice_info['total_amount'], number_format)
            worksheet.write(row, 4, invoice_info['payment_method'].upper(), cell_format)
            
            # First alcohol item
            first_item = invoice_alcohol_items[0]
            worksheet.write(row, 5, first_item['alcohol_name'], cell_format)
            worksheet.write(row, 6, first_item['quantity'], number_format)
            worksheet.write(row, 7, first_item['price'], number_format)
            worksheet.write(row, 8, first_item['total_amount'], number_format)
            row += 1
            
            # Additional alcohol items for same invoice
            for item in invoice_alcohol_items[1:]:
                worksheet.write(row, 5, item['alcohol_name'], cell_format)
                worksheet.write(row, 6, item['quantity'], number_format)
                worksheet.write(row, 7, item['price'], number_format)
                worksheet.write(row, 8, item['total_amount'], number_format)
                row += 1
    
    # Add summary row
    row += 1
    summary_format = workbook.add_format({
        'bold': True,
        'bg_color': '#FFC000',
        'border': 1
    })
    worksheet.write(row, 0, 'TỔNG CỘNG', summary_format)
    worksheet.write(row, 1, '', summary_format)
    worksheet.write(row, 2, '', summary_format)
    total_invoices = sum(inv['total_amount'] for inv in alcohol_invoices_info)
    worksheet.write(row, 3, total_invoices, workbook.add_format({
        'bold': True,
        'bg_color': '#FFC000',
        'border': 1,
        'num_format': '#,##0',
        'align': 'right'
    }))
    worksheet.write(row, 4, '', summary_format)
    worksheet.write(row, 5, '', summary_format)
    worksheet.write(row, 6, '', summary_format)
    worksheet.write(row, 7, '', summary_format)
    total_alcohol = sum(item['total_amount'] for item in alcohol_items_found)
    worksheet.write(row, 8, total_alcohol, workbook.add_format({
        'bold': True,
        'bg_color': '#FFC000',
        'border': 1,
        'num_format': '#,##0',
        'align': 'right'
    }))
    
    # Add note sheet
    note_sheet = workbook.add_worksheet("Ghi chú")
    note_sheet.set_column('A:A', 80)
    note_format = workbook.add_format({'text_wrap': True, 'valign': 'top'})
    note_sheet.write(0, 0, 'GHI CHÚ:', workbook.add_format({'bold': True}))
    note_sheet.write(1, 0, 
        'File này tổng hợp các hóa đơn có chứa bia/rượu đã được thay thế bằng món ăn khác.\n\n'
        'Các hóa đơn trong danh sách đã được điều chỉnh:\n'
        '- Thay thế bia/rượu bằng món ăn khác\n'
        '- Điều chỉnh thuế từ 10% xuống 8%\n'
        '- Tổng tiền cuối cùng được giữ nguyên\n\n'
        'Vui lòng kiểm tra lại các hóa đơn trên hệ thống trước khi gửi khách hàng.',
        note_format)
    
    workbook.close()
    return summary_filename

# ============================================================================
# THÊM PHÍ DỊCH VỤ
# ============================================================================

def add_service_fee_to_invoice(invoice):
    """
    Thêm phí dịch vụ vào hóa đơn nếu được bật (chỉ hôm nay).
    
    LƯU Ý QUAN TRỌNG: Hàm này được gọi SAU KHI đã thay thế bia/rượu bằng món ăn.
    Phí dịch vụ được tính trên tổng bill ĐÃ THAY THẾ bia/rượu (không thay đổi gì).
    
    Thứ tự tính toán:
    1. Tổng bill các món (chưa có VAT, chưa có phí dịch vụ, ĐÃ THAY THẾ bia/rượu)
    2. Tính phí dịch vụ = 8% của tổng bill ở bước 1
    3. Thêm phí dịch vụ vào items như một món ăn (số lượng 1)
    4. Sau đó, khi tính tổng bill cuối cùng (bao gồm phí dịch vụ), sẽ tính VAT 8% trên tổng đó
    
    Phí dịch vụ được thêm như một món ăn với số lượng 1.
    """
    # Kiểm tra xem phí dịch vụ có được bật không
    if not SERVICE_FEE_ENABLED:
        return False
    
    # Bước 1: Tính tổng giá trị các món ăn (TRƯỚC khi thêm phí dịch vụ, chưa có VAT)
    # LƯU Ý: Tổng bill này đã bao gồm các món đã được thay thế bia/rượu (nếu có)
    total_bill_before_service_fee = sum(item['quantity'] * item['price'] for item in invoice['items'])
    
    # Nếu không có món nào, không thêm phí dịch vụ
    if total_bill_before_service_fee <= 0:
        return False
    
    # Bước 2: Tính phí dịch vụ = 8% của tổng bill (chưa có VAT, chưa có phí dịch vụ)
    service_fee_amount = total_bill_before_service_fee * SERVICE_FEE_PERCENTAGE
    
    # Làm tròn về số nguyên (VND)
    service_fee_amount = round(service_fee_amount)
    
    # Nếu phí dịch vụ = 0, không thêm
    if service_fee_amount <= 0:
        return False
    
    # Bước 3: Thêm phí dịch vụ vào đầu danh sách items như một món ăn
    # Lưu ý: Phí dịch vụ không cần đơn vị, nhưng vẫn cần số lượng = 1
    service_fee_item = {
        'name': SERVICE_FEE_NAME,
        'quantity': 1,  # Số lượng = 1
        'unit': SERVICE_FEE_UNIT,  # Để trống
        'price': service_fee_amount  # Giá phí dịch vụ
    }
    
    # Thêm vào đầu danh sách
    invoice['items'].insert(0, service_fee_item)
    
    # Log để debug
    invoice_id = invoice.get('invoice_id', 'N/A')
    print(f"   💰 HĐ {invoice_id}: Đã thêm phí dịch vụ {service_fee_amount:,.0f}đ (8% của {total_bill_before_service_fee:,.0f}đ)")
    
    # Bước 4: VAT 8% sẽ được tính sau (trong _process_and_save_invoices) trên tổng bill đã có phí dịch vụ
    
    return True

# ============================================================================
# TẠO FILE EXCEL
# ============================================================================

def create_invoice_file(invoice, output_file):
    """Tạo file Excel"""
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    
    header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9', 'border': 1})
    cell_format = workbook.add_format({'border': 1})
    number_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00'})
    
    worksheet.set_column('A:A', 11.57)
    worksheet.set_column('B:B', 9.14)
    worksheet.set_column('C:C', 26.57)
    worksheet.set_column('D:D', 13.71)
    worksheet.set_column('E:E', 11.29)
    worksheet.set_column('F:F', 11)
    
    headers = ['Tinh_chat', 'Ma_so', 'Ten_san_pham', 'Don_vi_tinh', 'So_luong', 'Don_gia']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, header_format)
    
    for row_idx, item in enumerate(invoice['items'], 1):
        # Đảm bảo tên món có format đúng trước khi ghi vào file
        item_name = item['name']
        
        # Phí dịch vụ không cần format "Tiếng Việt / Tiếng Anh", giữ nguyên tên
        is_service_fee = item_name == SERVICE_FEE_NAME or 'Phí dịch vụ' in item_name
        
        if not is_service_fee:
            if ' / ' not in item_name:
                item_name = fix_item_name_format(item_name)
                if ' / ' not in item_name:
                    item_name = f"{item_name} / {item_name}"
        
        worksheet.write(row_idx, 0, 1, cell_format)
        worksheet.write(row_idx, 1, '', cell_format)
        worksheet.write(row_idx, 2, item_name, cell_format)
        # Phí dịch vụ: để trống đơn vị, nhưng vẫn có số lượng = 1
        unit_value = item['unit'] if item['unit'] else ''
        worksheet.write(row_idx, 3, unit_value, cell_format)
        # Số lượng = 1 cho phí dịch vụ
        worksheet.write(row_idx, 4, float(item['quantity']), number_format)
        worksheet.write(row_idx, 5, float(item['price']), number_format)
    
    workbook.close()

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Main function với menu chọn option"""
    
    print("=" * 70)
    print("🧾 PHẦN MỀM XỬ LÝ HÓA ĐƠN")
    print("=" * 70)
    
    # Check if command line argument provided (backward compatibility)
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        input_path = script_dir / input_file
        
        if not input_path.exists():
            print(f"\n❌ File không tồn tại: {input_file}")
            sys.exit(1)
        
        # Load menus
        print(f"\n📚 Đang load menu...")
        all_menu_items, name_mapping, price_to_items = load_menus()
        
        # Load content
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        input_basename = input_path.name.lower()
        if 'atm' in input_basename:
            source_type = 'atm'
        elif 'transfer' in input_basename:
            source_type = 'transfer'
        else:
            source_type = input_path.stem
        
        is_combined = 'sale_by_payment_method' in input_path.name.lower()
        invoices, alcohol_items_found = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
        _process_and_save_invoices(invoices, source_type, alcohol_items_found)
        return
    
    # Interactive menu
    while True:
        print("\n" + "=" * 70)
        print("📋 MENU CHÍNH")
        print("=" * 70)
        print("\nChọn chức năng:")
        print("   1. 🔄 Xử lý Sale by Payment Method (kết hợp và tách)")
        print("   2. 📄 Xử lý file đơn")
        print("   3. 🏪 Tạo hóa đơn Grab")
        print("   0. ❌ Thoát")
        
        choice = input("\n👉 Chọn option (0-3): ").strip()
        
        if choice == '0':
            print("\n👋 Tạm biệt!")
            break
        elif choice == '1':
            process_sale_by_payment_method()
        elif choice == '2':
            process_single_file()
        elif choice == '3':
            process_grab_invoice()
        else:
            print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 0-3.")

if __name__ == "__main__":
    main()

