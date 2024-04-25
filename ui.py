# Import standard libraries
import os

# Import local program scripts
import analysis
import ui_helpers

# Main Menu interface
def main_menu():

    """
    Displays the top-menu function options for the user and prompts the user for a selection.
    Depending on input, different top-level functions are called.
    """
    ui_helpers.clear_screen()

    while True:
        print(ui_helpers.CYAN + 'TextCrawl v.30 Main Menu\n' + ui_helpers.RESET)
        print('1. Scan .txt file using a local file or from the Web using a URL.')
        # print('2. NOT YET USED')
        print('..')
        print('8. Filter Settings (view or edit commonwords.txt)')
        print('9. Help/Readme\n')
        print(ui_helpers.YELLOW + 'Q to quit/exit.\n' + ui_helpers.RESET)

        choice = input('Enter your selection: ')

        if choice == '1':
            option_1()
        # elif choice == '2': ## Will be used again as more features are implemented
        #     option_2()
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
    Provides user options for scanning a text file from a local file or via URL.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Text Document Word Frequency Analysis\n' + ui_helpers.RESET + '''
1. Scan a .txt file found in the Textfiles subdirectory.
2. Scan a .txt file found on the web using a direct URL.'''
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

    print('\nType "list" at the prompt to list all files in the Textfiles directory.')
    
    # Requests user-specified file to scan
    user_file = input(ui_helpers.YELLOW + '\nEnter file name ' + ui_helpers.RESET + '(Press Enter to return): ')

    # Returns a list of all files located in 'Textfiles' subdirectory
    if user_file.lower() == 'list':
        cur_dir = str(os.getcwd())
        if cur_dir[-9:] != 'Textfiles':
            os.chdir(cur_dir + '\\Textfiles')

        # Clears screen, re-displays title, shows directory content heading
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Local Text File Word Count' + ui_helpers.RESET)
        print('\nThe contents of the Textfiles subdirectory are:\n')
        
        # Displays index of 'Textfiles' directory and prompts user to select a number
        for index, filename in enumerate(os.listdir(), start=1):
            print(f'{index}' + ') ' f'{filename}')
        user_file = input(ui_helpers.YELLOW + '\nEnter file name: ' + ui_helpers.RESET)

        # Manages user selection if they enter the Index number for a file
        try:
            all_files = os.listdir()
            user_file_index = int(user_file)
            user_file = all_files[user_file_index - 1]
        except ValueError:
            print('')

    # Accounts for common user input mistakes
    if len(user_file) < 1:
        option_1()
    if user_file[-4:] != '.txt':
        user_file += '.txt'

    # Loads commonwords.txt as a filter
    common_words = analysis.load_common_words()

    
    # Loads the user .txt file
    text_file_data = analysis.load_textfile(user_file)
    print(ui_helpers.YELLOW + 'The file ' + ui_helpers.RESET + f'{user_file}' + ui_helpers.YELLOW + ' was opened successfully!\n' + ui_helpers.RESET)

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

    # Perform analysis
    while True:
        # Analysis confirmation sentence
        ui_helpers.analysis_confirmation(user_file)

        # Calls the analysis functions
        wordtally_results = analysis.tally_words(text_file_data, common_words)
        analysis.display_word_frequency(wordtally_results, number_to_list)
        break

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

# Option 2 - Data Transformation Menu
def option_2():
    """
    Provides user options for transforming data into multiple formats and saving to disk.
    """
    while True:
        ui_helpers.clear_screen()
        print(ui_helpers.CYAN + 'Text Document Common Words Count\n' + ui_helpers.RESET + '''
1. Scan a .txt file found in the Textfiles subdirectory.
2. Scan a .txt file found on the web using a direct URL.'''
+ ui_helpers.YELLOW + '''\n\nPress Enter to return to Main Menu.''' + ui_helpers.RESET)
        choice = input('\nEnter your selection: ')
        if choice == '1':
            option_1_1()
        elif choice == '2':
            option_1_2()
        else:
            ui_helpers.clear_screen()
            main_menu()

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
    print(ui_helpers.CYAN + 'TextCrawl v.30 Help/Readme\n' + ui_helpers.RESET)
    print('''To use TextCrawl, ensure that you have placed at least one .txt file in a subdirectory called "Textfiles" and/or have a direct URL link to a .txt file. From there you can select how many of the most common words utilized in the .txt file.\n''')
    print('''If this is your first time using the program, I recommend viewing the commonwords.txt file by navigating to the Filter Settings menu. The words contained in this file will be filtered from TextCrawl's tally. From Settings, you may add or remove words from commonwords.txt or you may reset it to the default.''')
    print('''\nTextCrawl is a simple program that is designed to count the number of non-common words (i.e., "if, and, the, etc.") and provide a total count for how many instances of each word in a .txt file appear. This began as a relatively simple project to help teach myself how to use Python to:\n
    - Handle files (read, write, delete, append, etc.)
    - Access URLs
    - Provide a simple, but effective, user interface
    - Write error handling logic
    - Implement logic to allow a degree of user customization (i.e., which files to scan, how many words to print, etc.)\n''')
    print('''Later, I hope to implement SQL database support and the ability for users to extract interesting data to the database. Additionally, I want TextCrawl to enable users to gain insights into trends across multiple text files. Stay tuned for future versions and thanks for using TextCrawl! Finally, I wish to add more user options to the word tally function itself, allowing users to order the list in ascending order as well, or to save the output to a .txt or other file. Perhaps the program will even offer full GUI support!\n''')

    print('''I'd love to hear from you! Please send any feedback or questions to me at: ''' + ui_helpers.CYAN + 'c.fowler00@yahoo.com' + ui_helpers.RESET)

    input(ui_helpers.YELLOW + '\nPress Enter to return to the Main Menu.' + ui_helpers.RESET)
    ui_helpers.clear_screen()
    main_menu()
