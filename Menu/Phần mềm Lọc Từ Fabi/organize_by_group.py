#!/usr/bin/env python3
"""
Phân loại và sắp xếp menu theo Tên nhóm một cách thống nhất
"""

import pandas as pd
from pathlib import Path

def get_group_order(group_name):
    """Xác định thứ tự ưu tiên cho các nhóm"""
    if pd.isna(group_name):
        return (999, '')
    
    group_lower = str(group_name).strip().upper()
    
    # Định nghĩa thứ tự các nhóm
    group_order = {
        'SNACKS/ STARTERS': 1,
        'NACHOS': 2,
        'TACO': 3,
        'TACO TUESDAY': 4,
        'VEGETARIAN TACO': 5,
        'BURRITO': 6,
        'VEGETARIAN BURRITO': 7,
        'QUESADILLA': 8,
        'VEGETARIAN QUESADILLA': 9,
        'PIZZA': 10,
        'PIZZA KID': 11,
        'PASTA': 12,
        'SALAD': 13,
        'MAIN COURSE': 14,
        'EXTRA': 15,
        'SOFT DRINK': 16,
        'SMOOTHIES & JUICES': 17,
        'BEER & CRAFT BEERS': 18,
        'SANGRIA': 19,
        'WHITE': 20,
        'RED': 21,
        'DESSERT': 22,
    }
    
    # Tìm order cho group, nếu không tìm thấy thì dùng 999
    order = group_order.get(group_lower, 999)
    
    return (order, group_lower)

def organize_by_group():
    """Phân loại và sắp xếp menu theo Tên nhóm"""
    
    input_file = Path("menu-simple-place-update (1).xlsx")
    output_file = Path("menu-simple-place-update (1).xlsx")  # Ghi đè file gốc
    
    print("=" * 70)
    print("🔄 PHÂN LOẠI THEO TÊN NHÓM")
    print("=" * 70)
    
    # Đọc file
    print(f"\n📄 Đang đọc: {input_file}")
    df = pd.read_excel(input_file)
    print(f"   Tổng số dòng: {len(df)}")
    print(f"   Các cột: {list(df.columns)}")
    
    # Kiểm tra cột Tên nhóm
    if 'Tên nhóm' not in df.columns:
        print("\n❌ Không tìm thấy cột 'Tên nhóm'!")
        print(f"   Các cột có sẵn: {list(df.columns)}")
        return
    
    # Thống nhất tên nhóm (chuẩn hóa)
    print(f"\n🔍 Đang chuẩn hóa tên nhóm...")
    df['Tên nhóm'] = df['Tên nhóm'].astype(str).str.strip()
    
    # Thống nhất một số tên nhóm có thể viết khác nhau
    group_normalization = {
        'Dessert': 'DESSERT',
        'Pizza kid': 'PIZZA KID',
    }
    
    for old_name, new_name in group_normalization.items():
        df.loc[df['Tên nhóm'].str.upper() == old_name.upper(), 'Tên nhóm'] = new_name
    
    # Thêm cột order để sắp xếp
    print(f"\n📊 Đang phân loại...")
    df['_group_order'] = df['Tên nhóm'].apply(get_group_order)
    
    # Thống kê theo nhóm
    print(f"\n📈 Thống kê theo nhóm:")
    group_counts = df['Tên nhóm'].value_counts()
    for group, count in group_counts.items():
        order, _ = get_group_order(group)
        print(f"   {order:3d}. {group:<30} : {count:3d} món")
    
    # Sắp xếp: theo group order, sau đó theo tên món trong cùng nhóm
    print(f"\n🔄 Đang sắp xếp...")
    df = df.sort_values(['_group_order', 'Tên'])
    
    # Xóa cột tạm
    df = df.drop('_group_order', axis=1)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Hiển thị preview
    print(f"\n📋 Xem trước (30 món đầu):")
    print("-" * 70)
    current_group = None
    for i, row in df.head(30).iterrows():
        group = row['Tên nhóm']
        if group != current_group:
            print(f"\n📁 {group}")
            current_group = group
        name_display = row['Tên'][:45] + '...' if len(str(row['Tên'])) > 48 else row['Tên']
        price = f"{row['Giá']:,.0f}" if pd.notna(row['Giá']) else 'N/A'
        unit = row['Đơn vị'] if pd.notna(row['Đơn vị']) else ''
        print(f"   {name_display:<48} {unit:<8} {price:>12} đ")
    
    # Lưu file đã sắp xếp
    print(f"\n💾 Đang lưu vào: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Tự động điều chỉnh độ rộng cột
        worksheet = writer.sheets['Sheet1']
        worksheet.column_dimensions['A'].width = 50  # Tên
        worksheet.column_dimensions['B'].width = 15  # Giá
        worksheet.column_dimensions['C'].width = 12  # Đơn vị
        worksheet.column_dimensions['D'].width = 30  # Tên nhóm
        
        # Định dạng cột giá
        from openpyxl.styles import Alignment
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=2, max_col=2):
            for cell in row:
                if cell.value:
                    cell.number_format = '#,##0'
                    cell.alignment = Alignment(horizontal='right')
    
    print(f"✅ Đã lưu {len(df)} món vào {output_file}")
    print(f"\n✨ Hoàn thành phân loại!")
    print(f"\n📑 Thứ tự các nhóm:")
    print(f"   1. SNACKS/ STARTERS")
    print(f"   2. NACHOS")
    print(f"   3. TACO")
    print(f"   4. TACO TUESDAY")
    print(f"   5. VEGETARIAN TACO")
    print(f"   6. BURRITO")
    print(f"   7. VEGETARIAN BURRITO")
    print(f"   8. QUESADILLA")
    print(f"   9. VEGETARIAN QUESADILLA")
    print(f"   10. PIZZA")
    print(f"   11. PIZZA KID")
    print(f"   12. PASTA")
    print(f"   13. SALAD")
    print(f"   14. MAIN COURSE")
    print(f"   15. EXTRA")
    print(f"   16. SOFT DRINK")
    print(f"   17. SMOOTHIES & JUICES")
    print(f"   18. BEER & CRAFT BEERS")
    print(f"   19. SANGRIA")
    print(f"   20. WHITE")
    print(f"   21. RED")
    print(f"   22. DESSERT")

if __name__ == '__main__':
    organize_by_group()






