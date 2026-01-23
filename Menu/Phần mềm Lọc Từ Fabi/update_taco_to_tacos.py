#!/usr/bin/env python3
"""
Đổi "Taco" thành "Tacos" trong nhóm TACO
"""

import pandas as pd
import re
from openpyxl.styles import Alignment

# Đọc file
df = pd.read_excel('menu-simple-place-update (1).xlsx')

# Tìm các món trong nhóm TACO
taco_mask = df['Tên nhóm'].astype(str).str.upper().str.contains('^TACO$', na=False, regex=True)
taco_df = df[taco_mask]

print(f'📊 Tìm thấy {len(taco_df)} món trong nhóm TACO')
print('\n🔄 Đang đổi "Taco" thành "Tacos"...\n')

updated_count = 0

for idx in taco_df.index:
    current_name = str(df.loc[idx, 'Tên']).strip()
    original_name = current_name
    changed = False
    
    # Kiểm tra xem đã có format Tiếng Việt / Tiếng Anh chưa
    if ' / ' in current_name:
        parts = current_name.split(' / ')
        vietnamese = parts[0].strip()
        english = parts[1].strip()
        
        # Thay thế "Taco" thành "Tacos" ở cuối phần tiếng Anh
        # Chỉ thay nếu kết thúc bằng "Taco" (không phải "Tacos")
        if english.lower().endswith('taco') and not english.lower().endswith('tacos'):
            # Thay "Taco" thành "Tacos" ở cuối
            english = re.sub(r'Taco\s*$', 'Tacos', english, flags=re.IGNORECASE)
            new_name = f'{vietnamese} / {english}'
            df.loc[idx, 'Tên'] = new_name
            updated_count += 1
            changed = True
            print(f'   ✓ {original_name}')
            print(f'     → {new_name}\n')
        else:
            print(f'   ✓ Đã có "Tacos": {current_name}')
    else:
        # Nếu chưa có format, thay trực tiếp
        if current_name.lower().endswith('taco') and not current_name.lower().endswith('tacos'):
            new_name = re.sub(r'Taco\s*$', 'Tacos', current_name, flags=re.IGNORECASE)
            df.loc[idx, 'Tên'] = new_name
            updated_count += 1
            changed = True
            print(f'   ✓ {original_name}')
            print(f'     → {new_name}\n')
        else:
            print(f'   ✓ Đã có "Tacos": {current_name}')

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






