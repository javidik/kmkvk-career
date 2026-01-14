#!/usr/bin/env python3
"""
Script to create individual pages for all military universities based on the markdown file.
"""

import os
import re
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def parse_markdown_file(file_path):
    """Parse the markdown file to extract university information."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by the university separators
    sections = re.split(r'^---$', content, flags=re.MULTILINE)
    
    universities = []
    
    for section in sections:
        # Find the university title
        title_match = re.search(r'^##\s+(.+)$', section, re.MULTILINE)
        if not title_match:
            continue
            
        title = title_match.group(1).strip()
        
        # Remove the title from the section to get the table content
        section_content = re.sub(r'^##\s+.+$', '', section, count=1, flags=re.MULTILINE).strip()
        
        # Extract the table data
        table_match = re.search(r'\|(.+)\|(.+)\|', section_content, re.MULTILINE)
        if not table_match:
            continue
        
        # Parse the table into key-value pairs
        table_data = {}
        # Split by lines and process each row
        lines = section_content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('|') and '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    key = parts[1].strip()
                    value = parts[2].strip()
                    # Clean up bold formatting
                    key = re.sub(r'\*\*(.*?)\*\*', r'\1', key)
                    value = re.sub(r'\*\*(.*?)\*\*', r'\1', value)
                    value = re.sub(r'\*(.*?)\*', r'\1', value)
                    if key and value:
                        table_data[key] = value
        
        if table_data:
            universities.append({
                'title': title,
                'data': table_data
            })
    
    return universities

def create_university_page(university_info, output_dir):
    """Create an HTML page for a single university."""
    title = university_info['title']
    data = university_info['data']
    
    # Create filename slug from title
    filename_slug = slugify(title)
    filename = f"{filename_slug}.html"
    filepath = os.path.join(output_dir, filename)
    
    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Каталог ВУЗов</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>
  <header>
    <div class="container header-container">
      <div class="logo-section">
        <img src="../assets/logo.png" alt="КМКВК" class="logo">
        <div class="header-title">
          <h2 style="margin: 0; font-size: 18px;">КМКВК</h2>
          <p style="margin: 0; font-size: 12px; opacity: 0.9;">Путь к военной карьере</p>
        </div>
      </div>
      <nav>
        <ul>
          <li><a href="../index.html" class="nav-link">Главная</a></li>
          <li><a href="../vuzy.html" class="nav-link active">Военные ВУЗы</a></li>
          <li><a href="../etapy.html" class="nav-link">Этапы поступления</a></li>
          <li><a href="../lgoty.html" class="nav-link">Льготы</a></li>
          <li><a href="../podgotovka.html" class="nav-link">Подготовка</a></li>
          <li><a href="../biblioteka.html" class="nav-link">Библиотека</a></li>
          <li><a href="../contacts.html" class="nav-link">Контакты</a></li>
        </ul>
        <div class="burger-menu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero" style="padding: 60px 24px 40px;">
      <div class="container">
        <h1>{title}</h1>
        <p class="hero-subtitle">{data.get('Полное название', '')}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="card" style="background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px;">
"""
    
    # Add contact information sections
    contact_fields = [
        ('Город', 'map-marker-alt'),
        ('Адрес', 'map-marker-alt'),
        ('Сайт', 'globe'),
        ('Главный телефон', 'phone'),
        ('Горячая линия', 'phone'),
        ('Email', 'envelope'),
        ('Email приемной комиссии', 'envelope'),
        ('Основан', 'history'),
        ('Основано', 'history')
    ]
    
    for field, icon in contact_fields:
        if field in data:
            value = data[field]
            # Handle website links
            if field == 'Сайт':
                value = f'<a href="http://{value}" target="_blank">{value}</a>'
            html_content += f"""
            <div>
              <h3><i class="fas fa-{icon}" style="color: #d4af37;"></i> {field}</h3>
              <p><strong>{field}:</strong> {value}</p>
            </div>
"""
    
    html_content += """
          </div>
"""
    
    # Add description sections
    description_fields = [
        ('Описание', 'book'),
        ('Историческая справка', 'history'),
        ('Историческая справка (краткая)', 'history'),
        ('Факультеты', 'building'),
        ('Основные специальности', 'graduation-cap'),
        ('Основные специальности (коды и названия)', 'graduation-cap'),
        ('Гражданские аналоги', 'users'),
        ('Гражданские аналоги специальностей', 'users'),
        ('Сроки обучения', 'clock'),
        ('Количество мест 2025 год', 'users'),
        ('Количество мест 2026 год', 'users'),
        ('Бюджетные места по факультетам', 'users')
    ]
    
    for field, icon in description_fields:
        if field in data:
            value = data[field]
            html_content += f"""
          <div style="margin-top: 30px;">
            <h3><i class="fas fa-{icon}" style="color: #d4af37;"></i> {field}</h3>
            <p>{value}</p>
          </div>
"""
    
    html_content += """
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container footer-container">
      <div class="footer-section">
        <h3>Контактная информация</h3>
        <p>Email: <a href="mailto:info@kmkvk.ru">info@kmkvk.ru</a></p>
      </div>
      <div class="footer-section">
        <h3>Навигация</h3>
        <ul class="footer-links">
          <li><a href="../vuzy.html">ВУЗы</a></li>
          <li><a href="../contacts.html">Контакты</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 КМКВК. Все права защищены.</p>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>"""
    
    # Write the HTML file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Created: {filepath}")
    return filename

def main():
    markdown_file = "military_vuzes_table.md"
    output_dir = "vuz_pages"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse the markdown file
    universities = parse_markdown_file(markdown_file)
    
    print(f"Found {len(universities)} universities")
    
    # Create HTML pages for each university
    created_files = []
    for uni in universities:
        try:
            filename = create_university_page(uni, output_dir)
            created_files.append(filename)
        except Exception as e:
            print(f"Error creating page for {uni['title']}: {e}")
    
    print(f"\nSuccessfully created {len(created_files)} university pages.")
    
    # Also create an index of all universities
    index_content = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Все военные ВУЗы — Каталог ВУЗов</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
</head>
<body>
  <header>
    <div class="container header-container">
      <div class="logo-section">
        <img src="../assets/logo.png" alt="КМКВК" class="logo">
        <div class="header-title">
          <h2 style="margin: 0; font-size: 18px;">КМКВК</h2>
          <p style="margin: 0; font-size: 12px; opacity: 0.9;">Путь к военной карьере</p>
        </div>
      </div>
      <nav>
        <ul>
          <li><a href="../index.html" class="nav-link">Главная</a></li>
          <li><a href="../vuzy.html" class="nav-link active">Военные ВУЗы</a></li>
          <li><a href="../etapy.html" class="nav-link">Этапы поступления</a></li>
          <li><a href="../lgoty.html" class="nav-link">Льготы</a></li>
          <li><a href="../podgotovka.html" class="nav-link">Подготовка</a></li>
          <li><a href="../biblioteka.html" class="nav-link">Библиотека</a></li>
          <li><a href="../contacts.html" class="nav-link">Контакты</a></li>
        </ul>
        <div class="burger-menu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero" style="padding: 60px 24px 40px;">
      <div class="container">
        <h1>Все военные ВУЗы МО РФ</h1>
        <p class="hero-subtitle">Полный список военных образовательных учреждений</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="cards-grid">
"""
    
    for uni in universities:
        title = uni['title']
        # Remove numbering from title
        clean_title = re.sub(r'^\d+\.\s*', '', title)
        filename_slug = slugify(title)
        index_content += f"""          <a href="{filename_slug}.html" class="quick-card">
            <i class="fas fa-graduation-cap"></i>
            <h3>{clean_title}</h3>
            <p>Перейти к информации о ВУЗе</p>
          </a>
"""
    
    index_content += """        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container footer-container">
      <div class="footer-section">
        <h3>Контактная информация</h3>
        <p>Email: <a href="mailto:info@kmkvk.ru">info@kmkvk.ru</a></p>
      </div>
      <div class="footer-section">
        <h3>Навигация</h3>
        <ul class="footer-links">
          <li><a href="../vuzy.html">ВУЗы</a></li>
          <li><a href="../contacts.html">Контакты</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2025 КМКВК. Все права защищены.</p>
    </div>
  </footer>

  <script src="../js/main.js"></script>
</body>
</html>"""
    
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Created index page: {index_path}")

if __name__ == "__main__":
    main()