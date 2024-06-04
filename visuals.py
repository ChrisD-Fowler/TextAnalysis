# Import standard libraries
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Import local libraries
import ui_helpers
  
# Display word count
def display_word_frequency(filename, wordtally_dict, number_to_list):
    """
    This function uses the dictionary created in the tally_words function along with a user-defined number of words to list and displays the results of the .txt file word frequency count.

    Parameters:
    filename - the name of the file processed.
    wordtally_dict - must be the wordtally_dict{} returned by the tally_words function.
    number_to_list - typically a user-defined number of the top words to list (if user enters no value, all words will be displayed).

    Returns:
    wordtally_dict - the original wordtally dictionary (to be used by other functions)
    sorted_list - the list which displays the results of the tallying in order from greatest to smallest as of v.30.

    Raises:
    Exception for unexpected errors.
    """

    # Checks if wordtally_dict contains data
    if wordtally_dict is None:
        print(ui_helpers.RED + 'Error: expected a dictionary but got None' + ui_helpers.RESET)
        return
    
    try:
        # Preparing a list from the wordtally_dict dictionary
        tallied_list = list(wordtally_dict.items())
        sorted_list = sorted(tallied_list, key=lambda item:item[1], reverse=True)

        # Displays user-defined number of words (or all words)
        if number_to_list == '':
            top_count_words = sorted_list
        else:
            top_count_words = sorted_list[:number_to_list]

        # Prints the 'Top N Words' list
        print(ui_helpers.CYAN + '\n\nFILE: ' + ui_helpers.RESET + f'{filename}')
        print(ui_helpers.CYAN + '\nRank ) Word - Count\n' + '_'*19 + '\n' + ui_helpers.RESET)
        for index, (word, count) in enumerate(top_count_words, start=1):
            print(f'{index}' + ') ' f'{word[0].upper()}{word[1:]} - {count}')

            # Pauses execution for user input when printing large result set
            if index % 2500 == 0:
                input(ui_helpers.YELLOW + '\nDisplayed 2,500 results! Press Enter to continue...' + ui_helpers.RESET)

        return(wordtally_dict, sorted_list)
    
    except Exception as e:
        print(ui_helpers.RED + f'An error occurred while trying to display the word count: {e}' + ui_helpers.RESET)

# Create a dashboard for a TF-IDF DataFrame using Dash
def create_tf_idf_dash(tfidf_df, final_metadata, top_n=5):
    """
    Creates an interactive dashboard with bar chart based off a user's TF-IDF DataFrame.

    Parameters:
    tfidf_df - the user's TF-IDF DataFrame containing all TF-IDF scores.
    final_metadata - a list of dictionaries containing metadata from all text documents or SQL database
    top_n - an integer to determine how many 'top words' to show.
    """

    ui_helpers.move_to_parent()
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1('Text Analysis Dashboard - TF-IDF Scores'),
        dcc.Dropdown(
            id='document-dropdown',
            options=[{'label' : i, 'value' : i,} for i in tfidf_df.index],
            value=tfidf_df.index[0],
            clearable=False
        ),
        dcc.Graph(id='top-words-graph'),
        html.Div(id='document-metadata')
    ])

    @app.callback(
        [Output('top-words-graph', 'figure'),
        Output('document-metadata', 'children')],
        [Input('document-dropdown', 'value')]
        )
    
    def update_metrics(selected_document):
        """
        Displays the chart's data, including file metadata.
        """
        data = tfidf_df.loc[selected_document]
        
        # Top N Words by TF-IDF scores
        top_words = data.nlargest(top_n)

        # Figure to display Top TF-IDF scores
        fig = px.bar(top_words, 
                     x=top_words.values,
                     y=top_words.index, 
                     labels={'index':'Words', 
                             'x':'TF-IDF Score'}, 
                     title=f'Top {top_n} Words by TF-IDF', 
                     orientation='h')

        # Get metadata for selected document
        meta = final_metadata[selected_document]
        metadata_text = f'Title: {meta['doc_title']}, Author: {meta['author']}, Year: {meta['year']}, Genre: {meta['genre']}'

        return fig, f'{metadata_text}'

    app.run_server(debug=True)
    return tfidf_df, final_metadata

# Create a Bar Chart for a TF-IDF DataFrame
def create_counts_barchart(word_counts_df, top_n=5):
    """
    Creates a bar chart using plotly and saves to the 'Visuals' subdirectory. Sorts by Document and Total Count scores, grouping identical words with varying colors to show different documents.

    Note: Due to chart clutter, using smaller values for 'top_n' may be desired, especially when sourcing a high number of documents.

    Parameters:
    word_counts_df - the DataFrame containing all Word Count scores
    top_n - the number of words to plot, sorted by high score
    """
    # Moves to Visuals subdirectory
    ui_helpers.move_to_visuals()

    # List to store DataFrames for Top N words per Document (row)
    top_n_words_dfs = []

    # Iterate through each row to find Top N words per document
    for row_index, row in word_counts_df.iterrows():
        # Get Top N words for current document
        top_n_words = row.nlargest(top_n)
        # Add the document identifier
        top_n_words_df = pd.DataFrame(top_n_words).reset_index()
        top_n_words_df.columns = ['Word', 'Counts']
        top_n_words_df['Document'] = row_index
        top_n_words_dfs.append(top_n_words_df)

    # Combines the DataFrames for all documents
    combined_df = pd.concat(top_n_words_dfs)

    # Create column for sorting words by document (much better bar plot grouping this way)
    combined_df['Words by Document'] = combined_df['Word']

    # Plot the the bar chart
    fig = px.bar(combined_df, 
                 x='Words by Document', 
                 y='Counts', 
                 color='Document', 
                 barmode='group', 
                 title='Word Counts per Document')

    # User inputs file name
    filename = input(ui_helpers.YELLOW + 'Enter name for .png barchart: ' + ui_helpers.RESET)

    # Sets default name if none entered
    if len(filename) < 1:
        filename = 'word_counts_barchart.png'
        print(ui_helpers.YELLOW + 'No name entered! Bar chart will be saved as ' +
               ui_helpers.RESET + f'{filename}')
    
    if not filename.endswith('.png'):
        filename += '.png'

    fig.write_image(filename)

    print(ui_helpers.YELLOW + 'Save complete! Please navigate to your "Visuals" subdirectory to view your bar chart.' + ui_helpers.RESET)
    input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)
    
    return 

# Create a Bar Chart for a TF-IDF DataFrame
def create_tf_idf_barchart(tfidf_df, top_n=5):
    """
    Creates a bar chart using plotly and saves to the 'Visuals' subdirectory. Sorts by Document and TF-IDF scores, grouping identical words with varying colors to show different documents.

    Note: Due to chart clutter, using smaller values for 'top_n' may be desired, especially when sourcing a high number of documents.

    Parameters:
    tfidf_df - the DataFrame containing all TF-IDF scores
    top_n - the number of words to plot, sorted by high score
    """
    # Moves to Visuals subdirectory
    ui_helpers.move_to_visuals()

    # List to store DataFrames for Top N words per Document (row)
    top_n_words_dfs = []

    # Iterate through each row to find Top N words per document
    for row_index, row in tfidf_df.iterrows():
        # Get Top N words for current document
        top_n_words = row.nlargest(top_n)
        # Add the document identifier
        top_n_words_df = pd.DataFrame(top_n_words).reset_index()
        top_n_words_df.columns = ['Word', 'TF-IDF Score']
        top_n_words_df['Document'] = row_index
        top_n_words_dfs.append(top_n_words_df)

    # Combines the DataFrames for all documents
    combined_df = pd.concat(top_n_words_dfs)

    # Create column for sorting words by document (much better bar plot grouping this way)
    combined_df['Words by Document'] = combined_df['Word']

    # Plot the the bar chart
    fig = px.bar(combined_df, 
                 x='Words by Document', 
                 y='TF-IDF Score', 
                 color='Document', 
                 barmode='group', 
                 title='TF-IDF Word Scores per Document')

    # User inputs file name
    filename = input(ui_helpers.YELLOW + 'Enter name for .png barchart: ' + ui_helpers.RESET)

    # Sets default name if none entered
    if len(filename) < 1:
        filename = 'tfidf_df_barchart.png'
        print(ui_helpers.YELLOW + 'No name entered! Bar chart will be saved as ' +
               ui_helpers.RESET + f'{filename}')
    
    if not filename.endswith('.png'):
        filename += '.png'

    fig.write_image(filename)

    print(ui_helpers.YELLOW + 'Save complete! Please navigate to your "Visuals" subdirectory to view your bar chart.' + ui_helpers.RESET)
    input(ui_helpers.YELLOW + '\nPress Enter to continue...' + ui_helpers.RESET)
    
    return 