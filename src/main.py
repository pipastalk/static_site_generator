import os
import shutil
from markup_tools import *
def main():
    refresh_content()
    #MarkUpTools.generate_page("content/index.md", template_path, "public/index.html")
    
    template_path = "./template.html"
    directory = os.path.join(os.getcwd(), "content")
    dest_path = os.path.join(os.getcwd(), "public")
    MarkUpTools.generate_page_recursive(template_path, directory, dest_path)

    
def refresh_content():
    public_dir = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_dir):
        print("Removing existing public directory...")
        shutil.rmtree(public_dir)
    source = os.path.join(os.getcwd(), "static")
    shutil.copytree(source, public_dir)
main()