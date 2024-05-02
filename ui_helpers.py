import os

# For coloring of text inside the menu interface
RED = '\033[31m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

# For moving directories
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

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
    os.chdir(script_dir)

    # DELETE AFTER SUCCESSFUL TESTING:
    # current_dir = str(os.getcwd())
    # parent_dir = os.path.dirname(current_dir)
    # if current_dir[-9:] == 'Textfiles':
    #     os.chdir(parent_dir)
    # elif current_dir[-9:] == 'Databases':
    #     os.chdir(parent_dir)

# Moves to Textfiles subdirectory to access local .txt files
def move_to_textfiles():
    """
    Changes to 'Textfiles' directory when needed to load local .txt files. Used during load_textfile function.
    """
    # Moves to script directory and defines Textfiles subdirectory location
    os.chdir(script_dir)
    textfiles_path = os.path.join(script_dir, 'Textfiles')

    # Creates directory if it does not exist
    if not os.path.exists(textfiles_path):
        os.makedirs(textfiles_path)

    # Moves to Textfiles
    os.chdir(textfiles_path)

# Moves to Databases subdirectory to access SQL files
def move_to_databases():
    """
    Changes to 'Databases' directory when needed to access SQL databases.
    """
    # Moves to script directory and defines Databases subdirectory location
    os.chdir(script_dir)
    databases_path = os.path.join(script_dir, 'Databases')
    
    # Creates directory if it does not exist
    if not os.path.exists(databases_path):
        os.makedirs(databases_path)
    
    # Moves to Databases
    os.chdir(databases_path)

# Moves to Reports subdirectory to access CSV ouput files
def move_to_reports():
    """
    Changes to 'Reports' subdirectory when needed to access CSV files.
    """
    # Moves to script directory and defines Databases subdirectory location
    os.chdir(script_dir)
    reports_path = os.path.join(script_dir, 'Reports')
    
    # Creates directory if it does not exist
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)
    
    # Moves to Databases
    os.chdir(reports_path)

# Display of analysis confirmation sentence
def analysis_confirmation(user_file):
    """
    Provides confirmation to the user that analysis of specfied file name is about to begin. Insert before calling the analysis.tally_words function
    """
    clear_screen()
    print(YELLOW + f'\nBeginning analysis of ' + RESET + f'{user_file}' + YELLOW + ' now...\n')

