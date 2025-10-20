#!/usr/bin/env node

/**
 * Menu Extraction Script
 * 
 * This script extracts menu data from Excel files and generates menu_data.json
 * Run with: node scripts/extract-menu.js
 */

const fs = require('fs');
const path = require('path');

// Note: This script requires pandas and openpyxl to be installed
// Install with: pip install pandas openpyxl

const pythonScript = `
import pandas as pd
import json
import os

# Read only the simple-place-menu.xlsx file
files = ['simple-place-menu.xlsx']
all_items = []

for file in files:
    if os.path.exists(file):
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            name = row['Ten_san_pham'] if 'Ten_san_pham' in row else row.get('Ten_san_pham_EN', '')
            unit = row['Don_vi_tinh'] if 'Don_vi_tinh' in row else 'Phần'
            price = row['Don_gia'] if 'Don_gia' in row else 0
            
            if name and price > 0:
                # Check item type for special handling
                name_lower = name.lower()
                is_pizza = 'pizza' in name_lower or 'pizzadilla' in name_lower
                is_taco = 'taco' in name_lower
                is_burrito = 'burrito' in name_lower
                is_quesadilla = 'quesadilla' in name_lower
                is_spaghetti = 'spaghetti' in name_lower or 'pasta' in name_lower
                
                item = {
                    'name': name,
                    'unit': unit,
                    'price': int(price),
                    'source': file,
                    'isPizza': is_pizza,
                    'isTaco': is_taco,
                    'isBurrito': is_burrito,
                    'isQuesadilla': is_quesadilla,
                    'isSpaghetti': is_spaghetti,
                    'sizes': ['Medium', 'Large'] if is_pizza else None,
                    'tacoOptions': ['Crispy', 'Soft'] if is_taco else None
                }
                all_items.append(item)

# Remove duplicates based on name and price
unique_items = []
seen = set()
for item in all_items:
    key = (item['name'], item['price'])
    if key not in seen:
        seen.add(key)
        unique_items.append(item)

# Categorize items according to new structure
categories = {
    'Appetizers': [],
    'Salad': [],
    'Tacos': [],
    'Burrito': [],
    'Quesadilla': [],
    'Pizza': [],
    'Spaghetti': [],
    'Main Dish': [],
    'Drinks': [],
    'Extra': []
}

for item in unique_items:
    name = item['name'].lower()
    
    # Categorization logic
    if any(word in name for word in ['appetizer', 'starter', 'bruschetta', 'chips', 'fries', 'nugget', 'fish finger', 'soup']):
        categories['Appetizers'].append(item)
    elif 'salad' in name:
        categories['Salad'].append(item)
    elif 'taco' in name:
        categories['Tacos'].append(item)
    elif 'burrito' in name:
        categories['Burrito'].append(item)
    elif 'quesadilla' in name:
        categories['Quesadilla'].append(item)
    elif 'pizza' in name or 'pizzadilla' in name:
        categories['Pizza'].append(item)
    elif 'spaghetti' in name or 'pasta' in name:
        categories['Spaghetti'].append(item)
    elif any(word in name for word in ['beer', 'soda', 'juice', 'coffee', 'tea', 'water', 'bia', 'lon', 'ly', 'drink']):
        categories['Drinks'].append(item)
    elif any(word in name for word in ['rice', 'noodle', 'main', 'dish', 'entree', 'meal']):
        categories['Main Dish'].append(item)
    else:
        categories['Extra'].append(item)

# Save to JSON file
with open('public/menu_data.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print('Menu data extracted and saved to public/menu_data.json')
print(f'Total unique items: {len(unique_items)}')
for category, items in categories.items():
    print(f'{category}: {len(items)} items')
`;

// Write the Python script to a temporary file
const tempScriptPath = path.join(__dirname, 'temp_extract.py');
fs.writeFileSync(tempScriptPath, pythonScript);

// Execute the Python script
const { execSync } = require('child_process');

try {
    console.log('Extracting menu data from Excel files...');
    execSync(`python3 ${tempScriptPath}`, { stdio: 'inherit' });
    console.log('✅ Menu data extraction completed successfully!');
} catch (error) {
    console.error('❌ Error extracting menu data:');
    console.error('Make sure you have Python 3 installed with pandas and openpyxl:');
    console.error('pip install pandas openpyxl');
    process.exit(1);
} finally {
    // Clean up temporary file
    if (fs.existsSync(tempScriptPath)) {
        fs.unlinkSync(tempScriptPath);
    }
}
