import os
import shutil
import sys

def copy_folders():
    # Get the distribution directory
    dist_dir = os.path.join(os.getcwd(), 'dist', 'PetMedix')
    
    # Create necessary directories if they don't exist
    os.makedirs(os.path.join(dist_dir, 'profile_photos'), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, 'billing_pdf'), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, 'pdf_reports'), exist_ok=True)
    os.makedirs(os.path.join(dist_dir, 'styles'), exist_ok=True)
    
    # Copy data.sql to dist folder
    if os.path.exists('data.sql'):
        shutil.copy2('data.sql', dist_dir)
    
    # Copy styles folder
    if os.path.exists('styles'):
        for item in os.listdir('styles'):
            s = os.path.join('styles', item)
            d = os.path.join(dist_dir, 'styles', item)
            if os.path.isfile(s):
                shutil.copy2(s, d)
    
    # Copy modules directory
    modules_src = 'modules'
    modules_dst = os.path.join(dist_dir, 'modules')
    if os.path.exists(modules_src):
        if os.path.exists(modules_dst):
            shutil.rmtree(modules_dst)
        shutil.copytree(modules_src, modules_dst)
    
    # Copy assets directory
    assets_src = 'assets'
    assets_dst = os.path.join(dist_dir, 'assets')
    if os.path.exists(assets_src):
        if os.path.exists(assets_dst):
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst)
    
    print("Folders and files copied successfully!")

if __name__ == "__main__":
    copy_folders() 