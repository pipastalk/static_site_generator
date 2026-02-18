import os
import sys
import shutil
from markup_tools import *
def main():
    # Check if a base path argument is provided, otherwise default to "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    refresh_content("docs")
    template_path = "./template.html"
    directory = os.path.join(os.getcwd(), "content")
    dest_path = os.path.join(os.getcwd(), "docs")
    MarkUpTools.generate_pages_recursive(directory, template_path, dest_path, base_path)
    
def refresh_content(directory):
    public_dir = os.path.join(os.getcwd(), directory)
    if os.path.exists(public_dir):
        print("Removing existing public directory...")
        shutil.rmtree(public_dir)
    source = os.path.join(os.getcwd(), "static")
    shutil.copytree(source, public_dir)
main()