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

# Read all Excel files and combine the data
files = ['Menu-Taco-Place-Translated.xlsx', 'SimplePlace-dssanpham_hd.xlsx', 'simple-place-menu.xlsx', 'taco-place-menu.xlsx']
all_items = []

for file in files:
    if os.path.exists(file):
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            # Check if it's a pizza item
            name_lower = row['Ten_san_pham'].lower()
            is_pizza = 'pizza' in name_lower or 'pizzadilla' in name_lower
            
            item = {
                'name': row['Ten_san_pham'],
                'unit': row['Don_vi_tinh'],
                'price': int(row['Don_gia']),
                'source': file,
                'isPizza': is_pizza,
                'sizes': ['Medium', 'Large'] if is_pizza else None
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

# Categorize items
categories = {
    'Pizza': [],
    'Tacos': [],
    'Appetizers': [],
    'Drinks': [],
    'Desserts': [],
    'Other': []
}

for item in unique_items:
    name = item['name'].lower()
    if 'pizza' in name or 'margherita' in name or 'pepperoni' in name:
        categories['Pizza'].append(item)
    elif 'taco' in name or 'burrito' in name or 'quesadilla' in name:
        categories['Tacos'].append(item)
    elif any(word in name for word in ['soup', 'salad', 'bruschetta', 'chips', 'fries', 'nugget', 'fish finger']):
        categories['Appetizers'].append(item)
    elif any(word in name for word in ['beer', 'soda', 'juice', 'coffee', 'tea', 'water', 'bia', 'lon', 'ly']):
        categories['Drinks'].append(item)
    elif any(word in name for word in ['dessert', 'panna cotta', 'cake', 'ice cream', 'pudding']):
        categories['Desserts'].append(item)
    else:
        categories['Other'].append(item)

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
