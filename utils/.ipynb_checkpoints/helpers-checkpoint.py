import os
from pathlib import Path
import pandas as pd
import shutil

def get_overview(start_dir='.'):
    def find_environment_yml(start_dir):
        current_dir = Path(start_dir).resolve()
        
        while current_dir != current_dir.root:
            env_yml_path = current_dir / 'environment.yml'
            if env_yml_path.is_file():
                return env_yml_path
            
            current_dir = current_dir.parent

        return None

    def print_directory_overview(start_dir):
        overview_str = ""
        start_dir_abs = Path(start_dir).resolve()
        
        for root, dirs, files in os.walk(start_dir_abs):
            # Filter out hidden files and directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
            
            # Sort directories and files
            dirs.sort()
            files.sort()

            root_path = Path(root).resolve()
            relative_root = root_path.relative_to(start_dir_abs) if root_path != start_dir_abs else Path('.')
            level = len(relative_root.parts)
            indent = ' ' * 4 * level
            overview_str += f"{indent}{relative_root}/\n" if relative_root != Path('.') else f"{relative_root}/\n"
            sub_indent = ' ' * 4 * (level + 1)
            for f in files:
                overview_str += f'{sub_indent}{f}\n'
        return overview_str

    # Get current working directory
    home_dir = Path.home()
    current_working_directory = Path(start_dir).resolve()
    relative_working_directory = current_working_directory.relative_to(home_dir).as_posix()

    # Find the environment.yml file
    env_yml_path = find_environment_yml(start_dir)

    if env_yml_path:
        parent_directory = env_yml_path.parent
        relative_parent_directory = parent_directory.relative_to(home_dir).as_posix()
        with open(env_yml_path, 'r') as file:
            env_yml_content = file.read()
        directory_overview = print_directory_overview(parent_directory)
    else:
        relative_parent_directory = "Not found"
        env_yml_content = "No environment.yml file found."
        directory_overview = print_directory_overview(current_working_directory)

    # Replace home directory with ~ in paths
    if relative_working_directory.startswith('~'):
        relative_working_directory = '~/' + relative_working_directory.split('/', 1)[-1]
    else:
        relative_working_directory = '~/' + relative_working_directory

    if relative_parent_directory.startswith('~'):
        relative_parent_directory = '~/' + relative_parent_directory.split('/', 1)[-1]
    else:
        relative_parent_directory = '~/' + relative_parent_directory

    # Format the output
    output = f"""
Current working directory is: {relative_working_directory}

Parent directory is: {relative_parent_directory}

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
    home_dir = str(Path.home())
    for folder, contents in matches:
        relative_folder = folder.relative_to(folder.parents[1]).as_posix().replace(home_dir, '~')
        print(f"{relative_folder}/")
        for item in contents:
            relative_item = item.relative_to(folder)
            indent_level = len(relative_item.parts)
            indent = ' ' * 4 * indent_level  # Indentation level
            relative_item_path = relative_item.as_posix().replace(home_dir, '~')
            print(f"{indent}{relative_item_path}/" if item.is_dir() else f"{indent}{relative_item_path}")

def switch_readme_files(repository_path):
    """
    Switches the README.md file in the given repository path with the markdown file located
    at 'utils/README.md' within the same repository.
    
    Parameters:
    - repository_path (str): The path to the repository containing the README.md file.
    
    Returns:
    None
    """
    readme_path = os.path.join(repository_path, "README.md")
    new_readme_path = os.path.join(repository_path, "utils", "README.md")
    temp_readme_path = os.path.join(repository_path, "utils", "TEMP_README.md")

    # Check if the new README.md file exists in the utils directory
    if not os.path.exists(new_readme_path):
        print(f"The file {new_readme_path} does not exist.")
        return

    # Temporarily move the new README.md to a temp file to avoid conflicts
    shutil.move(new_readme_path, temp_readme_path)
    
    # Move the original README.md to the utils directory
    shutil.move(readme_path, new_readme_path)
    
    # Move the temp README.md to the repository root
    shutil.move(temp_readme_path, readme_path)

    print("Learning insights now in README. You are ready to upload your cloned repo to GitHub!")

# Example usage:
# switch_readme_files('path/to/your/repository')



