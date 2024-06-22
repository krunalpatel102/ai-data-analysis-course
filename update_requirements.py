import os
import re
import nbformat
from nbformat import NotebookNode
import stdlib_list  # Package to list standard library modules by Python version

def extract_base_module(import_statement: str):
    """
    Extracts the base module/package name from an import statement.

    Args:
        import_statement (str): The full import statement (e.g., 'from os import path').

    Returns:
        str: The base package name (e.g., 'os').
    """
    parts = import_statement.split()
    if parts[0] == 'import':
        return parts[1].partition('.')[0]
    elif parts[0] == 'from':
        return parts[1].partition('.')[0]
    return None

def extract_imports_from_cell(cell: NotebookNode):
    """
    Extract import statements from a single Jupyter notebook cell, focusing only on the base package.

    Args:
        cell (NotebookNode): A single cell of a Jupyter notebook.

    Returns:
        set: A set of base import statements found in the cell.
    """
    import_statements = set()
    if cell.cell_type == 'code':
        # Use regex to find lines that start with 'import' or 'from'
        matches = re.findall(r"^\s*(?:import|from)\s+([\w\.]+)", cell.source, re.MULTILINE)
        for match in matches:
            base_module = extract_base_module(match)
            if base_module:
                import_statements.add(base_module)
    return import_statements

def extract_imports_from_notebook(notebook_path: str):
    """
    Extract base import statements from all code cells in a Jupyter notebook.
    
    Args:
        notebook_path (str): Path to a Jupyter notebook file.

    Returns:
        set: A set of all unique base modules imported in the notebook.
    """
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = nbformat.read(file, as_version=4)
    
    imports = set()
    for cell in notebook.cells:
        imports.update(extract_imports_from_cell(cell))
    
    return imports

def generate_requirements(directory: str):
    """
    Generate or update a requirements.txt file for a project directory containing Jupyter notebooks,
    excluding standard library packages and ensuring no duplicates with existing entries.

    Args:
        directory (str): The directory to search for Jupyter notebook files.
    """
    existing_imports = set()
    std_libs = set(stdlib_list.stdlib_list())  # Get list of standard library modules for current Python version

    # Read the existing requirements.txt, if it exists
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as req_file:
            existing_imports = {line.strip() for line in req_file if line.strip() and not line.strip().startswith('#')}

    # Scan notebooks for additional imports
    new_imports = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                path = os.path.join(root, file)
                notebook_imports = extract_imports_from_notebook(path)
                # Filter out standard library modules
                filtered_imports = {imp for imp in notebook_imports if imp not in std_libs}
                new_imports.update(filtered_imports)

    # Combine old and new imports, excluding any that are standard library
    combined_imports = existing_imports.union(new_imports)

    # Write combined requirements back to the file
    with open('requirements.txt', 'w') as f:
        for item in sorted(combined_imports):
            f.write(f"{item}\n")

if __name__ == '__main__':
    # Use the current working directory as the project directory
    project_directory = os.getcwd()
    generate_requirements(project_directory)
