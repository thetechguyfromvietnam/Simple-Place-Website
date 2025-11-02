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

# Import parse_menu
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from Menu.parse_menu import parse_excel_menu

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
    
    for item in all_items:
        full_name = item['name']
        price = item['price']
        
        # Extract English part (sau dấu /)
        if ' / ' in full_name:
            parts = full_name.split(' / ')
            english_name = parts[-1].strip().lower()
            # If duplicate, prefer the first one found (Simple Place takes precedence)
            if english_name not in name_mapping:
                name_mapping[english_name] = full_name
        
        # Map cả tên đầy đủ (prefer Simple Place if duplicate)
        full_name_lower = full_name.lower()
        if full_name_lower not in name_mapping:
            name_mapping[full_name_lower] = full_name
        
        # Tạo price mapping cho món không phải bia/rượu
        alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 
                           'whisky', 'vodka', 'carlsberg', 'craft']
        is_alcohol = any(kw in full_name.lower() for kw in alcohol_keywords)
        
        if not is_alcohol:
            if price not in price_to_items:
                price_to_items[price] = []
            price_to_items[price].append(item)
    
    return all_items, name_mapping, price_to_items

# ============================================================================
# XỬ LÝ THAY THẾ RƯỢU/BIA
# ============================================================================

def find_replacement_for_alcohol(alcohol_name, alcohol_price, price_to_items):
    """Tìm món thay thế không cồn và điều chỉnh giá cho thuế"""
    import random
    
    adjusted_price = alcohol_price * 1.10 / 1.08
    
    # Tìm món có giá gần với giá gốc
    for delta in [0, 5000, -5000, 10000, -10000, 15000, -15000, 20000, -20000]:
        nearby_price = alcohol_price + delta
        if nearby_price in price_to_items and len(price_to_items[nearby_price]) > 0:
            best_replacement = random.choice(price_to_items[nearby_price])
            return best_replacement['name'], best_replacement['unit'], adjusted_price
    
    # Fallback: chọn random
    if price_to_items:
        random_price = random.choice(list(price_to_items.keys()))
        replacement = random.choice(price_to_items[random_price])
        return replacement['name'], replacement['unit'], adjusted_price
    
    return alcohol_name, 'Lon', alcohol_price

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
    
    # Direct match
    for candidate in [raw_normalized, raw_without_s, raw_without_extra, raw_lower]:
        if candidate in name_mapping:
            return name_mapping[candidate]
    
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
            
            for i in range(max(0, len(cells) - 3)):
                try:
                    name = cells[i]
                    qty_candidate = cells[i + 1]
                    unit_candidate = cells[i + 2]
                    price_candidate = cells[i + 3]
                    
                    if not (qty_candidate.isdigit() and 1 <= int(qty_candidate) <= 100):
                        continue
                    
                    qty = int(qty_candidate)
                    price_clean = price_candidate.replace(' ', '').replace(',', '').replace('.', '')
                    if not price_clean.isdigit():
                        continue
                    
                    price_value = float(price_clean)
                    unit = unit_candidate if unit_candidate and not unit_candidate.isdigit() else 'Phần'
                    
                    if (len(name) < 2 or name.isdigit() or 
                        name in ['', 'STT', 'Mã hoá đơn', 'Simple Place']):
                        continue
                    
                    skip_patterns = [
                        r'\bcrispy\b', r'\bsoft\b', r'cut in 4', r'- edit\s*$',
                        r'đổi phương thức', r'\bpayment\b', r'\btransfer\b',
                        r'\bcod\b', r'\batm\b', 'background-color', 'vertical-align',
                        'ghi chú', 'giảm sốt'
                    ]
                    if any(re.search(pattern, name.lower()) for pattern in skip_patterns):
                        continue
                    
                    if (price_value >= 1000 and price_value <= 1000000 and 
                        qty >= 1 and qty <= 100 and len(name) > 2):
                        
                        clean_unit = unit.strip() if (unit.strip() and not unit.strip().isdigit()) else 'Phần'
                        full_name = match_menu_name(name.strip(), all_menu_items, name_mapping)
                        
                        alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 
                                          'rượu', 'wine', 'whisky', 'vodka', 'carlsberg', 'craft']
                        is_alcohol = any(kw in full_name.lower() for kw in alcohol_keywords)
                        
                        if is_alcohol:
                            full_name, clean_unit, adjusted_price = find_replacement_for_alcohol(
                                full_name, price_value, price_to_items)
                            price_value = adjusted_price
                        
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
        
        if total_discount > 0 and len(invoice['items']) > 0:
            sorted_items = sorted(invoice['items'], 
                                key=lambda x: x['quantity'] * x['price'], 
                                reverse=True)
            
            remaining_discount = total_discount
            
            for i in range(min(3, len(sorted_items))):
                if remaining_discount <= 0:
                    break
                    
                item = sorted_items[i]
                item_total = item['quantity'] * item['price']
                
                if remaining_discount >= item_total:
                    item['price'] = 0
                    remaining_discount -= item_total
                else:
                    new_item_total = item_total - remaining_discount
                    item['price'] = new_item_total / item['quantity']
                    remaining_discount = 0
                    break
    
    # Filter empty invoices
    invoices = [inv for inv in invoices if len(inv['items']) > 0]
    
    return invoices

# ============================================================================
# GRAB INVOICE FUNCTIONS
# ============================================================================

def generate_random_items_with_target(menu_items, target_amount_before_tax, min_items=20, max_items=30):
    """Generate random menu items với INTEGER quantities để match target amount"""
    
    # Filter out alcoholic beverages
    alcohol_keywords = ['bia', 'beer', 'heineken', 'tiger', 'saigon', '333', 'rượu', 'wine', 'whisky', 'vodka']
    menu_items = [item for item in menu_items 
                  if not any(keyword in item['name'].lower() for keyword in alcohol_keywords)]
    
    # Adjust parameters based on target amount
    if target_amount_before_tax > 5000000:
        min_items = max(25, min_items)
        max_items = min(40, len(menu_items))
        num_attempts = 200
    elif target_amount_before_tax > 2000000:
        min_items = max(20, min_items)
        max_items = 35
        num_attempts = 100
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
            if random.random() < 0.7:
                sorted_by_price = sorted(available_items, key=lambda x: x['price'], reverse=True)
                pool_size = max(num_additional_items * 3, len(available_items) // 2)
                pool = sorted_by_price[:pool_size]
                selected_additional = random.sample(pool, min(num_additional_items, len(pool)))
            else:
                selected_additional = random.sample(available_items, min(num_additional_items, len(available_items)))
        elif target_amount_before_tax > 1000000:
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
        else:
            sorted_by_price = sorted(available_items, key=lambda x: x['price'])
            pool_size = max(num_additional_items * 3, len(available_items) // 2)
            pool = sorted_by_price[:pool_size]
            selected_additional = random.sample(pool, min(num_additional_items, len(pool)))
        
        selected_items = required_items + selected_additional
        result = []
        remaining = target_amount_before_tax
        sorted_items = sorted(selected_items, key=lambda x: x['price'], reverse=True)
        
        avg_price = sum(item['price'] for item in sorted_items) / len(sorted_items)
        estimated_avg_qty = target_amount_before_tax / (len(sorted_items) * avg_price)
        default_max_qty = min(5, max(2, int(estimated_avg_qty * 1.5))) if len(sorted_items) >= 20 else 9
        
        for i, item in enumerate(sorted_items):
            if i == len(sorted_items) - 1:
                # Last item: adjust price within ±10,000
                quantity = 1
                max_price_adjustment = 10000
                ideal_price = remaining
                price_difference = ideal_price - item['price']
                
                if abs(price_difference) <= max_price_adjustment and ideal_price >= 1000:
                    adjusted_price = ideal_price
                else:
                    if price_difference > 0:
                        adjusted_price = item['price'] + max_price_adjustment
                    else:
                        adjusted_price = max(1000, item['price'] - max_price_adjustment)
                
                if adjusted_price < 1000:
                    adjusted_price = 1000
                
                result.append({
                    'name': item['name'],
                    'unit': item['unit'],
                    'price': adjusted_price,
                    'quantity': quantity
                })
                remaining = 0
            else:
                items_left = len(sorted_items) - i
                avg_per_item = remaining / items_left
                target_qty = avg_per_item / item['price']
                
                if i == len(sorted_items) - 2:
                    last_item = sorted_items[-1]
                    last_item_price = last_item['price']
                    target_remaining_for_last = last_item_price
                    this_item_budget = remaining - target_remaining_for_last
                    if this_item_budget > item['price']:
                        max_affordable = min(int(this_item_budget / item['price']), default_max_qty)
                    else:
                        max_affordable = 1
                else:
                    max_qty = min(default_max_qty, max(1, int(target_qty * 2)))
                    max_affordable = min(max_qty, int(remaining / item['price']))
                
                if max_affordable >= 1:
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
            within_adjustment_limit = last_item_adjustment <= 10000
        else:
            within_adjustment_limit = False
        
        if within_adjustment_limit:
            if diff < best_diff or best_diff == float('inf'):
                best_diff = diff
                best_result = result
                if diff == 0:
                    break
        else:
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
                if diff < 1 and adjustment <= 10000:
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
    invoices = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
    print(f"   ✓ Tìm thấy {len(invoices)} hóa đơn")
    
    if len(invoices) == 0:
        print("\n⚠️  Không tìm thấy hóa đơn nào!")
        return
    
    # Process invoices
    _process_and_save_invoices(invoices, source_type)

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
    invoices = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
    print(f"   ✓ Tìm thấy {len(invoices)} hóa đơn")
    
    if len(invoices) == 0:
        print("\n⚠️  Không tìm thấy hóa đơn nào!")
        return
    
    # Process invoices
    _process_and_save_invoices(invoices, source_type)

def _process_and_save_invoices(invoices, source_type):
    """Helper function để process và save invoices"""
    output_dir = script_dir / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📝 Đang tạo file cho từng hóa đơn...")
    print(f"    {'ID':<10} {'Món':<5} {'Tổng tiền':<15} {'Giảm giá':<30} {'Validate':<10}")
    print("   " + "-" * 80)
    
    total_created = 0
    validation_warnings = []
    
    for invoice in invoices:
        total = sum(item['quantity'] * item['price'] for item in invoice['items'])
        final_with_tax = total * 1.08
        total_str = f"{int(final_with_tax):,}".replace(',', '.')
        
        invoice_source_type = invoice.get('payment_method') or source_type
        
        filename = output_dir / f"{invoice['invoice_id']} - {invoice_source_type} - {total_str}đ.xlsx"
        create_invoice_file(invoice, str(filename))
        
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
    
    print("\n" + "=" * 70)
    print(f"✅ HOÀN THÀNH!")
    print(f"📁 Thư mục: {OUTPUT_DIR}/")
    print(f"📊 Tổng số file: {total_created}")
    print("=" * 70)

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
        worksheet.write(row_idx, 0, 1, cell_format)
        worksheet.write(row_idx, 1, '', cell_format)
        worksheet.write(row_idx, 2, item['name'], cell_format)
        worksheet.write(row_idx, 3, item['unit'], cell_format)
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
        invoices = parse_invoices_from_html(content, all_menu_items, name_mapping, price_to_items, is_combined)
        _process_and_save_invoices(invoices, source_type)
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

