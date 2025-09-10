# PetMedix Development Guide

## Quick Start - Bypass Login for Development

This setup allows you to bypass the login process during development and directly access the main application.

### 🚀 How to Use

1. **Enable Development Mode**
   - Open `dev_config.py`
   - Set `DEVELOPMENT_MODE = True`
   - The application will now skip login and go directly to the main interface

2. **Switch User Roles for Testing**
   - Use the role switcher script: `python switch_role.py`
   - Or manually edit `dev_config.py` and change the `role` in `DEV_USER`

### 📁 Files Created/Modified

- `main.py` - Modified to support development mode
- `dev_config.py` - Development configuration file
- `switch_role.py` - Helper script to switch user roles
- `DEVELOPMENT.md` - This guide

### 🔧 Available User Roles

- **Admin** - Full access to all features
- **Veterinarian** - Medical staff access
- **Receptionist** - Front desk access  
- **Client** - Limited client access

### 🎯 Quick Commands

```bash
# Switch to Admin role
python switch_role.py Admin

# Switch to Veterinarian role
python switch_role.py Veterinarian

# Interactive role switcher
python switch_role.py

# Run the application (will use current dev_config.py settings)
python main.py
```

### 🔄 Switching Between Development and Production

**For Development:**
```python
# In dev_config.py
DEVELOPMENT_MODE = True
```

**For Production:**
```python
# In dev_config.py
DEVELOPMENT_MODE = False
```

### 💡 Tips

1. **Testing Different Roles**: Use `switch_role.py` to quickly test how the interface looks for different user types
2. **Database Independence**: Development mode doesn't require database authentication
3. **Easy Toggle**: Just change one line in `dev_config.py` to switch between dev and production modes
4. **Safe for Production**: The login system remains intact and will be used when `DEVELOPMENT_MODE = False`

### 🛠️ Customization

You can customize the development user in `dev_config.py`:

```python
DEV_USER = {
    "user_id": "DEV001",
    "role": "Admin",  # Change this to test different roles
    "last_name": "Developer",
    "first_name": "Test"
}
```

### 🔒 Security Note

- Development mode is for testing only
- Always set `DEVELOPMENT_MODE = False` before deploying to production
- The login system remains fully functional and secure
