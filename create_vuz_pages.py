#!/usr/bin/env python3
"""
Script to parse military universities table and create individual HTML pages for each university.
"""

import re
import os
from pathlib import Path

def parse_military_vuzes_table(file_path):
    """Parse the military universities markdown table and extract information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into sections for each university
    sections = re.split(r'---\s*\n', content)
    
    universities = []
    
    for section in sections:
        # Look for university title pattern
        title_match = re.search(r'## (\d+)\. (.+)', section)
        if title_match:
            num = title_match.group(1)
            name = title_match.group(2)
            
            # Extract table content
            table_content = {}
            # Find all parameter-value pairs in the table
            param_matches = re.findall(r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', section)
            
            for param, value in param_matches:
                # Clean up the parameter name and value
                clean_param = param.strip()
                clean_value = value.strip()
                
                # Handle special cases where value might contain markdown formatting
                if '*Данные не найдены*' in clean_value or '*Официальные данные не опубликованы*' in clean_value:
                    clean_value = 'Данные не найдены'
                
                table_content[clean_param] = clean_value
            
            universities.append({
                'number': num,
                'name': name,
                'data': table_content
            })
    
    return universities

def generate_vuz_page(university_info):
    """Generate HTML page for a single university."""
    name = university_info['name']
    data = university_info['data']
    
    # Create a URL-friendly filename
    filename = re.sub(r'[^\w\s-]', '', name.lower()).strip().replace(' ', '_')
    filename = f"{filename}.html"
    
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Информационно-методический сайт ВУЗов МО РФ</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>{name}</h1>
        </div>
    </header>

    <main class="container">
        <nav aria-label="Breadcrumb" class="breadcrumb">
            <a href="../vuzy.html">Военные ВУЗы</a> &gt; {name}
        </nav>

        <div class="vuz-info-table">
            <table class="info-table">
                <tbody>
"""
    
    # Add all available information from the table
    for param, value in data.items():
        html_content += f"""                    <tr>
                        <th scope="row">{param}</th>
                        <td>{value}</td>
                    </tr>
"""
    
    html_content += """                </tbody>
            </table>
        </div>
        
        <div class="back-link">
            <a href="../vuzy.html">&larr; Назад к списку военных ВУЗов</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Информационно-методический сайт ВУЗов МО РФ. Все права защищены.</p>
        </div>
    </footer>
</body>
</html>"""
    
    return filename, html_content

def main():
    # Parse the military universities table
    universities = parse_military_vuzes_table('/workspace/military_vuzes_table.md')
    
    # Create directory for university pages if it doesn't exist
    vuzes_dir = Path('/workspace/vuzes')
    vuzes_dir.mkdir(exist_ok=True)
    
    # Generate HTML page for each university
    for i, university in enumerate(universities):
        filename, content = generate_vuz_page(university)
        filepath = vuzes_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created page: {filepath.name}")
    
    print(f"\nTotal universities processed: {len(universities)}")
    print("University pages created successfully!")

if __name__ == "__main__":
    main()