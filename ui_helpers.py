# Import standard libraries
import os
import re
import pandas as pd

# For coloring of text inside the menu interface
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'
GRAY = '\033[90m'

# For moving directories
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Program Header
def header(tfidf_df, final_metadata, word_counts_df):
    """
    Displays whether the TF-IDF and Word Counts DataFrames and the Final Metadata dictionaries are loaded. Intended for display on each screen to provide the user constant awareness of the program's operating status.

    Parameters:
    tfidf_df - a global df that is loaded once a TF-IDF analysis is performed. Default None.
    final_metadata - a dictionary that contains user-input data concerning each file. Default None.
    word_counts_df - a global df that is loaded once a Word Count analysis performed. Default None.
    """
    while True:
        # Program version
        print(CYAN + 'TextAnalysis v.70' + RESET)
        print('_'*55)
        
        # Word Counts DF Status
        if word_counts_df is None:
            print(YELLOW + 'DataFrame Status' + RESET)
            print(GRAY + 'Word Count Analysis: Empty')
        else :
            shape = str(word_counts_df.shape)
            print(YELLOW + 'DataFrame Status' + RESET) 
            print(GREEN + 'Word Count Analysis: ' + RESET + f'{shape} (columns, rows)')
        
        # TF-IDF DF Status
        if tfidf_df is None:
            print(GRAY + 'TF-IDF Analysis: Empty')
        
        else :
            shape = str(tfidf_df.shape)
            print(GREEN + 'TF-IDF Analysis: ' + RESET + f'{shape} (documents, words)')
        
        # Final Metadata Status
        if final_metadata is None:
            print(GRAY + 'Final Metadata DataFrame: Empty' + RESET)
            print('_'*55)
        else:
            length = str(len(final_metadata))
            print(GREEN + 'Final Metadata DataFrame length: ' + RESET + length)
            print('_'*55)
        
        return
    
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

# Lists Textfiles subdirectory contents and requests user selection
def list_select_textfile(menu_return):
    """
    Lists all text files in the Textfiles subdirectory and prompts user for selection. Pressing "Enter" will return a list of all files for the word_tally function to process.

    Parameters:
    menu_return - specify which menu function the UI should return user to if no input for file selection.

    Returns:
    files_to_process - a list for the word_tally function to use to process the selected file(s).

    Raises:
    IndexError - if file selection is out of index range.
    ValueError - if non-number is input by the user.
    """

    # User message
    print(YELLOW + '\nAvailable files in Texfiles directory:\n' + RESET)
    
    # Moves to Textfiles directory
    move_to_textfiles()

    # Displays index of 'Textfiles' directory and prompts user to select a number
    text_files = os.listdir()
    for index, filename in enumerate(text_files, start=1):
        if filename.endswith('.txt'):
            print(f'{index}) {filename}')
    print(YELLOW + '\nEnter number(s) of the file to analyze separated by commas or spaces (i.e., 1, 2, 4) or type "all" to process all files listed.')
    user_selection = input(RESET + '\nEnter your selection: ')

    # Returns user to Quicklook menu if only "Enter" is pressed
    if user_selection == '':
        menu_return()

    # Manages user selection to process all files
    if user_selection.lower() == 'all':
        files_to_process = text_files
        return files_to_process

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            user_selected_files = [int(num) for num in re.split(r'[,\s]+', user_selection) if num.strip().isdigit()]
            files_to_process = [text_files[i - 1] for i in user_selected_files if 0 <= len(text_files)]
            return files_to_process
        
        except IndexError:
            print(RED + 'One or more file numbers are invalid.' + RESET)
            return
        
        except ValueError:
            print(RED + 'Invalid input. Please enter numbers only.' + RESET)
            return
        
# Lists Databases contents and requests user selection
def list_select_database(menu_return):
    """
    Lists the contents of Databases if the file ends with .sqlite. Prompts user to select a database, returning to previous menu if they press only "Enter".

    Parameters:
    menu_return - the menu function to call if no database is selected by the user.

    Returns:
    database_name - the name of the selected database, to be used by other functions as needed.

    Raises:
    IndexError - if the number entered by user is out of index range.
    ValueError - if the user enters a non-number.
    """

    # Moves to Database directory
    move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    
    while True:    
        try:
            user_selection = input(YELLOW + '\nSelect database using its index number: ' + RESET)

        # Returns user to desired menu (normally "one up" from current) if "Enter" is pressed
            if user_selection == '':
                menu_return()

            # Manages user selection based on single or multiple-file entry
            else:
                try:
                    selection_index = int(user_selection)
                    if selection_index < 0 or selection_index > len(database_files):
                        input(RED + 'Selection out of range. Please try again.' + RESET + ' Press Enter.')
                    database_name = database_files[selection_index - 1]
                    return database_name
                
                except ValueError:
                    print(RED + 'Invalid input. Please enter the index number only.' + RESET)
                
        except IndexError:
            print(RED + 'File number is out of range. Please check and try again.' + RESET)

# Input File Metadata
def input_file_metadata(filename):
    """
    Requests the user to input Title, Author, Genre, and Year for each file. Can be used in conjunction with SQL or TF-IDF functions to capture important data about documents for further analysis. If user does not input values, default values will be recorded to ensure compatability with all functions.

    Parameters:
    filename - the name of the file for which data is requested.

    Returns:
    doc_title - title of the file.
    author - of the file.
    year - of the publication.
    genre - of the publication.

    Raises:
    ValueError - if year is out of range or if input year is not a numerical value.
    """

    # Shows file name and requests title, author, genre inputs
    print(CYAN + '\nFILE INFORMATION: ' + RESET + f'{filename}')

    doc_title = input(YELLOW + 'Enter the title: ' + RESET)
    if doc_title == '':
        doc_title = filename

    author = input(YELLOW + 'Enter the author: ' + RESET)
    if author == '':
        author = 'Not Entered'

    genre = input(YELLOW + 'Enter the genre: ' + RESET)
    if genre == '':
        genre = 'Not Entered'
    
    # Prompt for year of publication
    while True:
        try:
            year = input(YELLOW + 'Enter the year of publication: ' + RESET)
            if year == '':
                break
            year = int(year)

            # Catches common year entry errors
            if year == 0:
                raise ValueError(RED + 'There is no 0 AD/CE! Please try again.')
            if year <= -3000 or year > 2075:
                raise ValueError(RED + 'Year must be between 3000 BC/BCE and 2075 AD/CE!' + RESET)
            break

        except ValueError:
            print(RED + 'Invalid input! Please try again.' + RESET)

    return doc_title, author, year, genre

# Moves to Reports subdirectory to access CSV ouput files
def move_to_reports():
    """
    Changes to 'Reports' subdirectory when needed to access CSV files.
    """
    # Moves to script directory and defines subdirectory
    os.chdir(script_dir)
    reports_path = os.path.join(script_dir, 'Reports')
    
    # Creates directory if it does not exist
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)
    
    # Moves to Reports subdirectory
    os.chdir(reports_path)

# Move to Reports\TF-IDF subdirectory
def move_to_reports_tfidf():
    """
    Moves to the Reports\TF-IDF subdirectory when needed to access or save CSV/TXT files.
    """
    # Moves to script directory and defines subdirectory
    os.chdir(script_dir)
    reports_path = os.path.join(script_dir, 'Reports\\TF-IDF')

    # Creates directory if it does not exist
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    # Moves to subdirectory
    os.chdir(reports_path)

# Move to Reports\Word Counts subdirectory
def move_to_reports_word_counts():
    r"""
    Moves to the Reports\Word Counts subdirectory when needed to access or save CSV/TXT files.
    """
    # Moves to script directory and defines subdirectory
    os.chdir(script_dir)
    reports_path = os.path.join(script_dir, 'Reports\\Word Counts')

    # Creates directory if it does not exist
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    # Moves to subdirectory
    os.chdir(reports_path)

# Move to Reports\Word Counts subdirectory
def move_to_reports_sql_queries():
    r"""
    Moves to the Reports\SQL Queries subdirectory when needed to access or save CSV/TXT files.
    """
    # Moves to script directory and defines subdirectory
    os.chdir(script_dir)
    reports_path = os.path.join(script_dir, 'Reports\\SQL Queries')

    # Creates directory if it does not exist
    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    # Moves to subdirectory
    os.chdir(reports_path)

# Move to Visuals subdirectory
def move_to_visuals():
    """
    Changes to the 'Visuals' subdirectory when needed to save bar charts or other pictures.
    """

    # Moves to script directory and defines Visuals subdirectory location
    os.chdir(script_dir)
    visuals_path = os.path.join(script_dir, 'Visuals')

    # Creates directory if it does not exist
    if not os.path.exists(visuals_path):
        os.makedirs(visuals_path)

    # Moves to Visuals subdirectory
    os.chdir(visuals_path)

# Lists Reports contents and requests user selection
def list_select_report(menu_return, report_subdir):
    """
    Lists the contents of Reports if the file ends with .csv. Prompts user to select a Report, returning to previous menu if they press only "Enter". Returns the name of the report for use by other functions

    Parameters:
    menu_return - the menu function to call if no database is selected by the user.

    Returns:
    report_name - the name of the selected database, to be used by other functions as needed.

    Raises:
    ValueError - if the user enters a non-number.
    """

    # Moves to appropriate subdirectory
    if report_subdir == 'wordcounts':
        move_to_reports_word_counts()
    elif report_subdir == 'sqlqueries':
        move_to_reports_sql_queries()
    elif report_subdir == 'tfidf':
        move_to_reports_tfidf()
    else:
        move_to_reports()

    # Displays contents of Reports subdirectory
    reports_files = os.listdir()
    
    # Lists .csv files located in Reports subdirectory
    for index, filename in enumerate(reports_files, start=1):
        if filename.endswith('.csv') or filename.endswith('.txt'):
            print(f'{index}) {filename}')

    # User selection prompt        
    user_selection = input(YELLOW + '\nSelect report using its index number: ' + RESET)
    
    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        menu_return()

    # Manages user selection if not "Enter"
    else:
        try:
            selection_index = int(user_selection)
        
        except ValueError:
            input(RED + 'Invalid input. Please enter the index number only.' + RESET + ' Press Enter.')
            menu_return()

        if selection_index < 0 or selection_index > len(reports_files):
            input(RED + 'Selection out of range. Please try again.' + RESET + ' Press Enter.')
            clear_screen()
            menu_return()

        report_name = reports_files[selection_index - 1]
        return report_name            

# Reads a csv or txt report
def read_txt_or_csv(filename):
    """
    Reads a txt or csv file and loads as a DataFrame.

    Parameters:
    filename - the name of the file to be read.

    Returns:
    df - the DataFrame once loaded.

    Raises:
    ValueError - if file type is not supported.
    """
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filename, index_col=0)

        elif filename.endswith('txt'):
            df = pd.read_csv(filename, sep='\t', index_col=0)
        else:
            raise ValueError(RED + 'Error reading report. Please check file type or select a different file.' + RESET)
    
    except AttributeError:
        print(RED + 'File selection invalid. Please check selection and retry.' + RESET)
        
    return df

# Display of analysis confirmation sentence
def analysis_confirmation(user_file):
    """
    Provides confirmation to the user that analysis of specfied file name is about to begin. Insert before calling the analysis.tally_words function
    """
    clear_screen()
    print(YELLOW + f'\nBeginning analysis of ' + RESET + f'{user_file}' + YELLOW + ' now...\n')

# Get top_n (number of rows) to return in SQL query and DataFrame operations
def get_top_n():
    """
    Prompts top_n for SQL database queries and specific DataFrame operations.

    Returns:
    top_n - must be a number.

    Raises:
    ValueError - if input is not a number.
    """
    # Requests user parameters
    while True:
        try:
            # Number range end 
            top_n = input(YELLOW + 'Enter a number: ' + RESET)
            if top_n == '':
                top_n = 5
            top_n = int(top_n)

            return top_n
        
        except ValueError:
            print(RED + 'Value must be a number only.' + RESET)

# Get start/end year
def get_start_end_years():
    """
    Prompts user to input the start_year, end_year, for SQL database queries

    Returns:
    start_year - must be between -3000 and 2075.
    end_year - must be between -3000 and 2075.

    Raises:
    ValueError - if input is not a number.
    """
    # Requests user parameters
    while True:
        try:
            # Starting year prompt
            start_year = input(YELLOW + '\n\nEnter start year: ' + RESET)
            
            # Sets default start year if nothing entered, converts input to integer otherwise
            if start_year == '':
                start_year = -3000
            start_year = int(start_year)

            # Raises error if year entered is outside of range
            if start_year < -3000 or start_year > 2075:
                print(RED + 'Year must be between -3000 and 2075.' + RESET + ' Please try again.')
            
            # Ending year prompt
            end_year = input(YELLOW + 'Enter end year: ' + RESET)

            # Sets default start year if nothing entered, converts input to integer otherwise
            if end_year == '':
                end_year = 2075
            end_year = int(end_year)

            # Raises error if year entered is outside of range or is before the start_year
            if end_year < -3000 or end_year > 2075:
                print(RED + 'Year must be between -3000 and 2075.' + RESET + ' Please try again.')
            if end_year < start_year:
                print(RED + 'End year cannot be earlier than start year.' + RESET + ' Please try again.')

            return start_year, end_year
        
        except ValueError:
            print(RED + 'Value must be a number only.' + RESET)

# Make list of user-input words
def make_list_from_user_input():
    """
    Function allows users to input words separated by space or comma, then splits/strips the input to return a list of words.

    Parameters:
    user_input_words - the string entered by the user.

    Returns:
    word_list - the list of words ready for use by other functions (i.e., work_lookup_over_time)
    """

    while True:
        # User prompt
        user_input_words = input(YELLOW + 'Enter the word(s) to find, separated by spaces or commas: ' + RESET)

        # Prompts user again to enter at least one word if none entered
        if user_input_words == '':
            input(RED + 'Please input one or more words to continue: ' + RESET)
        
        # Strips user input and returns as a list of words
        word_list = [word.strip() for word in re.split(',|\s+', user_input_words) if word.strip()]
        return word_list

# Saves a DataFrame as .csv file
def save_df_as_csv(df, default_name):
    """
    Prompts user to save the SQL Query Report, and if 'y' is entered, will save it as a .csv in the Reports subdirectory.

    Parameters:
    df - the Pandas DataFrame containing the query data.
    default_name - the name of the file if the user presses Enter without typing a name.
    """
    # CSV File Read Limitation Notice
    clear_screen()
    print(YELLOW + '\nNotice! Programs have different row and column limits. As of May 2024, the limitations of some of the most popular programs are:\n')
    print(RESET + 'Microsoft Excel: 1,048,576 rows, 16,384 columns')
    print(RESET + 'LibreOffice Calc: 1,048,576 rows, 1,024 columns')
    print(RESET + 'Google Sheets: 10 million total cells per sheet\n')
    print(YELLOW + 'Consider transforming the DataFrame first before writing to a .csv if you are concerned about truncation.\n')
    
    # User specifies name and .csv is added if necessary
    filename = input(YELLOW + 'Enter name for .csv report: ' + RESET)
    
    if len(filename) < 1:
        filename = default_name
        print(YELLOW + 'No name entered! Report will be saved as ' + 
              RESET + f'{filename}')
    
    # Adds .csv extension if needed
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    # Saves DF to the current directory
    df.to_csv(f'{filename}', index=True)
    print(RESET + filename + YELLOW + ' has been saved.' + RESET)
    
    return

# Saves a DataFrame as a .txt file (tab-delimited)
def save_df_as_txt(df, default_name):
    r"""
    Prompts user to save the DataFrame, and if 'y' is entered, will save it as a tab-delimited .txt file in the Reports subdirectory.

    Parameters:
    df - the Pandas DataFrame containing the query data.
    default_name - the name of the file if the user presses Enter without typing a name.
    """
    # File Read Limitation Notice
    print(YELLOW + '\nNotice! Programs have different row and column limits. As of May 2024, the limitations of some of the most popular programs are:\n')
    print(RESET + 'Microsoft Excel: 1,048,576 rows, 16,384 columns')
    print(RESET + 'LibreOffice Calc: 1,048,576 rows, 1,024 columns')
    print(RESET + 'Google Sheets: 10 million total cells per sheet\n')
    print(YELLOW + 'Consider transforming the DataFrame first before writing to a .csv if you are concerned about truncation.\n')
    
    # User specifies name and .csv is added if necessary
    filename = input(YELLOW + 'Enter name for the .txt file: ' + RESET)
    
    if len(filename) < 1:
        filename = default_name
        print(YELLOW + 'No name entered! Report will be saved as ' + 
              RESET + f'{filename}' + YELLOW + '.' + RESET)
    
    # Adds .csv extension if needed
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    # Saves DF to the current directory
    df.to_csv(f'{filename}', sep='\t', index=True, header=True)

    # Export confirmation and user prompt to return to SQL Queries menu
    print(RESET + f'\n{filename} ' + 
          YELLOW + 'saved to Reports subdirectory!')
    return
    

