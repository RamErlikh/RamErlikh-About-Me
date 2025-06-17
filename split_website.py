#!/usr/bin/env python3
"""
HTML File Splitter for Ram Erlikh's Portfolio Website
Split the large HTML file into multiple organized files for GitHub Pages
"""

import os
import re

def extract_section(content, start_pattern, end_pattern=None, include_patterns=None):
    """Extract a section from HTML content based on patterns"""
    start_match = re.search(start_pattern, content, re.MULTILINE | re.DOTALL)
    if not start_match:
        return ""
    
    start_pos = start_match.start()
    
    if end_pattern:
        end_match = re.search(end_pattern, content[start_pos:], re.MULTILINE | re.DOTALL)
        if end_match:
            end_pos = start_pos + end_match.end()
        else:
            end_pos = len(content)
    else:
        end_pos = len(content)
    
    section = content[start_pos:end_pos]
    
    # Include additional patterns if specified
    if include_patterns:
        for pattern in include_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if match.start() < start_pos or match.start() > end_pos:
                    section += "\n" + match.group()
    
    return section

def split_html_file():
    """Split the large HTML file into multiple organized files"""
    
    # Read the original HTML file
    html_file = "index.html"
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {html_file} not found")
        return False
    
    print(f"Original file size: {len(content)} characters")
    
    # Create directories for organized files
    directories = [
        'assets',
        'assets/css',
        'assets/js',
        'assets/data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Extract different sections
    
    # 1. Extract CSS styles
    css_content = extract_css_styles(content)
    with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    print("✓ Extracted CSS to assets/css/styles.css")
    
    # 2. Extract JavaScript
    js_content = extract_javascript(content)
    with open('assets/js/main.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("✓ Extracted JavaScript to assets/js/main.js")
    
    # 3. Extract theme-specific CSS
    theme_css = extract_theme_css(content)
    with open('assets/css/themes.css', 'w', encoding='utf-8') as f:
        f.write(theme_css)
    print("✓ Extracted theme CSS to assets/css/themes.css")
    
    # 4. Extract configuration data
    config_data = extract_config_data(content)
    with open('assets/data/config.js', 'w', encoding='utf-8') as f:
        f.write(config_data)
    print("✓ Extracted configuration to assets/data/config.js")
    
    # 5. Create the main HTML structure
    main_html = create_main_html(content)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(main_html)
    print("✓ Created new modular index.html")
    
    # 6. Create additional files
    create_readme()
    create_gitignore()
    create_github_pages_config()
    
    print("\n🎉 Website successfully split into multiple files!")
    print("\nFile structure:")
    print("├── index.html (main file)")
    print("├── assets/")
    print("│   ├── css/")
    print("│   │   ├── styles.css (main styles)")
    print("│   │   └── themes.css (theme styles)")
    print("│   ├── js/")
    print("│   │   └── main.js (all JavaScript)")
    print("│   └── data/")
    print("│       └── config.js (configuration)")
    print("├── README.md")
    print("├── .gitignore")
    print("└── _config.yml (GitHub Pages)")
    
    return True

def extract_css_styles(content):
    """Extract main CSS styles"""
    css_sections = []
    
    # Extract main style block
    style_pattern = r'<style[^>]*>(.*?)</style>'
    style_matches = re.finditer(style_pattern, content, re.DOTALL)
    
    for match in style_matches:
        style_content = match.group(1).strip()
        if style_content and not any(x in style_content.lower() for x in ['theme-', 'loading-', 'confetti-']):
            css_sections.append(style_content)
    
    return '\n\n'.join(css_sections)

def extract_theme_css(content):
    """Extract theme-specific CSS"""
    theme_css_sections = []
    
    # Extract theme-related styles
    style_pattern = r'<style[^>]*>(.*?)</style>'
    style_matches = re.finditer(style_pattern, content, re.DOTALL)
    
    for match in style_matches:
        style_content = match.group(1).strip()
        if style_content and any(x in style_content.lower() for x in ['theme-', 'loading-', 'confetti-']):
            theme_css_sections.append(style_content)
    
    return '\n\n'.join(theme_css_sections)

def extract_javascript(content):
    """Extract JavaScript code"""
    js_sections = []
    
    # Extract script blocks
    script_pattern = r'<script[^>]*>(.*?)</script>'
    script_matches = re.finditer(script_pattern, content, re.DOTALL)
    
    for match in script_matches:
        script_content = match.group(1).strip()
        if script_content and not script_content.startswith('document.addEventListener'):
            js_sections.append(script_content)
    
    # Wrap in DOMContentLoaded for safety
    js_code = '\n\n'.join(js_sections)
    
    return f"""// Ram Erlikh Portfolio Website - Main JavaScript
// Generated by split_website.py

document.addEventListener('DOMContentLoaded', function() {{
    {js_code}
}});"""

def extract_config_data(content):
    """Extract configuration data"""
    config_sections = []
    
    # Extract theme configurations
    theme_pattern = r'const themes = \[(.*?)\];'
    theme_match = re.search(theme_pattern, content, re.DOTALL)
    if theme_match:
        config_sections.append(f"window.themes = [{theme_match.group(1)}];")
    
    # Extract other configurations
    track_pattern = r'const tracks = \[(.*?)\];'
    track_match = re.search(track_pattern, content, re.DOTALL)
    if track_match:
        config_sections.append(f"window.tracks = [{track_match.group(1)}];")
    
    return '\n\n'.join(config_sections)

def create_main_html(content):
    """Create the main HTML structure"""
    
    # Extract head content (without styles and scripts)
    head_pattern = r'<head>(.*?)</head>'
    head_match = re.search(head_pattern, content, re.DOTALL)
    head_content = head_match.group(1) if head_match else ""
    
    # Remove existing styles and scripts from head
    head_content = re.sub(r'<style[^>]*>.*?</style>', '', head_content, flags=re.DOTALL)
    head_content = re.sub(r'<script[^>]*>.*?</script>', '', head_content, flags=re.DOTALL)
    
    # Extract body content
    body_pattern = r'<body[^>]*>(.*?)</body>'
    body_match = re.search(body_pattern, content, re.DOTALL)
    if not body_match:
        # Try to find content after head tag
        head_end = content.find('</head>')
        if head_end != -1:
            body_content = content[head_end + 7:]
            # Remove scripts from body
            body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL)
            body_content = body_content.replace('</html>', '').strip()
        else:
            body_content = "<!-- Body content extraction failed -->"
    else:
        body_content = body_match.group(1)
        # Remove scripts from body
        body_content = re.sub(r'<script[^>]*>.*?</script>', '', body_content, flags=re.DOTALL)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    {head_content.strip()}
    
    <!-- External CSS -->
    <link href="assets/css/styles.css" rel="stylesheet">
    <link href="assets/css/themes.css" rel="stylesheet">
</head>
<body>
    {body_content.strip()}
    
    <!-- External JavaScript -->
    <script src="assets/data/config.js"></script>
    <script src="assets/js/main.js"></script>
</body>
</html>"""

def create_readme():
    """Create README.md file"""
    readme_content = """# Ram Erlikh - Portfolio Website

A modern, responsive portfolio website featuring multiple themes and interactive elements.

## 🚀 Features

- **Multiple Themes**: Switch between 15+ unique themes including Dark Mode, Neon, Cyberpunk, and more
- **Responsive Design**: Optimized for all device sizes
- **Interactive Elements**: Animations, particle effects, and smooth transitions
- **Music Player**: Built-in audio player with multiple tracks
- **Contact Form**: Functional contact form with Web3Forms integration
- **Terminal Interface**: Interactive terminal for fun commands

## 🛠️ Technologies Used

- HTML5
- CSS3 (with advanced animations and transitions)
- Vanilla JavaScript (ES6+)
- Font Awesome Icons
- Animate.css
- Web3Forms API

## 📁 Project Structure

```
├── index.html              # Main HTML file
├── assets/
│   ├── css/
│   │   ├── styles.css      # Main stylesheet
│   │   └── themes.css      # Theme-specific styles
│   │   └── config.js       # Configuration data
│   ├── js/
│   │   └── main.js         # Main JavaScript functionality
│   └── data/
│       └── config.js       # Configuration data
├── favicon.svg             # Favicon (SVG)
├── favicon.png             # Favicon (PNG fallback)
├── apple-touch-icon.png    # Apple touch icon
└── CNAME                   # Custom domain configuration
```

## 🎨 Available Themes

1. Modern (Default)
2. Dark Mode
3. Neon
4. Windows XP
5. Modern Tech
6. Cyberpunk
7. Minimalist
8. Creative Agency
9. Portfolio
10. Vaporwave
11. Glassmorphism
12. Retro
13. Brutalist
14. Gradient
15. Cosmic Space

## 🚀 Getting Started

1. Clone this repository
2. Open `index.html` in your browser
3. Or serve using a local web server for best experience

## 📝 License

© 2025 Ram Erlikh. All rights reserved.

## 🌐 Live Demo

Visit: [https://ramerlikh.com](https://ramerlikh.com)
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✓ Created README.md")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE/Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Backup files
*_backup.html
*_backup_*.html

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Temporary files
*.tmp
*.temp

# Build outputs
dist/
build/
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_github_pages_config():
    """Create GitHub Pages configuration"""
    config_content = """# GitHub Pages Configuration
title: "Ram Erlikh - Portfolio"
description: "Full-stack developer and tech enthusiast"
author: "Ram Erlikh"
url: "https://ramerlikh.com"

# Build settings
markdown: kramdown
highlighter: rouge
plugins:
  - jekyll-feed
  - jekyll-sitemap

# Exclude files from processing
exclude:
  - "*.py"
  - "*.log"
  - "*_backup*"
  - README.md
  - .gitignore

# Include files
include:
  - assets/
  - CNAME
"""
    
    with open('_config.yml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("✓ Created _config.yml for GitHub Pages")

if __name__ == "__main__":
    print("🔧 Ram Erlikh Portfolio Website Splitter")
    print("========================================")
    print("Converting large HTML file into modular structure...")
    print()
    
    success = split_html_file()
    
    if success:
        print("\n🎉 SUCCESS! Your website has been successfully modularized.")
        print("\nNext steps:")
        print("1. Test the website locally by opening index.html")
        print("2. Commit and push to GitHub")
        print("3. Enable GitHub Pages in repository settings")
        print("4. Your site will be available at https://username.github.io/repository-name")
    else:
        print("\n❌ Error occurred during the split process") 