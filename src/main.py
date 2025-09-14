import os, shutil
from markdowntohtmlnode import markdown_to_html_node, extract_title

def copy_static():
    public_path = os.path.abspath("./public")
    print("=== Removing Public contents ===")
    shutil.rmtree(public_path)
    os.mkdir(public_path)
    print("=== Copying files recursively ===")
    copy_files_recursively("./static", "./public")

def copy_files_recursively(source_path, destination_path):
    directory_contents = os.listdir(source_path)
    
    if not os.path.exists(destination_path):
        print(f'Creating directory {destination_path}')
        os.mkdir(destination_path)

    for content in directory_contents:
        content_path = os.path.join(source_path, content)
        target_path = os.path.join(destination_path, content)
        
        if os.path.isfile(content_path):
            print(f'Copying {content_path} to {destination_path}')
            shutil.copy(content_path, target_path)
        else:
            copy_files_recursively(content_path, target_path)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    try:
        with open(from_path, "r") as file:
            page_source = file.read()
    except Exception as e:
        return f'Error: {e}'
    
    try:
        with open(template_path, "r") as file:
            template_source = file.read()
    except Exception as e:
        return f'Error: {e}'
    
    page_content = markdown_to_html_node(page_source).to_html()
    title = extract_title(page_source)
    full_page = template_source.replace("{{ Title }}", title).replace("{{ Content }}", page_content)

    if not os.path.exists(os.path.dirname(dest_path)):
        try:
            os.makedirs(os.path.dirname(dest_path))
        except Exception as e:
            return f'Error: {e}'
    
    try: 
        with open(dest_path, "w") as file:
            file.write(full_page)
        return f'Successfully wrote to "{dest_path}" ({len(full_page)} characters written)'
    except Exception as e:
        return f'Error: {e}' 
    
# I hate recursive functions, why couldn't it be done by queue
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    directory_contents = os.listdir(dir_path_content)
    
    if not os.path.exists(dest_dir_path):
        print(f'Creating directory {dest_dir_path}')
        os.mkdir(dest_dir_path)
        
    # I feel like both copy and generate I should have treated as reference to function and pass to just crawl_recursive(function, ...) 
    for content in directory_contents:
        content_path = os.path.join(dir_path_content, content)
        target_path = os.path.join(dest_dir_path, content)

        if os.path.isfile(content_path):
            generate_page(content_path, template_path, target_path.removesuffix(".md") + ".html")
        else:
            generate_pages_recursive(content_path, template_path, target_path)



def main():
    copy_static()
    #generate_page("content/index.md", "template.html", "public/index.html")
    # Some higher power is trolling me here. Somehow it worked first try

    generate_pages_recursive("content", "template.html", "public")
    # And once again first try.


main()