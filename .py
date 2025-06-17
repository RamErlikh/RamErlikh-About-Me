#!/usr/bin/env python3
"""
Script to fix Ram Erlikh's portfolio website timeline box widths
Make timeline content boxes more symmetrical and rectangular
"""

import re
import os

def fix_timeline_widths():
    """Fix the timeline content widths for better symmetrical appearance"""
    
    # Path to the website file
    website_path = r"C:\Users\ramno\RamErlikh-About-Me\index.html"
    
    # Read the HTML file
    try:
        with open(website_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: Could not find file at {website_path}")
        return False
    
    print("Original file loaded successfully!")
    
    # Make a backup
    backup_path = website_path.replace('.html', '_widths_backup.html')
    with open(backup_path, 'w', encoding='utf-8') as backup_file:
        backup_file.write(content)
    print(f"Backup created: {backup_path}")
    
    print("\n--- Fixing timeline content widths for symmetrical appearance ---")
    
    # Improved timeline-content CSS for better symmetry and rectangular appearance
    base_timeline_content_css = """.timeline-content {
    padding: 25px 30px; /* More generous padding for rectangular look */
    background: white;
    position: relative;
    border-radius: 10px; /* Slightly more rounded corners */
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    transition: all 0.3s ease;
    min-height: 110px; /* Consistent minimum height for rectangular shape */
    max-width: 420px; /* Maximum width for better proportions */
    width: 100%; /* Full width within the item */
    display: flex;
    flex-direction: column;
    justify-content: center;
    aspect-ratio: 2.8/1; /* Maintain rectangular proportions */
}"""

    # Desktop-specific improvements
    desktop_timeline_content_css = """    .timeline-content {
        padding: 25px 30px;
        background: white;
        position: relative;
        border-radius: 10px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        transition: all 0.3s ease;
        min-height: 110px; /* Consistent height for rectangular shape */
        max-width: 420px; /* Maximum width for better proportions */
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        aspect-ratio: 2.8/1; /* Maintain rectangular proportions */
    }
    
    .timeline-content:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }"""

    # Mobile-specific improvements
    mobile_timeline_content_css = """    .timeline-content {
        padding: 20px 25px; /* Better mobile padding */
        min-height: 100px; /* Slightly smaller on mobile */
        max-width: none; /* Allow full width on mobile */
        border-radius: 8px;
        aspect-ratio: 2.5/1; /* Slightly different ratio for mobile */
    }"""
    
    # Replace the base timeline-content CSS
    base_pattern = r'\.timeline-content \{[^}]*\}'
    if re.search(base_pattern, content):
        content = re.sub(base_pattern, base_timeline_content_css, content, count=1)
        print("✓ Updated base timeline-content CSS")
    
    # Update the desktop media query timeline-content
    desktop_pattern = r'@media screen and \(min-width: 769px\) \{[^{]*\.timeline-content \{[^}]*\}'
    desktop_section_start = content.find('@media screen and (min-width: 769px)')
    if desktop_section_start != -1:
        # Find the timeline-content within this media query
        desktop_section = content[desktop_section_start:desktop_section_start + 2000]  # Look ahead 2000 chars
        if '.timeline-content {' in desktop_section:
            # Replace the content within the desktop media query
            desktop_replacement = desktop_timeline_content_css
            # Find the exact location and replace
            start_pos = content.find('.timeline-content {', desktop_section_start)
            if start_pos != -1:
                end_pos = content.find('}', start_pos) + 1
                content = content[:start_pos] + desktop_timeline_content_css.strip() + content[end_pos:]
                print("✓ Updated desktop timeline-content CSS")
    
    # Update the mobile media query timeline-content
    mobile_section_start = content.find('@media screen and (max-width: 768px)')
    if mobile_section_start != -1:
        # Find the timeline-content within this media query
        mobile_section = content[mobile_section_start:mobile_section_start + 1500]  # Look ahead 1500 chars
        if '.timeline-content {' in mobile_section:
            start_pos = content.find('.timeline-content {', mobile_section_start)
            if start_pos != -1:
                end_pos = content.find('}', start_pos) + 1
                content = content[:start_pos] + mobile_timeline_content_css.strip() + content[end_pos:]
                print("✓ Updated mobile timeline-content CSS")
    
    # Add hover effects for better interactivity
    hover_css = """
.timeline-content:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.timeline-item:hover .timeline-date {
    transform: translateY(-50%) scale(1.05);
    background: #3b82f6;
    color: white;
}
"""
    
    # Add the hover effects before the theme-specific styles
    theme_start = content.find('/* Theme-specific timeline styles */')
    if theme_start != -1:
        content = content[:theme_start] + hover_css + '\n' + content[theme_start:]
        print("✓ Added hover effects for better interactivity")
    
    # Write the updated content back to the file
    try:
        with open(website_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"\n✅ Successfully updated {website_path}")
        return True
    except Exception as e:
        print(f"\n❌ Error writing file: {e}")
        return False

def commit_changes():
    """Commit the changes to git"""
    import subprocess
    
    repo_path = r"C:\Users\ramno\RamErlikh-About-Me"
    
    try:
        # Add changes
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
        print("✓ Changes added to git")
        
        # Commit changes
        commit_msg = "Fix timeline content widths for better symmetrical rectangular appearance"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_path, check=True)
        print("✓ Changes committed")
        
        # Push changes
        subprocess.run(['git', 'push'], cwd=repo_path, check=True)
        print("✓ Changes pushed to GitHub")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Ram Erlikh Portfolio - Timeline Width Fixer")
    print("=" * 55)
    
    success = fix_timeline_widths()
    
    if success:
        print("\n🎉 Timeline width fixes completed successfully!")
        print("\nChanges made:")
        print("1. ✓ Made timeline content boxes more symmetrical")
        print("2. ✓ Added consistent max-width (420px) for rectangular appearance")
        print("3. ✓ Implemented aspect-ratio for consistent proportions")
        print("4. ✓ Improved padding and spacing for better look")
        print("5. ✓ Enhanced shadow effects for depth")
        print("6. ✓ Added hover animations for interactivity")
        print("7. ✓ Optimized for both desktop and mobile")
        
        # Ask if user wants to commit changes
        commit_choice = input("\n🤔 Would you like to commit and push these changes to GitHub? (y/n): ").lower()
        if commit_choice == 'y':
            if commit_changes():
                print("\n🌐 Changes successfully pushed to GitHub!")
                print("Your website will update automatically within a few minutes.")
            else:
                print("\n⚠️ Manual git commit may be required")
        
        print("\nYour timeline boxes should now look perfectly symmetrical and rectangular!")
    else:
        print("\n❌ Some issues occurred during the fix process")