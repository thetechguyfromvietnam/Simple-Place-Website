#!/usr/bin/env python3
"""
Cập nhật Birria Beef (Spicy) thành Birria Beef Tacos (Spicy)
và đổi tất cả Taco thành Tacos
"""

import pandas as pd
import re
from openpyxl.styles import Alignment

# Đọc file
df = pd.read_excel('menu-simple-place-update (1).xlsx')

# Tìm các món trong nhóm TACO
taco_mask = df['Tên nhóm'].astype(str).str.upper().str.contains('^TACO$', na=False, regex=True)

print('🔄 Đang cập nhật...\n')

updated_count = 0

for idx in df[taco_mask].index:
    current_name = str(df.loc[idx, 'Tên']).strip()
    original_name = current_name
    changed = False
    
    # 1. Cập nhật Birria Beef (Spicy) Tacos thành Birria Beef Tacos (Spicy)
    if 'Birria Beef' in current_name:
        if ' / ' in current_name:
            parts = current_name.split(' / ')
            vietnamese = parts[0].strip()
            english = parts[1].strip()
            # Thay "Birria Beef (Spicy) Tacos" thành "Birria Beef Tacos (Spicy)"
            english_new = re.sub(r'Birria Beef\s*\(Spicy\)\s*Tacos', 'Birria Beef Tacos (Spicy)', english, flags=re.IGNORECASE)
            if english_new == english:
                # Hoặc "Birria Beef (Spicy)" thành "Birria Beef Tacos (Spicy)"
                english_new = re.sub(r'Birria Beef\s*\(Spicy\)', 'Birria Beef Tacos (Spicy)', english, flags=re.IGNORECASE)
            if english_new != english:
                new_name = f'{vietnamese} / {english_new}'
                df.loc[idx, 'Tên'] = new_name
                changed = True
        else:
            # Thay "Birria Beef (Spicy) Tacos" thành "Birria Beef Tacos (Spicy)"
            new_name = re.sub(r'Birria Beef\s*\(Spicy\)\s*Tacos', 'Birria Beef Tacos (Spicy)', current_name, flags=re.IGNORECASE)
            if new_name == current_name:
                # Hoặc "Birria Beef (Spicy)" thành "Birria Beef Tacos (Spicy)"
                new_name = re.sub(r'Birria Beef\s*\(Spicy\)', 'Birria Beef Tacos (Spicy)', current_name, flags=re.IGNORECASE)
            if new_name != current_name:
                df.loc[idx, 'Tên'] = new_name
                changed = True
    
    # 2. Đổi tất cả "Taco" thành "Tacos" (trừ khi đã là "Tacos")
    if not changed:
        if ' / ' in current_name:
            parts = current_name.split(' / ')
            vietnamese = parts[0].strip()
            english = parts[1].strip()
            
            # Thay "Taco" thành "Tacos" trong phần tiếng Anh
            english_new = re.sub(r'\bTaco\b', 'Tacos', english, flags=re.IGNORECASE)
            if english_new != english:
                new_name = f'{vietnamese} / {english_new}'
                df.loc[idx, 'Tên'] = new_name
                changed = True
        else:
            # Thay "Taco" thành "Tacos" trong toàn bộ tên
            new_name = re.sub(r'\bTaco\b', 'Tacos', current_name, flags=re.IGNORECASE)
            if new_name != current_name:
                df.loc[idx, 'Tên'] = new_name
                changed = True
    
    if changed:
        updated_count += 1
        new_name_display = df.loc[idx, 'Tên']
        print(f'   ✓ {original_name}')
        print(f'     → {new_name_display}\n')
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





