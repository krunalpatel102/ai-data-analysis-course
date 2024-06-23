import ipywidgets as widgets
from IPython.display import display
from pathlib import Path

# Function to create and display the widget
def create_reflection_widget(variable_name, description, placeholder):
    # Create text area for user input
    reflection_input = widgets.Textarea(
        value='',
        placeholder=placeholder,
        description=description,
        layout=widgets.Layout(width='100%', height='100px')
    )

    # Create a button for saving reflections
    save_button = widgets.Button(
        description='Save Reflections',
        button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click to save your reflections',
        icon='check'
    )

    # Create a label to display confirmation
    confirmation_label = widgets.Label()

    # Define the path to the Reflections folder relative to the notebook's location
    reflections_folder_path = Path('..') / 'Reflections'

    # Function to save input to a text file when button is clicked
    def save_reflections(b):
        try:
            # Create the Reflections folder if it doesn't exist
            reflections_folder_path.mkdir(parents=True, exist_ok=True)
            
            # Define the path to the file where reflections will be saved
            reflections_file_path = reflections_folder_path / f'{variable_name}.txt'
            
            # Prepare the content to be saved
            new_content = f"{description}\n{reflection_input.value}\n\n"
            
            # Write the content to the file
            reflections_file_path.write_text(new_content)

            confirmation_label.value = f"Your reflections have been saved as {variable_name}.txt."
        except Exception as e:
            confirmation_label.value = f"An error occurred: {e}"

    # Register the function to be called when the button is clicked
    save_button.on_click(save_reflections)

    # Display the text area, button, and confirmation label
    display(reflection_input)
    display(save_button)
    display(confirmation_label)
