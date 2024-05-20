# Import local script modules
import ui
"""
TextCrawl nalyzes text data to identify and display the frequency of words. 
It allows users to input text data from either local files or via URLs. Results can be
displayed either as total word counts or filtered to show only the most common words.

TextCrawl v.60 now features:
- Added Word Count Analysis DataFrame Manipulation Menu, enabling users to alter the results of a Word Count Analysis before exporting to reports or creating visuals.'
- Added specific word removal and "Keep Bottom N Words" options for both types of DataFrames.
- Reports are better organized and may now be used to load Word Count Analysis or TF-IDF DataFrames.
- Added Bar Charts for Word Count and TF-IDF Analysis DataFrames
- Word Count Analysis may be loaded directly into a DataFrame without first exporting to SQLite.
- Expanded DataFrame status bar to include Word Count Analysis DataFrame. This status bar is now a persistent header.
- Added menu tree status below DataFrame status bar, enhancing user awareness of menu tree location at all times.

Numerous bugfixes and performance improvements:
- Fixed SQL Database Build error which resulted in "Year" and "Genre" confusion during input.
- Improved error handling when users make selections out of range.
- Numerous modules have been split, improving code management and efficiency.

Usage:
Run the script and follow the on-screen prompts to choose data sources and output preferences.

Features:
    - Word Count analysis from files and URLs.
    - TF-IDF Score Analysis.
    - Powerful DataFrame manipulation options.
    - User-selectable word searches and filtering options.
    - Report export/import options enable continuity between sessions.
    - Full SQL integration offers efficient data storage and repeatable queries.
    - Interactive user interface for easy navigation.
    - Robust error handling for a smooth user experience.

Author: Christopher Fowler (c.fowler00@yahoo.com)
Date: 2024-05-20
"""

# Main program function
def main():
    ui.main_menu()

# Calls the 'main' function to run the program
if __name__ == '__main__': 
    main()