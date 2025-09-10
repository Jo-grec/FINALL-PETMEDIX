#!/usr/bin/env python3
"""
Quick role switcher for development testing
Usage: python switch_role.py [role]
"""

import sys
import os

def update_dev_config(role):
    """Update the dev_config.py file with the specified role"""
    
    # Read current dev_config.py
    try:
        with open('dev_config.py', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ dev_config.py not found. Please make sure it exists.")
        return False
    
    # Update the role in the DEV_USER dictionary
    import re
    pattern = r'("role":\s*)"[^"]*"'
    replacement = f'\\1"{role}"'
    
    new_content = re.sub(pattern, replacement, content)
    
    # Write back to file
    with open('dev_config.py', 'w') as f:
        f.write(new_content)
    
    print(f"✅ Role switched to: {role}")
    return True

def show_available_roles():
    """Show available roles"""
    roles = [
        "Admin",
        "Veterinarian", 
        "Receptionist",
        "Client"
    ]
    
    print("Available roles:")
    for i, role in enumerate(roles, 1):
        print(f"  {i}. {role}")
    print(f"  {len(roles) + 1}. Exit")

def main():
    if len(sys.argv) > 1:
        role = sys.argv[1]
        if update_dev_config(role):
            print(f"🎯 Next time you run the application, you'll be logged in as: {role}")
    else:
        print("🔧 PetMedix Development Role Switcher")
        print("=" * 40)
        
        show_available_roles()
        
        while True:
            try:
                choice = input("\nSelect a role (1-5): ").strip()
                
                if choice == "5":
                    print("👋 Goodbye!")
                    break
                elif choice == "1":
                    update_dev_config("Admin")
                    break
                elif choice == "2":
                    update_dev_config("Veterinarian")
                    break
                elif choice == "3":
                    update_dev_config("Receptionist")
                    break
                elif choice == "4":
                    update_dev_config("Client")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-5.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    main()
