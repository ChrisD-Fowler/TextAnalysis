import os

# For coloring of text inside the menu interface
RED = '\033[31m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

# Clear screen function
def clear_screen():
    """
    Provides a quick function to clear the screen. Essential for the user experience as
    the menus are traversed.
    """

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Changes to parent (script) directory
def move_to_parent():
    """
    Changes to parent directory when needed. Included to prevent errors after word_tally functions or future functions/code restructures from introducing problems.
    """
    current_dir = str(os.getcwd())
    parent_dir = os.path.dirname(current_dir)
    if current_dir[-9:] == 'Textfiles':
        os.chdir(parent_dir)

# Moves to Textfiles directory to access local .txt files
def move_to_textfiles():
    """
    Changes to 'Textfiles' directory when needed to load local .txt files. Used during load_textfile function.
    """
    current_dir = str(os.getcwd())
    if current_dir[-9:] != 'Textfiles':
        os.chdir('Textfiles')
    
# Display of analysis confirmation sentence
def analysis_confirmation(user_file):
    """
    Provides confirmation to the user that analysis of specfied file name is about to begin. Insert before calling the analysis.tally_words function
    """
    clear_screen()
    print(YELLOW + f'\nBeginning analysis of ' + RESET + f'{user_file}' + YELLOW + ' now...\n')