# TextCrawl v.50

TextCrawl is a Python application that analyzes text data to identify and display the frequency of words. It allows users to input text data from either local files or via URLs. The results can be displayed either as total word counts or filtered to show only the most common words. Results may be added to a SQL database and queries may be generated to provide insight into the data (i.e., word use changes over time, etc.).

## Features
- **Word Frequency Analysis**: Analyze text files to find and count the most frequent words, excluding common words like 'the', 'is', etc.
- **TF-IDF Analysis**: Term Frequency - Inverse Document Analysis measures word importance between two or more documents by balancing the raw counts of a word (TF) with the total number of documents analyzed (IDF). As a word is used more in a given document than it is in the others, the score is increased, revealing which words make each document unique.
- **SQLite Support**: Users may save results of word frequency analysis to database and execute database queries, which may be saved as .csv files. These custom databases may then be used for various SQL queries or TF-IDF analysis and reporting.
- **Interactive Dashboard**: Using Dash and Plotly, users may export the results of TF-IDF analysis to an interactive dashboard, enabling quick insight into each document's composition and uniqueness.
- **Support for Local and Web Text Files**: Load text data from local files or directly from URLs.
- **Interactive User Interface**: Simple and intuitive command-line interface for easy navigation and usage.
- **User Customization**: Users may define which words to filter, conduct word search queries, and manipulate DataFrames directly to organize and extract the data they need.
- **Robust Error Handling**: Includes detailed error handling to ensure a smooth user experience.

### Prerequisites
- Python 3.8 or higher.
- Python Libraries: pandas, sklearn, Dash, plotly.express, sqlite3 requests.
- 'Textfiles' subdirectory containing at least one .txt file or a direct URL for a .txt file (for basic Word Frequency function).
- 'Textfiles' subdirectory containing two or more .txt files are required to run TF-IDF Analysis.
- (Optional) DB Browser or other SQLite viewing tool for viewing databases outside of TextCrawl.

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

### v.50
- Added numerous SQL queries, enabling users to generate reports from database showing word counts by year, document, author, genre, and more.
- TF-IDF Analysis function, enabling users to create a DataFrame with statistical rankings per word by document.
- Visualizations menu allows users to display the results of TF-IDF analysis on an interactive bar chart.

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
