# Import standard libraries
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Import local libraries
import ui_helpers

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
                 title=f'Top {top_n} words per document')

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
                 title=f'Top {top_n} words per document')

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