#!/usr/bin/env python3
"""
Parse menu Excel files to extract menu items and prices
"""

import zipfile
import xml.etree.ElementTree as ET
import re

try:
    import pandas as pd
except ImportError:  # pandas might not be available in some environments
    pd = None

def parse_excel_menu(filepath):
    """
    Parse Excel file to extract menu items and prices
    Returns list of dicts: [{'name': 'Taco Gà', 'unit': 'Phần', 'price': 55000}, ...]
    """
    menu_items = []

    # ------------------------------------------------------------------
    # 1) ƯU TIÊN ĐỌC BẰNG PANDAS (HỖ TRỢ FORMAT MỚI + CŨ)
    # ------------------------------------------------------------------
    if pd is not None:
        try:
            df = pd.read_excel(filepath)
            cols = list(df.columns)

            # Tìm cột tên món
            name_candidates = ['Ten_san_pham', 'Tên', 'Ten', 'Tên món', 'Tên sản phẩm']
            name_col = next((c for c in name_candidates if c in cols), None)

            # Tìm cột đơn vị
            unit_candidates = ['Don_vi_tinh', 'Đơn vị', 'Don_vi', 'Đơn vị tính']
            unit_col = next((c for c in unit_candidates if c in cols), None)

            # Tìm cột giá
            price_candidates = ['Don_gia', 'Giá', 'Gia', 'Price']
            price_col = next((c for c in price_candidates if c in cols), None)

            # Tìm cột nhóm (Tên nhóm / Group)
            group_candidates = ['Tên nhóm', 'Ten_nhom', 'Group', 'Nhóm']
            group_col = next((c for c in group_candidates if c in cols), None)

            if name_col and price_col:
                for _, row in df.iterrows():
                    raw_name = row.get(name_col)
                    if pd.isna(raw_name):
                        continue
                    name = str(raw_name).strip()
                    if not name:
                        continue

                    raw_price = row.get(price_col, 0)
                    try:
                        price = float(raw_price)
                    except (TypeError, ValueError):
                        continue
                    if price <= 0:
                        continue

                    if unit_col:
                        raw_unit = row.get(unit_col)
                        unit = str(raw_unit).strip() if pd.notna(raw_unit) else ''
                    else:
                        unit = ''

                    unit_clean = unit.strip() if unit else ''
                    unit_normalized = unit_clean.lower()
                    if not unit_clean:
                        final_unit = 'Phần'
                    elif unit_normalized in {'món', 'mon', 'dish'}:
                        final_unit = 'Phần'
                    else:
                        final_unit = unit_clean
                    
                    # Nhóm món (chỉ có ở một số file như simple-place-menu)
                    if group_col:
                        raw_group = row.get(group_col)
                        group = str(raw_group).strip() if pd.notna(raw_group) else ''
                    else:
                        group = ''

                    item = {
                        'name': name,
                        'unit': final_unit,
                        'price': price
                    }
                    if group:
                        item['group'] = group

                    menu_items.append(item)

                # Nếu đã đọc được dữ liệu hợp lệ thì trả về luôn
                if menu_items:
                    return menu_items
        except Exception:
            # Nếu pandas đọc lỗi (file lạ), fallback sang XML parsing cũ
            menu_items = []

    # ------------------------------------------------------------------
    # 2) FALLBACK: PARSE TRỰC TIẾP BẰNG XML GIỐNG CODE CŨ
    # ------------------------------------------------------------------
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        # Try to read shared strings (contains all text values) - may not exist
        strings = []
        try:
            with zip_ref.open('xl/sharedStrings.xml') as f:
                strings_xml = f.read()
                strings_root = ET.fromstring(strings_xml)
                # Extract all text values
                for t in strings_root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                    strings.append(t.text if t.text else '')
        except KeyError:
            # No shared strings file - will use inline strings
            pass

        # Read worksheet data
        with zip_ref.open('xl/worksheets/sheet1.xml') as f:
            sheet_xml = f.read()
            sheet_root = ET.fromstring(sheet_xml)

            # Parse rows
            ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            rows = sheet_root.findall('.//main:row', ns)

            for row in rows[1:]:  # Skip header row
                cells = row.findall('./main:c', ns)
                if len(cells) < 3:
                    continue

                # Get values from cells
                name_cell = cells[0]
                unit_cell = cells[1] if len(cells) > 1 else None
                price_cell = cells[2] if len(cells) > 2 else None

                # Extract name (from shared strings or inline)
                name = ''
                name_v = name_cell.find('./main:v', ns)
                if name_v is not None:
                    if name_cell.get('t') == 's':
                        # Shared string
                        idx = int(name_v.text)
                        if idx < len(strings):
                            name = strings[idx]
                    else:
                        # Inline string or direct value
                        name = name_v.text if name_v.text else ''

                # Try inline string if no shared string found
                if not name:
                    inline_str = name_cell.find('./main:is/main:t', ns)
                    if inline_str is not None and inline_str.text:
                        name = inline_str.text

                # Extract unit (from shared strings or inline)
                unit = ''
                if unit_cell is not None:
                    unit_v = unit_cell.find('./main:v', ns)
                    if unit_v is not None:
                        if unit_cell.get('t') == 's':
                            # Shared string
                            idx = int(unit_v.text)
                            if idx < len(strings):
                                unit = strings[idx]
                        else:
                            # Inline string or direct value
                            unit = unit_v.text if unit_v.text else ''

                    # Try inline string if no shared string found
                    if not unit:
                        inline_str = unit_cell.find('./main:is/main:t', ns)
                        if inline_str is not None and inline_str.text:
                            unit = inline_str.text

                # Extract price (direct number)
                price = 0
                if price_cell is not None:
                    price_v = price_cell.find('./main:v', ns)
                    if price_v is not None and price_v.text:
                        try:
                            price = float(price_v.text)
                        except (ValueError, TypeError):
                            continue

                # Only add valid menu items
                if name and price > 0:
                    # Skip header rows
                    if name not in ['Ten_san_pham', 'Tinh_chat', 'Ma_so', 'Tên sản phẩm', 'Tính chất', 'Mã số']:
                        unit_clean = unit.strip() if unit else ''
                        unit_normalized = unit_clean.lower()
                        if not unit_clean:
                            final_unit = 'Phần'
                        elif unit_normalized in {'món', 'mon', 'dish'}:
                            final_unit = 'Phần'
                        else:
                            final_unit = unit_clean
                        menu_items.append({
                            'name': name.strip(),
                            'unit': final_unit,
                            'price': price
                        })

    return menu_items

if __name__ == "__main__":
    print("Testing menu parsing...")
    print("=" * 70)
    
    # Parse both menus
    print("\n📋 SIMPLE PLACE MENU:")
    simple_menu = parse_excel_menu('Menu/simple-place-menu.xlsx')
    print(f"   Found {len(simple_menu)} items")
    for i, item in enumerate(simple_menu[:5], 1):
        print(f"   {i}. {item['name']} - {item['price']:,.0f} VND")
    print("   ...")
    
    print("\n🌮 TACO PLACE MENU:")
    taco_menu = parse_excel_menu('Menu/taco-place-menu.xlsx')
    print(f"   Found {len(taco_menu)} items")
    for i, item in enumerate(taco_menu[:5], 1):
        print(f"   {i}. {item['name']} - {item['price']:,.0f} VND")
    print("   ...")

