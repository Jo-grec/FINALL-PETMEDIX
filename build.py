import os
import shutil
import subprocess
import sys
from datetime import datetime

def clean_build_dirs():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name} directory")

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        subprocess.run(['pyinstaller', 'petmedix.spec', '--clean'], check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        sys.exit(1)

def create_distribution():
    """Create a complete distribution package"""
    # Create a distribution directory
    dist_dir = os.path.join('dist', 'PetMedix')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # Copy the executable
    shutil.copy2('dist/PetMedix.exe', dist_dir)
    
    # Copy additional files
    files_to_copy = [
        'data.sql',
        'README.md',
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
    
    # Copy directories
    dirs_to_copy = [
        'assets',
        'styles',
        'modules',
        'profile_photos',
        'pdf_reports',
        'billing_pdf',
    ]
    
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            shutil.copytree(dir_name, os.path.join(dist_dir, dir_name))
    
    print("Created complete distribution package")

def create_zip():
    """Create a zip file of the distribution"""
    if os.path.exists('dist/PetMedix'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f'PetMedix_{timestamp}'
        shutil.make_archive(zip_name, 'zip', 'dist', 'PetMedix')
        print(f"Created {zip_name}.zip")
    else:
        print("Error: dist/PetMedix directory not found")

if __name__ == '__main__':
    print("Starting build process...")
    clean_build_dirs()
    build_executable()
    create_distribution()
    create_zip()
    print("Build process completed!") 