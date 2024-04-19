import os
import string
import re

"""
TextCrawl v.20 analyzes text data to identify and display the frequency of words. 
It allows users to input text data from either local files or via URLs. Results can be
displayed either as total word counts or filtered to show only the most common words.

Usage:
Run the script and follow the on-screen prompts to choose data sources and output preferences.

Features:
    - Word frequency analysis from files and URLs.
    - Interactive user interface for easy navigation.
    - Robust error handling for a smooth user experience.

Author: Christopher Fowler (c.fowler00@yahoo.com)
Date: 2024-04-19
"""

# For coloring of text inside the menu interface
RED = '\033[31m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

# Main program function
def main():
    main_menu()

# Main Menu interface
def main_menu():

    """
    Displays the top-menu function options for the user and prompts the user for a selection.
    Depending on input, different top-level functions are called.
    """
    clear_screen()

    while True:
        print(CYAN + '\nTextCrawl v.20 Main Menu\n' + RESET)
        print('1. Scan .txt file for the most used words.')
        print('2. Retrieve a .txt file from the Web using a URL.')
        print('..')
        print('8. Settings')
        print('9. Help/Readme\n')
        print(YELLOW + 'Q to quit/exit.\n' + RESET)

        choice = input('Enter your selection: ')

        if choice == '1':
            option_1()
        elif choice == '2':
            option_2()
        elif choice == '8':
            option_8()
        elif choice == '9':
            option_9()
        elif choice.lower() == 'q':
            clear_screen()
            print(YELLOW + 'Thanks for using TextCrawl! Exiting now...' + RESET)
            quit()
        else:
            clear_screen()
            print(RED + 'Invalid menu choice! Please try again.' + RESET)

# Option 1 - Requests user input for text file to scan, then calls tally_words function
def option_1():

    """
    Prompt the user to input a text file name for word frequency analysis. Depending on the user input,
    the function either processes the file to display the frequency of the most common words or returns 
    to the main menu if the user decides to cancel the operation.

    The function calls `load_textfile` to load the text file, `load_create_common_words` to load a list
    of common words for filtering, and `tally_words` to perform the analysis. If the user does not specify
    a number of words, all words are processed; otherwise, only the top N words as specified by the user
    are processed. The function handles errors related to file not found, invalid numeric input, and
    other unexpected errors.

    Raises:
    FileNotFoundError: If the specified text file does not exist.
    ValueError: If the user inputs an invalid number (not convertible to int) when asked for the number
                of words to process.
    Exception: Catches and logs any other unexpected exceptions that may occur during execution.
    """

    try:
        clear_screen()
        common_words = load_create_common_words()

        user_file = load_textfile(input('What text file would you like to scan today? (Enter "C" to cancel) '))
        
        if user_file.lower() == 'c':
            main_menu()

        top_words_count = input(YELLOW + '\nHow many of the most commonly used words would you like TextCrawl to display?' + RESET + ' (Press Enter to return all words.) ')

        if top_words_count == '':
            tally_words(user_file, top_words_count, common_words)          

        else:
            top_words_count = int(top_words_count)
            tally_words(user_file, top_words_count, common_words)
    
        return_to_main()

    except FileNotFoundError as e:
        clear_screen()
        print(RED + f'{e}' + RESET)
        return_to_main()

    except ValueError:
        clear_screen()
        print(RED + 'Please ensure you enter only a number for the number of words to count.' + RESET)

    except Exception as e:
        clear_screen()
        print(RED + f'TextCrawl encountered an unexpected error. Error: {e} ' + RESET)
        return_to_main()

# Option 2 - Using a URL to retrieve a .txt file
def option_2():
    """
    Prompts the user for a URL pointing to a .txt file and attempts to download and analyze the text. The function
    fetches the file, loads common words for filtering, and prompts the user for the number of most commonly used 
    words to display. It then normalizes and tallies the words, excluding those found in commonwords.txt, and 
    displays the results.

    Raises:
    Exception: catches and logs unexpected exceptions that may occur during execution.

    """

    import requests
    clear_screen()

    user_url = input('Please enter the complete URL here, ensuring the address points to a .txt file (Enter "C" to cancel): ')

    try:
        if user_url.lower() == 'c':
            main_menu() 

        response = requests.get(user_url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            print('\nSuccessfully accessed .txt file!')
            common_list = load_create_common_words()
            print('Commonwords.txt file loaded.')

            number_to_list = int(input('\nHow many of the most commonly-used words would you like TextCrawl to display? '))
            
            wordtally = {}
            text_data = response.text
            text_lines = text_data.splitlines()
            translator = str.maketrans('', '', string.punctuation + '“”‘’')

            for line in text_lines:
                data_words = line.strip().lower().split()
                for word in data_words:
                    clean_word = word.translate(translator)
                    if clean_word in common_list or len(clean_word) < 2:
                        continue
                    if clean_word in wordtally:
                        wordtally[clean_word] += 1
                    else:
                        wordtally[clean_word] = 1

            # Converts the 'wordtally' dictionary to a list, then sorts it by 'Top 25' common words and returns list.
            sorted_list = sorted(wordtally.items(), key=lambda item:item[1], reverse=True)
            top_count_words = sorted_list[:number_to_list]

            # Prints the 'Top N Words' list
            print(CYAN + '\nRank ) Word - Count','\n' + '_'*19 + '\n' + RESET)
            for index, (word, count) in enumerate(top_count_words, start=1):
                print(f'{index}' + ') ' f'{word[0].upper()}{word[1:]} - {count}')

        else:
            print(RED + 'Failed to retrieve data', response.status_code + RESET)
    
    except requests.exceptions.RequestException as e:
        print(RED + 'TextCrawl encountered an error retrieving the URL!' + RESET )

    return_to_main()

# Option 8 - Settings sub-menu
def option_8():
    """
    Displays the settings menu with multiple configuration options for managing the commonwords.txt file.
    Users can view, add, remove, reset, or clear the contents of commonwords.txt through a series of sub-menus.
    The working directory is adjusted if necessary to ensure file operations occur in the correct directory.
    
    Raises:
    Exception: catches and logs unexpected exceptions that may occur during execution.

    """
    clear_screen()
    load_create_common_words()

    try:
        print(CYAN + '8. Settings Menu\n' + RESET)
        print('1) Check commonwords.txt contents.')
        print('2) Add words to the commonwords.txt file.')
        print('3) Remove words from the commonwords.txt file.')
        print('4) Reset commonwords.txt to default list.')
        print('5) Remove contents of commonwords.txt')
        print(' ')
        choice = input('Select option or press Enter to return to Main Menu.')

        if choice == '1':
            option_8_1()
        elif choice == '2':
            option_8_2()
        elif choice == '3':
            option_8_3()
        elif choice == '4':
            option_8_4()
        elif choice == '5':
            option_8_5()
        else:
            main_menu()
            
    except Exception as e:
        clear_screen()
        print(RED + 'TextCrawl encountered an unexpected error. Error: {e} ' + RESET)
        main()

# Option 8_1 - opens commonwords.txt file and displays all words for the user to see
def option_8_1():
    """
    Displays the contents of commonwords.txt to the user. If the file does not exist, it recreates the default 
    commonwords.txt file using load_create_common_words function and retries displaying its contents.

    Exceptions:
    FileNotFoundError: If the commonwords.txt file does not exist.

    Note:
    This function is intended for user review of the common words list that influences word tallying.
    """
    clear_screen()

    try:
        print(YELLOW + 'The contents of the commonwords.txt file are shown below:\n' + RESET)

        # Reads commonwords.txt in the parent directory and displays to the user
        with open('commonwords.txt', 'r', encoding='utf-8') as commonwords:
            for line in commonwords:
                line.split()
                print(line)
        
        input(YELLOW + '\nPress Enter to return to Settings menu.' + RESET)

    except FileNotFoundError:
        load_create_common_words()
        option_8_1()
    
    option_8()

# Option 8_2 - adds user-defined words to commonwords.txt
def option_8_2():
    """
    Opens and displays the current contents of commonwords.txt, then prompts the user to add new words.
    New words are normalized and checked against existing entries to avoid duplicates before being added.
    The function allows multiple additions until the user decides to return to the settings menu. If the 
    file does not exist, it is created using the load_create_common_words function, and the user is 
    prompted to add words immediately.
    
    Raises:
    FileNotFoundError: If the commonwords.txt file does not exist.

    Notes:
    - User input is split by commas or whitespace to allow multiple word entries.
    - The function calls itself recursively if the user opts to add more words.
    """
    clear_screen()

    try:
        print(YELLOW + 'The contents of commonwords.txt are below. These will be filtered from the tally when TextCrawl scans a .txt file:\n' + RESET)

        # Reads commonwords.txt in the parent directory and displays to the user
        with open('commonwords.txt', 'r+', encoding='utf-8') as commonwords:
            
            # Creates a list of all words currently in commonwords.txt for comparison to user input later (also prints words for user)
            prev_common_words = []
            for line in commonwords:
                word = line.split()
                print(line)
                prev_common_words.extend(word)

            # Allows user to add words to commonwords.txt
            user_words_input = input(YELLOW + '\n\nEnter the word(s) you would like to add to commonwords.txt ' + RESET + '(Press Enter to return to Settings menu): ')
            print('')

            # Splits and strips user input for iteration loop
            user_words_split = re.split(r'[,\s]+', user_words_input)

            # Returns user to Settings menu if only 'Enter' is pressed
            if user_words_split == ['']:
                option_8()

            # Iterates over the user's words to add them to the commonwords.txt file, if necessary
            if len(user_words_split) != 0:
                for word in user_words_split:
                    if word in prev_common_words:
                        print(YELLOW + word + RESET + ' was already in commonwords.txt - no need to add!')
                        continue
                    elif word == '':
                        continue
                    else:
                        commonwords.write(' ' + word)
                        print(YELLOW + word + RESET + ' successfully added to commonwords.txt!')

    except FileNotFoundError:
        press_enter = input(RED + 'Commonwords.txt was not found!' + RESET + 'Press Enter to create.')
        load_create_common_words()
        option_8_2
        print('Commonwords.txt created successfully!')

    continue_prompt = input('\nAll done! Would you like to add more words? (Y = yes) ')
    if continue_prompt.lower() == 'y':
        option_8_2()
    else:
        option_8()

# Option 8_3 - Deletes words from commonwords.txt
def option_8_3():
    """
    Opens and displays contents of commonwords.txt and then prompts the user for words to be removed by
    normalizing and checking them against the current list of word. The function allows multiple additions
    until the user decides to return to the Settings menu. If the file does not exist, it is created
    by calling the load_create_common_words function, and the user is re-prompted to remove words.

    Raises:
    FileNotFoundError: If commonwords.txt cannot be found and needs to be recreated.

    Notes:
    - User input is split by commas or whitespace to allow multiple word entries.
    - The function calls itself recursively if the user opts to remove more words.
    """
    clear_screen()

    try:
        print(YELLOW + 'The contents of commonwords.txt are below. These will be filtered from the tally when TextCrawl scans a .txt file:\n' + RESET)

        # Reads commonwords.txt and displays to the user
        with open('commonwords.txt', 'r', encoding='utf-8') as commonwords:
            content = commonwords.read()
            print(content)

        # Enables user to remove words from commonwords.txt
            user_words_input = input(YELLOW + '\n\nEnter the word(s) you would like to remove from commonwords.txt ' + RESET + '(Press Enter to return to Setings menu): ')

            # Return to settings if user does not enter a word
            if user_words_input.strip() == '':
                option_8_3
            
            # Splits and strips user input for iteration loop
            user_words_split = re.split(r'[,\s]+', user_words_input.strip())

            # Returns user to settings menu if only 'Enter' is pressed
            if user_words_split == ['']:
                option_8()
            # Loop checks if the user-defined word(s) are in the content read from commonwords.txt and replaces (or not) as appropriate
            
            else:
                for word in user_words_split:
                    if word in content:
                        regex = r'\b' + re.escape(word) + r'\b'
                        content = re.sub(regex, '', content)
                        print(YELLOW + word + RESET + ' removed from commonwords.txt!')
                        continue
                    elif word not in content:
                        print(YELLOW + word + RESET + ' not found in commonwords.txt!')
                        option_8_3()

        # Writes the updated content to the commonwords.txt file
        with open('commonwords.txt', 'w', encoding='utf-8') as commonwords:
            commonwords.write(content)
            # print(YELLOW + word + RESET + ' successfully removed from commonwords.txt!')


    except FileNotFoundError:
        input(RED + 'Commonwords.txt was not found!' + RESET + 'Press Enter to create.')
        load_create_common_words()
        input('Commonwords.txt created successfully! Press Enter to continue...')
        option_8_3

    except Exception as e:
        clear_screen()
        print(RED + f'TextCrawl encountered an unexpected error. Error: {e} ' + RESET)
        return_to_main()

    continue_prompt = input('\nAll done! Would you like to remove more words? (Y = yes) ')
    if continue_prompt.lower() == 'y':
        option_8_3()
    else:
        option_8()
    
# Option 8_4 - Resets commonwords.txt to default
def option_8_4():
    """ 
    Resets the commonwords.txt to the default list by opening commonwords.txt in write mode and
    writing the contents defined within the function.

    """
    # Creates or overwrites commonwords.txt to the default list below
    with open('commonwords.txt', 'w', encoding='utf-8') as common_build:
        common_build.write('a about after again all am an and any are as at back be because been before being below between both but by came can cant come could couldnt day de did didnt dont do down during each even few for from further get got had has have having he hed her here hers herself him himself his how i if in into is it its itself just know like made man many may me might more most much must my myself new no nor not now of off on once only or other our out over own pg page said saw say says see she should shouldnt so some such than that the their them then there these they this those through to too toward under until up upon us very was wasnt we were what when where which while who whom why will with without would wouldnt yes yet you your yours yourself yourselves')

    input(YELLOW + '\nCommonwords.txt has been reset to the default list! Press Enter to continue...' + RESET)
    option_8()

# Option 8_5 - Removes all filters by deleting the contents of commonwords.txt
def option_8_5():
    """
    Deletes the contents of commonwords.txt by writing a single whitespace (' ') to the file. This
    will effectively remove all filters for the tally_words function, which may be desirable for
    some users' use cases.
    """
    with open('commonwords.txt', 'w', encoding='utf-8') as common_build:
        common_build.write(' ')
    
    input(YELLOW + '\nCommonwords.txt has been cleared! You may alawys reset to the default list by selection Option 8.4. Press Enter to continue...' + RESET)
    option_8()

# Option 9 - Provides instructions, notes, and help for users
def option_9():
    """
    Provides in-program instructions, future plans, user notes, and contact information for the program.
    """

    clear_screen()
    print(CYAN + 'TextCrawl v.20 Help/Readme\n' + RESET)
    print('''To use TextCrawl, ensure that you have placed at least one .txt file in a subdirectory called "Textfiles" and/or have a direct URL link to a .txt file. From there you can select how many of the most common words utilized in the .txt file.\n''')
    print('''If this is your first time using the program, I recommend viewing the commonwords.txt file by navigating to the Settings menu. The words contained in this file will be filtered from TextCrawl's tally. From Settings, you may add or remove words from commonwords.txt or you may reset it to the default.''')
    print('''\nTextCrawl is a simple program that is designed to count the number of non-common words (i.e., "if, and, the, etc.") and provide a total count for how many instances of each word in a .txt file appear. This began as a relatively simple project to help teach myself how to use Python to:\n
    - Handle files (read, write, delete, append, etc.)
    - Access URLs
    - Provide a simple, but effective, user interface
    - Write error handling logic
    - Implement logic to allow a degree of user customization (i.e., which files to scan, how many words to print, etc.)\n''')
    print('''Later, I hope to implement SQL database support and the ability for users to extract interesting data to the database. Additionally, I want TextCrawl to enable users to gain insights into trends across multiple text files. Stay tuned for future versions and thanks for using TextCrawl! Finally, I wish to add more user options to the word tally function itself, allowing users to order the list in ascending order as well, or to save the output to a .txt or other file. Perhaps the program will even offer full GUI support!\n''')

    print('''I'd love to hear from you! Please send any feedback or questions to me at: ''' + CYAN + 'c.fowler00@yahoo.com' + RESET)

    return_to_main()

# Allows user return to Main Menu
def return_to_main():
    """
    Prompts the user to press Enter before calling the clear_screen and main_menu functions,
    effectively returning them to the Main Menu.
    """

    menu_return = input(YELLOW + '\nPress Enter to return to the Main Menu.' + RESET)
    clear_screen()
    main_menu()

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

# Loads the .txt file
def load_textfile(filename):
    """ 
    Loads the user-specified text files when called as filename parameter 
    and returns contents as filename object. This function is essential for 
    the tally_words function.

    Parameters:
    filename

    Returns:
    filename

    Notes:
    - Input of 'c' cancels and calls main_menu function
    - If user does not provide input, the default 'lesmiserables.txt' is loaded
    """
    if filename.lower() == 'c':
        main_menu()
    if len(filename) < 1:
        filename = 'lesmiserables.txt'
    if filename[-4:] != '.txt':
        filename += '.txt'
       
    # Moves to 'Textfiles' subdirectory where .txt files are kept
    current_dir = str(os.getcwd())
    if current_dir[-9:] != 'Textfiles':
        os.chdir('Textfiles')
    
    # Opens the user text file and returns as 'filename' object
    with open(filename, 'r', encoding='utf-8'):
            print(YELLOW + f'\n{filename}' + RESET + ' opened successfully!' + RESET)
    return filename

# Creates (if needed) and loads the 'commonwords.txt' file
def load_create_common_words():
    """
    Creates the commonwords.txt file (if it is not found in the same directory as the script
    and writes a set of 'default words' to it. This is essential for the tally_words and option_2 
    functions to execute, as these words will be excluded from the tally process.

    Returns:
    common_words_list

    """

    # Changes to parent directory and loads commonwords.txt as common_words object
    current_dir = str(os.getcwd())
    parent_dir = os.path.dirname(current_dir)
    if current_dir[-9:] == 'Textfiles':
        os.chdir(parent_dir)
    
    # Checks to see is file exists, if not it will create a .txt with a default set of common words
    if os.path.isfile('commonwords.txt') == False:
        with open('commonwords.txt', 'w', encoding='utf-8') as common_build:
            common_build.write('a about after again all am an and any are as at back be because been before being below between both but by came can cant come could couldnt day de did didnt dont do down during each even few for from further get got had has have having he hed her here hers herself him himself his how i if in into is it its itself just know like made man many may me might more most much must my myself new no nor not now of off on once only or other our out over own pg page said saw say says see she should shouldnt so some such than that the their them then there these they this those through to too toward under until up upon us very was wasnt we were what when where which while who whom why will with without would wouldnt yes yet you your yours yourself yourselves')

    # Reads commonwords.txt and returns it as an object 'common_words' to be used later (i.e., by the tally_words function)
    with open('commonwords.txt', 'r', encoding='utf-8') as common_words_file:
        for line in common_words_file:
            common_words_list = line.split(' ')
    return common_words_list

# Parses the .txt file and returns a list of a user-specified number of most-used "uncommon words"
def tally_words(filename, number_to_list, common_list):
    """
    Counts the words in the user-specified text file which was loaded by the load_textfile function.
    Normalizes the words by stripping most punctuation, whitespace, and converts capital letters to
    lowercase. These noramlized words are then compared to the common_list object, and if not present,
    added to the wordtally dictionary. Finally, the function displays the number of user-specified
    words most commonly found in the text file by rank, showing both the word itself and number of
    occurrences within the text.

    Parameters:
    filename: The path to the text file. The load_textfile function can pass this.
    number_to_list: User-specified number of words to list. 
    common_list: The words to prevent tally_words from adding to wordtally dict for counting.
                The load_create_common_list function can pass this.

    Notes:
    - Changes to "Textfiles" directory before looking for file
    - Loads text files in UTF-8 for compatability
    - Will pause every 2,500 lines if the user selects a number > 2,500 to list 
    """
    
    wordtally = {}

    # Changes directory to "Textfiles" if necessary
    current_dir = str(os.getcwd())
    if current_dir[-9:] != 'Textfiles':
        os.chdir('Textfiles')
    
    # Opens and parses the user-specified .txt file
    with open(filename, 'r', encoding='utf-8') as textfile:
        for line in textfile:
            file_words = line.strip().lower().split(' ')

            # Strips punctuation from individual words
            for word in file_words:
                clean_word = word.strip().strip('\"').strip()
                clean_word = clean_word.translate(str.maketrans('', '', '1234567890%$#[]_().,;:!?\''))
                
                # Strips less-common quotation marks from words
                punctuation = string.punctuation = '“”‘’'
                for punct in punctuation:
                    clean_word = clean_word.replace(punct, '')
                
                # Any word more than one letter in length is added to the 'wordtally' dictionary once cleaned
                if clean_word in common_list or len(clean_word) < 2:
                    continue
                if clean_word in wordtally:
                    wordtally[clean_word] += 1
                else:
                    wordtally[clean_word] = 1
    
    # Converts the 'wordtally' dictionary to a list, then sorts it by 'Top 25' common words and returns list.
    tallied_list = list(wordtally.items())
    sorted_list = sorted(tallied_list, key=lambda item:item[1], reverse=True)

    if number_to_list == '':
        number_to_list = None
        top_count_words = sorted_list[:number_to_list]
    else:
        top_count_words = sorted_list[:number_to_list]

    # Prints the 'Top N Words' list
    counter = 0
    print(CYAN + '\nRank ) Word - Count','\n' + '_'*19 + '\n' + RESET)
    for index, (word, count) in enumerate(top_count_words, start=1):
        counter += 1
        print(f'{index}' + ') ' f'{word[0].upper()}{word[1:]} - {count}')

        if counter % 2500 == 0:
            input(YELLOW + '\nDisplayed 2,500 results! Press Enter to continue...' + RESET)

# Calls the 'main' function to run the program
if __name__ == '__main__': 
    main()