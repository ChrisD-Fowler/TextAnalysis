# Imports string method to enable easier parsing of text data
import string

# Welcome message
print()
print('Welcome to TextCrawl v.10!')
print()
print('This is a simple program I wrote to solidify some basic Python skills following my first month of self-directed learning.')
print()
print('To begin, you need only to place a .txt file in the same directory as the program and then tell the program which file you wish to scan (include the .txt in the filename).') 
print()
print('From there, TextCrawl will read your file and then parse, normalize, and add them to a dictionary data construct (except for very common words). Finally, the program will display the Top 25 most common words in the file. Enjoy!')
print('-- Christopher Fowler')
print()

# Sets ufile to whatever the user enters
ufile = input('What text file would you like to scan today? ')

# Defaults to Les Miserables if user enters nothing above
if len(ufile) <1 :
    ufile = 'lesmiserables.txt'

# Sets fhand as file handle, opens ufile var as read-only and sets encoding to UTF-8 for compatability
fhand = open(ufile, 'r', encoding='utf-8')

# Gives the user a warm-fuzzy confirmation message which includes file metadata
print('File opened successfully: ', fhand)
print()

# Sets wordtally as the dictionary which will contain all the words:counts as k:v
wordtally = dict()

# A customizable list of words NOT to include as determined by designer preference
common_words = ('the', 'of', 'and', 'a', 'to', 'in', 'he', ' ', 
                'was', 'she', 'it', 'his', 'her', 'on', 'at', 
                'which', 'with', 'for', 'you', 'have', 'that', 'had',
                'is', 'no', 'what', '', 'been', 'they', 'there', 'has',
                'an', 'this', 'not', 'as', 'i', 'one', 'will', 'we', 'were',
                'be', 'by', 'are', 'from', 'who', 'all', 'but', 'him',
                'said', 'when', 'their', 'would', 'so', 'did', 'into',
                'these', 'very', 'its', 'more', 'if', 'or', 'like',
                'than', 'then', 'some', 'my', 'made', 'only', 'about', 'two',
                'do', 'up', 'your', 'those', 'could', 'de', 'me', '"i', 'should',
                'them', 'other', 'him', 'say', 'where', 'any', 'back', 'out',
                'see', 'down', 'now', 'saw', 'dont', 'how', 'well', 'get',
                'just', 'can', 'over', 'here', 'yes', 'around', 'think', 'right',
                'off', 'go', 'again', 'through', 'thats', 'didnt', 'cant', 'know',
                'im', 'got', 'away', 'going', 'toward', 'came', 'good', 'old', 'men',
                'without', 'am', 'still', 'even', '\"', 'must', 'day', 'come', 'upon',
                'same', 'before', 'us', 'way', 'why', 'too', 'moved', 'too', 'went', 'man', 'few', 'our', 'hes', 'maybe', 'put', 'asked', 'wasnt', 'new',
                'sure', 'couldnt', 'want', 'might')

# It is necessary to include these less-common quotation characters to prevent their being added to the list
punctuation = string.punctuation + '“”‘’'

# Outer loop for processing the lines and splitting into words
for line in fhand :
    line = line.strip() # Eliminates spaces from each side of a line
    line = line.lower() # Sets each character as lowercase for ease of logging
    words = line.split(' ') # Splits each line into words each time a space is detected
    
    # Inner loop for processing each word and adding to the dictionary wordtally
    for word in words :
        clean_word = word.strip().strip('\"').strip() # Eliminates spaces and quotation punctuation from either side of words
        clean_word = clean_word.replace('\"', '') # Another step to ensure that any remaining quotations are replace with nothing, i.e., no spaces
        
        # Sub-loop to ensure special punctuation characters are caught and deleted
        for punct in punctuation :
            clean_word = clean_word.replace(punct,'')
        
        # Series of if/else statements to add words to dictionary and increase the value count appropriately
        if clean_word in common_words :
            continue
        if len(clean_word) < 2 : # Prevents logging of single characters
            continue
        if clean_word in wordtally :
            wordtally[clean_word] = wordtally[clean_word] + 1
        else :
            wordtally[clean_word] = 1

# Manipulates the wordtally dictionary into a usable and interesting form for the program
tallylist = list(wordtally.items()) # Takes k:v contents of wordtally dict and dumps into tallylist list for processing/sorting later
sortedlist = sorted(tallylist, key=lambda item: item[1], reverse=True) # Sorts tallylist appropriately, ranking the highest value on top
top_25 = sortedlist[:25] # Defines how many of the top words to display

# Prints the result for the user
print('The Top 25 most common interesting words in', ufile, 'are...' )
print()
print('Count -- Word')
print('______________')
for index, (word, count) in enumerate(top_25, start=1) :
    print(f"{index}. {word} - {count}")

#    print(line) #Debug line