#!/usr/bin/env python3
"""
Script to create HTML pages for uncovered universities from the CSV file.
"""

import csv
import re
import os
from pathlib import Path


def normalize_filename(name):
    """Convert university name to a URL-friendly filename."""
    # Remove special characters and convert to lowercase
    normalized = re.sub(r'[^\w\s-]', '', name.lower()).strip()
    # Replace spaces and special characters with hyphens
    normalized = re.sub(r'[\s_]+', '-', normalized)
    # Remove multiple consecutive hyphens
    normalized = re.sub(r'-+', '-', normalized)
    return normalized


def create_university_html(university_data):
    """Generate HTML content for a university."""
    num = university_data['№']
    name = university_data['Название ВУЗа']
    status = university_data['Статус']
    city = university_data['Город']
    specialties = university_data['Специальности (коды ФГОС)']
    civilian_analogs = university_data['Гражданские аналоги (коды ОКСО)']
    study_duration = university_data['Сроки обучения']
    faculties = university_data['Факультеты']
    places_2025 = university_data['Места 2025']
    places_2026 = university_data['Места 2026']
    website = university_data['Сайт']
    phones = university_data['Телефоны (приемная/ВУЗ)']
    email = university_data['Email']
    description = university_data['Описание (10-15 предложений)']
    history = university_data['История (10-15 предложений)']
    head_vuz = university_data['Головной ВУЗ']
    
    filename = f"{num}-{normalize_filename(name)}.html"
    
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
                    <tr>
                        <th scope="row">Порядковый номер</th>
                        <td>{num}</td>
                    </tr>
                    <tr>
                        <th scope="row">Название ВУЗа</th>
                        <td>{name}</td>
                    </tr>
                    <tr>
                        <th scope="row">Статус</th>
                        <td>{status}</td>
                    </tr>
                    <tr>
                        <th scope="row">Город</th>
                        <td>{city}</td>
                    </tr>
                    <tr>
                        <th scope="row">Специальности (коды ФГОС)</th>
                        <td>{specialties}</td>
                    </tr>
                    <tr>
                        <th scope="row">Гражданские аналоги (коды ОКСО)</th>
                        <td>{civilian_analogs}</td>
                    </tr>
                    <tr>
                        <th scope="row">Сроки обучения</th>
                        <td>{study_duration}</td>
                    </tr>
                    <tr>
                        <th scope="row">Факультеты</th>
                        <td>{faculties}</td>
                    </tr>
                    <tr>
                        <th scope="row">Места 2025</th>
                        <td>{places_2025}</td>
                    </tr>
                    <tr>
                        <th scope="row">Места 2026</th>
                        <td>{places_2026}</td>
                    </tr>
                    <tr>
                        <th scope="row">Сайт</th>
                        <td><a href="{website}" target="_blank">{website}</a></td>
                    </tr>
                    <tr>
                        <th scope="row">Телефоны (приемная/ВУЗ)</th>
                        <td>{phones}</td>
                    </tr>
                    <tr>
                        <th scope="row">Email</th>
                        <td>{email}</td>
                    </tr>
                    <tr>
                        <th scope="row">Описание (10-15 предложений)</th>
                        <td>{description}</td>
                    </tr>
                    <tr>
                        <th scope="row">История (10-15 предложений)</th>
                        <td>{history}</td>
                    </tr>
                    <tr>
                        <th scope="row">Головной ВУЗ</th>
                        <td>{head_vuz}</td>
                    </tr>
                </tbody>
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
    # Read the CSV file
    csv_file = '/workspace/table-962f00e2-3cad-49ec-ab64-4e4a0f6b5479.csv'
    vuz_pages_dir = Path('/workspace/vuz_pages/')
    
    # Create directory if it doesn't exist
    vuz_pages_dir.mkdir(exist_ok=True)
    
    # Get list of existing files to avoid duplicates
    existing_files = set()
    for filename in os.listdir(vuz_pages_dir):
        if filename.endswith('.html'):
            existing_files.add(filename)
    
    # Read CSV and find uncovered universities
    uncovered_count = 0
    with open(csv_file, 'r', encoding='utf-8-sig') as f:  # Using utf-8-sig to handle BOM
        reader = csv.DictReader(f)
        for row in reader:
            # Handle BOM in the first column header
            num = row['\ufeff№'] if '\ufeff№' in row else row['№']
            name = row['Название ВУЗа']
            
            # Check if a file for this university already exists
            expected_filename = f"{num}-{normalize_filename(name)}.html"
            
            if expected_filename not in existing_files:
                # Create HTML page for this university
                filename, content = create_university_html(row)
                filepath = vuz_pages_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                
                print(f"Created page: {filepath.name}")
                uncovered_count += 1
    
    print(f"\nTotal new university pages created: {uncovered_count}")


if __name__ == "__main__":
    main()