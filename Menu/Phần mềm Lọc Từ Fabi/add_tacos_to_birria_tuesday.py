#!/usr/bin/env python3
"""
Thêm "Tacos" vào món Birria Beef (Spicy) trong nhóm TACO TUESDAY
"""

import pandas as pd
import re
from openpyxl.styles import Alignment

# Đọc file
df = pd.read_excel('menu-simple-place-update (1).xlsx')

# Tìm món Birria Beef (Spicy) trong nhóm TACO TUESDAY
taco_tuesday_mask = df['Tên nhóm'].astype(str).str.upper().str.contains('TACO TUESDAY', na=False, regex=True)
birria_mask = df['Tên'].astype(str).str.contains('Birria Beef', case=False, na=False)

# Tìm món trong nhóm TACO TUESDAY có chứa Birria Beef
target_mask = taco_tuesday_mask & birria_mask

print('🔍 Tìm món Birria Beef trong nhóm TACO TUESDAY...\n')

if target_mask.sum() > 0:
    for idx in df[target_mask].index:
        current_name = str(df.loc[idx, 'Tên']).strip()
        original_name = current_name
        
        print(f'   Tìm thấy: {current_name}')
        print(f'   Nhóm: {df.loc[idx, "Tên nhóm"]}')
        print(f'   Đơn vị: {df.loc[idx, "Đơn vị"]}')
        print(f'   Giá: {df.loc[idx, "Giá"]}')
        
        # Kiểm tra xem đã có "Tacos" chưa
        if 'Tacos' not in current_name and 'tacos' not in current_name:
            # Thêm "Tacos" vào - format: Birria Beef Tacos (Spicy)
            if ' / ' in current_name:
                parts = current_name.split(' / ')
                vietnamese = parts[0].strip()
                english = parts[1].strip()
                # Thay "Birria Beef (Spicy)" thành "Birria Beef Tacos (Spicy)"
                english_new = re.sub(r'Birria Beef\s*\(Spicy\)', 'Birria Beef Tacos (Spicy)', english, flags=re.IGNORECASE)
                new_name = f'{vietnamese} / {english_new}'
            else:
                # Thay "Birria Beef (Spicy)" thành "Birria Beef Tacos (Spicy)"
                new_name = re.sub(r'Birria Beef\s*\(Spicy\)', 'Birria Beef Tacos (Spicy)', current_name, flags=re.IGNORECASE)
            
            df.loc[idx, 'Tên'] = new_name
            print(f'\n   ✓ Đã cập nhật:')
            print(f'     {original_name}')
            print(f'     → {new_name}\n')
        else:
            print(f'   ✓ Đã có "Tacos" trong tên\n')
else:
    print('   ⚠ Không tìm thấy món Birria Beef trong nhóm TACO TUESDAY')
    print('\n   Đang tìm tất cả món trong nhóm TACO TUESDAY:')
    taco_tuesday_df = df[taco_tuesday_mask]
    for idx, row in taco_tuesday_df.iterrows():
        print(f'      • {row["Tên"]}')

# Lưu file
print('\n💾 Đang lưu file...')
with pd.ExcelWriter('menu-simple-place-update (1).xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    worksheet = writer.sheets['Sheet1']
    worksheet.column_dimensions['A'].width = 60
    worksheet.column_dimensions['B'].width = 15
    worksheet.column_dimensions['C'].width = 12
    worksheet.column_dimensions['D'].width = 30
    
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=2, max_col=2):
        for cell in row:
            if cell.value:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right')

print('✅ Đã cập nhật và lưu file!')





