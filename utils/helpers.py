import os
from pathlib import Path

def get_overview(start_dir='.'):
    def find_environment_yml(start_dir):
        current_dir = os.path.abspath(start_dir)
        
        while True:
            env_yml_path = os.path.join(current_dir, 'environment.yml')
            if os.path.isfile(env_yml_path):
                return env_yml_path
            
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                # Reached the root directory
                return None
            current_dir = parent_dir

    def print_directory_overview(start_dir):
        overview_str = ""
        for root, dirs, files in os.walk(start_dir):
            # Filter out hidden files and directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            # Sort directories and files
            dirs.sort()
            files.sort()
            
            level = root.replace(start_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            overview_str += f'{indent}{os.path.basename(root)}/\n'
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                overview_str += f'{sub_indent}{f}\n'
        return overview_str

    # Get current working directory
    current_working_directory = os.getcwd()

    # Find the environment.yml file
    env_yml_path = find_environment_yml(start_dir)

    if env_yml_path:
        parent_directory = os.path.dirname(env_yml_path)
        with open(env_yml_path, 'r') as file:
            env_yml_content = file.read()
        directory_overview = print_directory_overview(parent_directory)
    else:
        parent_directory = "Not found"
        env_yml_content = "No environment.yml file found."
        directory_overview = print_directory_overview(current_working_directory)

    # Format the output
    output = f"""
Current working directory is: {current_working_directory}

Parent directory is: {parent_directory}

Full directory overview: 
{directory_overview}

Environment is:
{env_yml_content}
"""
    return output, parent_directory

def search_datasets(parent_directory: Path, search_string: str):
    """Search for dataset folders and their contents based on a string variable."""
    datasets_path = parent_directory / "Datasets"
    if not datasets_path.exists():
        raise FileNotFoundError(f"Datasets directory not found in {parent_directory}")

    matches = []
    for root, dirs, files in os.walk(datasets_path):
        # Filter out hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for d in dirs:
            if search_string.lower() in d.lower():
                folder_path = Path(root) / d
                # Filter out hidden files
                folder_contents = [item for item in folder_path.glob('**/*') if not any(part.startswith('.') for part in item.parts)]
                matches.append((folder_path, folder_contents))
    
    return matches

def print_search_results(matches):
    """Print the search results in a pretty format."""
    for folder, contents in matches:
        relative_folder = folder.relative_to(folder.parents[1])
        print(f"{relative_folder}/")
        for item in contents:
            relative_item = item.relative_to(folder)
            indent_level = len(relative_item.parts)
            indent = ' ' * 4 * indent_level  # Indentation level
            print(f"{indent}{relative_item}/" if item.is_dir() else f"{indent}{relative_item}")
