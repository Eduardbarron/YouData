import sqlite3

DB_PATH = "youdata.db"

def insert_video(video_data):
    """
    Inserts a video record into the database.
    video_data: Tuple (id, name, views, likes, comments, publication_date, publication_hour, description, thumbnail, channel)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO videos (id, name, views, likes, comments, publication_date, publication_hour, description, thumbnail, channel)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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


def insert_channel(channel_data):
    """
    Inserts a channel record into the database.
    channel_data: Tuple (channel_id, youtube_id, channel_name, is_active)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT OR IGNORE INTO channels (channel_id, youtube_id, channel_name, is_active)
    VALUES (?, ?, ?, ?)
    ''', channel_data)
    conn.commit()
    conn.close()

def fetch_all_channels():
    """
    Fetches all channel records from the database.
    Returns a list of tuples containing channel data.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM channels')
    results = cursor.fetchall()
    conn.close()
    return results

def set_active_channel(channel_id):
    """
    Sets the active channel by updating the is_active flag.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE channels SET is_active = 0')  # Reset all channels to inactive
    cursor.execute('UPDATE channels SET is_active = 1 WHERE channel_id = ?', (channel_id,))
    conn.commit()
    conn.close()

def fetch_active_channel():
    """
    Fetches the currently active channel.
    Returns a tuple containing the active channel's data or None if no active channel exists.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM channels WHERE is_active = 1 LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result

