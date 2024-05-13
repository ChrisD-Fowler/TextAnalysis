# Import standard libraries
import os
import re
import pandas as pd
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px

# Import local libraries
import ui_helpers

# Create a dashboard using Dash
def create_tf_idf_dash(tfidf_df, final_metadata, top_n=25):
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