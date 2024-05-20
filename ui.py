# Import standard libraries
import os
import re
import pandas as pd

# Import local program scripts
import analysis
import ui_helpers
import sql_manager
import visuals

# Define global variables to prevent Visualizations menu errors
tfidf_df = None
final_metadata = None
word_counts_df = None

# Main Menu interface
def main_menu():
    """
    Displays the top-menu function options for the user and prompts the user for a selection.
    Depending on input, different top-level functions are called.

    Globals:
    tfidf_df - the DataFrame produced by the TF-IDF analysis function.
    final_metadata - a dictionary containing metadata for each document analyzed.
    word_coutns_df - the DataFrame produced by the Word Count Analysis functions.
    """

    global tfidf_df, final_metadata, word_counts_df

    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.CYAN + 'Main Menu\n' + ui_helpers.RESET)
    print('1. Word Count Analysis')
    print('2. SQLite Database Menu')
    print('3. TF-IDF Analysis')
    print('4. Visualizations')
    
    # Option 5 is inaccessible unless a DataFrame is loaded
    if tfidf_df is None and word_counts_df is None:
        print(ui_helpers.GRAY + '5. DataFrame Manipulation' + ui_helpers.RESET)
    else:
        print('5. DataFrame Manipulation')

    print('6. Manage Databases')
    print('7. View/Manage Reports')
    print('8. Filter Settings (view/edit commonwords.txt)')
    print('9. Help/Readme\n')
    print(ui_helpers.YELLOW + 'Q to quit/exit.\n' + ui_helpers.RESET)

    choice = input('Enter your selection: ')

    if choice == '1':
        option_1()
    elif choice == '2':
        option_2()
    elif choice == '3':
        option_3()
    elif choice == '4':
        option_4()
    elif choice == '5':
        if tfidf_df is None and word_counts_df is None:
            input(ui_helpers.RED + 'Must perform Word Count Analysis, TF-IDF Analysis, or load a .csv or .txt Report into a DataFrame first!' + ui_helpers.RESET)
            main_menu()
        else:
            option_5()
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
    elif choice == '':
        main_menu()
    else:
        main_menu()

# Option 1 - Text Analysis Menu
def option_1():
    """
    Allows users to select Word Counts using either local file or URL.
    """
    global tfidf_df, final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'Word Count Analysis Menu\n')
        print(ui_helpers.RESET + '1. Analyze Word Counts and Load into DataFrame') 
        print(ui_helpers.RESET + '2. Quick Display Using URL')
        print(ui_helpers.RESET + '3. Quick Display Using Local File(s)')
        print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
        
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_1_1()
        elif choice == '2':
            option_1_2()
        elif choice == '3':
            option_1_3()
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

    Globals:
    word_counts_df - a DataFrame created once all Word Counts (indexed to the file names) are complete
    """       
    
    global tfidf_df, final_metadata, word_counts_df

    # Page title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Analyze Word Counts and Load into DataFrame' + ui_helpers.RESET)
    print('\nThis tool performs a word count analysis on .txt file(s) and loads the results into a DataFrame for user manipulation. Once complete, this DataFrame can be utilized to save the analysis to a bar chart or .csv/.txt file. This tool filters any words specified in commonwords.txt, which is editable from the ' + ui_helpers.CYAN + 'Settings ' + ui_helpers.RESET + 'menu from the ' + ui_helpers.CYAN + 'Main Menu' + ui_helpers.RESET + '.')
    
    print('\nThis function is compatible with .txt files in UTF-8 format and the file(s) you wish to analyze must be placed in a directory named "Textfiles" located as a subdirectory in the main script\'s parent folder.\n\n- Type "all" to perform Quicklook Counts on all files\n- Press "enter" on number of rows will default to "5" rows')

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

        # Creates a nested dictionary {filename:{word:counts}} structure
        word_counts_all_docs[filename] = wordtally_dict
    
    # Convert nested dictionary to DataFrame
    word_counts_df = analysis.word_counts_to_df(word_counts_all_docs)
    
    # Data Manipulation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Manipulation options.' + ui_helpers.RESET)
    word_count_df_manipulation_menu(word_counts_df)
    option_1()

# Option 1_2 - Text File Word Count with URL
def option_1_2():
    """
    Allows user to input URL for a .txt file for word tallying. It then calls the appropriate analysis functions to complete the scan and display the results.

    Raises:
    ValueError if user inputs a non-integer
    """
    
    global tfidf_df, final_metadata, word_counts_df, wordtally_dict

    # Clears screen and provides title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Word Count Analysis Menu > ' + ui_helpers.CYAN + 'Quick Display Using URL\n' + ui_helpers.RESET)
    print('Enter or paste a URL link to a .txt file for word frequency analysis. This tool filters any words specified in commonwords.txt, which is editable from the ' + ui_helpers.CYAN + 'Settings ' + ui_helpers.RESET + 'menu from the ' + ui_helpers.CYAN + 'Main Menu' + ui_helpers.RESET + '.')
    print('\nThis function is compatible with .txt files in UTF-8 format.\n')
    
    # Prompts user for the URL
    user_url = input(ui_helpers.YELLOW + 'Please enter or paste the complete URL here ' + ui_helpers.RESET + '(Press Enter to return to ' + ui_helpers.CYAN + 'Analysis ' + ui_helpers.RESET + 'menu): ')

    # Returns to Analysis menu or checks for "http" prefix
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
    top_n = ui_helpers.get_top_n()

    # Opens the URL and returns a string
    filename, text_file_data = analysis.url_text_file_open(user_url)

    # Completes the Word Count
    wordtally_dict = analysis.tally_words(text_file_data, common_words)
    analysis.display_word_frequency(filename, wordtally_dict, top_n)
    
    # Returns to Analysis menu
    input('\nPress Enter to return to the ' + ui_helpers.CYAN + 'Analysis '  + ui_helpers.RESET + 'menu.')
    ui_helpers.clear_screen()
    option_1()

    return wordtally_dict

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
    print('\nSpecify a .txt file or set of text files to quickly display a word count analysis. This tool filters any words specified in commonwords.txt, which is editable from the ' + ui_helpers.CYAN + 'Settings ' + ui_helpers.RESET + 'menu from the ' + ui_helpers.CYAN + 'Main Menu' + ui_helpers.RESET + '.')
    
    print('\nThis function is compatible with .txt files in UTF-8 format and the file(s) you wish to analyze must be placed in a directory named "Textfiles" located as a subdirectory in the main script\'s parent folder.\n\n- Type "all" to perform Quicklook Counts on all files\n- Press "enter" on number of rows will default to "5" rows')

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
        analysis.display_word_frequency(filename, wordtally_dict, number_to_list)
    
    # Return Prompt
    input(ui_helpers.YELLOW + '\nPress Enter for to return...' + ui_helpers.RESET)
    option_1()

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
        print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
        
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_1()
        elif choice == '2':
            option_2_2()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 2_1 - Complete a word count analysis and export to SQL DB
def option_2_1():
    """
    Completes a word frequency analysis and exports results to a SQL database. Filters any words from commonwords.txt from the analysis. Users may choose a single file, multiple files, or all files located in the Textfiles directory.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Header and user instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > ' + ui_helpers.CYAN + 'Export Word Count Analysis to SQLite Database' + ui_helpers.RESET)
    print('\nThis will tally all words in a .txt file, filtering any that are defined in the commonwords.txt file, and export to a user-defined SQL database.\n\nYou may make multiple selections by entering the numbers corresponding to the files listed below.\n\nEnter "all" to analyze all files listed.')

    # Lists Textfiles contents and requests user file selection
    files_to_process = ui_helpers.list_select_textfile(option_2)

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
        doc_title, author, year, genre = ui_helpers.input_file_metadata(filename)

        # Calls SQL functions
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
        print(ui_helpers.YELLOW + '\n\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
        
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_2_2_1()
        elif choice == '2':
            option_2_2_2()
        elif choice == '3':
            option_2_2_3()
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

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > SQLite Database Menu > SQLite Database Queries > ' + ui_helpers.CYAN + 'Summarize SQLite Database' + ui_helpers.RESET)
    print('\nDisplay summary information for a database.')
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

# Option 2_2_2_1 - Word Counts Over Time (All Authors)
def option_2_2_2_1():
    """
    Provides users the ability to specify a database and appropriate options for building a Word Count Over Time report using all authors in the database. Users may then save the report to a .csv file.

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
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

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
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

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
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

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
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

    Raises:
    IndexError - if user enters a number not on the file index or an invalid year.
    ValueError - if non-number is entered.
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
    print(ui_helpers.YELLOW + 'Enter the number of words to return per Author.\n' + ui_helpers.RESET)
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
    print(ui_helpers.YELLOW + 'Enter the number of words to return per Genre.\n' + ui_helpers.RESET)
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
    print(ui_helpers.YELLOW + 'Enter the number of words to return per Document.\n' + ui_helpers.RESET)
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
    print(ui_helpers.RESET + '1. Perform TF-IDF Analysis on Multiple Text Files')
    print(ui_helpers.RESET + '2. Query SQL Database for TF-IDF Analysis')
    print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
    
    # Handles user choice
    choice = input(ui_helpers.YELLOW + '\nEnter your selection: ' + ui_helpers.RESET)

    if choice == '1':
        option_3_1()
    elif choice == '2':
        option_3_2()
    else:
        ui_helpers.clear_screen()
        main_menu()

# Option 3_1 - TF-IDF Analysis on Multiple Text Files
def option_3_1():
    """
    Allows user to select multiple files from the Textfiles subdirectory to perform a TF-IDF analysis. Users may input metadata for each file manually. Takes user to the TF-IDF Manipulation Menu after analysis is complete.

    Globals:
    tfidf_df - the DataFrame produced by the TF-IDF analysis function.
    final_metadata - a dictionary containing metadata for each document analyzed.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > TF-IDF Analysis Menu > ' + ui_helpers.CYAN + 'TF-IDF Analysis of Multiple Text files' + ui_helpers.RESET)
    print('\nPerforms a Term Frequency-Inverse Document Frequency (TF-IDF) analysis on multiple text files. The TF-IDF is a statistical analysis tool which accounts for the significance of a given word across a range of documents.\n')
    print('Very common words which do not add much wortwhile data are assigned a low value while more distinct and meaningful words are assigned a high value. Generally, these words can be thought of as closely related to the core meaning of the text document(s) in which they are found.')
    print('\nThe formula for TF-IDF is:\nTF-IDF = (Number of times a word appears in a document) / (Number of documents containing the word)\n\nPress Enter to return.')
    
    # Lists files in Textfiles and prompts for user input
    files_to_process = ui_helpers.list_select_textfile(option_3)

    # Performs analysis
    tfidf_df, final_metadata = analysis.text_tf_idf_analysis(files_to_process, option_3_1)

    # Success confirmation and header print
    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TF-IDF Analysis of Multiple Text files' + ui_helpers.RESET)
    print(ui_helpers.YELLOW + '\nOperation success!\n\n' + 
          ui_helpers.RESET + 'Pandas DataFrame Header:') 
    print(tfidf_df.head())

    # Data Manipulation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Manipulation options.' + ui_helpers.RESET)
    tf_idf_df_manipulation_menu(tfidf_df)
    option_3()

# Option 3_2 - Query SQL Databse for TF-IDF Analysis
def option_3_2():
    """
    Allows user to select SQLite database from which to perform a TF-IDF analysis. Takes user to the TF-IDF Manipulation Menu after analysis is complete.

    Globals:
    tfidf_df - the DataFrame produced by the TF-IDF analysis function.
    final_metadata - a dictionary containing metadata for each document analyzed.
    """
    global tfidf_df, final_metadata, word_counts_df

    # Screen title and menu tree
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > TF-IDF Analysis Menu > ' + ui_helpers.CYAN + 'Query SQL Database for TF-IDF Analysis' + ui_helpers.RESET)
    print('\nPerforms a Term Frequency-Inverse Document Frequency (TF-IDF) analysis on a SQL database. The TF-IDF is a statistical analysis tool which accounts for the significance of a given word across a range of documents.\n')
    print('Very common words which do not add much wortwhile data are assigned a low value while more distinct and meaningful words are assigned a high value. Generally, these words can be thought of as closely related to the core meaning of the text document(s) in which they are found.')
    print('\nThe formula for TF-IDF is:\nTF-IDF = (Number of times a word appears in a document) / (Number of documents containing the word)\n\nPress Enter to return.')

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

    # Data Manipulation prompt
    input(ui_helpers.YELLOW + '\nPress Enter for DataFrame Manipulation options.' + ui_helpers.RESET)
    tf_idf_df_manipulation_menu(tfidf_df)
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
    print(ui_helpers.RESET + ' 1. Save Word Counts as Bar Chart')
    print(ui_helpers.RESET + ' 2. Save TF-IDF Analysis as Bar Chart')
    print(ui_helpers.RESET + ' 3. Initialize Interactive Dashboard Bar Chart (TF-IDF)')   
    print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.')
    choice = input(ui_helpers.RESET + '\nEnter your selection: ')
    
    if choice == '1':
        # Ensures a Word Count DataFrame exists
        if word_counts_df is None:
            prompt = input(ui_helpers.RED + 'Must perform Word Count Analysis first!' + ui_helpers.RESET + ' Go to Word Count Analysis Menu now? ("Y" for yes.) ')
            if prompt.lower() == 'y':
                option_1_1()
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
        if tfidf_df is None:
            prompt = input(ui_helpers.RED + 'Must perform TF-IDF Analysis first!' + ui_helpers.RESET + ' Go to TF-IDF Analysis Menu now? ("Y" for yes.) ')
            if prompt.lower() == 'y':
                option_3()
            else:
                option_4()
        else:
            option_4_3()

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
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Visualizations Menu > ' + ui_helpers.CYAN +  'Save Word Counts as Bar Chart')
    print(ui_helpers.RESET + ' This will save the Word Counts DataFrame to a Bar Chart in the "Visuals" subdirectory. You will need to specify how many of the "top words by count" to display.\n')

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
    print(ui_helpers.RESET + 'Main Menu > Visualizations Menu > ' + ui_helpers.CYAN +  'Initialize TF-IDF Dashboard' + ui_helpers.RESET)
    print('\nUses the DataFrame produced following TF-IDF analysis to initialize an interactive dashboard, allowing users to select documents to view a specified number of words with top TF-IDF scores per document.\n')
    print('The dashboard may be viewed locally at: ' + 
        ui_helpers.CYAN + 'http://127.0.0.1:8050/')
    
    top_n = ui_helpers.get_top_n()
    
    # Initializes Dashboard
    tfidf_df, final_metadata = visuals.create_tf_idf_dash(tfidf_df, final_metadata, top_n)
    
    input('Press Enter to continue...')
    option_4()

# Option 5 - DataFrame Manipulation
def option_5():
    """
    Allows user to access the DataFrame Manipulation Menu if a DataFrame is loaded.

    Globals:
    word_counts_df - the DataFrame that is loaded after a Word Counts Analysis is completed or a Report is loaded
    tfidf_df - the DataFrame that is loaded after a TF-IDF Analysis is completed or a Report is loaded
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen Header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN + 'DataFrame Manipulation\n')
    if word_counts_df is None:
        print(ui_helpers.GRAY + ' 1. Word Count Analysis DataFrame' + ui_helpers.RESET)
    else:
        print(ui_helpers.RESET + ' 1. Word Count Analysis DataFrame')

    if tfidf_df is None:
        print(ui_helpers.GRAY + ' 2. TF-IDF Analysis DataFrame')
    else:
        print(ui_helpers.RESET + ' 2. TF-IDF Analysis DataFrame')

    print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.')
    choice = input(ui_helpers.RESET + '\nEnter your selection: ')
    
    if choice == '1':
        # Ensures a Word Count DataFrame exists
        if word_counts_df is None:
            print(ui_helpers.RED + 'Must perform a new Word Count Analysis or load a Word Count Report first.\n' + ui_helpers.RESET)
            print(ui_helpers.YELLOW + 'Choose an option:' + ui_helpers.RESET)
            print('\n 1. Perform New Word Count Analysis')
            print(' 2. Load a Word Count Report')
            print('\n Press Enter to cancel')
            prompt = input(ui_helpers.YELLOW + '\nEnter selection: ' + ui_helpers.RESET)
            
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
            word_count_df_manipulation_menu(word_counts_df)
            main_menu()

    elif choice == '2':
        # Ensures a TF-IDF DataFrame exists
        if tfidf_df is None:
            print(ui_helpers.RED + 'Must perform a new TF-IDF Analysis or load a .TF-IDF Report first.\n' + ui_helpers.RESET)
            print(ui_helpers.YELLOW + 'Choose an option:' + ui_helpers.RESET)
            print('\n 1. Perform New TF-IDF Analysis')
            print(' 2. Load TF-IDF Report')
            print('\nPress Enter to cancel')
            prompt = input(ui_helpers.YELLOW + '\nEnter selection: ' + ui_helpers.RESET)
            
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
            tf_idf_df_manipulation_menu(tfidf_df)
            main_menu()

    else:
        ui_helpers.clear_screen()
        main_menu()

# Option 6 - Database Management
def option_6():
    """
    Provides user options for managing Databases.
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen header and instructions
    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > ' + ui_helpers.CYAN +  'Manage Databases\n' + ui_helpers.RESET)
        print('1. Delete Database(s)')
        print(ui_helpers.YELLOW + '\n\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
        
        # Handles user choice
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

    global tfidf_df, final_metadata, word_counts_df

    # Screen header and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Manage Databases > ' + ui_helpers.CYAN + 'Delete Database(s)' + ui_helpers.RESET)
    print('\nYou may select a database to Delete it.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Databases directory:\n' + ui_helpers.RESET)

    # Displays contents of Databases, prompts user for selection
    database_name = ui_helpers.list_select_database(option_6)
            
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

# Option 7 - Reports Menu
def option_7():
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
        print(ui_helpers.YELLOW + '\nPress Enter to return to Main Menu.' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_7_1()
        elif choice == '2':
            option_7_2()
        elif choice == '3':
            option_7_3()
        elif choice == '4':
            option_7_4()
        else:
            ui_helpers.clear_screen()
            main_menu()

# Option 7_1 - Word Count Reports
def option_7_1():
    """
    Displays contents of Reports/Word Counts subdirectory. Enables user to view list of .csv and .txt files (reports) they can view and load into a DF for further manipulation.

    Globals:
    word_counts_df - used for setting the report as the word_counts_df after loading
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'Word Count Reports' + ui_helpers.RESET)
    print('\nYou may select a report to view, load, and manipulate its DataFrame in Pandas.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Reports, prompts user for selection
    report_name = ui_helpers.list_select_report(option_7, 'wordcounts')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    choice = input(ui_helpers.YELLOW + '\nDataFrame loaded!' + ui_helpers.RESET + ' Enter "Y" to load the report as a DataFrame and enter the DataFrame Manipulation Menu, or Enter to skip: ')
    while True:

        if choice.lower() == 'y':
            word_counts_df = df
            word_count_df_manipulation_menu(word_counts_df)
            main_menu()

        else:
            option_7_1()
            return
        
# Option 7_2 - SQL Query Reports
def option_7_2():
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
    report_name = ui_helpers.list_select_report(option_7, 'sqlqueries')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    input(ui_helpers.YELLOW + '\nReport loaded!' + ui_helpers.RESET + ' Press Enter to continue...')
    option_7_2()

# Option 7_3 - TF-IDF Reports
def option_7_3():
    """
    Displays contents of Reports/TF-IDF subdirectory. Enables user to view list of .csv and .txt files (reports) they can view and load into a DF for further manipulation.

    Globals:
    tfidf_df - used for setting the report as the tfidf_df after loading
    """

    global tfidf_df, final_metadata, word_counts_df

    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'TF-IDF Reports' + ui_helpers.RESET)
    print('\nYou may select a report to view, load, and manipulate its DataFrame in Pandas.\n\nPress Enter to return.')
    print(ui_helpers.YELLOW + '\nAvailable files in Reports directory:\n' + ui_helpers.RESET)
    
    # Displays contents of Reports, prompts user for selection
    report_name = ui_helpers.list_select_report(option_7, 'tfidf')

    # Reads Report (.csv) as PD DataFrame, prints the head    
    df = ui_helpers.read_txt_or_csv(report_name)
    print(df.head())
        
    # Prompt to set DataFrame as word_counts_df, tfidf_df, or return to menu
    choice = input(ui_helpers.YELLOW + '\nDataFrame loaded!' + ui_helpers.RESET + ' Enter "Y" to load the report as a DataFrame and enter the DataFrame Manipulation Menu, or Enter to skip: ')
    while True:

        if choice.lower() == 'y':
            tfidf_df = df
            tf_idf_df_manipulation_menu(tfidf_df)
            main_menu()

        else:
            option_7_3()
            return

# Option 7_4 - Delete Report(s)
def option_7_4():
    """
    Displays .csv files located in the Reports subdirectory and allows users to input an index number corresponding to reports for deletion.

    Raises:
    IndexError - if user specifies an index value out of range.
    ValueError - if user enters a non-number.
    """

    global tfidf_df, final_metadata, word_counts_df
    
    # Screen title and instructions
    ui_helpers.clear_screen()
    ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
    print(ui_helpers.RESET + 'Main Menu > Reports Menu > ' + ui_helpers.CYAN + 'Delete CSV Reports' + ui_helpers.RESET)
    print(ui_helpers.RESET + '\nPlease select a report type to view available reports. You may then select a report for deletion.\nPress Enter to return without viewing/deleting.')

    # Prompts user for report type selection
    print(ui_helpers.YELLOW + '\nTypes of Reports:' + ui_helpers.RESET)
    print(ui_helpers.RESET + '1. Word Counts Reports')
    print(ui_helpers.RESET + '2. SQL Query Reports')
    print(ui_helpers.RESET + '3. TF-IDF Reports')
    
    choice = input(ui_helpers.YELLOW + '\nEnter your selection: ' + ui_helpers.RESET)

    # Defines report subdirectory based on user choice

    if choice == '1':
        report_subdir = 'wordcounts'
    elif choice == '2':
        report_subdir = 'sqlqueries'
    elif choice == '3':
        report_subdir = 'tfidf'
    else:
        option_7()

    # Displays 
    print(ui_helpers.YELLOW + '\nAvailable reports:\n' + ui_helpers.RESET)
    report_name = ui_helpers.list_select_report(option_7, report_subdir)

    # Delete confirmation prompt
    print(ui_helpers.RED + 'Really delete ' + 
          ui_helpers.RESET + f'{report_name}' + 
          ui_helpers.RED + '?' + ui_helpers.RESET)
    delete_confirmation = input('Enter "C" to cancel or press Enter to continue with deletion.')
    
    # Cancels deletion if user enters "c"
    if delete_confirmation.lower() == 'c':
        input(ui_helpers.RESET + f'{report_name} ' + 
              ui_helpers.YELLOW + 'NOT deleted!' + ui_helpers.RESET)
        option_7_4()
    
    # Deletes the Report
    else:
        os.remove(report_name)
        input(ui_helpers.RESET + f'{report_name} ' + 
              ui_helpers.YELLOW + 'deleted!' + ui_helpers.RESET)
        option_7_4()
    
    # User return prompt
    input(ui_helpers.YELLOW + ' Press Enter to continue.' + ui_helpers.RESET)
    option_7_4()

# Option 8 - Word count filter (commonwords.txt) settings mneu
def option_8():
    """
    Displays the filter settings menu with multiple configuration options for managing the commonwords.txt file.
    Users can view, add, remove, ui_helpers.RESET, or clear the contents of commonwords.txt through a series of sub-menus.
    The working directory is adjusted if necessary to ensure file operations occur in the correct directory.
    
    Raises:
    Exception: catches and logs unexpected exceptions that may occur during execution.
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
    print(' ')

    choice = input('Select option or press Enter to return to Main Menu.')

    if choice == '1':
        option_8_1()
    elif choice == '2':
        option_8_2()
    elif choice == '3':
        option_8_3()
    elif choice == '4':
        conf_prompt = input(ui_helpers.YELLOW + 'Really reset the filter to default list? (Enter "Y" for "Yes"): ' + ui_helpers.RESET)
        if conf_prompt.lower() == 'y':
            analysis.reset_commonwords_txt() # Resets commonwords.txt to default
            print(ui_helpers.YELLOW + '\nAttention! ' + ui_helpers.RESET + 'The contents of commonwords.txt has been reset to the default list! These are the only words which will be excluded from future text analyses. You may return to this menu to customize the list appropriately.')
            input('\nPress Enter to continue...')
            option_8()
        else:
            option_8()
    
    elif choice == '5':
        conf_prompt = input(ui_helpers.YELLOW + 'Really delete all words from filter? (Enter "Y" for "Yes"): ' + ui_helpers.RESET)
        if conf_prompt.lower() == 'y':
            analysis.delete_commonwords_txt_contents() # Deletes commonwords.txt contents
            print(ui_helpers.YELLOW + '\nAttention! ' + ui_helpers.RESET + 'The contents of commonwords.txt has been cleared! All words will now be counted when analyzing text documents. You may always reset the filter to default or create your own words list using this menu.')
            input('\nPress Enter to continue...')
            option_8()
        else:
            option_8()

    else:
        ui_helpers.clear_screen()
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
    option_8()

# Option 8_2 - Add words to commonwords.txt filter
def option_8_2():
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
        option_8_2()
    else:
        option_8()

# Option 8_3 - Deletes words from commonwords.txt filter
def option_8_3():
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
        option_8_3()
    else:
        option_8()

# Option 9 - Provides instructions, notes, and help for users
def option_9():
    """
    Provides in-program instructions, future plans, user notes, and contact information for the program.
    """

    ui_helpers.clear_screen()
    print(ui_helpers.CYAN + 'TextCrawl v.60 Help/Readme\n' + ui_helpers.RESET)
    print('''To use TextCrawl, ensure that you have placed at least one .txt file in a subdirectory called "Textfiles" and/or have a direct URL link to a .txt file. To get the most out of the program by using the Term Frequency - Inverse Document Frequency (TF-IDF) Analysis functions, please ensure you have a minmum of two .txt files.\n''')
    print('''TF-IDF is a statistical analysis tool which totals the number of times a given word appears in a text document and then compares this word count in a single document to the corresponding word counts in the other documents in the set. By inverting the weighting of each given word based on the number of instances it is used by other documents in the set, the user can quickly analyze which words are most "important" or most "unique" in a given document.''')
    print('''\nUsers may maniuplate the TF-IDF DataFrame to filter based on threshold, Top N scores per document, or via a word search. Additionally, users may choose to output the DataFrame results to a .txt or .csv report, or initiate an interactive bar chart dashboard!''')
    print('''\nBefore analyzing a .txt file for addition to a database, I recommend viewing the commonwords.txt filter (Option 8 on Main Menu) to ensure the desired words (if any) are excluded from the word frequency analysis.''')
    print('''\n New features in v.60:
    - Expanded DataFrame status bar to include Word Count Analysis DataFrame. This status bar is now a persistent header.
    - Added menu tree status below DataFrame status bar, enhancing user awareness of menu tree location at all times.
    - Added Word Count DataFrame Manipulation Menu.
    - Added more options to both DataFrame Manipulation Menus, including filtering for "bottom N" words and specific word filtering.
    - Reports are better organized and may now be used to load Word Count Analysis or TF-IDF DataFrames.
    - Added Bar Charts for Word Count and TF-IDF Analysis DataFrames
    - Word Count Analysis may be loaded directly into a DataFrame without exporting to SQLite.\n
    - Numerous bugfixes and performance improvements:
        - Fixed SQL Database Build error which resulted in "Year" and "Genre" confusion during input.
        - Improved error handling when users make selections out of range.
        - Numerous modules have been split, improving code management and efficiency.''')
    print('''\nKnown limitations:
    - TextCrawl has only been tested using English-language .txt files. Other languages may not work properly.
    - Some menu or sub-menu options may break if not used properly. This will be fixed in future revisions.
    - Attempting to generate a .csv report with a very large DataFrame may result in truncation based on the program opening the file later. If outputting a TF-IDF DataFrame, it is recommended to apply a threshold or other filter to reduce the size of the dataset when using large documents and (consequently) DataFrames.
    - The codebase has not been fully optimized to remove redundancy. As more functions are build, tested, and incorporated, future versions of TextCrawl will feature improved modularity, readability, and error handling.      
    ''')

    print('''I'd love to hear from you! Please send any feedback or questions to me at: ''' + ui_helpers.CYAN + 'c.fowler00@yahoo.com' + ui_helpers.RESET)

    input(ui_helpers.YELLOW + '\nPress Enter to return to the Main Menu.' + ui_helpers.RESET)
    ui_helpers.clear_screen()
    main_menu()

# TF-IDF DataFrame Manipulation menu
def tf_idf_df_manipulation_menu(tfidf_df):
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

    Globals:
    final_metadata - a dictionary containing metadata for each document analyzed.
    """
    global final_metadata, word_counts_df

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > DataFrame Manipulation > ' + ui_helpers.CYAN + 'Manipulate TF-IDF DataFrame')
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
        print(ui_helpers.YELLOW + '\nEnter "D" when done to return to menu')

        choice = input(ui_helpers.YELLOW + '\nEnter your selection: ' + ui_helpers.RESET)
        
        # Applies threshold to TF-IDF values
        if choice == '1':

            # Calculate and display the min and max TF-IDF values
            min_value, max_value = analysis.get_min_max(tfidf_df)
            print(ui_helpers.YELLOW + '\nThe TF-IDF range for this DataFrame is:' + 
                  ui_helpers.RESET + f'{min_value:.2f}' + 
                  ui_helpers.YELLOW + ' to ' + 
                  ui_helpers.RESET + f'{max_value:.2f}')

            # Get user threshold and convert to float
            threshold = input(ui_helpers.YELLOW + '\nEnter desired threshold: ' + ui_helpers.RESET)
            
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
            top_n = input(ui_helpers.YELLOW + 'Enter how many "top words" to keep in the DataFrame: ' + ui_helpers.RESET)
            
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
            print(ui_helpers.YELLOW + 'DataFrame Manipulation complete!' + 
                  ui_helpers.RESET + '\n\nYou may start a new query or go to the ' +
                  ui_helpers.CYAN + 'Visualizations' +
                  ui_helpers.RESET + ' menu for more options.')
            input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)

            return

# Word Counts DataFrame Manipulation menu
def word_count_df_manipulation_menu(word_counts_df):
    """
    Once a Word Count DataFrame is created, this can be utilized to allow the user to perform a variety of actions on the DataFrame:
        1. Apply a minimum count number to be retained
        2. Search for and keep specific words in the DataFrame
        3. Search for and remove specific words from the DataFrame
        4. Keep only the top user-specified number of words per document
        5. Output to a .csv file
        6. Output to a .txt file
        7. Initialize a Dashboard for visualization using Dash


    The menu is continuously displayed until the user inputs 'd' for Done.
    
    Parameters:
    word_counts_df - the DataFrame produced by Word Counts functions
    """
    global tfidf_df, final_metadata

    while True:
        ui_helpers.clear_screen()
        ui_helpers.header(tfidf_df, final_metadata, word_counts_df)
        print(ui_helpers.RESET + 'Main Menu > DataFrame Manipulation > ' + ui_helpers.CYAN + 'Manipulate Word Counts DataFrame')
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
        print(ui_helpers.YELLOW + '\nEnter "D" when done to return to menu')

        choice = input(ui_helpers.YELLOW + '\nEnter your selection: ' + ui_helpers.RESET)
        
        # Applies threshold to Word Count values
        if choice == '1':

            # Calculate and display the min and max Word Count values
            min_value, max_value = analysis.get_min_max(word_counts_df)
            print(ui_helpers.YELLOW + '\nThe "count per word" range for this DataFrame is:' + 
                  ui_helpers.RESET + f'{min_value:.2f}' + 
                  ui_helpers.YELLOW + ' to ' + 
                  ui_helpers.RESET + f'{max_value:.2f}')

            # Get user threshold and convert to float
            threshold = input(ui_helpers.YELLOW + '\nEnter desired threshold: ' + ui_helpers.RESET)
            
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
            print(ui_helpers.YELLOW + 'DataFrame Manipulation complete!' + 
                  ui_helpers.RESET + '\n\nYou may start a new query or go to the ' +
                  ui_helpers.CYAN + 'Visualizations' +
                  ui_helpers.RESET + ' menu for more options.')
            input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)

            return
