#!/usr/bin/env python3
"""
Cập nhật bản dịch Pork Carnitas thành Thịt Heo Hầm Xé Sợi
"""

import pandas as pd
import re
from openpyxl.styles import Alignment

# Đọc file
df = pd.read_excel('menu-simple-place-update (1).xlsx')

print('🔄 Đang cập nhật bản dịch "Pork Carnitas"...\n')

updated_count = 0

# Tìm các món có chứa Pork Carnitas
for idx, row in df.iterrows():
    current_name = str(row['Tên']).strip()
    original_name = current_name
    changed = False
    
    # Kiểm tra xem có chứa Pork Carnitas không
    if 'Pork Carnitas' in current_name or 'pork carnitas' in current_name.lower():
        if ' / ' in current_name:
            parts = current_name.split(' / ')
            vietnamese = parts[0].strip()
            english = parts[1].strip()
            
            # Cập nhật phần tiếng Việt
            # Tìm từ đầu (Taco, Burrito, Quesadilla) và thay phần sau
            if 'Taco' in vietnamese:
                vietnamese_new = 'Taco Thịt Heo Hầm Xé Sợi'
            elif 'Burrito' in vietnamese:
                vietnamese_new = 'Burrito Thịt Heo Hầm Xé Sợi'
            elif 'Quesadilla' in vietnamese:
                vietnamese_new = 'Quesadilla Thịt Heo Hầm Xé Sợi'
            else:
                # Nếu không có từ đầu, thêm dựa vào tiếng Anh
                if 'Taco' in english:
                    vietnamese_new = 'Taco Thịt Heo Hầm Xé Sợi'
                elif 'Burrito' in english:
                    vietnamese_new = 'Burrito Thịt Heo Hầm Xé Sợi'
                elif 'Quesadilla' in english:
                    vietnamese_new = 'Quesadilla Thịt Heo Hầm Xé Sợi'
                else:
                    vietnamese_new = 'Thịt Heo Hầm Xé Sợi'
            
            new_name = f'{vietnamese_new} / {english}'
            df.loc[idx, 'Tên'] = new_name
            changed = True
        else:
            # Nếu chưa có format, tạo mới
            if 'Taco' in current_name:
                vietnamese_new = 'Taco Thịt Heo Hầm Xé Sợi'
            elif 'Burrito' in current_name:
                vietnamese_new = 'Burrito Thịt Heo Hầm Xé Sợi'
            elif 'Quesadilla' in current_name:
                vietnamese_new = 'Quesadilla Thịt Heo Hầm Xé Sợi'
            else:
                vietnamese_new = 'Thịt Heo Hầm Xé Sợi'
            new_name = f'{vietnamese_new} / {current_name}'
            df.loc[idx, 'Tên'] = new_name
            changed = True
    
    if changed:
        updated_count += 1
        print(f'   ✓ {original_name}')
        print(f'     → {df.loc[idx, "Tên"]}\n')

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





