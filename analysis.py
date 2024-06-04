# Import standard library modules
import os
import requests
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Import local program scripts
import ui_helpers

# Loads a single .txt file from Textfiles and returns it as string
def load_textfile(filename):
    """ 
    Loads the user-specified text files when called as filename parameter 
    and returns contents as filename object. This function is essential for the tally_words function.

    Parameters:
    filename - the name of the file to be loaded.

    Returns:
    text_file - a string containing the contents of the .txt file after it has been read.

    Raises:
    - FileNotFoundError - if text file is not found in Textfiles directory
    - ValueError - if number is not entered for words to count
    - Exception - for other unexpected issues 
    """
    # Moves to 'Textfiles' directory
    ui_helpers.move_to_textfiles()

    # Opens the user text file and returns as 'filename' object
    if filename:
        try: 
            with open(filename, 'r', encoding='utf-8') as text_file:
                return text_file.read()

        except FileNotFoundError as e:
            print(ui_helpers.RED + 'The file was not found!' + ui_helpers.RESET + 'Please try again.')
            return None

        except Exception as e:
            print(ui_helpers.RED + f'\nThe following error occurred while attempting to load the .txt file: {e}' + ui_helpers.RESET + '\n\nPlease try again.\n')
            return None
        
    else:
        print(ui_helpers.RED + 'The load_textfile function expected a valid file name, but none was passed')
        input(ui_helpers.RESET + 'Press Enter to continue')

# Clean and strip a txt file prior to processing
def clean_strip_txt_file(loaded_text_file):
    """
    Assists other functions (such as analysis.text_tf_idf_analysis()) with noramlizing the contents of a .txt file and filtering any words found in the commonwords.txt filter prior to performing the TF-IDF calculation. Uses Regular Expressions.

    Parameters:
    loaded_text_file - a string containing the contents of a .txt after it has been read by load_textfile().

    Returns:
    cleaned_content - the full text of the original file, normalized and stripped of any words found in commonwords.txt.

    Raises:
    Exception - for any unexpected errors encountered.
    """
    # Load commonwords.txt filter
    common_words_list = load_common_words()
    
    if loaded_text_file:
        try:
            # Perform text cleaning operations using RE
            text = loaded_text_file.lower()
            text = re.sub(r'[\d_]+|[^\w\s]', '', text)

            # Creat list of words not found in the common_words_list filter, rejoin as string
            filtered_words = [word for word in text.split() if word not in common_words_list]
            cleaned_content = ' '.join(filtered_words)
            
            return cleaned_content
        
        except Exception as e:
            print(ui_helpers.RED + f'An error was encountered while trying to normalize and filter the .txt file: {e}' + ui_helpers.RESET)

    else:
        print(ui_helpers.RED + 'The clean_strip_txt_file function failed because it was not given a valid string containing the contents of a .txt file')
        input(ui_helpers.RESET + 'Press Enter to continue.')

# URL-based text file open
def url_text_file_open(user_url):
    """
    Prompts the user for a URL pointing to a .txt file and attempts to download and analyze the text. The function
    fetches the file, loads common words for filtering, and prompts the user for the number of most commonly used 
    words to display. It then normalizes and tallies the words, excluding those found in commonwords.txt, and 
    displays the results.
    
    Parameters:
    user_url - the user-specified URL for the .txt to open

    Returns:
    filename - the name of the file
    text_file_data - a string containing the complete text of the file retrieved at the URL specified. Used by other functions to process the words contained.

    Raises:
    Exception: catches unexpected exceptions that may occur during execution.
    """
    # Accesses the .txt file from URL and returns contents as string object
    try:
        response = requests.get(user_url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            text_file_data = response.text
            
            # Retrieves the filename
            filename = user_url.split('/')
            filename = filename[-1:]

            print(f'\nSuccessfully accessed {filename} file!')
            return filename, text_file_data
            
        else:
            print(ui_helpers.RED + 'Failed to retrieve data.', response.status_code + ui_helpers.RESET + 'Please check the URL or your connection and try again.')
    
    except requests.exceptions.RequestException as e:
        print(ui_helpers.RED + 'TextAnalysis encountered an error retrieving the URL!' + ui_helpers.RESET)

# Performs word frequency analysis with user parameters
def tally_words(text_file_data, common_list):
    r"""
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
    wordtally_dict - a dictionary containing all words from text_file_data and NOT in common_list with number of occurrences (k:v = word:count)

    Raises:
    - Exception - for other unexpected issues 

    Notes:
    - Changes to "Textfiles" directory before looking for file
    - Loads text files in UTF-8 for compatability
    - Will pause every 2,500 lines if the user selects a number > 2,500 to list 
    """

    wordtally_dict = {}

    if text_file_data:
        try:
            # REGEX findall method to separate each word from the lower-case normalized string object text_file_data
            words = re.findall(r"\b[a-zA-Z]+(?:-[a-zA-Z]+)*(?:(?<=\w)[\'’](?![sSdD]\b)[a-zA-Z]+)?\b", text_file_data.lower())

            # Iterate over words list to add to wordtally_dict count
            for word in words:
                if word not in common_list and len(word) > 2:
                    wordtally_dict[word] = wordtally_dict.get(word, 0) + 1
        
            return wordtally_dict

        except Exception as e:
            ui_helpers.clear_screen()
            print(ui_helpers.RED + f'TextAnalysis encountered an unexpected error during the word_tally function: {e} ' + ui_helpers.RESET)
            input('...')

    else:
        print(ui_helpers.RED + 'Error: A string containing text data was expected by the tally_words function, but was not found')
        input(ui_helpers.RESET + '\nPress Enter to continue.')



def url_tf_idf_analysis(menu_return):
    r"""
    Enables TF-IDF analysis of multiple URLs. Prompts user to enter metadata (title, author, genre, year) for each URL, which is saved to the final_metadata dictionary to be used by other functions (i.e., visual dashboard)

    Parameters:
    menu_return - the user-specified menu to return to if user cancels operation or for the program to return to once an error has occurred.

    Returns:
    tfidf_df - the DataFrame containing the TF-IDF scores for each document.
    final_metadata - the dictionary containing the user-defined metadata for each document.

    """
    # Set lists for the TF-IDF Vectorizer and Pandas to use for data organization
    texts = []
    file_names = []
    final_metadata = {}

    while True:
        # Prompts user for the URL
        user_url = input(ui_helpers.YELLOW + '\nPlease enter or paste the complete URL here ' + 
                         ui_helpers.RESET + '(Enter "D" when Done or "C" to Cancel): ')

        # Changes user_url to a string to perform checks
        user_url_check = str(user_url).lower()

        # Returns to previous menu and clears DFs if user enters "c"
        if user_url_check == 'c':
            tfidf_df = None
            final_metadata = None
            menu_return()
            return tfidf_df, final_metadata
        
        # If user enters "d" for done
        if user_url_check == 'd':

            # Checks if user has not entered at least two URLs
            if len(final_metadata) < 2:
                input(ui_helpers.RED + 'Error! Must enter at least two URLs.' + 
                      ui_helpers.RESET + ' Press Enter to return to TF-IDF Menu.')
                tfidf_df = None
                final_metadata = None
                menu_return()
                return tfidf_df, final_metadata

            else:
                break

        # Checks for "http" prefix
        if user_url_check[0:4] != 'http':
            input(ui_helpers.RED + 'Invalid URL! Please check and try again.' + ui_helpers.RESET)
            menu_return()
            break
        
        if user_url == '':
            break
        
        else:
            # Opens the URL and returns the filename and entire .txt as a string
            default_filename, text_file_data = url_text_file_open(user_url)

        # If the URL is successfully loaded as a string, it is cleaned/normalized for further processing
        if text_file_data:
            cleaned_content = clean_strip_txt_file(text_file_data)
            filename = str(default_filename[0])

            # Prompts user to input file metadata
            doc_title, author, year, genre = ui_helpers.input_file_metadata(filename)
        
            # Adds metadata to final_metadata dictionary
            if doc_title not in final_metadata: 
                final_metadata[doc_title] = {
                'doc_title': doc_title, 
                'author': author,
                'year': year,
                'genre': genre
                }

                # Adds file name and cleaned content to lists for Vectorizer
                texts.append(cleaned_content)
                file_names.append(default_filename)

    if len(final_metadata) > 1:

        # Initialize Vectorizer
        vectorizer = TfidfVectorizer()

        # Load contents of each file into Vectorizer
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Convert TF-IDF matrix to Pandas DataFrame
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(),
                                index=final_metadata.keys(),
                                columns=vectorizer.get_feature_names_out())
        
        # Filter words with very low TF-IDF for data efficiency/performance
        threshold = 0.01
        tfidf_df = tfidf_df.loc[:, (tfidf_df.max() > threshold)]

        return tfidf_df, final_metadata

# TF-IDF Text File Analysis
def text_tf_idf_analysis(files_to_process, menu_return):
    """
    Performs TF-IDF analysis on two or more text files. Returns the results as a DataFrame which can be used by other functions (i.e., to save as CSV, to visualize, etc.)

    Parameters:
    files_to_process - a list of file names to perform the analysis. Usually determined by the ui_helpers.list_select_textfile() function.
    menu_return - specifies where to take the user if no file selection is made (i.e., "Enter" is pressed with no other input).
    
    Returns:
    tfidf_df - a Pandas DF for use by other functions.
    final_metadata - an optional list of dictionaries containing information about the file processed.
    """
    # Set lists for the TF-IDF Vectorizer and Pandas to use for data organization
    texts = []
    file_names = []
    final_metadata = {}

    # Checks to ensure list has two or more files
    if len(files_to_process) < 2:
        input(ui_helpers.RED + 'Error! You must select at least two documents to perform TF-IDF analysis!' + ui_helpers.RESET)
        menu_return()
        return

    try:
        # Ensures function looks in "Textfiles" subdirectory
        ui_helpers.move_to_textfiles()

        # Read each file specified
        for filename in files_to_process:
            file_content = load_textfile(filename)

            # If the .txt file is not blank, requests user input file metadata
            if file_content:

                # Removes common words, numbers, punctuation
                cleaned_content = clean_strip_txt_file(file_content)
                doc_title, author, year, genre = ui_helpers.input_file_metadata(filename)
                
                # Adds metadata to final_metadata dictionary
                if doc_title not in final_metadata: 
                    final_metadata[doc_title] = {
                    'doc_title': doc_title, 
                    'author': author,
                    'year': year,
                    'genre': genre
                }

                # Adds file names and cleaned content to lists for Vectorizer
                texts.append(cleaned_content)
                file_names.append(filename)

        # Initialize TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()

        # Load contents of each file into Vectorizer
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Convert TF-IDF matrix to Pandas DataFrame
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                                index=final_metadata.keys(), 
                                columns=vectorizer.get_feature_names_out())

        # Filter words with very low TF-IDF for data efficiency/performance
        threshold = 0.01
        tfidf_df = tfidf_df.loc[:, (tfidf_df.max() > threshold)]

        return tfidf_df, final_metadata
    
    except Exception as e:
        print(ui_helpers.RED + f'An error occurred while trying to analyze the .txt files: {e}' + ui_helpers.RESET)

# TF-IDF SQL Query
def sql_tf_idf_analysis(df):
    r"""
    Performs TF-IDF analysis on a DataFrame created using a SQL query and containing 'word counts by document.' Utilizes TfidfVectorizer for TF-IDF analysis once the DataFrame's data is re-aggregated into the documents dictionary. Creates a final_metadata dictionary for use by other functions (i.e., visuals.create_tf_idf_dash() in displaying document information.)

    Parameters:
    df - the DataFrame containing 'word counts by document' before TF-IDF scores are computed.

    Returns:
    tfidf_df - a new DataFrame with the same data as the original DataFrame, now including TF-IDF scores.
    final_metadata - a dictionary containing key information about each document included in the DataFrame.

    Raises:
    Exception - for any unexpected errors encountered.
    """

    # Aggregate words into documents dictionary
    documents = {}
    final_metadata = {}
    
    try:
        for index, row in df.iterrows():
            doc_title = row['doc_title']
            if doc_title not in documents:
                documents[doc_title] = []
            documents[doc_title].append((row['word'] + ' ') * row['count'])

            # Get document metadata from SQL query
            if doc_title not in final_metadata:
                final_metadata[doc_title] = {
                    'doc_title' : doc_title,
                    'author' : row['author'],
                    'year' : row['year'],
                    'genre' : row['genre']
                }
        
        # Rejoin words to form full document
        for doc_title in documents:
            documents[doc_title] = ''.join(documents[doc_title])

        # Initialize TF-IDF Vectorizer
        texts = list(documents.values())
        vectorizer = TfidfVectorizer()

        # Load contents of each file into Vectorizer
        tfidf_matrix = vectorizer.fit_transform(texts)

        # Convert TF-IDF matrix to Pandas DataFrame
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), 
                                index=documents.keys(), 
                                columns=vectorizer.get_feature_names_out())

        return tfidf_df, final_metadata
    
    except Exception as e:
        print(ui_helpers.RED + f'An error occurred while attempting to calculate TF-IDF scores: {e}' + ui_helpers.RESET)

# Applies user-defined threshold to DataFrame containing TF-IDF scores
def apply_threshold_filter(tfidf_df, threshold=0.01):
    """
    Applies a minimum threshold for filtering scores in a DataFrame which contains TF-IDF values. A TF-IDF typically contains large quantities of words and users often only need a select few.

    Parameters:
    tfidf_df - the DataFrame containing TF-IDF scores
    threshold - a user-defined minimum threshold below which all columns (words) are removed. Default is .01.

    Returns:
    tfidf_df - with values filtered below the threshold.
    """
    return tfidf_df.loc[:, (tfidf_df.max() > threshold)]

# Calculates the Min and Max values for a DataFrame
def get_min_max(df):
    """
    Calculates and returns the Min/Max values for values in a DataFrame. Enables the user to quickly sort or truncate a DF based on TF-IDF values.

    Parameters:
    df - a Pandas DataFrame which contains TF-IDF score calculations. Can be either the TF-IDF or Word Counts DataFrames.

    Returns:
    min_value - the smallest value in the DataFrame.
    max_value - the largest value in the DataFrame.
    """

    min_value = df.min().min()
    max_value = df.max().max()

    return min_value, max_value

# Enables user to search a DataFrame for specific words
def word_search_dataframe(df, words_list):
    """
    Performs a search within a DataFrame for specific words (columns) and keeps only the user-defined words.

    Parameters:
    df - a Pandas DataFrame which contains Word Counts or TF-IDF scores.
    words_list - a user-defined list of search words.

    Returns:
    filtered_df - the DataFrame once all undesired columns have been filtered.
    """

    # Checks if word is in DF column list and applies filter
    filtered_words = [word for word in words_list if word in df.columns]
    filtered_df = df[filtered_words]

    return filtered_df

# Enables user to search a DataFrame for specific words
def remove_words_from_df(df, words_list):
    """
    Performs a search within a DataFrame for specific words (columns) removes the words.

    Parameters:
    df - a Pandas DataFrame which contains Word Counts or TF-IDF scores.
    words_list - a user-defined list of search words.

    Returns:
    filtered_df - the DataFrame once all undesired columns have been filtered.
    """

    # Checks if word is in DF column list and applies filter
    filtered_words = [word for word in words_list if word in df.columns]
    filtered_df = df.drop(filtered_words, axis=1)

    return filtered_df

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
    Loads commonwords.txt file and returns it as a list for use by other functions, such as tally_words.

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
            print(ui_helpers.RED + f'TextAnalysis encountered an unexpected error: {e}' + ui_helpers.RESET)

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
    
    except FileNotFoundError:
        initialize_common_words()

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

# Create DataFrame from Word Counts Nested Dictionary
def word_counts_to_df(word_counts_all_docs):
    """
    Returns a DataFrame from the nested dictionary created during the Word Counts functions.

    Note: the word_counts_all_docs must be structured: {filename:{word:counts}}

    Parameters:
    word_counts_all_docs - nested dictionary created during the Word Counts functions

    Returns:
    word_counts_df - a DataFrame using the file names as row index and containing the word counts for each document
    """

    # Create the DF
    word_counts_df = pd.DataFrame.from_dict(word_counts_all_docs, orient='index')
    
    # Replace 'NaN' with '0'
    word_counts_df = word_counts_df.fillna(0)

    return word_counts_df