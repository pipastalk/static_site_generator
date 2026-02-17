import os
import shutil
def main():
    refresh_content()
    
def refresh_content():
    public_dir = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_dir):
        print("Removing existing public directory...")
        shutil.rmtree(public_dir)
    source = os.path.join(os.getcwd(), "static")
    shutil.copytree(source, public_dir)
main()