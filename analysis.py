# Import standard library modules
import os
import requests
import re

# Import local program scripts
import ui_helpers

# Loads a .txt file from Textfiles and returns it as string object
def load_textfile(filename):
    """ 
    Loads the user-specified text files when called as filename parameter 
    and returns contents as filename object. This function is essential for the tally_words function.

    Parameters:
    filename

    Returns:
    text_file_data

    Raises:
    - FileNotFoundError - if text file is not found in Textfiles directory
    - ValueError - if number is not entered for words to count
    - Exception - for other unexpected issues 
    """
    # Moves to 'Textfiles' directory
    ui_helpers.move_to_textfiles()

    # Opens the user text file and returns as 'filename' object
    try: 
        with open(filename, 'r', encoding='utf-8') as text_file:
            return text_file.read()

    except FileNotFoundError as e:
        print(ui_helpers.RED + 'The file was not found!' + ui_helpers.RESET + 'Please try again.')
        return None

    except Exception as e:
        print(ui_helpers.RED + f'\nThe following error occurred: {e}' + ui_helpers.RESET + '\n\nPlease try again.\n')
        return None

# URL-based text file open
def url_text_file_open(user_url):
    """
    Prompts the user for a URL pointing to a .txt file and attempts to download and analyze the text. The function
    fetches the file, loads common words for filtering, and prompts the user for the number of most commonly used 
    words to display. It then normalizes and tallies the words, excluding those found in commonwords.txt, and 
    displays the results.

    Raises:
    Exception: catches unexpected exceptions that may occur during execution.
    """
    # Accesses the .txt file from URL and returns contents as string object
    try:
        response = requests.get(user_url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            text_file_data = response.text
            print('\nSuccessfully accessed .txt file!')
            return text_file_data
            
        else:
            print(ui_helpers.RED + 'Failed to retrieve data.', response.status_code + ui_helpers.RESET + 'Please check the URL or your connection and try again.')
    
    except requests.exceptions.RequestException as e:
        print(ui_helpers.RED + 'TextCrawl encountered an error retrieving the URL!' + ui_helpers.RESET)

# Performs word frequency analysis with user parameters
def tally_words(text_file_data, common_list):
    """
    Counts the words in the user-specified text file which was loaded by the load_textfile function.
    Normalizes the words by stripping most punctuation, whitespace, and converts capital letters to
    lowercase. These noramlized words are then compared to the common_list object, and if not present,
    added to the wordtally dictionary. Finally, the function displays the number of user-specified
    words most commonly found in the text file by rank, showing both the word itself and number of
    occurrences within the text.

    Explanation of REGEX: 
    - \b[a-zA-Z]+       Matches the beginning of a word followed by one or more letters
    - (?:-[a-zA-Z]+)*   Matches zero or more occurrences of a hyphen followed by more letters
    - (?<=\w)           Looks behind to ensure apostrophes are preceded by a word
    - [\'’]             Matches an apostrophe, either straight or curly character type
    - (?![sSdD]\b)      Looks ahead to ensure the apostrophe is NOT followed by "s, S, d, D" at a word boundary
    - [a-zA-Z]+         Matches one or more letters following the apostrophe (to include contractions)
    - \b                Matches the end of a word

    Parameters:
    text_file_data: This should be a string returned by load_textfile()
    common_list: A list object of words to filter returned by load_common_words()

    Returns:
    wordtally_dict

    Raises:
    - FileNotFoundError - if text file is not found in Textfiles directory
    - ValueError - if number is not entered for words to count
    - Exception - for other unexpected issues 

    Notes:
    - Changes to "Textfiles" directory before looking for file
    - Loads text files in UTF-8 for compatability
    - Will pause every 2,500 lines if the user selects a number > 2,500 to list 
    """
    wordtally_dict = {}
    try:
        # REGEX findall method to separate each word from the lower-case normalized string object text_file_data
        words = re.findall(r"\b[a-zA-Z]+(?:-[a-zA-Z]+)*(?:(?<=\w)[\'’](?![sSdD]\b)[a-zA-Z]+)?\b", text_file_data.lower())

        # Iterate over words list to add to wordtally_dict count
        for word in words:
            if word not in common_list and len(word) > 2:
                wordtally_dict[word] = wordtally_dict.get(word, 0) + 1

    except FileNotFoundError as e:
        ui_helpers.clear_screen()
        print(ui_helpers.RED + f'{e}' + ui_helpers.RESET)
        input('...')

    except ValueError as e:
        ui_helpers.clear_screen()
        print(ui_helpers.RED + f'The following Value Error was encountered while trying to analyze the file: {e}')
        input('...')

    except Exception as e:
        ui_helpers.clear_screen()
        print(ui_helpers.RED + f'TextCrawl encountered an unexpected error during the word_tally function: {e} ' + ui_helpers.RESET)
        input('...')

    return wordtally_dict

# Display word frequency
def display_word_frequency(wordtally_results, number_to_list):
    """
    This function uses the dictionary object created in the tally_words function along with a user-defined number of words to list and displays the results of the .txt file word frequency count.

    Parameters:
    wordtally_results: Must be the wordtally_dict{} returned by the tally_words function.
    number_to_list: Typically a user-defined number of the top words to list (if user enters no value, all words will be displayed).

    Returns:
    sorted_list: This is the list object which displays the results of the tallying in order from greatest to smallest as of v.30.
    """

    # Checks if wordtally_results contains data
    if wordtally_results is None:
        print(ui_helpers.RED + 'Error: expected a dictionary but got None' + ui_helpers.RESET)
        return
    
    # Preparing a list from the wordtally_results dictionary
    tallied_list = list(wordtally_results.items())
    sorted_list = sorted(tallied_list, key=lambda item:item[1], reverse=True)

    # Displays user-defined number of words (or all words)
    if number_to_list == '':
        top_count_words = sorted_list
    else:
        top_count_words = sorted_list[:number_to_list]

    # Prints the 'Top N Words' list
    print(ui_helpers.CYAN + '\nRank ) Word - Count','\n' + '_'*19 + '\n' + ui_helpers.RESET)

    for index, (word, count) in enumerate(top_count_words, start=1):
        print(f'{index}' + ') ' f'{word[0].upper()}{word[1:]} - {count}')

        # Pauses execution for user input when printing large result set
        if index % 2500 == 0:
            input(ui_helpers.YELLOW + '\nDisplayed 2,500 results! Press Enter to continue...' + ui_helpers.RESET)

    return(sorted_list)

# Creates the default commonwords.txt filter
def initialize_common_words():
    """
    Creates the defaultcommonwords.txt file
    """

    # Changes to parent directory if needed
    ui_helpers.move_to_parent()
    
    # Checks to see is file exists, if not it will create a .txt with a default set of common words
    if os.path.isfile('commonwords.txt') == False:
        with open('commonwords.txt', 'w', encoding='utf-8') as common_build:
            common_build.write("a about after again all am an and any are arent aren't as at back be because been before being below between both but by came can cant come could couldnt day de did didnt didn't dont don't do down during each even few for from further get got had hadnt hadn't has hasnt hasn't have having he hed her here hers herself him himself his how i i'll im i'm if in into is isnt isn't it its itself ive i've just know like made man many may me might more most much must my myself new no nor not now of off on once only or other our out over own pg page put said saw say says see she should shouldnt so some such than that the their them then there these they this those through to too toward under until up upon us very was wasnt we we'll were what when where which while who whom why will with without won't would wouldnt yes yet you your yours yourself yourselves")

# Loads commonwords.txt filter for user
def load_common_words():
    """
    Loads commonwords.txt file and returns it as a list object for use by other functions, such as tally_words.

    Returns:
    common_words_list: For use in tally_words and other functions.
    """
    # Changes to parent directory if needed
    ui_helpers.move_to_parent()

    # Loads and returns commonwords.txt into a list 
    while True:
        try:
            with open('commonwords.txt', 'r', encoding='utf-8') as common_words_file:
                for line in common_words_file:
                    common_words_list = line.split(' ')
                return common_words_list
        
        except FileNotFoundError:
            initialize_common_words()
            ui_helpers.clear_screen()
            print(ui_helpers.YELLOW + 'Notice: commonwords.txt was not found and has been created using default word filters.' + ui_helpers.RESET)
            input('\nPress enter to continue.\n')

        except Exception as e:
            print(ui_helpers.RED + f'TextCrawl encountered an unexpected error: {e}' + ui_helpers.RESET)

# Read/display commonwords.txt file
def read_commonwords_txt():
    """
    Reads the contents of commonwords.txt and displays them to the user for reference.

    Raises:
    FileNotFoundError if commonwords.txt is not found

    Notes:
    - If commonwords.txt does not exist, it will be created by calling the load_common_words function.
    """
    # Changes to parent directory if needed
    ui_helpers.move_to_parent()

    # Opens and displays the contents of commonwords.txt
    try:
        with open('commonwords.txt', 'r', encoding='utf-8') as commonwords:
            content = commonwords.read()
            print(content)

    except FileNotFoundError:
        load_common_words()

# Adds user-defined words to commonwords.txt
def add_to_commonwords_txt(user_words_input):
    """
    Opens and displays the current contents of commonwords.txt, then prompts the user to add new words.
    New words are normalized and checked against existing entries to avoid duplicates before being added.
    The function allows multiple additions until the user decides to return to the settings menu. If the 
    file does not exist, it is created using the load_common_words function, and the user is 
    prompted to add words immediately.
    
    Parameters:
    user_words_input: The words the user wishes to add to commonwords.txt

    Raises:
    FileNotFoundError: If the commonwords.txt file does not exist.

    Notes:
    - User input is split by commas or whitespace to allow multiple word entries.
    - The function calls itself recursively if the user opts to add more words.
    - If commonwords.txt is not found, it will be created using the load_common_words function
    """

    # Loads the commonwords.txt file as a list
    commonwords_content = load_common_words()

    # Splits and strips user input for iteration loop
    user_words_split = re.split(r'[,\s]+', user_words_input.strip().lower())
    user_words_split = [word.strip() for word in user_words_split if word]  # Remove empty strings

    # Iterates over the user's words to add them to the commonwords.txt file, if necessary
    changes_made = False
    for word in user_words_split:
        
        if word not in commonwords_content:
            commonwords_content.append(word)
            print(ui_helpers.YELLOW + word + ui_helpers.RESET + ' added to commonwords.txt!')
            changes_made = True
        
        else:
            print(ui_helpers.YELLOW + word + ui_helpers.RESET + ' already in commonwords.txt!')
            continue

    # Writes the updated content to the commonwords.txt file
    if changes_made == True:
        with open('commonwords.txt', 'w', encoding='utf-8') as commonwords:
            commonwords.write(' '.join(commonwords_content))

# Deletes user-defined words from commonwords.txt
def delete_from_commonwords_txt(user_words_input):
    """
    Opens and displays contents of commonwords.txt and then prompts the user for words to be removed by
    normalizing and checking them against the current list of word. The function allows multiple additions
    until the user decides to return to the Settings menu. If the file does not exist, it is created
    by calling the load_common_words function, and the user is re-prompted to remove words.

    Parameters:
    user_words_input: A user-specified string of words to remove from the commonwords.txt filter.

    Raises:
    FileNotFoundError: If commonwords.txt cannot be found and needs to be recreated.

    Notes:
    - User input is split by commas or whitespace to allow multiple word entries.
    - The function calls itself recursively if the user opts to remove more words.
    """

    # Loads the commonwords.txt file as a list
    commonwords_content = load_common_words()

    # Splits and strips user input for iteration loop
    user_words_split = re.split(r'[,\s]+', user_words_input.strip().lower())
    user_words_split = [word.strip() for word in user_words_split if word]  # Remove empty strings

    # Loop checks if the user-defined word(s) are in the content read from commonwords.txt and replaces (or not) as appropriate
    changes_made = False
    for word in user_words_split:
        original_len = len(commonwords_content)
        commonwords_content = [existing_word for existing_word in commonwords_content if existing_word.lower() != word]
        
        if len(commonwords_content) < original_len:
            print(ui_helpers.YELLOW + word + ui_helpers.RESET + ' removed from commonwords.txt!')
            changes_made = True
        
        else:
            print(ui_helpers.YELLOW + word + ui_helpers.RESET + ' not found in commonwords.txt!')

    # Writes the updated content to the commonwords.txt file
    if changes_made == True:
        with open('commonwords.txt', 'w', encoding='utf-8') as commonwords:
            commonwords.write(' '.join(commonwords_content))
    
# Resets commonwords.txt to default
def reset_commonwords_txt():
    """ 
    Resets the commonwords.txt to the default list by opening commonwords.txt in write mode and writing the contents defined within the function.

    Raises:
    FileNotFoundError: If commonwords.txt is not found, it will create it using initiliaze_common_words function.
    """
    # Changes to parent directory if needed
    ui_helpers.move_to_parent()

    # Creates or overwrites commonwords.txt to the default list below
    try:
        os.remove('commonwords.txt')
        initialize_common_words()
        input(ui_helpers.YELLOW + '\nCommonwords.txt has been reset to the default list!'
          + ui_helpers.RESET + '\n\nPress Enter to continue...')
    
    except FileNotFoundError:
        initialize_common_words()
        input(ui_helpers.YELLOW + '\nCommonwords.txt has been reset to the default list!'
          + ui_helpers.RESET + ' Press Enter to continue...')

# Removes all filters by deleting the contents of commonwords.txt
def delete_commonwords_txt_contents():
    """
    Deletes the contents of commonwords.txt by writing a single whitespace (' ') to the file. This will effectively remove all filters for the tally_words function, which may be desirable for some users' use cases.
    """
    # Changes to parent directory if needed
    ui_helpers.move_to_parent()

    # Removes filters and displays user confirmation
    with open('commonwords.txt', 'w', encoding='utf-8') as common_build:
        common_build.write(' ')
    
    # User confirmation prompt and return
    input(ui_helpers.YELLOW + '\nCommonwords.txt has been cleared!' + ui_helpers.RESET +  '\n\nYou may alawys reset to the default list by selecting Option 4 in ' + ui_helpers.CYAN + 'Filter Settings' + ui_helpers.RESET + ' menu.\n\nPress Enter to continue...')
