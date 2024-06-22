import os
import re
import nbformat

def extract_imports_from_code(code):
    imports = set()
    matches = re.findall(r'^\s*(?:import|from)\s+(\S+)', code, re.MULTILINE)
    imports.update(matches)
    return imports

def extract_imports_from_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = nbformat.read(file, as_version=4)
    
    imports = set()
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            imports.update(extract_imports_from_code(cell.source))
    
    return imports

def update_requirements_file(directory):
    all_imports = set()
    
    # Extract existing requirements
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as req_file:
            for line in req_file:
                all_imports.add(line.strip())
    
    # Scan notebooks for additional imports
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):
                notebook_path = os.path.join(root, file)
                imports = extract_imports_from_notebook(notebook_path)
                all_imports.update(imports)
    
    # Write combined requirements back to the file
    with open('requirements.txt', 'w') as req_file:
        for imp in sorted(all_imports):
            req_file.write(f"{imp}\n")

if __name__ == '__main__':
    project_directory = os.getcwd()  # Use the current working directory
    update_requirements_file(project_directory)
