# TextAnalysis v.70

TextAnalysis is a Python application that analyzes text data to identify and display the frequency of words. It allows users to input text data from either local files or via URLs. The results can be displayed either as total word counts or filtered to show only the most common words. Results may be added to a SQL database and queries may be generated to provide insight into the data (i.e., word use changes over time, etc.). 

Additionally, the results of Word Count and TF-IDF Analyses may be exported as .txt or .csv files and later re-imported from within the program, enabling session-to-session continuity. SQL Queries may also be exported (these queries may not be re-imported, however).

## Features
- **Word Frequency Analysis**: Analyze text files to find and count the most frequent words, excluding common words like 'the', 'is', etc.
- **TF-IDF Analysis**: Term Frequency - Inverse Document Analysis measures word importance between two or more documents by balancing the raw counts of a word (TF) with the total number of documents analyzed (IDF). As a word is used more in a given document than it is in the others, the score is increased, revealing which words make each document unique.
- **SQLite Support**: Users may save results of word frequency analysis to database and execute database queries, which may be saved as .csv files. These custom databases may then be used for various SQL queries or TF-IDF analysis and reporting.
- **Visualization Tools** Users may export Word Count and TF-IDF Analyses DataFrames into custom bar charts, quickly displaying the most significant words in each document or set of documents.
- **Interactive Dashboard**: Using Dash and Plotly, users may export the results of TF-IDF analysis to an interactive dashboard, enabling quick insight into each document's composition and uniqueness.
- **Support for Local and Web Text Files**: Load text data from local files or directly from URLs.
- **Interactive User Interface**: Simple and intuitive command-line interface for easy navigation and usage.
- **Powerful DataFrame Transformation**: Users may set value thresholds, perform word searches, remove specific words, truncate, and export DataFrames as desired - before displaying to charts or exporting to .csv or .txt reports.
- **User Customization**: Users may define which words to filter, conduct word search queries.
- **Robust Error Handling**: Includes detailed error handling to ensure a smooth user experience.

### Prerequisites
- Python 3.8 or higher.
- Python Libraries: pandas, sklearn, Dash, plotly.express, sqlite3, requests.
- 'Textfiles' subdirectory containing at least one .txt file or a direct URL for a .txt file (for basic Word Frequency function).
- 'Textfiles' subdirectory containing two or more .txt files or two or more URLs are required to run TF-IDF Analysis.
- (Optional) DB Browser or other SQLite viewing tool for viewing databases outside of TextAnalysis.

## Limitations
- This script was built and tested on a Windows 11 PC. Using on a platform other than Windows 10 may result in colors or other features not displaying or executing properly.
- Text files in UTF-8 format are the only supported file types. While URLs to HTML pages may work, users may find a lot of undesired HTML code included in Word Count or TF-IDF Analysis (these may be filtered manually via commonwords.txt or DataFrame Transformation).
- This program has only been tested using English-language .txt files. Using .txt files in other languages may produce unreliable results.
- The v.40 script greatly increased program functionality by adding SQL support, but the current query features are not final. More will be added.
- Code modularity and error handling is currently undergoing review and improvement. Some functions may act unpredictably if users provide very unexpected input.
- UI is designed to enhance the user experience through consistency and color-coding. However, it is not in a final state and there may be areas in which formatting appears inconsistent.

## Acknowledgements
Special thanks to Professor Charles Severance for his excellent "Python for Everybody" book and series on Coursera!

## Contact
Christopher Fowler - c.fowler00@yahoo.com

## Version History

### v.70
- TextCrawl is not TextAnalysis!
- Word Count Analysis can now be loaded directly from URLs for multiple files.
- TF-IDF Analysis can now be performed using two or more URLs - no need to download files anymore.
- Added helpful instructions to most sub-screens. Revised others for clarity.
- Streamlined the UI for a refined user experience: removed two options from Main Menu.
- Improved file, data, and error handling throughout the program, especially in the analysis.py script.
- Integrated a "Help for this page" option for Level 2 menus.

### v.60
- Added Word Count Analysis DataFrame Manipulation Menu, enabling users to alter the results of a Word Count Analysis before exporting to reports or creating visuals.'
- Added specific word removal and "Keep Bottom N Words" options for both types of DataFrames.
- Reports are better organized and may now be used to load Word Count Analysis or TF-IDF DataFrames.
- Added Bar Charts for Word Count and TF-IDF Analysis DataFrames
- Word Count Analysis may be loaded directly into a DataFrame without first exporting to SQLite.
- Expanded DataFrame status bar to include Word Count Analysis DataFrame. This status bar is now a persistent header.
- Added menu tree status below DataFrame status bar, enhancing user awareness of menu tree location at all times.

- Numerous bugfixes and performance improvements:
  - Fixed SQL Database Build error which resulted in "Year" and "Genre" confusion during input.
  - Improved error handling when users make selections out of range.
  - Numerous modules have been split, improving code management and efficiency.

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
