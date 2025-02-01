import sqlite3

def initialize_database():
    # Connect to the database
    conn = sqlite3.connect("youdata.db")
    cursor = conn.cursor()

    # Create the channels table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        channel_id TEXT PRIMARY KEY,   -- Unique identifier for the channel
        youtube_id TEXT NOT NULL,     -- YouTube ID associated with the channel
        channel_name TEXT NOT NULL,   -- Name of the channel
        is_active INTEGER DEFAULT 0   -- Indicates if this channel is currently active
    )
    ''')

    # Create the videos table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id TEXT PRIMARY KEY,           -- Unique identifier for the video
        name TEXT,                     -- Title of the video
        views INTEGER,                 -- Number of views
        likes INTEGER,                 -- Number of likes
        comments INTEGER,              -- Number of comments
        publication_date TEXT,         -- Publication date of the video
        publication_hour TEXT,         -- Publication hour of the video
        description TEXT,              -- Description of the video
        thumbnail TEXT,                 -- URL of the thumbnail
        channel TEXT,                  -- Channel name
        youtube_id TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    initialize_database()
