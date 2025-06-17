#!/usr/bin/env python3
"""
Website Validation Script
Check if the modular HTML structure is working correctly
"""

import os
import re

def validate_file_exists(file_path, description):
    """Check if a file exists and report its size"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✓ {description}: {file_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} (NOT FOUND)")
        return False

def validate_html_links(html_file):
    """Validate that HTML file properly links to CSS and JS files"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for CSS links
        css_links = re.findall(r'<link[^>]*href="([^"]*\.css)"', content)
        js_links = re.findall(r'<script[^>]*src="([^"]*\.js)"', content)
        
        print(f"\n📝 HTML File Analysis ({html_file}):")
        print(f"   CSS files linked: {len(css_links)}")
        for css in css_links:
            if os.path.exists(css):
                print(f"   ✓ {css}")
            else:
                print(f"   ❌ {css} (NOT FOUND)")
        
        print(f"   JS files linked: {len(js_links)}")
        for js in js_links:
            if os.path.exists(js):
                print(f"   ✓ {js}")
            else:
                print(f"   ❌ {js} (NOT FOUND)")
        
        return len(css_links) > 0 and len(js_links) > 0
        
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return False

def validate_website():
    """Validate the entire website structure"""
    print("🔍 Ram Erlikh Portfolio Website Validation")
    print("==========================================")
    
    all_valid = True
    
    # Check main files
    main_files = [
        ("index.html", "Main HTML file"),
        ("README.md", "README file"),
        (".gitignore", "Git ignore file"),
        ("_config.yml", "GitHub Pages config")
    ]
    
    for file_path, description in main_files:
        if not validate_file_exists(file_path, description):
            all_valid = False
    
    # Check assets directory structure
    asset_files = [
        ("assets/css/styles.css", "Main CSS styles"),
        ("assets/css/themes.css", "Theme CSS styles"),
        ("assets/js/main.js", "Main JavaScript"),
        ("assets/data/config.js", "Configuration data")
    ]
    
    print(f"\n📁 Assets Directory:")
    for file_path, description in asset_files:
        if not validate_file_exists(file_path, description):
            all_valid = False
    
    # Validate HTML links
    if not validate_html_links("index.html"):
        all_valid = False
    
    # Check for original backup files
    print(f"\n🗃️ Backup Files:")
    backup_files = [f for f in os.listdir('.') if f.endswith('_backup.html')]
    if backup_files:
        print(f"   Found {len(backup_files)} backup files (original data preserved)")
        for backup in backup_files[:3]:  # Show first 3
            print(f"   • {backup}")
        if len(backup_files) > 3:
            print(f"   • ... and {len(backup_files) - 3} more")
    else:
        print("   No backup files found")
    
    # Calculate size reduction
    if os.path.exists("index.html"):
        new_size = os.path.getsize("index.html")
        original_size = 387000  # Approximate original size
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"\n📊 Size Reduction:")
        print(f"   Original: ~{original_size:,} bytes")
        print(f"   New: {new_size:,} bytes")
        print(f"   Reduction: {reduction:.1f}%")
    
    print(f"\n{'='*50}")
    if all_valid:
        print("🎉 VALIDATION SUCCESSFUL!")
        print("✅ All files are properly structured and linked")
        print("✅ Website should work correctly on GitHub Pages")
        print("\n🌐 Next steps:")
        print("1. Visit your GitHub repository")
        print("2. Go to Settings > Pages")
        print("3. Select 'Deploy from a branch' and choose 'master'")
        print("4. Your site will be live at: https://username.github.io/RamErlikh-About-Me")
    else:
        print("❌ VALIDATION FAILED!")
        print("⚠️  Some files are missing or incorrectly linked")
        print("Please check the errors above and re-run the split script")
    
    return all_valid

if __name__ == "__main__":
    validate_website() 