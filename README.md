# TextCrawl v.40

TextCrawl is a Python application that analyzes text data to identify and display the frequency of words. It allows users to input text data from either local files or via URLs. The results can be displayed either as total word counts or filtered to show only the most common words. Results may be added to a SQL database and queries may be generated to provide insight into the data (i.e., word use changes over time, etc.).

## Features
- **Word Frequency Analysis**: Analyze text files to find and count the most frequent words, excluding common words like 'the', 'is', etc.
- **Support for Local and Web Text Files**: Load text data from local files or directly from URLs.
- **SQLite Support**: Users may save results of word frequency analysis to database and execute database queries, which may be saved as .csv files.
- **Interactive User Interface**: Simple and intuitive command-line interface for easy navigation and usage.
- **Robust Error Handling**: Includes detailed error handling to ensure a smooth user experience.

### Prerequisites
- Python 3.8 or higher.
- "requests" library for Python.
- Ensure you have a subdirectory named "Textfiles" to place .txt files in to use Option 1 for Word Frequency Analysis.
- Otherwise, a valid URL to a .txt file will suffice to use Option 2 for Word Frequency Analysis.

## Limitations
- This script was built and tested on a Windows 11 PC. Using on a platform other than Windows 10 may result in colors or other features not displaying or executing properly.
- Text files in UTF-8 format are the only supported file types.
- This program has only been tested using English-language .txt files. Using .txt files in other languages may produce unreliable results.
- The v.40 script greatly increased program functionality by adding SQL support, but the current query features are not final. More will be added.
- Code modularity and error handling is currently undergoing review and improvement. Some functions may act unpredictably if users provide very unexpected input.
- UI is designed to enhance the user experience through consistency and color-coding. However, it is not in a final state and there may be areas in which formatting appears inconsistent.

### Usage
To install "requests", run the following command:
- "pip install requests"
To utilize the script, run the following command:
- "python main.py"

## Acknowledgements
Special thanks to Professor Charles Severance for his excellent "Python for Everybody" book and series on Coursera!

## Contact
Christopher Fowler - c.fowler00@yahoo.com

## Version History

### v.40
- Added SQL database support, enabling users to save word frequency analyses from multiple files at a time to a specified database.
- Added a range of database query options and the ability to save results to .csv files in the Reports subdirectory.
- Changed the Word Frequency Analysis to 'Quicklook Word Counts' and now allow for scanning multiple files at once.

### v.30
- Codebase split among four scripts (main.py, analysis.py, ui.py, ui_helpers.py) for easier code management.
- Word frequency engine overhauled using Regular Expressions - resulting in much more predictable results.
- Multiple functions were split into smaller sub-functions to improve modularity and management.
- Numerous UI improvements to improve user experience.

### v.20
- Codebase overhauled to incorporate error handling, Python functions, and docstrings.
- Support for .txt analysis from a URL.
- User menu added to expand utility of program.
- User-selectable number of words to display (no longer limited to 'Top 25').
- Settings menu allows for user-customizable filters by viewing and editing the commonwords.txt file.


### v.10
- Simple script which returns the word frequency of a user-specified .txt file and returns the top 25 most-frequent words.
- Filters words based on a hard-coded internal list of commonly-used words.
