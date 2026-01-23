#!/usr/bin/env python3
"""
Bỏ chữ "Tacos" thừa ở cuối các món trong nhóm TACO
"""

import pandas as pd
import re
from openpyxl.styles import Alignment

# Đọc file
df = pd.read_excel('menu-simple-place-update (1).xlsx')

# Tìm các món trong nhóm TACO
taco_mask = df['Tên nhóm'].astype(str).str.upper().str.contains('^TACO$', na=False, regex=True)

print('🔄 Đang bỏ chữ "Tacos" thừa ở cuối...\n')

updated_count = 0

for idx in df[taco_mask].index:
    current_name = str(df.loc[idx, 'Tên']).strip()
    original_name = current_name
    
    # Kiểm tra xem có format Tiếng Việt / Tiếng Anh chưa
    if ' / ' in current_name:
        parts = current_name.split(' / ')
        vietnamese = parts[0].strip()
        english = parts[1].strip()
        
        # Kiểm tra xem có "Tacos" ở cuối và cũng có "Tacos" trong tên không
        if english.lower().endswith(' tacos'):
            # Đếm số lần xuất hiện "tacos" trong tên
            tacos_count = english.lower().count('tacos')
            if tacos_count > 1:
                # Bỏ " Tacos" ở cuối
                english_new = re.sub(r'\s+Tacos\s*$', '', english, flags=re.IGNORECASE)
                if english_new != english:
                    new_name = f'{vietnamese} / {english_new}'
                    df.loc[idx, 'Tên'] = new_name
                    updated_count += 1
                    print(f'   ✓ {original_name}')
                    print(f'     → {new_name}\n')
                else:
                    print(f'   ✓ Không cần thay đổi: {current_name}')
            else:
                print(f'   ✓ Không cần thay đổi: {current_name}')
        else:
            print(f'   ✓ Không cần thay đổi: {current_name}')
    else:
        # Nếu chưa có format, kiểm tra trực tiếp
        if current_name.lower().endswith(' tacos'):
            tacos_count = current_name.lower().count('tacos')
            if tacos_count > 1:
                new_name = re.sub(r'\s+Tacos\s*$', '', current_name, flags=re.IGNORECASE)
                if new_name != current_name:
                    df.loc[idx, 'Tên'] = new_name
                    updated_count += 1
                    print(f'   ✓ {original_name}')
                    print(f'     → {new_name}\n')
                else:
                    print(f'   ✓ Không cần thay đổi: {current_name}')
            else:
                print(f'   ✓ Không cần thay đổi: {current_name}')
        else:
            print(f'   ✓ Không cần thay đổi: {current_name}')

print(f'\n📊 Đã cập nhật {updated_count} món')

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





