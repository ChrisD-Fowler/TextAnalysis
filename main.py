# Import local script modules
import ui
"""
TextAnalysis nalyzes text data to identify and display the frequency of words. 
It allows users to input text data from either local files or via URLs. Results can be
displayed either as total word counts or filtered to show only the most common words.

TextAnalysis v.70 Updates:
    - Word Count Analysis can now be loaded directly from URLs for multiple files.
    - TF-IDF Analysis can now be performed using two or more URLs - no need to download files anymore.
    - Added helpful instructions to most sub-screens. Revised others for clarity.
    - Streamlined the UI for a refined user experience: removed two options from Main Menu.
    - Improved file, data, and error handling throughout the program, especially in the analysis.py script.
    - Integrated a "Help for this page" option for Level 2 menus.

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
Date: 2024-06-04
"""

# Main program function
def main():
    ui.main_menu()

# Calls the 'main' function to run the program
if __name__ == '__main__': 
    main()