import os
import shutil
import sys
from tools import *
def main():
    refresh_content()
    #generate_page("content/index.md", template_path, "public/index.html")
    
    template_path = "./template.html"
    directory = os.path.join(os.getcwd(), "content")
    dest_path = os.path.join(os.getcwd(), "docs")
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    generate_page_recursive(template_path, directory, dest_path, base_path)

    
def refresh_content():
    public_dir = os.path.join(os.getcwd(), "docs")
    if os.path.exists(public_dir):
        print("Removing existing public directory...")
        shutil.rmtree(public_dir)
    source = os.path.join(os.getcwd(), "static")
    shutil.copytree(source, public_dir)
main()