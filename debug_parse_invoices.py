#!/usr/bin/env python3
"""
Script debug để kiểm tra các hóa đơn bị bỏ sót
Tìm các hóa đơn có tổng tiền 81k, 205k, 1.659k trong file gốc
"""

import re
from pathlib import Path

def extract_invoices_from_html(content):
    """Trích xuất tất cả hóa đơn từ HTML content"""
    invoices_found = []
    rows = content.split('<tr>')
    
    for row in rows:
        # Tìm số hóa đơn
        invoice_match = re.search(r'rowspan="\d+">(\d{6})</td>', row)
        if invoice_match:
            invoice_num = invoice_match.group(1)
            
            # Tìm tổng tiền trong row
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row)
            cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
            
            # Tìm tổng tiền (thường ở cuối row)
            total_amount = None
            for cell in cells:
                cell_clean = cell.replace(' ', '').replace(',', '').replace('.', '')
                if cell_clean.isdigit() and len(cell_clean) >= 4:
                    value = float(cell_clean)
                    if value >= 50000:  # Tổng tiền thường >= 50k
                        total_amount = value
                        break
            
            # Tìm payment method
            payment_method = None
            row_upper = row.upper()
            if 'ATM (' in row_upper or row_upper.startswith('ATM'):
                payment_method = 'atm'
            elif 'TRANSFER (' in row_upper or row_upper.startswith('TRANSFER'):
                payment_method = 'transfer'
            
            if total_amount:
                invoices_found.append({
                    'invoice_id': invoice_num,
                    'total': total_amount,
                    'payment_method': payment_method,
                    'row': row[:200]  # Lưu 200 ký tự đầu để debug
                })
    
    return invoices_found

def find_missing_invoices():
    """Tìm các hóa đơn bị bỏ sót"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    tax_dir = base_dir / "tax_files"
    
    # Tìm các file input
    input_files = []
    if data_dir.exists():
        input_files = list(data_dir.glob("*.xls")) + list(data_dir.glob("*.html"))
    
    if not input_files:
        # Fallback to root
        input_files = list(base_dir.glob("sale_by_payment_method*.xls"))
    
    print("=" * 80)
    print("🔍 DEBUG: TÌM CÁC HÓA ĐƠN BỊ BỎ SÓT")
    print("=" * 80)
    print()
    
    # Tổng tiền cần tìm
    target_totals = [81000, 205000, 1659000]
    
    # Đọc tất cả file input
    all_invoices_from_input = []
    for input_file in input_files:
        print(f"📂 Đang đọc file: {input_file.name}")
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            invoices = extract_invoices_from_html(content)
            all_invoices_from_input.extend(invoices)
            print(f"   ✓ Tìm thấy {len(invoices)} hóa đơn")
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")
    
    print()
    print(f"📊 Tổng số hóa đơn trong file input: {len(all_invoices_from_input)}")
    print()
    
    # Lấy danh sách hóa đơn đã được tạo
    created_invoices = set()
    if tax_dir.exists():
        for tax_file in tax_dir.glob("*.xlsx"):
            # Trích xuất số hóa đơn từ tên file
            invoice_num = tax_file.stem.split(' - ')[0] if ' - ' in tax_file.stem else tax_file.stem
            created_invoices.add(invoice_num)
    
    print(f"📊 Tổng số hóa đơn đã tạo: {len(created_invoices)}")
    print()
    
    # Tìm các hóa đơn có tổng tiền target
    print("=" * 80)
    print("🎯 TÌM CÁC HÓA ĐƠN CÓ TỔNG TIỀN: 81k, 205k, 1.659k")
    print("=" * 80)
    print()
    
    found_targets = []
    for inv in all_invoices_from_input:
        for target in target_totals:
            # Cho phép sai số ±5000 (do làm tròn và VAT)
            if abs(inv['total'] - target) <= 5000:
                found_targets.append(inv)
                print(f"✅ Tìm thấy: HĐ {inv['invoice_id']} - {inv['total']:,.0f}đ - {inv['payment_method'] or 'N/A'}")
                if inv['invoice_id'] not in created_invoices:
                    print(f"   ⚠️  HÓA ĐƠN NÀY CHƯA ĐƯỢC TẠO FILE!")
                else:
                    # Kiểm tra file đã tạo
                    tax_file = tax_dir / f"{inv['invoice_id']} - {inv['payment_method'] or 'unknown'} - *.xlsx"
                    matching_files = list(tax_dir.glob(f"{inv['invoice_id']} - *"))
                    if matching_files:
                        print(f"   ✓ Đã tạo file: {matching_files[0].name}")
                break
    
    if not found_targets:
        print("❌ Không tìm thấy hóa đơn nào có tổng tiền 81k, 205k, hoặc 1.659k")
    else:
        print()
        print(f"📊 Tổng cộng tìm thấy {len(found_targets)} hóa đơn có tổng tiền target")
    
    # Tìm các hóa đơn bị bỏ sót (có trong input nhưng không có file output)
    print()
    print("=" * 80)
    print("❌ CÁC HÓA ĐƠN BỊ BỎ SÓT (có trong input nhưng không có file output)")
    print("=" * 80)
    print()
    
    missing_invoices = []
    for inv in all_invoices_from_input:
        if inv['invoice_id'] not in created_invoices:
            missing_invoices.append(inv)
    
    if missing_invoices:
        print(f"⚠️  Tìm thấy {len(missing_invoices)} hóa đơn bị bỏ sót:")
        for inv in sorted(missing_invoices, key=lambda x: x['total']):
            print(f"   - HĐ {inv['invoice_id']}: {inv['total']:,.0f}đ ({inv['payment_method'] or 'N/A'})")
    else:
        print("✅ Không có hóa đơn nào bị bỏ sót")
    
    # Tìm các hóa đơn có bia 333
    print()
    print("=" * 80)
    print("🍺 TÌM CÁC HÓA ĐƠN CÓ BIA 333")
    print("=" * 80)
    print()
    
    # Đọc lại file input để tìm bia 333
    for input_file in input_files:
        try:
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            rows = content.split('<tr>')
            current_invoice = None
            
            for row in rows:
                # Tìm số hóa đơn
                invoice_match = re.search(r'rowspan="\d+">(\d{6})</td>', row)
                if invoice_match:
                    current_invoice = invoice_match.group(1)
                
                # Tìm bia 333
                if current_invoice and ('333' in row.upper() or 'saigon' in row.lower()):
                    # Kiểm tra xem có phải là món bia không
                    cells = re.findall(r'<td[^>]*>(.*?)</td>', row)
                    cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
                    
                    for i, cell in enumerate(cells):
                        if '333' in cell.upper() or 'saigon' in cell.lower():
                            print(f"   HĐ {current_invoice}: Tìm thấy '{cell}' trong row")
                            # In thêm context
                            if i < len(cells) - 3:
                                print(f"      Số lượng: {cells[i+1] if i+1 < len(cells) else 'N/A'}")
                                print(f"      Đơn vị: {cells[i+2] if i+2 < len(cells) else 'N/A'}")
                                print(f"      Giá: {cells[i+3] if i+3 < len(cells) else 'N/A'}")
        except Exception as e:
            print(f"   ❌ Lỗi khi đọc {input_file.name}: {e}")

if __name__ == '__main__':
    find_missing_invoices()
