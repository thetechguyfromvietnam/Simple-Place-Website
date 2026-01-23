#!/usr/bin/env python3
"""
Sort update-item-filtered.xlsx by category:
1. Tacos
2. Burrito
3. Pizza
4. Other dishes (Quesadilla, Pasta, Salad, Soup, etc.)
5. Drinks (Nước)
6. Extra (at the end)
7. Others (items that don't fit any category)
"""

import pandas as pd
from pathlib import Path

def get_category_order(name):
    """Get category order for sorting"""
    name_lower = name.lower()
    
    # 6. Extra (check FIRST - before other categories, as extras can be for any dish)
    extra_keywords = ['extra', 'thêm', 'topping', 'shell', 'tortilla extra', 
                     'mozzarella extra', 'cheese extra', 'onion extra', 'tomato extra']
    # Check for extra patterns
    is_extra = False
    if 'extra' in name_lower or 'thêm' in name_lower:
        is_extra = True
    elif 'shell' in name_lower and ('taco' in name_lower or 'crispy' in name_lower):
        is_extra = True
    elif 'tortilla' in name_lower and 'extra' in name_lower:
        is_extra = True
    elif ('cheese' in name_lower or 'mozzarella' in name_lower or 'parmesan' in name_lower) and ('extra' in name_lower or 'shredded' in name_lower):
        is_extra = True
    
    if is_extra:
        return (6, name)
    
    # 1. Tacos (first)
    if 'taco' in name_lower:
        return (1, name)
    
    # 2. Burrito (second)
    if 'burrito' in name_lower:
        return (2, name)
    
    # 3. Pizza (third)
    # Check for pizza patterns: "pizza", "pizzadilla", or "V -" prefix (usually vegetarian pizza)
    if 'pizza' in name_lower or 'pizzadilla' in name_lower:
        return (3, name)
    # "V -" prefix usually indicates vegetarian pizza
    if name_lower.startswith('v -') or name_lower.startswith('v-'):
        # Check if it's not a salad or pasta
        if 'salad' not in name_lower and 'pasta' not in name_lower and 'penne' not in name_lower:
            return (3, name)
    # Pizza with size indicators (L/M) - common pizza names
    pizza_names = ['hawaii', 'margherita', 'pepperoni', 'meat lovers', 'italian sausage',
                  'pesto sausage', 'parmaham', 'prosciutto', 'pollo e funghi', 
                  'prosciutto e funghi', 'smoked salmon', 'mediterranean', 'margerita',
                  'parmigiana', 'quattro formaggi', 'spinach formaggi', 'spinaci e funghi',
                  'veggie']
    # Check if name ends with L or M (size indicators) and contains pizza name
    if (name_lower.endswith(' l') or name_lower.endswith(' m') or 
        name_lower.endswith('l') or name_lower.endswith('m')):
        for pizza_name in pizza_names:
            if pizza_name in name_lower:
                return (3, name)
    
    # 5. Drinks (before extras)
    drink_keywords = ['beer', 'bia', 'wine', 'rượu', 'juice', 'nước ép', 
                     'smoothie', 'sinh tố', 'coffee', 'cà phê', 'tea', 'trà',
                     'soda', 'coke', 'fanta', 'sprite', 'nước ngọt', 'water', 'nước',
                     'drink', 'beverage', 'cocktail', 'mocktail', 'sangria', 
                     'fizzy', 'draught', 'tiger', 'heineken', 'corona', 'stella']
    if any(kw in name_lower for kw in drink_keywords):
        return (5, name)
    
    # 4. Other dishes (Quesadilla, Pasta, Salad, Soup, Appetizers, etc.)
    # Check for pasta first (fettuccine, linguine, penne, alfredo, etc.)
    pasta_keywords = ['fettuccine', 'linguine', 'penne', 'alfredo', 'carbonara', 
                     'bolognese', 'marinara', 'arrabbiata', 'pasta', 'spaghetti', 'mì']
    if any(kw in name_lower for kw in pasta_keywords):
        return (4, name)
    
    # Check for "V -" that might be pasta
    if (name_lower.startswith('v -') or name_lower.startswith('v-')) and ('penne' in name_lower or 'alfredo' in name_lower):
        return (4, name)
    
    other_dish_keywords = ['quesadilla', 'salad', 'xà lách', 'soup', 'súp', 'nachos', 
                          'bruschetta', 'chips', 'fries', 'nugget', 'fish finger', 
                          'bread', 'bánh', 'queso', 'dip', 'guacamole', 'salsa', 
                          'sauce', 'sốt', 'appetizer', 'starter', 'wings', 'nuggets', 
                          'finger', 'stick', 'wrap', 'roll', 'sandwich', 'burger', 
                          'steak', 'grilled', 'fried', 'roasted', 'stew', 'curry', 
                          'rice', 'cơm', 'noodle', 'phở', 'bún', 'spring roll', 
                          'gỏi', 'bánh mì', 'pancake', 'waffle', 'lasagna', 
                          'mash potato', 'kid dough', 'pickled vegetables']
    if any(kw in name_lower for kw in other_dish_keywords):
        return (4, name)
    
    # 7. Others (items that don't fit any category - at the very end)
    return (7, name)

def sort_menu():
    """Sort menu by category"""
    
    input_file = Path("update-item-filtered.xlsx")
    output_file = Path("update-item-filtered.xlsx")  # Overwrite same file
    
    print("=" * 70)
    print("🔄 SORTING MENU BY CATEGORY")
    print("=" * 70)
    
    # Read file
    print(f"\n📄 Reading: {input_file}")
    df = pd.read_excel(input_file)
    print(f"   Total rows: {len(df)}")
    
    # Add category order column
    print(f"\n🔍 Categorizing items...")
    df['_category_order'] = df['Ten_san_pham'].apply(get_category_order)
    
    # Count items by category
    category_counts = {}
    for idx, row in df.iterrows():
        order, _ = row['_category_order']
        category_name = {
            1: 'Tacos',
            2: 'Burrito',
            3: 'Pizza',
            4: 'Other Dishes',
            5: 'Drinks',
            6: 'Extra',
            7: 'Others'
        }.get(order, 'Unknown')
        category_counts[category_name] = category_counts.get(category_name, 0) + 1
    
    print("\n📊 Category breakdown:")
    for cat, count in sorted(category_counts.items()):
        print(f"   {cat}: {count} items")
    
    # Sort by category order, then by name within category
    print(f"\n🔄 Sorting...")
    df = df.sort_values('_category_order')
    
    # Remove temporary column
    df = df.drop('_category_order', axis=1)
    
    # Reset index
    df = df.reset_index(drop=True)
    
    # Show preview
    print(f"\n📋 Preview (first 30 items):")
    print("-" * 70)
    for i, row in df.head(30).iterrows():
        name_display = row['Ten_san_pham'][:50] + '...' if len(row['Ten_san_pham']) > 53 else row['Ten_san_pham']
        print(f"{i+1:3d}. {name_display:<53} {row['Don_vi_tinh']:<8} {row['Don_gia']:>10,} đ")
    
    # Save sorted file
    print(f"\n💾 Saving sorted data to: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        
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
    
    print(f"✅ Saved {len(df)} items to {output_file}")
    print(f"\n✨ Sorting complete!")
    print(f"\n📑 Order:")
    print(f"   1. Tacos")
    print(f"   2. Burrito")
    print(f"   3. Pizza")
    print(f"   4. Other Dishes (Quesadilla, Pasta, Salad, Soup, etc.)")
    print(f"   5. Drinks (Nước)")
    print(f"   6. Extra (at the end)")
    print(f"   7. Others (items that don't fit any category)")

if __name__ == '__main__':
    sort_menu()







