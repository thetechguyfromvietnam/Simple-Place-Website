#!/usr/bin/env python3
"""
Filter update-item.xlsx sheet according to simple-place-menu.xlsx format
"""

import pandas as pd
from pathlib import Path

def filter_sheet_by_format():
    """Filter update-item.xlsx to match simple-place-menu.xlsx format"""
    
    # File paths
    update_file = Path("update-item.xlsx")
    simple_file = Path("simple-place-menu.xlsx")
    output_file = Path("update-item-filtered.xlsx")
    
    print("=" * 70)
    print("🔍 FILTERING SHEET BY FORMAT")
    print("=" * 70)
    
    # Read format reference
    print(f"\n📄 Reading format reference: {simple_file}")
    df_format = pd.read_excel(simple_file)
    print(f"   Format columns: {list(df_format.columns)}")
    print(f"   Format sample:")
    print(df_format.head(3).to_string(index=False))
    
    # Read update file
    print(f"\n📄 Reading: {update_file}")
    df_update = pd.read_excel(update_file)
    print(f"   Total rows: {len(df_update)}")
    print(f"   Columns: {list(df_update.columns)}")
    
    # Map columns from update-item.xlsx to format
    # Format columns: Ten_san_pham, Don_vi_tinh, Don_gia
    # Update columns: Tên, Đơn vị, Giá
    
    # Create filtered dataframe
    filtered_data = []
    
    for idx, row in df_update.iterrows():
        # Get values from update file
        ten = str(row['Tên']).strip() if pd.notna(row['Tên']) else ''
        don_vi = str(row['Đơn vị']).strip() if pd.notna(row['Đơn vị']) else 'Phần'
        gia = row['Giá'] if pd.notna(row['Giá']) else 0
        
        # Skip invalid rows
        if not ten or len(ten) < 2:
            continue
        
        # Skip if price is 0 or invalid
        try:
            gia = float(gia)
            if gia <= 0:
                continue
        except:
            continue
        
        # Normalize unit
        don_vi_upper = don_vi.upper()
        unit_mapping = {
            'PHAN': 'Phần',
            'MON': 'Phần',
            'LY': 'Ly',
            'LON': 'Lon',
            'CHAI': 'Chai',
            'GL': 'Ly',
            'BOTTLE': 'Chai',
            'TRAI': 'Trái',
            'SET': 'Set'
        }
        don_vi = unit_mapping.get(don_vi_upper, don_vi.capitalize())
        
        # Add to filtered data
        filtered_data.append({
            'Ten_san_pham': ten,
            'Don_vi_tinh': don_vi,
            'Don_gia': int(gia)
        })
    
    # Create filtered dataframe
    df_filtered = pd.DataFrame(filtered_data)
    
    print(f"\n✅ Filtered {len(df_filtered)} rows")
    print(f"\n📋 Preview (first 10 items):")
    print("-" * 70)
    print(df_filtered.head(10).to_string(index=False))
    
    # Save filtered file
    print(f"\n💾 Saving filtered data to: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, sheet_name='Sheet1', index=False)
        
        # Auto-adjust column widths
        worksheet = writer.sheets['Sheet1']
        worksheet.column_dimensions['A'].width = 60  # Ten_san_pham
        worksheet.column_dimensions['B'].width = 15  # Don_vi_tinh
        worksheet.column_dimensions['C'].width = 15  # Don_gia
        
        # Format price column as number
        from openpyxl.styles import Alignment
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=3, max_col=3):
            for cell in row:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal='right')
    
    print(f"✅ Saved {len(df_filtered)} items to {output_file}")
    print(f"\n✨ Filtering complete!")
    print(f"   Filtered file: {output_file}")
    print(f"   Format matches: {simple_file}")

if __name__ == '__main__':
    filter_sheet_by_format()







