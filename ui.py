# Import standard libraries
import os

# Import local program scripts
import analysis
import ui_helpers
import sql_manager
import visuals

# Define global objects to prevent Visualizations menu errors
"""
Globals objects:
tfidf_df - the DataFrame produced by the TF-IDF analysis function.
final_metadata - a dictionary containing metadata for each document analyzed.
word_coutns_df - the DataFrame produced by the Word Count Analysis functions.
"""

tfidf_df = None
final_metadata = None
word_counts_df = None

# Main Menu interface
def main_menu():
    """
    Displays the top-menu function options for the user and prompts the user for a selection.

    Depending on input, different top-level functions are called.

    Visualizations and DataFrame Transformation menus are only accessible if a DataFrame is loaded (the global objects are checked to ensure they are not "None" first).
    """

    global tfidf_df, final_metadata, word_counts_df

    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.CYAN + 'Main Menu\n' + ui_helpers.RESET)
    print('1. Word Count Analysis')
    print('2. SQLite Database Menu')
    print('3. TF-IDF Analysis')
    
    if tfidf_df is None and word_counts_df is None:
        print(ui_helpers.GRAY + '4. Visualizations' + ui_helpers.RESET)
    else:
        print('4. Visualizations')
    
    # Option 5 is inaccessible unless a DataFrame is loaded
    if tfidf_df is None and word_counts_df is None:
        print(ui_helpers.GRAY + '5. DataFrame Transformation' + ui_helpers.RESET)
    else:
        print('5. DataFrame Transformation')

    print('6. View/Manage Reports')
    print('7. Filter Settings (view/edit commonwords.txt)')
    print(ui_helpers.YELLOW + '\n(R)eadme or (Q)uit\n' + ui_helpers.RESET)

    choice = input('Enter your selection: ')

    if choice == '1':
        option_1()
    elif choice == '2':
        option_2()
    elif choice == '3':
        option_3()

    elif choice == '4':
        if tfidf_df is None and word_counts_df is None:
            input(ui_helpers.RED + 'Must perform Word Count Analysis with DataFrame, a new TF-IDF Analysis, or load a .csv or .txt Report into a DataFrame first!' + ui_helpers.RESET)
            main_menu()
        else:
            option_4()
    
    elif choice == '5':
        if tfidf_df is None and word_counts_df is None:
            input(ui_helpers.RED + 'Must perform Word Count Analysis with DataFrame, a new TF-IDF Analysis, or load a .csv or .txt Report into a DataFrame first!' + ui_helpers.RESET)
            main_menu()
        else:
            option_5()

    elif choice == '6':
        option_6()
    elif choice == '7':
        option_7()
    elif choice.lower() == 'r':
        readme()
    elif choice.lower() == 'q':
        ui_helpers.clear_screen()
        print(ui_helpers.YELLOW + 'Thanks for using TextAnalysis! Exiting now...' + ui_helpers.RESET)
        quit()
    elif choice == '':
        main_menu()
    else:
        main_menu()

# Option 1 - Word Count Analysis Menu
def option_1():
    """
    Allows users to select from various Word Count Analysis options.
    """
    global tfidf_df, final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Word Count Analysis Menu\n')
        print(ui_helpers.RESET + '1. Load into DataFrame with Local File(s)') 
        print(ui_helpers.RESET + '2. Load into DataFrame with URL(s)')
        print(ui_helpers.RESET + '3. Quick Display Using Local File(s)')
        print(ui_helpers.RESET + '4. Quick Display Using URL')
        print(ui_helpers.RESET + '\n(H)elp for this page')
        print(ui_helpers.RESET + 'Press Enter without selection to return')
        
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_1_1()
        elif choice == '2':
            option_1_2()
        elif choice == '3':
            option_1_3()
        elif choice == '4':
            option_1_4()

        # Help screen    
        elif choice.lower() == 'h':
            ui_helpers.clear_screen()
            ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
            print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Word Count Analysis Menu\n')
            print(ui_helpers.RESET + 'These menu options will count the number of instances of each word located in a .txt file or set of .txt files, stored locally in the "Textfiles" subdirectory or using web URL(s). \n\nFrom there, results will either be displayed within the program or loaded into a Pandas DataFrame, enabling user options such as word lookups, .csv report generation, and visualization output (i.e., barcharts).')
            print('\nPlease note that only .txt files in UTF-8 format are supported. While HTML may work, expect to see undesired results such as HTML code within the Word Counts. If desired, users can manually eliminate these from word counts by adding them to the filter in the commonwords.txt from the Main Menu, or by manually eliminating undesired words from the DataFrame.')
            input(ui_helpers.YELLOW + '\nPress Enter to return to Word Count Analysis Menu: ' + ui_helpers.RESET)
            option_1()

        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 1_1 - Local Text File Word Count with DataFrame
def option_1_1():
    """
    Enables the user to select local text file(s) to perform a Word Count Analysis. Once complete, the DataFrame Transformation Menu is entered for further processing.

    Globals:
    word_counts_df - this is updated with the desired word counts once complete.
    """       
    
    global tfidf_df, final_metadata, word_counts_df

    # Page title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Load into DataFrame with Local File(s)' + ui_helpers.RESET)

    # Lists available text files and gets user selection
    files_to_process = ui_helpers.list_select_textfile(option_1)

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Creates dictionary for all word counts by docs
    word_counts_all_docs = {}

    # Loads the user .txt files and displays confirmation
    for filename in files_to_process:
        text_file_data = analysis.load_textfile(filename)
        wordtally_dict = analysis.tally_words(text_file_data, common_words)
        filename = filename[0:-4]

        # Creates a nested dictionary {filename:{word:counts}} structure
        word_counts_all_docs[filename] = wordtally_dict
    
    # Convert nested dictionary to DataFrame
    word_counts_df = analysis.word_counts_to_df(word_counts_all_docs)
    
    # Data Transformation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Transformation options.' + ui_helpers.RESET)
    word_count_df_transformation_menu(word_counts_df)
    option_1()

# Option 1_2 - Text File Word Count with URL with DataFrame
def option_1_2():
    """
    Allows user to input a URL or multiple URLs for a .txt file and conduct a word analysis. It loads the word counts into a DataFrame and takes the user to the DataFrame Transformation Menu.

    word_counts_df - this is updated with the desired word counts once complete.
    """
    
    global tfidf_df, final_metadata, word_counts_df, wordtally_dict

    # Clears screen and provides title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Load into DataFrame with URL(s)\n' + ui_helpers.RESET)

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Creates dictionary for all word counts by docs
    word_counts_all_docs = {}

    while True:
        # Prompts user for the URL
        user_url = input(ui_helpers.YELLOW + '\nPlease enter or paste the complete URL here ' + ui_helpers.RESET + '(Press Enter when complete): ')

        # Returns to Analysis menu or checks for "http" prefix
        user_url_check = str(user_url).lower()
        
        if len(user_url_check) < 1:
            break

        elif user_url_check[0:4] != 'http':
            print(ui_helpers.RED + 'Invalid URL! Please check and try again.' + ui_helpers.RESET)
            input('')
            option_1_2()

        else:
            # Opens the URL and returns the filename and entire .txt as a string
            default_filename, text_file_data = analysis.url_text_file_open(user_url)
            
            # Enables user to set custom file name (row index for DF)
            filename = input(ui_helpers.RESET + 'Enter the name of the file: ' + ui_helpers.RESET)
            
            # Keeps the file name of the URL if user inputs nothing
            if filename == '':
                filename = str(default_filename)
                filename = filename[2:-2]

            # Completes the Word Count
            wordtally_dict = analysis.tally_words(text_file_data, common_words)
            
            # Creates a nested dictionary {filename:{word:counts}} structure
            word_counts_all_docs[filename] = wordtally_dict

    # Returns to previous menu if no URLs were entered
    if len(word_counts_all_docs) < 1:
        option_1()

    # Continues to analysis if at least one URL was entered
    else:
        # Convert nested dictionary to DataFrame
        word_counts_df = analysis.word_counts_to_df(word_counts_all_docs)

        # Data Transformation prompt
        input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Transformation options.' + ui_helpers.RESET)
        word_count_df_transformation_menu(word_counts_df)
        option_1()

# Option 1_3 - Quick Display of Word Counts in Text File
def option_1_3():
    """
    Displays the number of 'Top Words' by count in a text file or set of text files. Uses other functions to display available .txt files in Textfiles subdirectory, then requests user selection of file(s) by inputing the corresponding number before displaying a user-defined number of the 'Top N' words per text file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Page title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Quick Display Using Local File(s)' + ui_helpers.RESET)

    # Lists available text files and gets user selection
    files_to_process = ui_helpers.list_select_textfile(option_1)

    # Requests user input for number of words to display
    number_to_list = ui_helpers.get_top_n()

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Loads the user .txt files and displays confirmation
    for filename in files_to_process:
        text_file_data = analysis.load_textfile(filename)
        wordtally_dict = analysis.tally_words(text_file_data, common_words)
        visuals.display_word_frequency(filename, wordtally_dict, number_to_list)
    
    # Return Prompt
    input(ui_helpers.YELLOW + '\nPress Enter for to return...' + ui_helpers.RESET)
    option_1()

# Option 1_3 - Quick Display Word Count with URL
def option_1_4():
    """
    Allows user to input URL for a .txt file for Word Count Analysis. It then calls the appropriate analysis functions to complete the scan and display the results on-screen. A DataFrame is not loaded for this function.

    Raises:
    ValueError if user inputs a non-integer
    """
    
    global tfidf_df, final_metadata, word_counts_df

    # Clears screen and provides title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Quick Display Using URL\n' + ui_helpers.RESET)
  
    # Prompts user for the URL
    user_url = input(ui_helpers.YELLOW + 'Please enter or paste the complete URL here ' + ui_helpers.RESET + '(Press Enter to return to ' + ui_helpers.CYAN + 'Analysis ' + ui_helpers.RESET + 'menu): ')

    # Returns to Analysis menu or checks for "http" prefix
    user_url_check = str(user_url).lower()
    if len(user_url_check) < 1:
        option_1()
    elif user_url_check[0:4] != 'http':
        print(ui_helpers.RED + 'Invalid URL! Please check and try again.' + ui_helpers.RESET)
        input('')
        option_1_3()

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # Requests user input for number of words to display
    top_n = ui_helpers.get_top_n()

    # Opens the URL and returns a string
    filename, text_file_data = analysis.url_text_file_open(user_url)

    # Completes the Word Count
    wordtally_dict = analysis.tally_words(text_file_data, common_words)
    visuals.display_word_frequency(filename, wordtally_dict, top_n)
    
    # Returns to Analysis menu
    input('\nPress Enter to return to the ' + ui_helpers.CYAN + 'Analysis '  + ui_helpers.RESET + 'menu.')
    ui_helpers.clear_screen()
    option_1()

    return wordtally_dict

# Option 2 - SQL Database Menu
def option_2():
    """
    Provides user selection menu for SQL functions.
    """

    global tfidf_df, final_metadata, word_counts_df

    while True:
    # Page title and instructions
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'SQLite Database Menu\n' + ui_helpers.RESET)
        print(ui_helpers.RESET + '1. Export Word Count Analysis to SQLite Database')
        print(ui_helpers.RESET + '2. SQLite Database Queries')
        print(ui_helpers.RESET + '\n(H)elp for this page')
        print(ui_helpers.RESET + 'Press Enter without selection to return')

        # User prompt and choice handling
        choice = input('\nEnter your selection: ')
        
        if choice == '1':
            option_2_1()
        elif choice == '2':
            option_2_2()

        # Help screen
        elif choice.lower() == 'h':
            ui_helpers.clear_screen()
            ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
            print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'SQLite Database Menu\n' + ui_helpers.RESET)
            print('These menu options allow users to perform a Word Count Analysis on as many .txt files from the "Textfiles" subdirectory as desired and to export the results to a .sqlite database file in the "Databases" subdirectory.')
            print('\nWords that are included in the commonwords.txt file will be excluded from Word Count Analysis.')
            print('\nEntering the file metadata is not required, but is recommended for future analysis as it will enable proper results for SQL queries.')
            print('\nThe SQL Database Queries submenu allows users to perform numerous queries and to export these as .csv reports as desired. Users may also examine Database file information and perform Word Lookups.')
            input(ui_helpers.YELLOW + '\nPress Enter to return to SQL Database Menu: ' + ui_helpers.RESET)
            option_2()

        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 2_1 - Complete a word count analysis and export to SQL DB
def option_2_1():
    """
    Completes a word frequency analysis and exports results to a SQL database. Filters any words from commonwords.txt from the analysis. Users may choose a single file, multiple files, or all files located in the Textfiles directory.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Header and user instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > ' + ui_helpers.CYAN + 'Export Word Count Analysis to SQLite Database' + ui_helpers.RESET)

    # Lists Textfiles contents and requests user file selection
    files_to_process = ui_helpers.list_select_textfile(option_2)

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    # User prompt for Database name
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > Export Word Count Analysis to SQLite Database' + ui_helpers.CYAN + ' SQL Database Information Entry'+ ui_helpers.RESET)
    print(ui_helpers.RESET + '\nEnter the name of the SQL database to which you would like to export data. You may also enter metadata about the file, including title, author, and year (optional, but recommended!).\n\nNOTE: If entered, Year must be a non-zero integer between -3000 and 2075.\n')

    # Get SQL database information  
    database_name = input(ui_helpers.RESET + 'Enter the name of the SQL database: ' + ui_helpers.RESET)
    if not database_name.endswith('sqlite'):
        database_name += '.sqlite'

    # Loads, analyzes the .txt files
    for filename in files_to_process:
        text_file_data = analysis.load_textfile(filename)
        wordtally_results = analysis.tally_words(text_file_data, common_words)

        # User prompts for file metadata
        doc_title, author, year, genre = ui_helpers.input_file_metadata(filename)

        # Builds the database and exports results to it
        sql_manager.database_build(database_name)
        sql_manager.wordtally_to_database(wordtally_results, database_name, doc_title, author, year, genre)

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

    global tfidf_df, final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > ' + ui_helpers.CYAN + 'SQLite Database Queries\n' + ui_helpers.RESET)
        print(ui_helpers.RESET + '1. Summarize SQLite Database')
        print(ui_helpers.RESET + '2. Word Counts Over Time Queries')
        print(ui_helpers.RESET + '3. Word Frequency by Other Queries')
        print(ui_helpers.RESET + '4. Delete SQLite Database')
        print(ui_helpers.RESET + '\nPress Enter without selection to return')
        
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_2_1()
        elif choice == '2':
            option_2_2_2()
        elif choice == '3':
            option_2_2_3()
        elif choice == '4':
            option_2_2_4()
        else:
            ui_helpers.clear_screen()
            option_2()

# Option 2_2_1 - Summarize SQL Database(s)
def option_2_2_1():
    """
    Provides summary information (metadata) for a user-selected SQL database or multiple databases.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > ' + ui_helpers.CYAN + 'Summarize SQLite Database' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
    
    # Lets user select database from listed files
    filename = ui_helpers.list_select_database(option_2_2)
    sql_manager.summarize_database(filename)

    input(ui_helpers.YELLOW + '\nSummary complete! Press Enter to return to' + 
          ui_helpers.CYAN + ' Database Queries ' + 
          ui_helpers.YELLOW + 'menu.' + ui_helpers.RESET)

# Option 2_2_2 - Word Frequency Trends Over Time
def option_2_2_2():
    """
    Provides user options for time-based queries, such as word counts over time.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Menu tree
    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > ' + ui_helpers.CYAN + 'Word Counts Over Time\n')
        print(ui_helpers.YELLOW + 'Choose a report to run. Reports may be saved as .csv files to the Reports subdirectory.')
        print(ui_helpers.RESET + '1. All Authors')
        print(ui_helpers.RESET + '2. Per Author')
        print(ui_helpers.RESET + '3. By Genre')
        print(ui_helpers.RESET + '4. Documents by Author')
        print(ui_helpers.RESET + '5. Word(s) Lookup')
        print(ui_helpers.YELLOW + '\n\nPress Enter to return to' + 
              ui_helpers.CYAN + ' Database Queries ' + 
              ui_helpers.YELLOW + 'menu.' + ui_helpers.RESET)
        
        # Handles user selection
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_2_2_1()
        elif choice == '2':
            option_2_2_2_2()
        elif choice == '3':
            option_2_2_2_3()
        elif choice == '4':
            option_2_2_2_4()
        elif choice == '5':
            option_2_2_2_5()
        else:
            ui_helpers.clear_screen()
            option_2_2()

# Option 2_2_3 - Word Counts by Other 
def option_2_2_3():
    """
    Provides menu tree for Word Frequncy queries over dimensions other than time.
    """

    global tfidf_df, final_metadata, word_counts_df
    
    # Menu tree
    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > ' + ui_helpers.CYAN + 'Word Counts by Other' + ui_helpers.RESET) 
        print('\n Choose a report to run. Reports may be saved as .csv files to the Reports subdirectory.')
        print('1. Word Counts by Author')
        print('2. Word Counts by Genre')
        print('3. Word Counts by Document')
        print('4. Documents by Genre with Author')
        print('5. Word(s) Lookup by Document')
        print(ui_helpers.YELLOW + '\n\nPress Enter to return to' + 
              ui_helpers.CYAN + ' Database Queries ' + 
              ui_helpers.YELLOW + 'menu.' + ui_helpers.RESET)

        # Handles user selection
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_2_3_1()
        elif choice == '2':
            option_2_2_3_2()
        elif choice == '3':
            option_2_2_3_3()
        elif choice == '4':
            option_2_2_3_4()
        elif choice == '5':
            option_2_2_3_5()
        else:
            ui_helpers.clear_screen()
            option_2_2()

# Option 2_2_4 - Delete Database(s)
def option_2_2_4():
    """
    Provides a list of .sqlite files in Database subdirectory and allows users to specify the index number desired to delete database(s).
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > ' + ui_helpers.CYAN + 'Delete Database(s)' + ui_helpers.RESET)
    print('\nYou may select a database to Delete it.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)

    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2)
            
    # Confirmation prompt
    print(ui_helpers.RED + 'Really delete ' + ui_helpers.RESET + f'{database_name}' + ui_helpers.RED + '?' + ui_helpers.RESET)
    delete_confirmation = input('Enter "C" to cancel or press Enter to continue with deletion.')
    
    # Cancels deletion
    if delete_confirmation.lower() == 'c':
        input(ui_helpers.RESET + f'{database_name} ' + ui_helpers.YELLOW + 'NOT deleted!' + ui_helpers.RESET)
        option_2_2_4()
    
    # Deletes the database
    else:
        os.remove(database_name)
        input(ui_helpers.RESET + f'{database_name} ' + ui_helpers.YELLOW + 'deleted!' + ui_helpers.RESET)
        option_2_2_4()


# Option 2_2_2_1 - Word Counts Over Time (All Authors)
def option_2_2_2_1():
    """
    Provides users the ability to specify a database and appropriate options for building a Word Count Over Time report using all authors in the database. Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts Over Time > ' + ui_helpers.CYAN + 'All Authors' + ui_helpers.RESET)
    print('\nDisplay the most-used words in a database between desired years. Authors are not included as a column.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)

    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_2)

    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (All Authors)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number to List = 5')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    start_year, end_year = ui_helpers.get_start_end_years()
    top_n = ui_helpers.get_top_n()
    
    # Output SQL query to Pandas DF
    df = sql_manager.query_most_used_words(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets name if user provides none
        default_name = f'{database_name}_counts_all_authors_over_time.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + 
          ui_helpers.CYAN + 'SQL Queries' + 
          ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_2()

# Option 2_2_2_2 - Word Counts Over Time (Per Author)
def option_2_2_2_2():
    """
    Provides user interface to specify a database and appropriate options for building a Word Count Over Time report grouped by author. Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts Over Time > ' + ui_helpers.CYAN + 'Per Author' + ui_helpers.RESET)
    print('\nDisplay the most-used words in a database between desired years. Authors are included as a column.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_2)

    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number to List = 5')
    print('\nNote: Number (of data rows) to list will return specified number of rows per author (i.e., "5" will return the Top 5 words by each author).')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    start_year, end_year = ui_helpers.get_start_end_years()
    top_n = ui_helpers.get_top_n()
    
    # Calls function to output SQL query to Pandas DF
    df = sql_manager.query_most_used_words_by_author(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets name if user provides none
        default_name = f'{database_name}_frequency_by_author_over_time.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + 
          ui_helpers.CYAN + 'SQL Queries' + 
          ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_2()

# Option 2_2_2_3 - Word Counts Over Time (By Genre)
def option_2_2_2_3():
    """
    Provides user interface to specify a database and appropriate options for building a Word Frequency Over Time report grouped by genre. Users may then save the report to a .csv file.
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts Over Time > ' + ui_helpers.CYAN + 'By Genre' + ui_helpers.RESET)
    print('\nDisplay the most-used words in a database between desired years. Genres are included as a column.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_2)
    
    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Word Count Trends Over Time (By Genre)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number to List = 5')
    print('\nNote: Number (of data rows) to list will return specified number of rows per genre (i.e., "5" will return the Top 5 words in each genre).')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    start_year, end_year = ui_helpers.get_start_end_years()
    top_n = ui_helpers.get_top_n()

    # Output SQL query to Pandas DF
    df = sql_manager.query_most_used_words_by_genre(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_frequency_by_genre_over_time.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + 
          ui_helpers.CYAN + 'SQL Queries' + 
          ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_2()

# Option 2_2_2_4 - Documents Over Time (By Author)
def option_2_2_2_4():
    """
    Provides user interface  to specify a database and appropriate options for building a Documents By Author Over Time report using all authors in the database. Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts Over Time > ' + ui_helpers.CYAN + 'Documents By Author' + ui_helpers.RESET)
    print('\nDisplay the number of Documents over time by each author in the database.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_2)

    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Documents Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')
    print('Number of Data Rows = 10')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    start_year, end_year = ui_helpers.get_start_end_years()
    top_n = ui_helpers.get_top_n()

    # Output SQL query to Pandas DF
    df = sql_manager.publications_over_time_by_author(database_name, start_year, end_year, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                    ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    # Saves DF
    if save_prompt.lower() == 'y':
        # Sets name if user provides none
        default_name = f'{database_name}_documents_over_time.csv'

        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + 
          ui_helpers.CYAN + 'SQL Queries' + 
          ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_2()

# Option 2_2_2_5 - Word(s) Count Lookup Over Time
def option_2_2_2_5():
    """
    Allows user to specify word(s) to look up in a database and appropriate options for building a Word Count Over Time report using only those words. Users may then save the report to a .csv file.
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts Over Time > ' + ui_helpers.CYAN + 'Word(s) Lookup' + ui_helpers.RESET)
    print('\nDisplay the frequency of user-defined word(s) in a database over time.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_2)
        
    # Clears screen, re-displays title
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Documents Over Time (By Author)' + ui_helpers.RESET)
    print('\nSummary of selected database is displayed below.\n\nEnter desired parameters or press enter for the default values:')
    print('Start Year = 3000 BC')
    print('End Year = 2075')

    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers function
    start_year, end_year = ui_helpers.get_start_end_years()

    # Prompts for user-defined words to search database
    word_list = ui_helpers.make_list_from_user_input()

    # Output SQL query to Pandas DF
    df = sql_manager.words_lookup_over_time(database_name, start_year, end_year, word_list)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Set name if user provides none
        default_name = f'{database_name}_word_lookup_over_time.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'SQL Queries' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_2()

# Option 2_2_3_1 - Word Count by Author
def option_2_2_3_1():
    """
    Allows user to view most common words by Author in a database and return a report (Pandas df). Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Counts by Other > ' + ui_helpers.CYAN + 'Word Counts by Author' + ui_helpers.RESET)
    print('\nDisplay the most common word counts by Author in a database.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_3)
        
    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    print(ui_helpers.RESET + 'Enter the number of words to return per Author.\n' + ui_helpers.RESET)
    top_n = ui_helpers.get_top_n()

    # Output SQL query to Pandas DF
    df = sql_manager.query_most_used_words_by_author_no_time(database_name, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_word_count_by_author.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'Word Frequency by Other' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_3()

# Option 2_2_3_2 - Word Count by Genre
def option_2_2_3_2():
    """
    Allows user to view the word frequency by genre in a database and return a report (Pandas df). Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Count Trends by Other > ' + ui_helpers.CYAN +  'Word Counts by Genre' + ui_helpers.RESET)
    print('\nDisplay the most common word counts by Genre in a database.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_3)
        
    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    print(ui_helpers.RESET + 'Enter the number of words to return per Genre.\n' + ui_helpers.RESET)
    top_n = ui_helpers.get_top_n()

    # Output SQL query to Pandas DF
    df = sql_manager.query_most_used_words_by_genre_no_time(database_name, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_word_count_by_genre.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'Word Frequency by Other' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_3()

# Option 2_2_3_3 - Word Count by Document
def option_2_2_3_3():
    """
    Allows user to view the word count by Document in a database and return a report (Pandas df). Users may then save the report to a .csv file.
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Count Trends by Other > ' + ui_helpers.CYAN + 'Word Counts by Document' + ui_helpers.RESET)
    print('\nDisplay the most common words by document in a database.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_3)
        
    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Requests user parameters using ui_helpers functions
    print(ui_helpers.RESET + 'Enter the number of words to return per Document.\n' + ui_helpers.RESET)
    top_n = ui_helpers.get_top_n()

    # Output SQL query to Pandas DF
    df = sql_manager.query_word_count_by_pub(database_name, top_n)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_word_count_by_docs.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'Word Frequency by Other' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_3()

# Option 2_2_3_4 - Documents by Genre
def option_2_2_3_4():
    """
    Allows user to generate a report showing number of documents by genre in a database. Users select database and specify the number of data rows to return before choosing to save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Count Trends by Other > ' + ui_helpers.CYAN + 'Documents by Genre' + ui_helpers.RESET)
    print('\nDisplay the most commonly used words in a database by Document.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)

    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_3)
        
    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Output SQL query to Pandas DF
    df = sql_manager.publications_by_genre_no_time(database_name)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_docs_by_genre.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'Word Frequency by Other' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_3()

# Option 2_2_3_5 - Word Lookup by Document with Author
def option_2_2_3_5():
    """
    Allows user to specify word(s) to look up in a database and return a report (Pandas df) showing word frequency by document with author. Users may then save the report to a .csv file.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > Word Count Trends by Other > ' + ui_helpers.CYAN +  'Word(s) Lookup by Document' + ui_helpers.RESET)
    print('\nDisplay the frequency of user-defined word(s) in a database by document, including author.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)
        
    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_2_2_3)
        
    # Displays Database Summary
    sql_manager.summarize_database(database_name)

    # Prompts for user-defined words to search database
    word_list = ui_helpers.make_list_from_user_input()

    # Output SQL query to Pandas DF
    df = sql_manager.words_lookup_publication_with_author(database_name, word_list)

    # Prompts user to save DF as .csv file
    save_prompt = input(ui_helpers.YELLOW + '\nQuery complete!' + 
                        ui_helpers.RESET + ' Save as .csv? (Y/N) ')
    
    if save_prompt.lower() == 'y':
        # Sets default name if user provides none
        default_name = f'{database_name}_word_lookup_by_pub.csv'
        
        # Saves DF in the SQL Queries subdir
        ui_helpers.move_to_reports_sql_queries()
        ui_helpers.save_df_as_csv(df, default_name)
        print(ui_helpers.RESET + 'Report may be found in Reports > SQL Queries subdirectory.')

    # User prompt to return to SQL Queries menu
    input(ui_helpers.YELLOW + '\nPress Enter to return to ' + ui_helpers.CYAN + 'Word Frequency by Other' + ui_helpers.YELLOW + ' menu.' + ui_helpers.RESET)
    option_2_2_3()

# Option 3 - TF-IDF Analysis Menu
def option_3():
    """
    Provides user selection menu for TF-IDF (Term Frequency - Inverse Document Frequency) analysis.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'TF-IDF Analysis Menu\n')
    print(ui_helpers.YELLOW + 'Select from options below, or press Enter to return.\n' + ui_helpers.RESET)
    print(ui_helpers.RESET + '1. Query SQL Database for TF-IDF Analysis')
    print(ui_helpers.RESET + '2. Perform TF-IDF Analysis on Multiple Text Files')
    print(ui_helpers.RESET + '3. Perform TF-IDF Analysis using Multiple URLs')
    print(ui_helpers.RESET + '\n(H)elp for this page')
    print(ui_helpers.RESET + 'Press Enter without selection to return')
    
    # Handles user choice
    choice = input('\nEnter your selection: ')

    if choice == '1':
        option_3_1()
    elif choice == '2':
        option_3_2()
    elif choice == '3':
        option_3_3()
    elif choice.lower() == 'h':
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'TF-IDF Analysis Menu\n')
        print(ui_helpers.RESET + "TF-IDF (Term Frequency-Inverse Document Frequency) is a statistical measure used in text analysis to evaluate the importance of a word in a document relative to a collection of documents (corpus). It combines two metrics: " + ui_helpers.YELLOW + "term frequency (TF)" + ui_helpers.RESET + ", which counts how often a word appears in a document, and "  + ui_helpers.YELLOW + "inverse document frequency (IDF)" + ui_helpers.RESET + ", which measures the word's rarity across all documents. \n\nThe formula is TF multiplied by IDF. This approach helps highlight words that are significant in a specific document but not common across the entire corpus, making it useful for tasks like information retrieval and text mining.\n"
        )
        print('To perform a TF-IDF analysis, you must analyze at least two different files. These may come from two or more local files, two or more URLs, or a SQL database containing the information of at least two files may be queried.')
        input(ui_helpers.YELLOW + '\nPress enter to return to TF-IDF Analysis Menu: ' + ui_helpers.RESET)
        option_3()

    else:
        ui_helpers.clear_screen()
        main_menu()

# Option 3_1 - Query SQL Databse for TF-IDF Analysis
def option_3_1():
    """
    Allows user to select SQLite database from which to perform a TF-IDF analysis. Takes user to the TF-IDF Transformation Menu after analysis is complete.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > TF-IDF Analysis Menu > ' + ui_helpers.CYAN + 'Query SQL Database for TF-IDF Analysis\n' + ui_helpers.RESET)

    # Displays available databases and prompts user for selection
    database_name = ui_helpers.list_select_database(option_3)

    # Queries selected database, returns Pandas DF
    df = sql_manager.query_sql_for_tf_idf(database_name)
    tfidf_df, final_metadata = analysis.sql_tf_idf_analysis(df)

    # Success confirmation and header print
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'Query SQL Database for TF-IDF Analysis' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nOperation success!\n\n' + 
          ui_helpers.RESET + 'Pandas DataFrame Header:') 
    print(tfidf_df.head())

    # Data Transformation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Transformation options.' + ui_helpers.RESET)
    tf_idf_df_transformation_menu(tfidf_df)
    option_3()

# Option 3_2 - TF-IDF Analysis on Multiple Text Files
def option_3_2():
    """
    Allows user to select multiple files from the Textfiles subdirectory to perform a TF-IDF analysis. Users may input metadata for each file manually. Takes user to the TF-IDF Transformation Menu after analysis is complete.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > TF-IDF Analysis Menu > ' + ui_helpers.CYAN + 'TF-IDF Analysis of Multiple Text files' + ui_helpers.RESET)
    
    # Lists files in Textfiles and prompts for user input
    files_to_process = ui_helpers.list_select_textfile(option_3)

    # Performs analysis
    tfidf_df, final_metadata = analysis.text_tf_idf_analysis(files_to_process, option_3_2)

    # Success confirmation and header print
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TF-IDF Analysis of Multiple Text files' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nOperation success!\n\n' + 
          ui_helpers.RESET + 'Pandas DataFrame Header:') 
    print(tfidf_df.head())

    # Data Transformation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Transformation options.' + ui_helpers.RESET)
    tf_idf_df_transformation_menu(tfidf_df)
    option_3()

# Option 3_3 - TF-IDF Analysis Using Multiple URLs
def option_3_3():
    r"""
    Allows user to perform a TF-IDF analysis using two or more URLs. Once the analysis is complete, the user enters the DataFrame Transformation menu.
    """
    
    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > TF-IDF Analysis Menu > ' + ui_helpers.CYAN + 'TF-IDF Analysis Using Multiple URLs' + ui_helpers.RESET)
    

    tfidf_df, final_metadata = analysis.url_tf_idf_analysis(option_3)

    # Success confirmation and header print
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TF-IDF Analysis Using Multiple URLs' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nOperation success!\n\n' + 
        ui_helpers.RESET + 'Pandas DataFrame Header:') 
    print(tfidf_df.head())

    # Data Transformation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Transformation options.' + ui_helpers.RESET)
    tf_idf_df_transformation_menu(tfidf_df)
    option_3()

# Option 4 - Visualizations menu
def option_4():
    """
    Provides user selection menu for Visualizations menu. Checks to ensure the tfidf_df exists before allowing user to go to Dashboard menu.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Scren header and menu
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Visualizations\n')
    if word_counts_df is None:
        print(ui_helpers.GRAY + ' 1. Save Word Counts as Bar Chart' + ui_helpers.RESET)
    else:
        print(ui_helpers.RESET + ' 1. Save Word Counts as Bar Chart')
    
    if tfidf_df is None:
        print(ui_helpers.GRAY + ' 2. Save TF-IDF Analysis as Bar Chart' + ui_helpers.RESET)
    else:
        print(ui_helpers.RESET + ' 2. Save TF-IDF Analysis as Bar Chart')
    
    if final_metadata is None:
        print(ui_helpers.GRAY + ' 3. Initialize Interactive Dashboard Bar Chart (TF-IDF)' + ui_helpers.RESET)   
    else:
        print(ui_helpers.RESET + ' 3. Initialize Interactive Dashboard Bar Chart (TF-IDF) - (BETA)')  

    print(ui_helpers.RESET + '\n(H)elp for this page')
    print(ui_helpers.RESET + 'Press Enter without selection to return')
    choice = input(ui_helpers.RESET + '\nEnter your selection: ')
    
    if choice == '1':
        # Ensures a Word Count DataFrame exists
        if word_counts_df is None:
            prompt = input(ui_helpers.RED + 'Must perform Word Count Analysis with DataFrame first!' + ui_helpers.RESET + ' Go to Word Count Analysis Menu now? ("Y" for yes.) ')
            if prompt.lower() == 'y':
                option_1()
        else:
            option_4_1()

    if choice == '2':
        # Ensures a TFIDF DF exists
        if tfidf_df is None:
            prompt = input(ui_helpers.RED + 'Must perform TF-IDF Analysis first!' + ui_helpers.RESET + ' Go to TF-IDF Analysis Menu now? ("Y" for yes.) ')
            if prompt.lower() == 'y':
                option_3()
            else:
                option_4()
        else:
            option_4_2()

    # Handles user choice
    if choice == '3':
        # Ensures a TFIDF DF exists
        if final_metadata is None:
            prompt = input(ui_helpers.RED + 'Must perform a TF-IDF Analysis with File Metadata information first! (Start new SQL Query or new Text File TF-IDF Analysis)' + ui_helpers.RESET + ' Go to TF-IDF Analysis Menu now? ("Y" for yes.) ')
            if prompt.lower() == 'y':
                option_3()
            else:
                option_4()
        else:
            option_4_3()

    # Help screen
    elif choice.lower() == 'h':
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Visualizations\n')
        
        print(ui_helpers.RESET + 'The Visualizations Menu enables the user to output a Word Count Analysis or TF-IDF Analysis DataFrame to a bar chart. Users may specify how many of the top word values per document inside the DataFrame to display.')
        print(ui_helpers.RESET + '\nThe Dashboard option outputs a TF-IDF DataFrame to an interactive chart, increasing the number of words which can be displayed at a time along with file metadata. Note that this feature is still in beta and can behave unexpectedly at times.')
        print('\nFor all visualizations, it is recommended to consider the number of documents inside the DataFrame and to adjust the number of words to display from each one accordingly. Choosing too many words per document to display may result in some words or values not displaying correctly or at all.')

        input(ui_helpers.YELLOW + '\nPress Enter to return to Visualizations Menu: ' + ui_helpers.RESET)
        option_4()

    else:
        ui_helpers.clear_screen()
        main_menu()

# Option 4_1 - Save Word Count DF as Bar Chart
def option_4_1():
    """
    Provides interface for calling the functions necessary to create a bar chart for a Word Counts Dataframe.

    Globals:
    word_count_df - the DataFrame created by the Word Counts functions
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen Header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Visualizations Menu > ' + ui_helpers.CYAN +  'Save Word Counts as Bar Chart')
    print(ui_helpers.RESET + '\nSave the Word Counts DataFrame to a Bar Chart in the "Visuals" subdirectory. You will need to specify how many of the "top words by count" to display.\n')

    # Prompts user for number of words to display before calling Bar Chart
    top_n = ui_helpers.get_top_n()
    visuals.create_counts_barchart(word_counts_df, top_n)
    
    option_4()

# Option 4_2 - Save TF-IDF as Bar Chart
def option_4_2():
    """
    Provides interface for calling the function to create a barchart. Requires a DataFrame with TF-IDF scores.

    Globals:
    tfidf_df - the DataFrame created once TF-IDF Analysis is complete
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen Header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Visualizations Menu > ' + ui_helpers.CYAN +  'Save TF-IDF Analysis as Bar Chart' + ui_helpers.RESET)
    print('\nUses the DataFrame produced by the TF-IDF Analysis function to create a Bar Chart and save it to the "Visuals" subdirectory.\n')
    
    # Prompts user for number of words to display before calling Bar Chart
    top_n = ui_helpers.get_top_n()
    visuals.create_tf_idf_barchart(tfidf_df, top_n)
    
    option_4()

# Option 4_3 - Initialize TF-IDF Dashboard
def option_4_3():
    """
    Initializes a Dashboard once a TF-IDF DF exists. Requires user to input number of returns per document before initializing visuals.create_tf_idf_dash() function.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen Header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Visualizations Menu > ' + ui_helpers.CYAN +  'Initialize TF-IDF Dashboard (BETA)' + ui_helpers.RESET)
    print('\nUses the DataFrame produced following TF-IDF analysis to initialize an interactive dashboard, allowing users to select documents to view a specified number of words with top TF-IDF scores per document.\n')
    print('The dashboard may be viewed locally at: ' + 
        ui_helpers.CYAN + 'http://127.0.0.1:8050/')
    
    top_n = ui_helpers.get_top_n()
    
    # Initializes Dashboard
    try:
        tfidf_df, final_metadata = visuals.create_tf_idf_dash(tfidf_df, final_metadata, top_n)
    except KeyboardInterrupt:
        print('Dashboard ended by user!')
    
    input('\n\nPress Enter to continue...')
    option_4()

# Option 5 - DataFrame Transformation
def option_5():
    """
    Allows user to access the DataFrame Transformation Menu if a DataFrame is loaded.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen Header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'DataFrame Transformation\n')
    if word_counts_df is None:
        print(ui_helpers.GRAY + ' 1. Word Count Analysis DataFrame' + ui_helpers.RESET)
    else:
        print(ui_helpers.RESET + ' 1. Word Count Analysis DataFrame')

    if tfidf_df is None:
        print(ui_helpers.GRAY + ' 2. TF-IDF Analysis DataFrame')
    else:
        print(ui_helpers.RESET + ' 2. TF-IDF Analysis DataFrame')

    print(ui_helpers.RESET + '\n(H)elp for this page')
    print(ui_helpers.RESET + 'Press Enter without selection to return')
    choice = input(ui_helpers.RESET + '\nEnter your selection: ')
    
    if choice == '1':
        # Ensures a Word Count DataFrame exists
        if word_counts_df is None:
            print(ui_helpers.RED + 'Must perform a new Word Count Analysis or load a Word Count Report first.\n' + ui_helpers.RESET)
            print(ui_helpers.YELLOW + 'Choose an option:' + ui_helpers.RESET)
            print('\n 1. Perform New Word Count Analysis')
            print(' 2. Load a Word Count Report')
            print('\n Press Enter to cancel')
            prompt = input(ui_helpers.RESET + '\nEnter selection: ' + ui_helpers.RESET)
            
            # Handles user choice
            while True:
                if prompt == '1':
                    option_1()
                elif prompt == '2':
                    option_7_1()  
                elif prompt == '':
                    option_5()
                
                else:
                    print(ui_helpers.RED + 'Please select one of the choices above.' + ui_helpers.RESET)
        else:
            word_count_df_transformation_menu(word_counts_df)
            main_menu()

    elif choice == '2':
        # Ensures a TF-IDF DataFrame exists
        if tfidf_df is None:
            print(ui_helpers.RED + 'Must perform a new TF-IDF Analysis or load a .TF-IDF Report first.\n' + ui_helpers.RESET)
            print(ui_helpers.YELLOW + 'Choose an option:' + ui_helpers.RESET)
            print('\n 1. Perform New TF-IDF Analysis')
            print(' 2. Load TF-IDF Report')
            print('\nPress Enter to cancel')
            prompt = input(ui_helpers.RESET + '\nEnter selection: ' + ui_helpers.RESET)
            
            # Handles user choice
            while True:
                if prompt == '1':
                    option_3()         
                elif prompt == '2':
                    option_7_3()
                elif prompt == '':
                    option_5()
                else:
                    print(ui_helpers.RED + 'Please select one of the choices above.' + ui_helpers.RESET)
        else:
            tf_idf_df_transformation_menu(tfidf_df)
            main_menu()

    # Help screen
    elif choice.lower() == 'h':
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'DataFrame Transformation\n')
        print(ui_helpers.RESET + '\nThe DataFrame Transformation Menu enables the user to manipulate a Word Count Analysis DataFrame or a TF-IDF DataFrame in a variety of powerful ways.')
        print(ui_helpers.RESET + '\nOptions include setting minimum value thresholds (for Counts or TF-IDF score), removing specific words, word lookup, keeping only the top or bottom user-defined number words, visualizations via barchart or dashboard, or exporting to .csv or .txt files.')
        print(ui_helpers.RESET + '\nThis menu is only available when a DataFrame is loaded.')
        input(ui_helpers.YELLOW + '\nPress Enter to return to DataFrame Transformation Menu: ' + ui_helpers.RESET)
        option_5()

    else:
        ui_helpers.clear_screen()
        main_menu()

# Option 6 - Reports Menu
def option_6():
    """
    Provides user options for viewing Reports.
    """

    global tfidf_df, final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' +ui_helpers.CYAN + 'Reports Menu' + ui_helpers.RESET)

        print(ui_helpers.RESET + '\n1. Word Count Reports')
        print(ui_helpers.RESET + '2. SQL Query Reports')
        print(ui_helpers.RESET + '3. TF-IDF Reports')
        print(ui_helpers.RESET + '4. Delete Reports')
        print(ui_helpers.RESET + '\n(H)elp for this page')
        print(ui_helpers.RESET + 'Press Enter without selection to return')
        
        # User prompt and choice handling
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_6_1()
        elif choice == '2':
            option_6_2()
        elif choice == '3':
            option_6_3()
        elif choice == '4':
            option_6_4()
        
        # Help Screen
        elif choice.lower() == 'h':
            ui_helpers.clear_screen()
            ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
            print(ui_helpers.RESET + 'Main Menu > ' +ui_helpers.CYAN + 'Reports Menu' + ui_helpers.RESET)
            print(ui_helpers.RESET + '\nReports can be saved to the Reports subdirectory after completing a Word Count or TF-IDF Analysis. These reports can later be loaded or deleted using this menu. Loading a report will enable you to load it as a DataFrame for further transformation or visual generation (such as bar charts) or to output as a new Report.')
            input(ui_helpers.YELLOW + '\nPress enter to return to Reports Menu: ' + ui_helpers.RESET)
            option_6()

        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 6_1 - Word Count Reports
def option_6_1():
    """
    Displays contents of Reports/Word Counts subdirectory. Enables user to view list of .csv and .txt files (reports) they can view and load into a DF for further transformation.

    Globals:
    word_counts_df - used for setting the report as the word_counts_df after loading
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'Word Count Reports' + ui_helpers.RESET)

    # Displays contents of Reports, prompts user for selection
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)
    report_name = ui_helpers.list_select_report(option_6, 'wordcounts')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    choice = input(ui_helpers.YELLOW + '\nDataFrame loaded!' + ui_helpers.RESET + ' Enter "Y" to load the report as a DataFrame and enter the DataFrame Transformation Menu, or Enter to skip: ')
    
    while True:
        if choice.lower() == 'y':
            word_counts_df = df
            word_count_df_transformation_menu(word_counts_df)
            main_menu()

        else:
            option_6_1()
            return
        
# Option 6_2 - SQL Query Reports
def option_6_2():
    """
    Displays contents of Reports/SQL Queries subdirectory. Enables user to view list of .csv and .txt files (reports) they can view.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'SQL Query Reports' + ui_helpers.RESET)
    print('\nYou may select a report to view its contents.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Reports, prompts user for selection
    report_name = ui_helpers.list_select_report(option_6, 'sqlqueries')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    input(ui_helpers.YELLOW + '\nReport loaded!' + ui_helpers.RESET + ' Press Enter to continue...')
    option_6_2()

# Option 7_3 - TF-IDF Reports
def option_6_3():
    """
    Displays contents of Reports/TF-IDF subdirectory. Enables user to view list of .csv and .txt files (reports) they can view and load into a DF for further transformation.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'TF-IDF Reports' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Reports, prompts user for selection
    report_name = ui_helpers.list_select_report(option_6, 'tfidf')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    choice = input(ui_helpers.YELLOW + '\nDataFrame loaded!' + ui_helpers.RESET + ' Enter "Y" to load the report as a DataFrame and enter the DataFrame Transformation Menu, or Enter to skip: ')
    while True:

        if choice.lower() == 'y':
            tfidf_df = df
            tf_idf_df_transformation_menu(tfidf_df)
            main_menu()

        else:
            option_6_3()
            return

# Option 7_4 - Delete Report(s)
def option_6_4():
    """
    Displays .csv files located in the Reports subdirectory and allows users to input an index number corresponding to reports for deletion.
    """

    global tfidf_df, final_metadata, word_counts_df
    
    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'Delete CSV Reports' + ui_helpers.RESET)

    # Prompts user for report type selection
    print(ui_helpers.YELLOW + '\nTypes of Reports:\n' + ui_helpers.RESET)
    print(ui_helpers.RESET + '1. Word Counts Reports')
    print(ui_helpers.RESET + '2. SQL Query Reports')
    print(ui_helpers.RESET + '3. TF-IDF Reports')
    
    choice = input(ui_helpers.RESET + '\nEnter your selection: ' + ui_helpers.RESET)

    # Defines report subdirectory based on user choice
    if choice == '1':
        report_subdir = 'wordcounts'
    elif choice == '2':
        report_subdir = 'sqlqueries'
    elif choice == '3':
        report_subdir = 'tfidf'
    else:
        option_6()

    # Displays available reports
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'Delete CSV Reports' + ui_helpers.RESET)

    print(ui_helpers.YELLOW + '\nAvailable reports:\n' + ui_helpers.RESET)
    report_name = ui_helpers.list_select_report(option_6, report_subdir)

    # Delete confirmation prompt
    print(ui_helpers.RED + 'Really delete ' + 
          ui_helpers.RESET + f'{report_name}' + 
          ui_helpers.RED + '?' + ui_helpers.RESET)
    delete_confirmation = input('Enter "Y" (Yes) to delete: ')
    
    # Cancels deletion if user does not enter "y"
    if delete_confirmation.lower() != 'y':
        input(ui_helpers.RESET + f'{report_name} ' + 
              ui_helpers.YELLOW + 'NOT deleted!' + ui_helpers.RESET)
        option_6_4()
    
    # Deletes the Report
    else:
        os.remove(report_name)
        input(ui_helpers.RESET + f'{report_name} ' + 
              ui_helpers.YELLOW + 'deleted!' + ui_helpers.RESET)
        option_6_4()
    
    # User return prompt
    input(ui_helpers.YELLOW + ' Press Enter to continue.' + ui_helpers.RESET)
    option_6_4()

# Option 8 - Word count filter (commonwords.txt) settings mneu
def option_7():
    """
    Displays the filter settings menu with multiple configuration options for managing the commonwords.txt file.
    Users can view, add, remove, ui_helpers.RESET, or clear the contents of commonwords.txt through a series of sub-menus.
    The working directory is adjusted if necessary to ensure file operations occur in the correct directory.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Header and Menu Tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Filter Settings Menu\n' + ui_helpers.RESET)
    print('1. Filter Contents')
    print('2. Add words to filter')
    print('3. Remove words from the filter')
    print('4. Reset filter to default')
    print('5. Remove all word filters')
    print('\n(H)elp for this page')
    print('Press Enter without selection to return')

    choice = input(ui_helpers.RESET + '\nEnter your selection: ')

    if choice == '1':
        option_7_1()
    elif choice == '2':
        option_7_2()
    elif choice == '3':
        option_7_3()
    elif choice == '4':
        conf_prompt = input(ui_helpers.YELLOW + 'Really reset the filter to default list? (Enter "Y" for "Yes"): ' + ui_helpers.RESET)
        if conf_prompt.lower() == 'y':
            analysis.reset_commonwords_txt() # Resets commonwords.txt to default
            print(ui_helpers.YELLOW + '\nAttention! ' + ui_helpers.RESET + 'The contents of commonwords.txt has been reset to the default list! These are the only words which will be excluded from future text analyses. You may return to this menu to customize the list appropriately.')
            input('\nPress Enter to continue...')
            option_7()
        else:
            option_7()
    
    elif choice == '5':
        conf_prompt = input(ui_helpers.YELLOW + 'Really delete all words from filter? (Enter "Y" for "Yes"): ' + ui_helpers.RESET)
        if conf_prompt.lower() == 'y':
            analysis.delete_commonwords_txt_contents() # Deletes commonwords.txt contents
            print(ui_helpers.YELLOW + '\nAttention! ' + ui_helpers.RESET + 'The contents of commonwords.txt has been cleared! All words will now be counted when analyzing text documents. You may always reset the filter to default or create your own words list using this menu.')
            input('\nPress Enter to continue...')
            option_7()
        else:
            option_7()

    # Help screen
    elif choice.lower() == 'h':
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Filter Settings Menu\n' + ui_helpers.RESET)
        print('This filter applies only to Word Count Analyses. Words contained within the commonwords.txt file will not be added to the the Word Count results.\n\nThis is useful for removing common words ("and," "the", "if," etc.) or any other words the user wishes to remove.')
        print('\nIf words are not filtered prior to Word Count Analyses, they may be removed manually from the DataFrame Transformation Menu later.')
        print('\nThe menu options on this page allow users to view the current filter, add/remove words from it, erase the contents, and restore it to a default set of words.')
        print('\nThe filter words can also be manually edited outside the program simply by editing the commonwords.txt file located in the same directory as the script. Because this filter list pulls from this file directly, the filter will not change from session-to-session provided this file has not been altered.')

        input(ui_helpers.YELLOW + '\nPress Enter to return to Filter Settings Menu: ' + ui_helpers.RESET)
        option_1()

    else:
        ui_helpers.clear_screen()
        main_menu()
            
# Option 8_1 - opens commonwords.txt file and displays all words for the user to see
def option_7_1():
    """
    Displays the contents of commonwords.txt to the user. If the file does not exist, it recreates the default 
    commonwords.txt file using load_common_words function and retries displaying its contents.

    Note:
    This function is intended for user review of the common words list that acts as a filter during Word Count Analysis.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Menu display
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Filter Settings Menu > ' + ui_helpers.CYAN + 'Filter Contents' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nThe contents of the commonwords.txt file are shown below:\n' + ui_helpers.RESET)

    # Calls the function to display the commonwords
    analysis.read_commonwords_txt()

    # User return prompt
    input(ui_helpers.YELLOW + '\nPress Enter to return to Settings menu.' + ui_helpers.RESET)
    option_7()

# Option 8_2 - Add words to commonwords.txt filter
def option_7_2():
    """
    User prompt for adding words to the commonwords.txt filter used during the word_tally function.
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Filter Settings Menu > ' + ui_helpers.CYAN + 'Add Words to Filter' + ui_helpers.RESET)
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
        option_7_2()
    else:
        option_7()

# Option 8_3 - Deletes words from commonwords.txt filter
def option_7_3():
    """
    User prompt for deleting words from the commonwords.txt filter used during the word_tally function.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Filter Settings Menu > ' + ui_helpers.CYAN + 'Delete Words from Filter' + ui_helpers.RESET + '\n\nYou may remove multiple words at a time, using spaces or commas to separate each word.')
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
        option_7_3()
    else:
        option_7()

# Readme - Provides instructions, notes, and help for users
def readme():
    """
    Provides in-program instructions, future plans, user notes, and contact information for the program.
    """

    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TextAnalysis v.70 Readme\n' + ui_helpers.RESET)
    print('''To use TextAnalysis, ensure that you have placed at least one .txt file in a subdirectory called "Textfiles" and/or have a direct URL link to a .txt file. To get the most out of the program by using the Term Frequency - Inverse Document Frequency (TF-IDF) Analysis functions, please ensure you have a minmum of two .txt files.\n''')
    print('''TF-IDF is a statistical analysis tool which totals the number of times a given word appears in a text document and then compares this word count in a single document to the corresponding word counts in the other documents in the set. By inverting the weighting of each given word based on the number of instances it is used by other documents in the set, the user can quickly analyze which words are most "important" or most "unique" in a given document.''')
    print('''\nUsers may maniuplate the TF-IDF DataFrame to filter based on threshold, Top N scores per document, or via a word search. Additionally, users may choose to output the DataFrame results to a .txt or .csv report, or initiate an interactive bar chart dashboard!''')
    print('''\nBefore analyzing a .txt file for addition to a database, I recommend viewing the commonwords.txt filter (Option 8 on Main Menu) to ensure the desired words (if any) are excluded from the word frequency analysis.''')
    print('''\n New features in v.70:
    - TextCrawl is now TextAnalysis!
    - Users may now perform TF-IDF Analysis on multiple URLs directly.
    - Header format fixed,
    ''')
    print('''\nKnown limitations:
    - When using URLs, other file types (such as HTML) may work, however they are not yet officially supported. Users may retrieve results with HTML code counted as words. If desired, undesired words may be removed using the DataFrame Transformation menu or by editing the commonwords.txt filter.
    - TextAnalysis has only been tested using English-language .txt files. Other languages may not work properly.
    - Some menu or sub-menu options may break if not used properly. This will be fixed in future revisions.
    - Attempting to generate a .csv report with a very large DataFrame may result in truncation based on the program opening the file later. If outputting a TF-IDF DataFrame, it is recommended to apply a threshold or other filter to reduce the size of the dataset when using large documents and (consequently) DataFrames.
    - The codebase has not been fully optimized to remove redundancy. As more functions are build, tested, and incorporated, future versions of TextAnalysis will feature improved modularity, readability, and error handling.      
    ''')

    print('''I'd love to hear from you! Please send any feedback or questions to me at: ''' + ui_helpers.CYAN + 'c.fowler00@yahoo.com' + ui_helpers.RESET)

    input(ui_helpers.YELLOW + '\nPress Enter to return to the Main Menu.' + ui_helpers.RESET)
    ui_helpers.clear_screen()
    main_menu()

# TF-IDF DataFrame Transformation menu
def tf_idf_df_transformation_menu(tfidf_df):
    """
    Once a TF-IDF DataFrame is created, this can be utilized to allow the user to perform a variety of actions on the DataFrame:
        1. Apply a minimum threshold to all TF-IDF values
        2. Search for and keep specific words in the DataFrame
        3. Search for and remove specific words from the DataFrame
        4. Keep only 'Top N' user-specified words per document
        5. Output to a .csv file
        6. Output to a .txt file
        7. Initialize a Dashboard for visualization using Dash
        8. Save Bar Chart with "Top N" Words')

    The menu is continuously displayed until the user inputs 'd' for Done.
    
    Parameters:
    tfidf_df - the DataFrame produced by the TF-IDF analysis function.
    """
    global final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > DataFrame Transformation > ' + ui_helpers.CYAN + 'Transform TF-IDF DataFrame')
        print(ui_helpers.YELLOW + '\nCurrent DataFrame Header:' + ui_helpers.RESET)
        print(tfidf_df.head(5))
        print(ui_helpers.YELLOW + '\nWhat would you like to do next?\n')
        print(ui_helpers.RESET + '1. Apply threshold to TF-IDF values')
        print(ui_helpers.RESET + '2. Search DataFrame for specific words')
        print(ui_helpers.RESET + '3. Remove Word(s) From DataFrame')
        print(ui_helpers.RESET + '4. Keep Only "Top N" words per document')
        print(ui_helpers.RESET + '5. Keep Only "Bottom N" words per document')
        print(ui_helpers.RESET + '6. Output DataFrame to .csv file')
        print(ui_helpers.RESET + '7. Output DataFrame to .txt file')
        print(ui_helpers.RESET + '8. Initialize Dashboard')
        print(ui_helpers.RESET + '9. Save Bar Chart with "Top N" Words')
        print(ui_helpers.RESET + '\nEnter "D" when done to return to menu')

        choice = input(ui_helpers.RESET + '\nEnter your selection: ' + ui_helpers.RESET)
        
        # Applies threshold to TF-IDF values
        if choice == '1':

            # Calculate and display the min and max TF-IDF values
            min_value, max_value = analysis.get_min_max(tfidf_df)
            print(ui_helpers.YELLOW + '\nThe TF-IDF range for this DataFrame is:' + 
                  ui_helpers.RESET + f'{min_value:.2f}' + 
                  ui_helpers.YELLOW + ' to ' + 
                  ui_helpers.RESET + f'{max_value:.2f}')

            # Get user threshold and convert to float
            threshold = input(ui_helpers.RESET + '\nEnter desired threshold: ' + ui_helpers.RESET)
            
            # Apply threshold
            try:
                threshold = float(threshold)
                tfidf_df = analysis.apply_threshold_filter(tfidf_df, threshold)

                # User confirmation prompt and DF head
                ui_helpers.clear_screen()
                print(ui_helpers.YELLOW + '\nThreshold ' + 
                    ui_helpers.RESET + f'{threshold}' + 
                    ui_helpers.YELLOW + ' applied! DataFrame Header is below:' +
                    ui_helpers.RESET)
                print(tfidf_df.head(5))
                input(ui_helpers.YELLOW + 'Press Enter to continue.' + ui_helpers.RESET)

            except ValueError:
                print(ui_helpers.RED + 'Please Enter a valid number.' + ui_helpers.RESET)
        
        # Enables user word search of the DF
        elif choice == '2':
            words_list = ui_helpers.make_list_from_user_input()
            tfidf_df = analysis.word_search_dataframe(tfidf_df, words_list)
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  'DataFrame word search complete! DataFrame Header is below:' + ui_helpers.RESET)
            print(tfidf_df.head(5))
            input(ui_helpers.YELLOW + '\nPress Enter to continue.' + ui_helpers.RESET)
        
        # Removes words from DF
        elif choice == '3':
            words_list = ui_helpers.make_list_from_user_input()
            tfidf_df = analysis.remove_words_from_df(tfidf_df, words_list)
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  'Word Removal complete! DataFrame header is below:' + ui_helpers.RESET)
            print(tfidf_df.head(5))
            input(ui_helpers.YELLOW + '\nPress Enter to continue.' + ui_helpers.RESET)

        # Applies 'Top N' Words per Document
        elif choice == '4':
            
            print(ui_helpers.RESET + 'The number entered below will keep only the "Top N" words by TF-IDF score per document in the DataFrame.')
            top_n = ui_helpers.get_top_n()
            
            # Applies the 'top n words' to the DF based on user preference
            tfidf_df = tfidf_df.apply(lambda row: row.nlargest(top_n), axis=1)
            tfidf_df = tfidf_df.fillna(0)  # Replace NaN with 0

            # User confirmation prompt
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  f'Only the top {top_n} words were kept. Press Enter to continue...')
        
        # Applies 'Bottom N' Words per Document
        elif choice =='5':
            print(ui_helpers.RESET + 'The number entered below will keep only the "Bottom N" words by TF-IDF score per document in the DataFrame.')
            bottom_n = ui_helpers.get_top_n()

            # Applies the 'bottom n words' to the DF based on user preference
            tfidf_df = tfidf_df.apply(lambda row: row.nsmallest(bottom_n), axis=1)
            tfidf_df = tfidf_df.fillna(0)

            # User confirmation prompt
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  f'Only the bottom {bottom_n} words were kept. Press Enter to continue...')

        # Saves the DataFrame as a .csv
        elif choice == '6':
            default_name = 'TF_IDF_DataFrame'
            ui_helpers.move_to_reports_tfidf()
            ui_helpers.save_df_as_csv(tfidf_df, default_name)
            print(ui_helpers.RESET + 'DataFrame Output may be found in Reports > TF-IDF subdirectory.')
            input(ui_helpers.YELLOW + '\nPress Enter to continue.' + ui_helpers.RESET)

        # Saves the DataFrame as tab-delimited .txt
        elif choice == '7':
            default_name = 'TF_IDF_DataFrame'
            ui_helpers.move_to_reports_tfidf()
            ui_helpers.save_df_as_txt(tfidf_df, default_name)
            print(ui_helpers.RESET + 'DataFrame Output may be found in Reports > TF-IDF subdirectory.')
            input(ui_helpers.YELLOW + 'Press Enter to continue.' + ui_helpers.RESET)
            
        elif choice == '8':
            # Prompts user for Top N from DF
            input(ui_helpers.YELLOW + 'Notice! Press ' + 
                  ui_helpers.RESET + 'Ctrl + C ' + 
                  ui_helpers.YELLOW + 'when Dashboard is running to quit and return to menu.')
            top_n = input(ui_helpers.RESET + 'Enter how many "top words" to keep in the DataFrame: ' + ui_helpers.RESET)
            
            # Ensure top_n is a number
            try:
                top_n = int(top_n)

            except ValueError:
                print (ui_helpers.RED + 'Please enter a number!' + ui_helpers.RESET)

            # Calls the Dashboard
            visuals.create_tf_idf_dash(tfidf_df, final_metadata, top_n)

        elif choice == '9':
            # Prompts user for Top N from DF
            print(ui_helpers.YELLOW + 'Specify number of words "per document" to display on the Bar Chart.' + 
                  ui_helpers.RESET)
            top_n = ui_helpers.get_top_n()

            # Creates the bar chart, saves to 'Visuals' subdirectory
            visuals.create_tf_idf_barchart(tfidf_df, top_n)
            
        elif choice.lower() == 'd':
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 'DataFrame Transformation complete!' + 
                  ui_helpers.RESET + '\n\nYou may start a new query or go to the ' +
                  ui_helpers.CYAN + 'Visualizations' +
                  ui_helpers.RESET + ' menu for more options.')
            input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)

            return

# Word Counts DataFrame Transformation menu
def word_count_df_transformation_menu(word_counts_df):
    """
    Once a Word Count DataFrame is created, this can be utilized to allow the user to perform a variety of actions on the DataFrame:
        1. Apply a minimum count number to be retained
        2. Search for and keep specific words in the DataFrame
        3. Search for and remove specific words from the DataFrame
        4. Keep only the top user-specified number of words per document
        5. Keep only "Bottom N" words per document
        6. Output to a .csv file
        7. Output to a .txt file
        8. Save Bar Chart with "Top N" Words

    The menu is continuously displayed until the user inputs 'd' for Done.
    
    Parameters:
    word_counts_df - the DataFrame produced by Word Counts functions
    """
    global tfidf_df, final_metadata

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > DataFrame Transformation > ' + ui_helpers.CYAN + 'Transform Word Counts DataFrame')
        print(ui_helpers.YELLOW + '\nCurrent DataFrame Header:' + ui_helpers.RESET)
        print(word_counts_df.head(5))
        print(ui_helpers.YELLOW + '\nWhat would you like to do next?\n')
        print(ui_helpers.RESET + '1. Apply Minimum Number of Counts')
        print(ui_helpers.RESET + '2. Search DataFrame for Word(s)')
        print(ui_helpers.RESET + '3. Remove Word(s) From DataFrame')
        print(ui_helpers.RESET + '4. Keep Only "Top N" words per document')
        print(ui_helpers.RESET + '5. Keep Only "Bottom N" words per document')
        print(ui_helpers.RESET + '6. Output DataFrame to .csv file')
        print(ui_helpers.RESET + '7. Output DataFrame to .txt file')
        print(ui_helpers.RESET + '8. Save Bar Chart with "Top N" Words')
        print(ui_helpers.RESET + '\nEnter "D" when done to return to menu')

        choice = input(ui_helpers.RESET + '\nEnter your selection: ' + ui_helpers.RESET)
        
        # Applies threshold to Word Count values
        if choice == '1':

            # Calculate and display the min and max Word Count values
            min_value, max_value = analysis.get_min_max(word_counts_df)
            print(ui_helpers.YELLOW + '\nThe "count per word" range for this DataFrame is:' + 
                  ui_helpers.RESET + f'{min_value:.2f}' + 
                  ui_helpers.YELLOW + ' to ' + 
                  ui_helpers.RESET + f'{max_value:.2f}')

            # Get user threshold and convert to float
            threshold = input(ui_helpers.RESET + '\nEnter desired threshold: ' + ui_helpers.RESET)
            
            # Apply threshold
            try:
                threshold = float(threshold)
                word_counts_df = analysis.apply_threshold_filter(word_counts_df, threshold)

                # User confirmation prompt and DF head
                ui_helpers.clear_screen()
                print(ui_helpers.YELLOW + '\nThreshold ' + 
                    ui_helpers.RESET + f'{threshold}' + 
                    ui_helpers.YELLOW + ' applied! DataFrame Header is below:' +
                    ui_helpers.RESET)
                print(word_counts_df.head(5))
                input(ui_helpers.YELLOW + 'Press Enter to continue.' + ui_helpers.RESET)

            except ValueError:
                print(ui_helpers.RED + 'Please Enter a valid number.' + ui_helpers.RESET)
        
        # Enables user word search of the DF
        elif choice == '2':
            words_list = ui_helpers.make_list_from_user_input()
            word_counts_df = analysis.word_search_dataframe(word_counts_df, words_list)
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  'DataFrame word search complete! DataFrame Header is below:' + ui_helpers.RESET)
            print(word_counts_df.head(5))
            input(ui_helpers.YELLOW + '\nPress Enter to continue.' + ui_helpers.RESET)

        # Removes words from DF
        elif choice == '3':
            words_list = ui_helpers.make_list_from_user_input()
            word_counts_df = analysis.remove_words_from_df(word_counts_df, words_list)
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  'Word Removal complete! DataFrame header is below:' + ui_helpers.RESET)
            print(word_counts_df.head(5))
            input(ui_helpers.YELLOW + '\nPress Enter to continue.' + ui_helpers.RESET)

        # Applies 'Top N' Words per Document
        elif choice == '4':
            print(ui_helpers.RESET + 'The number entered below will keep only the "Top N" words ranked by word count per document in the DataFrame.')
            top_n = ui_helpers.get_top_n()
            
            # Applies the 'top n words' to the DF based on user preference
            word_counts_df = word_counts_df.apply(lambda row: row.nlargest(top_n), axis=1)
            word_counts_df = word_counts_df.fillna(0)  # Replace NaN with 0

            # User confirmation prompt
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  f'Only the top {top_n} words were kept. Press Enter to continue...')

        # Applies 'Bottom N' Words per Document
        elif choice == '5':
            print(ui_helpers.RESET + 'The number entered below will keep only the "Bottom N" words ranked by word count per document in the DataFrame.')
            bottom_n = ui_helpers.get_top_n()

            # Applies the 'bottom n words' to the DF based on user preference
            word_counts_df = word_counts_df.apply(lambda row: row.nsmallest(bottom_n), axis=1)
            word_counts_df = word_counts_df.fillna(0)

            # User confirmation prompt
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 
                  f'Only the bottom {bottom_n} words were kept. Press Enter to continue...')

        # Saves the DataFrame as a .csv
        elif choice == '6':
            default_name = 'Word_Counts_DataFrame'
            ui_helpers.move_to_reports_word_counts()
            ui_helpers.save_df_as_csv(word_counts_df, default_name)
            print(ui_helpers.RESET + 'DataFrame Output may be found in Reports > Word Counts subdirectory.')
            input(ui_helpers.YELLOW + 'Press Enter to continue.' + ui_helpers.RESET)

        # Saves the DataFrame as tab-delimited .txt
        elif choice == '7':
            default_name = 'Word_Counts_DataFrame'
            ui_helpers.move_to_reports_word_counts()
            ui_helpers.save_df_as_txt(word_counts_df, default_name)
            print(ui_helpers.RESET + 'DataFrame Output may be found in Reports > Word Counts subdirectory.')
            input(ui_helpers.YELLOW + 'Press Enter to continue.' + ui_helpers.RESET)
            
        # Saves the DataFrame as Bar Chart
        elif choice == '8':
            # Prompts user for Top N from DF
            print(ui_helpers.YELLOW + 'Specify number of words "per document" to display on the Bar Chart.' + 
                  ui_helpers.RESET)
            top_n = ui_helpers.get_top_n()

            # Creates the bar chart, saves to 'Visuals' subdirectory
            visuals.create_counts_barchart(word_counts_df, top_n)
            
        elif choice.lower() == 'd':
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 'DataFrame Transformation complete!' + 
                  ui_helpers.RESET + '\n\nYou may start a new query or go to the ' +
                  ui_helpers.CYAN + 'Visualizations' +
                  ui_helpers.RESET + ' menu for more options.')
            input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)

            return
