# Import local script modules
import ui
"""
TextCrawl v.40 analyzes text data to identify and display the frequency of words. 
It allows users to input text data from either local files or via URLs. Results can be
displayed either as total word counts or filtered to show only the most common words.

Usage:
Run the script and follow the on-screen prompts to choose data sources and output preferences.

Features:
    - Word frequency analysis from files and URLs.
    - Interactive user interface for easy navigation.
    - Robust error handling for a smooth user experience.

Author: Christopher Fowler (c.fowler00@yahoo.com)
Date: 2024-05-02
"""

# Main program function
def main():
    ui.main_menu()

# Calls the 'main' function to run the program
if __name__ == '__main__': 
    main()
