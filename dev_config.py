# Development Configuration
# This file allows you to easily configure development settings

# Set to True to bypass login and go directly to main application
DEVELOPMENT_MODE = True

# Development user configuration
DEV_USER = {
    "user_id": "DEV001",
    "role": "Admin",  # Options: "Admin", "Veterinarian", "Receptionist", "Client"
    "last_name": "Developer",
    "first_name": "Test"
}

# Available roles for testing (you can change DEV_USER["role"] to any of these):
AVAILABLE_ROLES = [
    "Admin",           # Full access to all features
    "Veterinarian",    # Medical staff access
    "Receptionist",    # Front desk access
    "Client"           # Limited client access
]

# Quick role switcher - uncomment the role you want to test
# DEV_USER["role"] = "Admin"
# DEV_USER["role"] = "Veterinarian" 
# DEV_USER["role"] = "Receptionist"
# DEV_USER["role"] = "Client"
