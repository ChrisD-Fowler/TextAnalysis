# Import standard libraries
import os
import sqlite3
import pandas as pd

# Import local library
import ui_helpers

# Builds a SQL database with user-defined name using the correct database schema
def database_build(database_name):
    """
    Builds database for storing text frequency analysis data.

    Schema is as follows:
    Documents
    doc_id (PK)
    doc_title
    author
    year

    Words
    word_id (PK)
    word

    WordCounts
    word_id (FK)
    doc_id (FK)
    count
    Note: word_id and doc_id are the composite primary key.

    Parameters:
    database_name - the name that will serve as the .sqlite database file name.

    Raises:
    sqlite3.OperationalError - for errors encountered while creating the database.
    sqlite3.DatabaseError - for errors encountered while creating the database.
    sqlite3.Error - for other unexpected sqlite3 errors.
    Exception - for all other unexpected errors.
    """
    # Moves to Databases folder, if necessary
    ui_helpers.move_to_databases()

    # SQL connection and cursor objects
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    
    # Create database, tables, and columns
    try:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Words (
            word_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            word VARCHAR(100) UNIQUE
        );            
        ''')
    
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Documents (
            doc_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            doc_title VARCHAR(105),
            author VARCHAR(75),
            year INTEGER        
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS WordCounts (
            word_id INTEGER,
            doc_id INTEGER,
            count INTEGER,
            PRIMARY KEY (word_id, doc_id),
            FOREIGN KEY (word_id) REFERENCES Words(word_id),
            FOREIGN KEY (doc_id) REFERENCES Documents(doc_id)
        );
        ''')
        conn.commit()

    except sqlite3.OperationalError as e:
        print(ui_helpers.RED + f'The following Operational Error occurred while creating the database: {e}' + ui_helpers.RESET)
    
    except sqlite3.DatabaseError as e:
        print(ui_helpers.RED + f'The following Database Error occurred while creating the database: {e}' + ui_helpers.RESET)
    
    except sqlite3.Error as e:
        print(ui_helpers.RED + f'The following SQLite3 error occurred while creating the database: {e}' + ui_helpers.RESET)

    except Exception as e:
        print(ui_helpers.RED + f'The following Exception occurred while creating the database: {e}' + ui_helpers.RESET)

    finally:
        conn.close()

# Adds data from the wordtally dict to the SQL database
def wordtally_to_database(wordtally_dict, database_name, doc_title, author, year):
    """
    Uses the wordtally dictionary to add to the specified SQLite database.

    Parameters:
    wordtally_dict - must be the dictionary that is returned by analysis.tally_words().
    database_name - the name of the database to which the dictionary results are added.
    doc_title - inserts into SQL as the title of the .txt document for corresponding words.
    author - inserts into SQL as the author of the .txt document for corresponding words.
    year - inserts into SQL as the year of publication for the .txt document for corresponding words.

    Raises:
    sqlite3.Error - for sqlite3 errors.
    Exception - for all other errors.
    """
    # Moves to Databases folder
    ui_helpers.move_to_databases()

    # SQL connection and cursor objects
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    try:
        # Adds user-specified document name, author, and year
        cur.execute('''
        INSERT INTO Documents (doc_title, author, year)
        VALUES (?, ?, ?)        
        ''', (doc_title, author, year))
        doc_id = cur.lastrowid

        # Checks if the word exists in Words table already; if not, insert
        for word in wordtally_dict:
            cur.execute('''
            INSERT INTO Words (word)
            VALUES (?)
            ON CONFLICT(word) DO NOTHING;
            ''', (word,))

        # SQL statement for insertion into WordCounts table
        sql_insertion = '''
        INSERT INTO WordCounts (word_id, doc_id, count) 
        VALUES ((SELECT word_id FROM Words WHERE word = ?), ?, ?)
        ON CONFLICT (word_id, doc_id) DO UPDATE SET count = count + EXCLUDED.count;
        '''

        for word, count in wordtally_dict.items():
            cur.execute(sql_insertion, (word, doc_id, count))

        conn.commit()

    except sqlite3.Error as e:
        print(ui_helpers.RED + f'The following SQLite3 error occurred while adding data to the database: {e}' + ui_helpers.RESET)

    except Exception as e:
        print(ui_helpers.RED + f'The following Exception occurred while adding data to the database: {e}' + ui_helpers.RESET)

    finally:
        conn.close()
    
# Summarizes SQL database
def summarize_database(database_name):
    """
    Summarizes the specified database using at-a-glance data to help users make query or management decisions.

    Parameters:
    database_name - the database to be summarized.
    """

    # Create objects for connecting to the database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Query unique author count
    cursor.execute("SELECT COUNT(DISTINCT author) FROM Documents;")
    sum_authors = cursor.fetchone()[0]

    # Query unique titles count
    cursor.execute("SELECT COUNT(DISTINCT doc_id) FROM Documents;")
    sum_titles = cursor.fetchone()[0]

    # Query publication year range of all titles
    cursor.execute("SELECT MIN(year), MAX(year) FROM Documents;")
    range_years = cursor.fetchone()

    # Query total number of words
    cursor.execute("SELECT COUNT(DISTINCT word_id) FROM WORDS;")
    total_words = cursor.fetchone()[0]

    # Close connection
    cursor.close()
    conn.close()

    # Get file size of the database
    db_size = os.path.getsize(database_name)

    print(ui_helpers.CYAN + '\nSummary of ' + ui_helpers.RESET + f'{database_name}:' + ui_helpers.RESET)
    print(ui_helpers.CYAN + 'Authors: ' + ui_helpers.RESET + f'{sum_authors}')
    print(ui_helpers.CYAN + 'Titles: ' + ui_helpers.RESET + f'{sum_titles}')
    print(ui_helpers.CYAN + 'Year Range: ' + ui_helpers.RESET + f'{range_years}')
    print(ui_helpers.CYAN + 'Unique Words: ' + ui_helpers.RESET + f'{total_words}')
    print(ui_helpers.CYAN + 'File Size: ' + ui_helpers.RESET + f'{db_size} bytes')

# Query most-used words over time
def query_most_used_words(database_name, start_year=-3000, end_year=2075, top_n=25):
    """
    Queries the specified database to return the most frequently used words over time. Supports user customization of three parameters. Users may save the result to a .csv file in Reports subdirectory.

    Parameters:
    database_name - the database to be queried.
    start_year - the earliest year in the database from which to query word counts. -3000 by default.
    end_year - the latest year in the database from which to query word counts. 2075 by default.
    top_n - the number of data rows to be returned by the query. 25 by default.

    Returns:
    df - the Pandas DataFrame
    """
    # Create objects for connecting to the database
    conn = sqlite3.connect(database_name)

    # Query database for most-used words over time
    query = """
        WITH TotalCounts AS (
        SELECT w.word, SUM(wc.count) AS grand_total
        FROM Words As w
        JOIN WordCounts AS wc ON w.word_id = wc.word_id
        JOIN Documents AS d ON wc.doc_id = d.doc_id
        WHERE d.year BETWEEN ? AND ?
        AND w.word IN (
            SELECT w2.word
            FROM Words AS w2
            JOIN WordCounts as wc2 on w2.word_id = wc2.word_id
            JOIN Documents AS d2 ON wc2.doc_id = d2.doc_id
            GROUP BY w2.word
            HAVING COUNT(DISTINCT d2.year) > 1
        )
        GROUP BY w.word
    )
    SELECT d.year, w.word, SUM(wc.count) AS total_count
    FROM Words as w
    JOIN WordCounts AS wc ON w.word_id = wc.word_id
    JOIN Documents AS d on wc.doc_id = d.doc_id
    JOIN TotalCounts AS tc ON w.word = tc.word
    WHERE d.year BETWEEN ? AND ?
    AND w.word IN (
        SELECT w2.word
        FROM Words AS w2
        JOIN WordCounts as wc2 on w2.word_id = wc2.word_id
        JOIN Documents AS d2 ON wc2.doc_id = d2.doc_id
        GROUP BY w2.word
        HAVING COUNT(DISTINCT d2.year) > 1
    )
    GROUP BY d.year, w.word
    ORDER BY tc.grand_total DESC, w.word, d.year, total_count
    LIMIT ?    
    """

    # Execute the query and load results as DataFrame
    df = pd.read_sql_query(query, conn, params=(start_year, end_year, start_year, end_year, top_n))

    # Close connection and Return Dataframe
    conn.close()
    return df

# Word Count Trends Over Time (By Author(s))
def query_most_used_words_by_author(database_name, start_year=-3000, end_year=2075, top_n=25):
    """
    Queries the specified database to return the most frequently used words by different authors over time. Supports user customization of three parameters. Users may save the result to a .csv file in Reports subdirectory.

    Parameters:
    database_name - the database to be queried.
    start_year - the earliest year in the database from which to query word counts. -3000 by default.
    end_year - the latest year in the database from which to query word counts. 2075 by default.
    top_n - the number of data rows to be returned by the query. 25 by default.

    Returns:
    df - the Pandas DataFrame
    """
    # Create objects for connecting to the database
    conn = sqlite3.connect(database_name)

    # Query database for most-used words over time
    query = """
    WITH TotalCounts AS (
        SELECT w.word, SUM(wc.count) AS grand_total
        FROM Words As w
        JOIN WordCounts AS wc ON w.word_id = wc.word_id
        JOIN Documents AS d ON wc.doc_id = d.doc_id
        WHERE d.year BETWEEN ? AND ?
        AND w.word IN (
            SELECT w2.word
            FROM Words AS w2
            JOIN WordCounts as wc2 on w2.word_id = wc2.word_id
            JOIN Documents AS d2 ON wc2.doc_id = d2.doc_id
            GROUP BY w2.word
            HAVING COUNT(DISTINCT d2.year) > 1
        )
        GROUP BY w.word
    )
    SELECT d.year, d.author, w.word, SUM(wc.count) AS total_count
    FROM Words as w
    JOIN WordCounts AS wc ON w.word_id = wc.word_id
    JOIN Documents AS d on wc.doc_id = d.doc_id
    JOIN TotalCounts AS tc ON w.word = tc.word
    WHERE d.year BETWEEN ? AND ?
    AND w.word IN (
        SELECT w2.word
        FROM Words AS w2
        JOIN WordCounts as wc2 on w2.word_id = wc2.word_id
        JOIN Documents AS d2 ON wc2.doc_id = d2.doc_id
        GROUP BY w2.word
        HAVING COUNT(DISTINCT d2.year) > 1
    )
    GROUP BY d.year, d.author, w.word
    ORDER BY tc.grand_total DESC, w.word, d.year, d.author, total_count
    LIMIT ?    
    """

    # Execute the query and load results as DataFrame
    df = pd.read_sql_query(query, conn, params=(start_year, end_year, start_year, end_year, top_n))

    # Close connection and Return Dataframe
    conn.close()
    return df

# Publications Over Time (By Author)
def publications_over_time_by_author(database_name, start_year=-3000, end_year=2075, max_authors=10):
    """
    Queries SQL Database to return the number of publications by each author over time.

    Parameters:
    database_name - Name of the database to query
    start_year - Starting year of range for SQL query
    end_year - Ending year of range for SQL query
    max_authors - Maximum number of authors to return in SQL query
    
    Returns:
    df - Pandas DataFrame for use by other functions (i.e., output as .csv).
    """

    # SQL Connection
    conn = sqlite3.connect(database_name)

    # SQL Query
    query = """
    SELECT d.year, d.author, COUNT(d.doc_title) AS publication_count
    FROM Documents AS d
    WHERE d.year BETWEEN ? AND ?
    GROUP BY d.year, d.author
    ORDER BY d.year ASC, d.author ASC
    LIMIT ?
    """

    # Execute query and load results as DataFrame
    df = pd.read_sql_query(query, conn, params=(start_year, end_year, max_authors))

    # Close connection and return DataFrame
    conn.close()
    return df

# Word(s) Lookup Over Time
def words_lookup_over_time(database_name, start_year=-3000, end_year=2075, word_list=None):
    """
    Queries the specified database to return the frequency of user-specified word(s) over time. Supports user customization of three parameters. Users may save the result to a .csv file in Reports subdirectory.

    Parameters:
    database_name - the database to be queried.
    start_year - the earliest year in the database from which to query word counts. -3000 by default.
    end_year - the latest year in the database from which to query word counts. 2075 by default.
    word_list - must be a list of words to be queried.

    Returns:
    df - the Pandas DataFrame
    """

    # Connect to SQL database
    conn = sqlite3.connect(database_name)

    # Prepare the word list for SQL query
    formatted_word_list = ', '.join(f"'{word}'" for word in word_list) if word_list else "'default_word'"

    # SQL Query
    query = f"""
    WITH TotalCounts AS (
        SELECT w.word, SUM(wc.count) AS grand_total
        FROM Words AS w
        JOIN WordCounts AS wc ON w.word_id = wc.word_id
        JOIN Documents AS d ON wc.doc_id = d.doc_id
        WHERE d.year BETWEEN ? AND ?
        AND w.word IN ({formatted_word_list})
        GROUP BY w.word
    )
    SELECT d.year, w.word, SUM(wc.count) AS total_count
    FROM Words AS w
    JOIN WordCounts AS wc ON w.word_id = wc.word_id
    JOIN Documents AS d ON wc.doc_id = d.doc_id
    JOIN TotalCounts as tc ON w.word = tc.word
    WHERE d.year BETWEEN ? AND ?
    AND w.word IN ({formatted_word_list})
    GROUP BY d.year, w.word
    ORDER BY tc.grand_total DESC, w.word, d.year
    """

    # Execute the query and load as Pandas DataFrame
    df = pd.read_sql_query(query, conn, params=(start_year, end_year, start_year, end_year))

    # Close connection and return DataFrame
    conn.close()
    return df