# Import local script modules
import ui
"""
TextCrawl nalyzes text data to identify and display the frequency of words. 
It allows users to input text data from either local files or via URLs. Results can be
displayed either as total word counts or filtered to show only the most common words.

TextCrawl v.50 anow features:
- Term Frequency - Inverse Document Frequency (TF-IDF) Analysis: find the words which most distinguish one document from another, providing insight into word counts beyond a simple tally. Users may manipulate the DataFrame to set threshold, display top N scores, and perform word searches.
- Visualization: Display the results of TF-IDF Analysis using an interactive bar chart showing Top N terms per document by TF-IDF score.

Usage:
Run the script and follow the on-screen prompts to choose data sources and output preferences.

Features:
    - Word frequency analysis from files and URLs.
    - TF-IDF Score Analysis.
    - DataFrame manipulation options.
    - User-selectable word searches and filtering options.
    - Full SQL integration offers efficient data storage and repeatable queries.
    - Interactive user interface for easy navigation.
    - Robust error handling for a smooth user experience.

Author: Christopher Fowler (c.fowler00@yahoo.com)
Date: 2024-05-13
"""

# Main program function
def main():
    ui.main_menu()

# Calls the 'main' function to run the program
if __name__ == '__main__': 
    main()