import sqlite3

DB_PATH = "youdata.db"

def insert_video(video_data):
    """
    Inserts a video record into the database.
    video_data: Tuple (id, name, publication_date, description, views, likes, comments, channel, thumbnail)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO videos (id, name, publication_date, description, views, likes, comments, channel, thumbnail)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', video_data)
    conn.commit()
    conn.close()

def fetch_videos_by_date(publication_date):
    """
    Fetches all videos published on a specific date.
    publication_date: Date in the format "YYYY-MM-DD".
    Returns a list of tuples containing video data.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos WHERE publication_date = ?', (publication_date,))
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_all_videos():
    """
    Fetches all video records from the database.
    Returns a list of tuples containing all video data.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM videos')
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Example usage of the functions
    sample_video = ("12345", "Sample Video", "2025-01-08", "This is a description", 1000, 100, 50, "Sample Channel", "https://example.com/thumbnail.jpg")
    insert_video(sample_video)

    print("Videos on 2025-01-08:", fetch_videos_by_date("2025-01-08"))
    print("All videos:", fetch_all_videos())
