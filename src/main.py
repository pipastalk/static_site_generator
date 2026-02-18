import os
import shutil
from markup_tools import *
def main():
    refresh_content()
    #MarkUpTools.generate_page("content/index.md", template_path, "public/index.html")
    
    template_path = "./template.html"
    directory = os.path.join(os.getcwd(), "content")
    dest_path = os.path.join(os.getcwd(), "public")
    for path, subdirs, files in os.walk(directory):
        rel_path = os.path.relpath(path, directory)
        dest_dir = os.path.join(dest_path, rel_path) if rel_path != '.' else dest_path
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for name in files:
            if name.endswith('.md'):
                src_file = os.path.join(path, name)
                # Output file: same relative path, .html extension
                base_name = os.path.splitext(name)[0] + '.html'
                dest_file = os.path.join(dest_dir, base_name)
                MarkUpTools.generate_page(src_file, template_path, dest_file)

    
def refresh_content():
    public_dir = os.path.join(os.getcwd(), "public")
    if os.path.exists(public_dir):
        print("Removing existing public directory...")
        shutil.rmtree(public_dir)
    source = os.path.join(os.getcwd(), "static")
    shutil.copytree(source, public_dir)
main()