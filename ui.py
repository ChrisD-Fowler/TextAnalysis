# Import standard libraries
import os
import re
import pandas as pd

# Import local program scripts
import analysis
import ui_helpers
import sql_manager

# Main Menu interface
def main_menu():

    """
    Displays the top-menu function options for the user and prompts the user for a selection.
    Depending on input, different top-level functions are called.
    """
    ui_helpers.clear_screen()

    while True:
        print(ui_helpers.CYAN + 'TextCrawl v.40 Main Menu\n' + ui_helpers.RESET)
        print('1. Quicklook Word Counts')
        print('2. SQL Functions and Queries')
        print('..')
        print('6. Manage Databases')
        print('7. View/Manage Reports')
        print('8. Filter Settings (view or edit commonwords.txt)')
        print('9. Help/Readme\n')
        print(ui_helpers.YELLOW + 'Q to quit/exit.\n' + ui_helpers.RESET)

        choice = input('Enter your selection: ')

        if choice == '1':
            option_1()
        elif choice == '2':
            option_2()
        elif choice == '6':
            option_6()
        elif choice == '7':
            option_7()
        elif choice == '8':
            option_8()
        elif choice == '9':
            option_9()
        elif choice.lower() == 'q':
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 'Thanks for using TextCrawl! Exiting now...' + ui_helpers.RESET)
            quit()
        else:
            ui_helpers.clear_screen()
            print(ui_helpers.RED + 'Invalid menu choice! Please try again.' + ui_helpers.RESET)

# Option 1 - Text Analysis Menu
def option_1():
    """
    Allows users to select Quicklook Word Counts using either local file or URL.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Quicklook Display of Word Counts in Text File\n' + ui_helpers.RESET + '''
1. One or more .txt files located in Textfiles subdirectory
2. Single file using direct URL'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_1_1()
        elif choice == '2':
            option_1_2()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 1_1 - Local Text File Word Count
def option_1_1():
    """
    Prompt the user to input a text file name for word frequency analysis. Depending on the user input,
    the function either processes the file to display the frequency of the most common words or returns 
    to the main menu if the user decides to cancel the operation.

    The function calls `load_textfile` to load the text file, `load_common_words` to load a list
    of common words for filtering, and `tally_words` to perform the analysis. If the user does not specify
    a number of words, all words are processed; otherwise, only the top N words as specified by the user
    are processed. The function handles errors related to file not found, invalid numeric input, and
    other unexpected errors.

    Raises:
    Exception: Catches and logs any other unexpected exceptions that may occur during execution.
    """       
    
    # Page title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Local Text File Word Count' + ui_helpers.RESET)
    
    # Page instructions
    print('\nSpecify a .txt file for word frequency analysis and will return the desired number of words. This tool filters any words specified in commonwords.txt, which is editable from the ' + ui_helpers.CYAN + 'Settings ' + ui_helpers.RESET + 'menu from the ' + ui_helpers.CYAN + 'Main Menu' + ui_helpers.RESET + '.')
    
    print('\nThis function is compatible with .txt files in UTF-8 format and the file(s) you wish to analyze must be placed in a directory named "Textfiles" located as a subdirectory in the main script\'s parent folder.')

    print(ui_helpers.YELLOW + '\nAvailable files in Texfiles directory:\n' + ui_helpers.RESET)
    
    # Moves to Textfiles directory
    ui_helpers.move_to_textfiles()

    # Displays index of 'Textfiles' directory and prompts user to select a number
    text_files = os.listdir()
    for index, filename in enumerate(text_files, start=1):
        if filename.endswith('.txt'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nEnter number(s) of the file to analyze separated by commas or spaces (i.e., 1, 2, 4): ' + ui_helpers.RESET)

    # Returns user to Quicklook menu if only "Enter" is pressed
    if user_selection == '':
        option_1()

    # Manages user selection to process all files
    if user_selection.lower() == 'all':
        files_to_process = text_files

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            user_selected_files = [int(num) for num in re.split(r'[,\s]+', user_selection) if num.strip().isdigit()]
            files_to_process = [text_files[i - 1] for i in user_selected_files if 0 <= len(text_files)]
        
        except IndexError:
            print(ui_helpers.RED + 'One or more file numbers are invalid.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter numbers only.' + ui_helpers.RESET)
            return

    # Requests user input for number of words to display
    while True:
        number_to_list = input(ui_helpers.YELLOW + 'Enter number of words to display ' + ui_helpers.RESET + ' (Press Enter to return all words): ')

        if number_to_list.strip() == '':
            number_to_list == None
            break
        try:
            number_to_list = int(number_to_list)
            break

        except ValueError:
            print(ui_helpers.RESET + f'\nInvalid input! Please try again.\n')

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Loads the user .txt files and displays confirmation
    for filename in files_to_process:
        text_file_data = analysis.load_textfile(filename)
        wordtally_results = analysis.tally_words(text_file_data, common_words)
        print(ui_helpers.CYAN + '\n\nFILE: ' + ui_helpers.RESET + f'{filename}')
        analysis.display_word_frequency(wordtally_results, number_to_list)

    # Prompts user to return to main menu once the word count has been displayed
    input('\nPress Enter to return to the ' + ui_helpers.CYAN + 'Analysis '  + ui_helpers.RESET + 'menu.')
    ui_helpers.clear_screen()
    option_1()

# Option 1_2 - Text File Word Count with URL
def option_1_2():
    """
    Allows user to input URL for a .txt file for word tallying. It then calls the appropriate analysis functions to complete the scan and display the results.

    Raises:
    ValueError if user inputs a non-integer
    """
    
    # Clears screen and provides title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Text File Word Count via the Web\n' + ui_helpers.RESET)
    print('Enter or paste a URL link to a .txt file for word frequency analysis. This tool filters any words specified in commonwords.txt, which is editable from the ' + ui_helpers.CYAN + 'Settings ' + ui_helpers.RESET + 'menu from the ' + ui_helpers.CYAN + 'Main Menu' + ui_helpers.RESET + '.')
    print('\nThis function is compatible with .txt files in UTF-8 format.\n')
    
    # Prompts user for the URL
    user_url = input(ui_helpers.YELLOW + 'Please enter or paste the complete URL here ' + ui_helpers.RESET + '(Press Enter to return to ' + ui_helpers.CYAN + 'Analysis ' + ui_helpers.RESET + 'menu): ')

    # Returns to Analysis menu and checks for "http" prefix
    user_url_check = str(user_url).lower()
    if len(user_url_check) < 1:
        option_1()
    elif user_url_check[0:4] != 'http':
        print(ui_helpers.RED + 'Invalid URL! Please check and try again.' + ui_helpers.RESET)
        input('')
        option_1_2()

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Requests user input for number of words to display
    while True:
        number_to_list = input(ui_helpers.YELLOW + 'Enter number of words to display ' + ui_helpers.RESET + ' (Press Enter to return all words): ')

        if number_to_list.strip() == '':
            number_to_list == None
            break
        try:
            number_to_list = int(number_to_list)
            break

        except ValueError:
            print(ui_helpers.RESET + f'\nInvalid input! Please try again.\n')

    # Calls the analysis functions
    text_file_data = analysis.url_text_file_open(user_url)
    ui_helpers.analysis_confirmation(user_url)

    while True:
        # If user pressed only Enter, all words will be displayed, otherwise number_to_list will convert to integer
        if number_to_list == '':
            number_to_list == None
        else:
            try:
                number_to_list = int(number_to_list)
            except TypeError as e:
                print(ui_helpers.RESET + f'\nInvalid input! Please try again.\n')

        wordtally_results = analysis.tally_words(text_file_data, common_words)
        analysis.display_word_frequency(wordtally_results, number_to_list)
        break

    # Returns to Analysis menu
    input('\nPress Enter to return to the ' + ui_helpers.CYAN + 'Analysis '  + ui_helpers.RESET + 'menu.')
    ui_helpers.clear_screen()
    option_1()

# Option 2 - SQL Database Menu
def option_2():
    """
    Provides user selection menu for SQL functions.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'SQL Database Menu\n' + ui_helpers.RESET + '''
1. Export Word Counts to SQL Database
2. SQL Database Queries and Report Generation (.csv)'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_1()
        elif choice == '2':
            option_2_2()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 2_1 - Complete a word tally and export to SQL DB
def option_2_1():
    """
    Completes a word frequency analysis and exports results to a SQL database. Filters any words from commonwords.txt from the analysis. Users may choose a single file, multiple files, or all files located in the Textfiles directory.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """

    # Header and user instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Tally Words and Export to SQL Database' + ui_helpers.RESET)
    print('\nThis will tally all words in a .txt file, filtering any that are defined in the commonwords.txt file, and export to a user-defined SQL database.\n\nYou may make multiple selections by entering the numbers corresponding to the files listed below.\n\nEnter "all" to analyze all files listed.')

    print(ui_helpers.YELLOW + '\nAvailable files in Texfiles directory:\n' + ui_helpers.RESET)
    
    # Moves to Textfiles directory
    ui_helpers.move_to_textfiles()

    # Displays index of 'Textfiles' directory and prompts user to select a number
    text_files = os.listdir()
    for index, filename in enumerate(text_files, start=1):
        if filename.endswith('.txt'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nEnter number(s) of the file to analyze separated by commas or spaces (i.e., 1, 2, 4): ' + ui_helpers.RESET)

    # Returns user to SQL menu if only "Enter" is pressed
    if user_selection == '':
        option_2()

    # Manages user selection to process all files
    if user_selection.lower() == 'all':
        files_to_process = text_files
    
    # Manages user selection based on single or multiple-file entry
    else:
        try:
            user_selected_files = [int(num) for num in re.split(r'[,\s]+', user_selection) if num.strip().isdigit()]
            files_to_process = [text_files[i - 1] for i in user_selected_files if 0 <= len(text_files)]
        
        except IndexError:
            print(ui_helpers.RED + 'One or more file numbers are invalid.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter numbers only.' + ui_helpers.RESET)
            return

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Get SQL database information
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'SQL Database Information Entry' + ui_helpers.RESET)
    print(ui_helpers.RESET + '\nEnter the name of the SQL database to which you would like to export data. You may also enter metadata about the file, including title, author, and year (optional, but recommended!).\n\nNOTE: If entered, Year must be a non-zero integer between -3000 and 2075.\n')

    # User prompt for Database name
    print(ui_helpers.RESET + 'SQL DATABASE INFORMATION')
    database_name = input(ui_helpers.YELLOW + 'Enter the name of the SQL database: ' + ui_helpers.RESET)
    if not database_name.endswith('sqlite'):
        database_name += '.sqlite'

    # Loads, analyzes the .txt files
    for filename in files_to_process:
        text_file_data = analysis.load_textfile(filename)
        wordtally_results = analysis.tally_words(text_file_data, common_words)

        # User prompts for file metadata
        print(ui_helpers.RESET + f'\nFILE INFORMATION: {filename}')
        doc_title = input(ui_helpers.YELLOW + 'Enter the title: ' + ui_helpers.RESET)
        author = input(ui_helpers.YELLOW + 'Enter the author: ' + ui_helpers.RESET)
        
        # Prompt for year of publication
        while True:
            try:
                year = input(ui_helpers.YELLOW + 'Enter the year of publication: ' + ui_helpers.RESET)
                if year == '':
                    break
                year = int(year)

                # Catches common year entry errors
                if year == 0:
                    raise ValueError(ui_helpers.RED + 'There is no 0 AD/CE! Please try again.')
                if year <= -3000 or year > 2075:
                    raise ValueError(ui_helpers.RED + 'Year must be between 3000 BC/BCE and 2075 AD/CE!' + ui_helpers.RESET)
                break

            except ValueError:
                print(ui_helpers.RED + 'Invalid input! Please try again.' + ui_helpers.RESET)

        # Calls SQL functions
        sql_manager.database_build(database_name)
        sql_manager.wordtally_to_database(wordtally_results, database_name, doc_title, author, year)

        # Confirmation prompt
        print(ui_helpers.YELLOW + 'Added ' + 
              ui_helpers.RESET + f'{filename}' + 
              ui_helpers.YELLOW + ' to ' + 
              ui_helpers.RESET + f'{database_name}' + 
              ui_helpers.YELLOW + '.' + 
              ui_helpers.RESET)

    # User prompt to return or continue
    input(ui_helpers.YELLOW + '\nOperation complete! Press Enter to return to ' + ui_helpers.CYAN + 'SQL Database Menu'  + ui_helpers.RESET + '.')
    ui_helpers.clear_screen()
    option_2()

# Option 2_2 - Database Queries
def option_2_2():
    """
    Provides user options for SQL Database Queries.
    """

    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'SQL Database Queries\n' + ui_helpers.RESET + '''
1. Summarize Database(s)
2. Trends Over Time Queries'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_2_1()
        elif choice == '2':
            option_2_2_2()
        else:
            ui_helpers.clear_screen()
            option_2()

# Option 2_2_1 - Summarize SQL Database(s)
def option_2_2_1():
    """
    Provides summary information (metadata) for a user-selected SQL database or multiple databases.

    Raises:
    IndexError - if number entered is not on the databse index.
    ValueError - if non-numerical entry is detected.
    """
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Summarize SQL Database(s)' + ui_helpers.RESET)
    print('\nDisplay summary information for one or more existing databases.')

    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
    
    # Moves to Database directory
    ui_helpers.move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nEnter number(s) of the file to analyze separated by commas or spaces (i.e., 1, 2, 4): ' + ui_helpers.RESET)

    # Returns user to Database Queries menu if only "Enter" is pressed
    if user_selection == '':
        option_2_2()

    # Manages user selection to process all files
    if user_selection.lower() == 'all':
        files_to_process = database_files

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            user_selected_files = [int(num) for num in re.split(r'[,\s]+', user_selection) if num.strip().isdigit()]
            files_to_process = [database_files[i - 1] for i in user_selected_files if 0 <= len(database_files)]
        
        except IndexError:
            print(ui_helpers.RED + 'One or more file numbers are invalid.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter numbers only.' + ui_helpers.RESET)
            return

    for filename in files_to_process:
        sql_manager.summarize_database(filename)

    input(ui_helpers.YELLOW + '\nSummary complete! Press Enter to return to' + ui_helpers.CYAN + ' Database Queries ' + ui_helpers.YELLOW + 'menu.' + ui_helpers.RESET)

# Option 2_2_2 - Trends Over Time
def option_2_2_2():
    """
    Provides user options for time-based queries, such as word counts over time.
    """
    
    # Menu tree
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Trends Over Time\n' + ui_helpers.RESET + '''
Choose a report to run. Reports may be saved as .csv files to the Reports subdirectory.
              
1. Word Count Trends Over Time (All Authors)
2. Word Count Trends Over Time (By Author)
3. Publications Over Time (By Author)
4. Word(s) Frequency Lookup Over Time'''
+ ui_helpers.YELLOW + '\n\nPress Enter to return to' + ui_helpers.CYAN + ' Database Queries ' + ui_helpers.YELLOW + 'menu.' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')

        # Handles user selection
        if choice == '1':
            option_2_2_2_1()
        elif choice == '2':
            option_2_2_2_2()
        elif choice == '3':
            option_2_2_2_3()
        elif choice == '4':
            option_2_2_2_4()
        else:
            ui_helpers.clear_screen()
            option_2_2()

# Option 2_2_2_1 - Word Count Trends Over Time (All Authors)
def option_2_2_2_1():
    """
    Provides users the ability to specify a database and appropriate options for building a Word Count Over Time report using all authors in the database. Users may then save the report to a .csv file.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """

    # Screen title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (All Authors)' + ui_helpers.RESET)
    print('\nDisplay the most-used words in a database between desired years. Authors are not included as a column.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Moves to Database directory
    ui_helpers.move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect database using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_2_2_2()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index >= len(database_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            database_name = database_files[selection_index - 1]
        
        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return

    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (All Authors)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number to List = 25')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters
    try:
        # Starting year prompt
        start_year = input(ui_helpers.YELLOW + '\n\nEnter start year: ' + ui_helpers.RESET)
        if start_year == '':
            start_year = -3000
        start_year = int(start_year)
        if start_year < -3000 or start_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
        
        # Ending year prompt
        end_year = input(ui_helpers.YELLOW + 'Enter end year: ' + ui_helpers.RESET)
        if end_year == '':
            end_year = 2075
        end_year = int(end_year)
        if end_year < -3000 or end_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
    
        # Number range end 
        top_n = input(ui_helpers.YELLOW + 'Enter number of words to return: ' + ui_helpers.RESET)
        if top_n == '':
            top_n = 25
        top_n = int(top_n)
    
    except ValueError:
        print(ui_helpers.RED + 'Value must be a number only.' + ui_helpers.RESET)

    # Calls function to output SQL query to Pandas DF
    print(ui_helpers.RESET + '\nQuerying database now...' + ui_helpers.RESET)
    df = sql_manager.query_most_used_words(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':

        # User specifies name and .csv is added if necessary
        filename = input(ui_helpers.YELLOW + 'Enter name for .csv report: ' + ui_helpers.RESET)
        if len(filename) < 1:
            filename = f'{database_name}_counts_all_authors_over_time.csv'
            print(ui_helpers.YELLOW + 'No name entered! Report will be saved as ' + ui_helpers.RESET + f'{filename}' + ui_helpers.YELLOW + '.' + ui_helpers.RESET)
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Moves to Reports subdirectory and exports df as .csv there
        ui_helpers.move_to_reports()
        df.to_csv(f'{filename}', index=False)

        # Export confirmation and user prompt to return to SQL Queries menu
        print(ui_helpers.RESET + f'\n{filename}' + ui_helpers.YELLOW + ' successfully saved to ' + ui_helpers.RESET + 'Reports ' + ui_helpers.YELLOW + 'subdirectory!')
        input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'SQL Queries' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
        option_2_2_2()
    
    else:
        option_2_2_2()

# Option 2_2_2_2 - Word Count Trends Over Time (By Author)
def option_2_2_2_2():
    """
    Provides user interface to specify a database and appropriate options for building a Word Count Over Time report grouped by author. Users may then save the report to a .csv file.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """
    # Screen title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (By Author)' + ui_helpers.RESET)
    print('\nDisplay the most-used words in a database between desired years. Authors are included as a column.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Moves to Database directory
    ui_helpers.move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect database using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_2_2_2()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index >= len(database_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            database_name = database_files[selection_index - 1]
        
        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return

    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number to List = 25')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters
    try:
        # Starting year prompt
        start_year = input(ui_helpers.YELLOW + '\n\nEnter start year: ' + ui_helpers.RESET)
        if start_year == '':
            start_year = -3000
        start_year = int(start_year)
        if start_year < -3000 or start_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
        
        # Ending year prompt
        end_year = input(ui_helpers.YELLOW + 'Enter end year: ' + ui_helpers.RESET)
        if end_year == '':
            end_year = 2075
        end_year = int(end_year)
        if end_year < -3000 or end_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
    
        # Number range end 
        top_n = input(ui_helpers.YELLOW + 'Enter number of words to return: ' + ui_helpers.RESET)
        if top_n == '':
            top_n = 25
        top_n = int(top_n)
    
    except ValueError:
        print(ui_helpers.RED + 'Value must be a number only.' + ui_helpers.RESET)

    # Calls function to output SQL query to Pandas DF
    print(ui_helpers.RESET + '\nQuerying database now...' + ui_helpers.RESET)
    df = sql_manager.query_most_used_words_by_author(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':

        # User specifies name and .csv is added if necessary
        filename = input(ui_helpers.YELLOW + 'Enter name for .csv report: ' + ui_helpers.RESET)
        if len(filename) < 1:
            filename = f'{database_name}_counts_by_author_over_time.csv'
            print(ui_helpers.YELLOW + 'No name entered! Report will be saved as ' + ui_helpers.RESET + f'{filename}' + ui_helpers.YELLOW + '.' + ui_helpers.RESET)
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        # Moves to Reports subdirectory and exports df as .csv there
        ui_helpers.move_to_reports()
        df.to_csv(f'{filename}', index=False)

        # Export confirmation and user prompt to return to SQL Queries menu
        print(ui_helpers.RESET + f'\n{filename}' + ui_helpers.YELLOW + ' successfully saved to ' + ui_helpers.RESET + 'Reports ' + ui_helpers.YELLOW + 'subdirectory!')
        input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'SQL Queries' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
        option_2_2_2()
    
    else:
        option_2_2_2()

# Option 2_2_2_3 - Publications Over Time (By Author)
def option_2_2_2_3():
    """
    Provides user interface  to specify a database and appropriate options for building a Publications By Author Over Time report using all authors in the database. Users may then save the report to a .csv file.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """

    # Screen title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Publications Over Time (By Author)' + ui_helpers.RESET)
    print('\nDisplay the number of publications over time by each author in the database.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Moves to Database directory
    ui_helpers.move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect database using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_2_2_2()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index >= len(database_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            database_name = database_files[selection_index - 1]
        
        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return
        
    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Publications Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number of Authors = 10')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters
    try:
        # Starting year prompt
        start_year = input(ui_helpers.YELLOW + '\n\nEnter start year: ' + ui_helpers.RESET)
        if start_year == '':
            start_year = -3000
        start_year = int(start_year)
        if start_year < -3000 or start_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
        
        # Ending year prompt
        end_year = input(ui_helpers.YELLOW + 'Enter end year: ' + ui_helpers.RESET)
        if end_year == '':
            end_year = 2075
        end_year = int(end_year)
        if end_year < -3000 or end_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
    
        # Number range end 
        max_authors = input(ui_helpers.YELLOW + 'Enter number of authors to return: ' + ui_helpers.RESET)
        if max_authors == '':
            max_authors = 10
        max_authors = int(max_authors)
    
    except ValueError:
        print(ui_helpers.RED + 'Value must be a number only.' + ui_helpers.RESET)

    # Calls function to output SQL query to Pandas DF
    print(ui_helpers.RESET + '\nQuerying database now...' + ui_helpers.RESET)
    df = sql_manager.publications_over_time_by_author(database_name, start_year, end_year, max_authors)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':

        # User specifies name and .csv is added if necessary
        filename = input(ui_helpers.YELLOW + 'Enter name for .csv report: ' + ui_helpers.RESET)
        if len(filename) < 1:
            filename = f'{database_name}_publications_over_time.csv'
            print(ui_helpers.YELLOW + 'No name entered! Report will be saved as ' + ui_helpers.RESET + f'{filename}' + ui_helpers.YELLOW + '.' + ui_helpers.RESET)
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Moves to Reports subdirectory and exports df as .csv there
        ui_helpers.move_to_reports()
        df.to_csv(f'{filename}', index=False)

        # Export confirmation and user prompt to return to SQL Queries menu
        print(ui_helpers.RESET + f'\n{filename}' + ui_helpers.YELLOW + ' successfully saved to ' + ui_helpers.RESET + 'Reports ' + ui_helpers.YELLOW + 'subdirectory!')
        input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'SQL Queries' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
        option_2_2_2()
    
    else:
        option_2_2_2()

# Option 2_2_2_4 - Word(s) Lookup Over Time
def option_2_2_2_4():
    """
    Allows user to specify word(s) to look up in a database and appropriate options for building a Word Count Over Time report using only those words. Users may then save the report to a .csv file.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """
    # Screen title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word(s) Frequency Lookup Over Time' + ui_helpers.RESET)
    print('\nDisplay the frequency of user-defined word(s) in a database over time.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Moves to Database directory
    ui_helpers.move_to_databases()

    # Displays contents of Databases, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect database using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_2_2_2()

    # Manages user selection
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index >= len(database_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            database_name = database_files[selection_index - 1]
        
        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return
        
    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Publications Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters
    try:
        # Starting year prompt
        start_year = input(ui_helpers.YELLOW + '\n\nEnter start year: ' + ui_helpers.RESET)
        if start_year == '':
            start_year = -3000
        start_year = int(start_year)
        if start_year < -3000 or start_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
        
        # Ending year prompt
        end_year = input(ui_helpers.YELLOW + 'Enter end year: ' + ui_helpers.RESET)
        if end_year == '':
            end_year = 2075
        end_year = int(end_year)
        if end_year < -3000 or end_year > 2075:
            input(ui_helpers.RED + 'Year must be between -3000 and 2075.' + ui_helpers.RESET + ' Please try again.')
    
    except ValueError:
        print(ui_helpers.RED + 'Value must be a number only.' + ui_helpers.RESET)

    # User-defined words to search database
    while True:
        user_input_words = input(ui_helpers.YELLOW + 'Enter the word(s) to find' + ui_helpers.RESET + ' (multiple words allowed separated by commas or spaces)' + ui_helpers.YELLOW + ': ' + ui_helpers.RESET)
        if user_input_words == '':
            raise Exception(ui_helpers.RED + 'Please input one or more words to continue: ')
        word_list = [word.strip() for word in re.split(',|\s+', user_input_words) if word.strip()]
        break

    # Calls function to output SQL query to Pandas DF
    print(ui_helpers.RESET + '\nQuerying database now...' + ui_helpers.RESET)
    df = sql_manager.words_lookup_over_time(database_name, start_year, end_year, word_list)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':

        # User specifies name and .csv is added if necessary
        filename = input(ui_helpers.YELLOW + 'Enter name for .csv report: ' + ui_helpers.RESET)
        if len(filename) < 1:
            filename = f'{database_name}_word_lookup_over_time.csv'
            print(ui_helpers.YELLOW + 'No name entered! Report will be saved as ' + ui_helpers.RESET + f'{filename}' + ui_helpers.YELLOW + '.' + ui_helpers.RESET)
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Moves to Reports subdirectory and exports df as .csv there
        ui_helpers.move_to_reports()
        df.to_csv(f'{filename}', index=False)

        # Export confirmation and user prompt to return to SQL Queries menu
        print(ui_helpers.RESET + f'\n{filename}' + ui_helpers.YELLOW + ' successfully saved to ' + ui_helpers.RESET + 'Reports ' + ui_helpers.YELLOW + 'subdirectory!')
        input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'SQL Queries' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
        option_2_2_2()
    
    else:
        option_2_2_2()

# Option 6 - Database Management
def option_6():
    """
    Provides user options for managing Databases.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Manage Databases\n' + ui_helpers.RESET + '''
1. Delete Database(s)
2. ...'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_6_1()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 6_1 - Delete Database(s)
def option_6_1():
    """
    Provides a list of .sqlite files in Database subdirectory and allows users to specify the index number desired to delete database(s).

    Raises:
    IndexError - if user specifies an index number that is out of range.
    ValueError - if user specifies a non-number
    """
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Delete Database(s)' + ui_helpers.RESET)
    print('\nYou may select a database to Delete it.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)

    # Moves to Reports subdirectory
    ui_helpers.move_to_databases()

    # Displays contents of Reports, prompts user for selection
    database_files = os.listdir()
    for index, filename in enumerate(database_files, start=1):
        if filename.endswith('.sqlite'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect database using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_6()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index > len(database_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            database_name = database_files[selection_index - 1]
            
            # Confirmation prompt
            print(ui_helpers.RED + 'Really delete ' + ui_helpers.RESET + f'{database_name}' + ui_helpers.RED + '?' + ui_helpers.RESET)
            delete_confirmation = input('Enter "C" to cancel or press Enter to continue with deletion.')
            
            # Cancels deletion
            if delete_confirmation.lower() == 'c':
                input(ui_helpers.RESET + f'{database_name} ' + ui_helpers.YELLOW + 'NOT deleted!' + ui_helpers.RESET)
                option_6_1()
            
            # Deletes the database
            else:
                os.remove(database_name)
                input(ui_helpers.RESET + f'{database_name} ' + ui_helpers.YELLOW + 'deleted!' + ui_helpers.RESET)
                option_6_1()

        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return
    
    # User confirmation prompt and return
    input(ui_helpers.YELLOW + '\nDataFrame read complete.' + ui_helpers.RESET + ' Press Enter to continue.')
    option_6_1()

# Option 7 - Reports Menu
def option_7():
    """
    Provides user options for viewing Reports.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'View Reports\n' + ui_helpers.RESET + '''
1. View Report(s)
2. Delete Report(s)'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_7_1()
        elif choice == '2':
            option_7_2()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 7_1 - View Report(s)
def option_7_1():
    """
    Displays an index of .csv files in Reports subdirectory and displays user-selected file as a Pandas DataFrame.

    Raises:
    IndexError - if user specifies an index value out of range.
    ValueError - if user enters a non-number.
    """

    # Screen title and instructions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'View CSV Reports' + ui_helpers.RESET)
    print('\nYou may select a report to view its DataFrame in Pandas.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)

    # Moves to Reports subdirectory
    ui_helpers.move_to_reports()

    # Displays contents of Reports, prompts user for selection
    reports_files = os.listdir()
    for index, filename in enumerate(reports_files, start=1):
        if filename.endswith('.csv'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect report using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_7()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index > len(reports_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            report_name = reports_files[selection_index - 1]
            df = pd.read_csv(report_name)
            print(df.head())
        
        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return
        
    # User confirmation prompt and return
    input(ui_helpers.YELLOW + '\nDataFrame read complete.' + ui_helpers.RESET + ' Press Enter to continue.')
    option_7_1()

# Option 7_2 - Delete Report(s)
def option_7_2():
    """
    Displays .csv files located in the Reports subdirectory and allows users to input an index number corresponding to reports for deletion.

    Raises:
    IndexError - if user specifies an index value out of range.
    ValueError - if user enters a non-number.
    """
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Delete CSV Reports' + ui_helpers.RESET)
    print('\nYou may select a report to Delete it.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)

    # Moves to Reports subdirectory
    ui_helpers.move_to_reports()

    # Displays contents of Reports, prompts user for selection
    reports_files = os.listdir()
    for index, filename in enumerate(reports_files, start=1):
        if filename.endswith('.csv'):
            print(f'{index}) {filename}')
    user_selection = input(ui_helpers.YELLOW + '\nSelect report using its index number: ' + ui_helpers.RESET)

    # Returns user to Trends Over Time menu if only "Enter" is pressed
    if user_selection == '':
        option_7()

    # Manages user selection based on single or multiple-file entry
    else:
        try:
            selection_index = int(user_selection)
            if selection_index < 0 or selection_index > len(reports_files):
                input(ui_helpers.RED + 'Selection out of range. Please try again.' + ui_helpers.RESET + ' Press Enter.')
            report_name = reports_files[selection_index - 1]
            print(ui_helpers.RED + 'Really delete ' + ui_helpers.RESET + f'{report_name}' + ui_helpers.RED + '?' + ui_helpers.RESET)
            delete_confirmation = input('Enter "C" to cancel or press Enter to continue with deletion.')
            if delete_confirmation.lower() == 'c':
                input(ui_helpers.RESET + f'{report_name} ' + ui_helpers.YELLOW + 'NOT deleted!' + ui_helpers.RESET)
                option_7_2()
            else:
                os.remove(report_name)
                input(ui_helpers.RESET + f'{report_name} ' + ui_helpers.YELLOW + 'deleted!' + ui_helpers.RESET)
                option_7_2()

        except IndexError:
            print(ui_helpers.RED + 'File number is out of range. Please check and try again.' + ui_helpers.RESET)
            return
        
        except ValueError:
            print(ui_helpers.RED + 'Invalid input. Please enter the index number only.' + ui_helpers.RESET)
            return
    
    input(ui_helpers.YELLOW + '\nDataFrame read complete.' + ui_helpers.RESET + ' Press Enter to continue.')
    option_7_2()

# Option 8 - Word count filter (commonwords.txt) settings mneu
def option_8():
    """
    Displays the filter settings menu with multiple configuration options for managing the commonwords.txt file.
    Users can view, add, remove, ui_helpers.RESET, or clear the contents of commonwords.txt through a series of sub-menus.
    The working directory is adjusted if necessary to ensure file operations occur in the correct directory.
    
    Raises:
    Exception: catches and logs unexpected exceptions that may occur during execution.
    """
    ui_helpers.clear_screen()

    try:
        print(ui_helpers.CYAN + '8. Filter Settings Menu\n' + ui_helpers.RESET)
        print('1) Check contents.')
        print('2) Add words to filter.')
        print('3) Remove words from the filter.')
        print('4) Reset filter to default.')
        print('5) Remove all word filters.')
        print(' ')

        choice = input('Select option or press Enter to return to Main Menu.')

        if choice == '1':
            option_8_1()
        elif choice == '2':
            option_8_2()
        elif choice == '3':
            option_8_3()
        elif choice == '4':
            analysis.reset_commonwords_txt() # Resets commonwords.txt to default
            option_8()
        elif choice == '5':
            option_8_5()
        else:
            ui_helpers.clear_screen()
            main_menu()
            
    except Exception as e:
        ui_helpers.clear_screen()
        print(ui_helpers.RED + 'TextCrawl encounteui_helpers.RED an unexpected error. Error: {e} ' + ui_helpers.RESET)
        main_menu()

# Option 8_1 - opens commonwords.txt file and displays all words for the user to see
def option_8_1():
    """
    Displays the contents of commonwords.txt to the user. If the file does not exist, it recreates the default 
    commonwords.txt file using load_common_words function and retries displaying its contents.

    Exceptions:
    FileNotFoundError: If the commonwords.txt file does not exist.

    Note:
    This function is intended for user review of the common words list that acts as a filter during word tallying.
    """

    # Menu display
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Filter Contents' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nThe contents of the commonwords.txt file are shown below:\n' + ui_helpers.RESET)

    # Calls the function to display the commonwords
    analysis.read_commonwords_txt()

    # User return prompt
    input(ui_helpers.YELLOW + '\nPress Enter to return to Settings menu.' + ui_helpers.RESET)
    option_8()

# Option 8_2 - Add words to commonwords.txt filter
def option_8_2():
    """
    User prompt for adding words to the commonwords.txt filter used during the word_tally function.
    """
    # Menu display
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Add Words to Filter' + ui_helpers.RESET)
    print('\nYou may add multiple words at a time, using spaces or commas to separate each word.\n' + ui_helpers.YELLOW + '\nThe contents of the commonwords.txt file are shown below\n' + ui_helpers.RESET)

    # Reads commonwords.txt and displays to the user
    analysis.read_commonwords_txt()

    # User prompt to add words to commonwords.txt
    user_words_input = input(ui_helpers.YELLOW + '\n\nEnter the word(s) you would like to add to commonwords.txt ' + ui_helpers.RESET + '(Press Enter to return to Settings menu): ')

    # Calls function to add to filter
    analysis.add_to_commonwords_txt(user_words_input)

    # User continue prompt and menu return
    continue_prompt = input('\nAll done! Would you like to add more words? (Y = yes) ')
    if continue_prompt.lower() == 'y':
        option_8_2()
    else:
        option_8()

# Option 8_3 - Deletes words from commonwords.txt filter
def option_8_3():
    """
    User prompt for deleting words from the commonwords.txt filter used during the word_tally function.
    """

    # Menu display and directions
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Delete Words from Filter' + ui_helpers.RESET + '\n\nYou may remove multiple words at a time, using spaces or commas to separate each word.')
    print(ui_helpers.YELLOW + '\nThe contents of the commonwords.txt file are shown below\n' + ui_helpers.RESET)

    # Reads commonwords.txt and displays to the user
    analysis.read_commonwords_txt()

    # User prompt to remove words from commonwords.txt
    user_words_input = input(ui_helpers.YELLOW + '\n\nEnter the word(s) you would like to remove from commonwords.txt ' + ui_helpers.RESET + '(Press Enter to return to Setings menu): ')
    
    # Function to delete words
    analysis.delete_from_commonwords_txt(user_words_input)

    # User continue prompt and menu return
    continue_prompt = input('\nAll done! Would you like to remove more words? (Y = yes) ')
    if continue_prompt.lower() == 'y':
        option_8_3()
    else:
        option_8()

# Option 8_5 - Removes filters on wordcounts by deleting commonwords.txt contents
def option_8_5():
    """
    Deletes the contents of the commonwords.txt, effectively removing all word filters.
    """
    analysis.delete_commonwords_txt_contents()
    option_8()

# Option 9 - Provides instructions, notes, and help for users
def option_9():
    """
    Provides in-program instructions, future plans, user notes, and contact information for the program.
    """

    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TextCrawl v.40 Help/Readme\n' + ui_helpers.RESET)
    print('''To use TextCrawl, ensure that you have placed at least one .txt file in a subdirectory called "Textfiles" and/or have a direct URL link to a .txt file. From there you can select how many of the most common words utilized in the .txt file.\n''')
    print('''As of v.40, TextCrawl now supports SQLite database building, querying, and management. It continues to support the simpler viewing of most frequent words by .txt file as the Quicklook Word Counts option (1) on the Main Menu. This feature is now most useful to check whether the commonwords.txt filter is returning the desired result before building a SQLite database.''')
    print('''\nBefore analyzing a .txt file for addition to a database, I recommend viewing the commonwords.txt filter (Option 8 on Main Menu) to ensure the desired words (if any) are excluded from the word frequency analysis.''')
    print('''\nSQL queries can be saved as .csv files to the Reports subdirectory. Future releases will feature expanded options for report building and for visuals (i.e., charts) based on the reports.''')
    print('''\nKnown limitations:
    - TextCrawl has only been tested using English-language .txt files. Other languages may not work properly.
    - Some menu or sub-menu options may break if not used properly. This will be fixed in future revisions.
    - Small aspects of the UI are not fully polished yet; please bear with me as I continue to revise and improve TextCrawl!
    - The codebase has not been fully optimized to remove redundancy. As more functions are build, tested, and incorporated, future versions of TextCrawl will feature improved modularity, readability, and error handling.      
    ''')

    print('''I'd love to hear from you! Please send any feedback or questions to me at: ''' + ui_helpers.CYAN + 'c.fowler00@yahoo.com' + ui_helpers.RESET)

    input(ui_helpers.YELLOW + '\nPress Enter to return to the Main Menu.' + ui_helpers.RESET)
    ui_helpers.clear_screen()
    main_menu()
