import sqlite3

def initialize_database():
    # Connect to the database
    conn = sqlite3.connect("youdata.db")
    cursor = conn.cursor()
    
    # Create the videos table 
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,           -- Unique identifier for the video
        name TEXT,                     -- Title of the video
        publication_date TEXT,         -- Publication date of the video
        description TEXT,              -- Description of the video
        views INTEGER,                 -- Number of views
        likes INTEGER,                 -- Number of likes
        comments INTEGER,              -- Number of comments
        channel TEXT,                  -- Channel name
        thumbnail TEXT                 -- URL of the thumbnail
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
