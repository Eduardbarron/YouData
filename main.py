from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from utils import select_time_frame, generate_table
from db_utils import insert_video, fetch_videos_by_date, fetch_all_videos, insert_channel, fetch_all_channels, set_active_channel, fetch_active_channel

def fetch_and_store_videos(channel_id, date):
    """
    Fetches videos from the given channel for a specific date and stores them in the database.
    """
    API_KEY = "AIzaSyCLLrmj7wz7_HqdfXIsGc1C51Ci0UFq0QQ"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    try:
        # Search videos uploaded on the specified date by the channel
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            publishedAfter=f"{date}T00:00:00Z",
            publishedBefore=f"{date}T23:59:59Z",
            maxResults=50
        )
        response = request.execute()

        for item in response.get("items", []):
            video_id = item["id"].get("videoId")
            if not video_id:
                continue

            video_details = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            for video in video_details.get("items", []):
                video_data = (
                    video["id"],
                    video["snippet"]["title"],
                    int(video["statistics"].get("viewCount", 0)),
                    int(video["statistics"].get("likeCount", 0)),
                    int(video["statistics"].get("commentCount", 0)),
                    date,
                    video["snippet"]["publishedAt"].split("T")[1][:5],
                    video["snippet"].get("description", ""),
                    video["snippet"]["thumbnails"]["default"]["url"],
                    video["snippet"]["channelTitle"]
                )
                insert_video(video_data)

        print(f"Videos for {date} have been successfully stored in the database.")

    except Exception as e:
        print(f"An error occurred while fetching and storing videos: {e}")

def download_data(channel_id):
    """
    Handles the downloading of video data for a user-defined time frame.
    """
    dates = select_time_frame()
    if dates:
        for date in dates:
            print(f"Downloading data for {date}...")
            fetch_and_store_videos(channel_id, date)
        print("Download complete.")
    else:
        print("No valid dates selected.")

def generate_report(date):
    """
    Generates an Excel report of the top 10 videos for the given date.
    """
    # Fetch videos from the database
    videos = fetch_videos_by_date(date)

    if videos:
        # Create a DataFrame from the database results
        columns = ["ID", "Title", "Views", "Likes", "Comments", "Publication Date", "Publication Hour", "Description", "Thumbnail", "Channel"]
        df = pd.DataFrame(videos, columns=columns)
        df = df.sort_values(by="Views", ascending=False).head(10)

        file_name = f"top_videos_{date}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Report generated: {file_name}")
    else:
        print("No videos found in the database for the specified date.")


def configure_channel():
    """
    Manages channel configurations: add, change, or set active channel.
    """
    while True:
        print("\nChannel Configuration Menu")
        print("1. Add New Channel")
        print("2. List All Channels")
        print("3. Set Active Channel")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            channel_id = input("Enter the new channel ID: ")
            youtube_id = input("Enter the YouTube ID: ")
            channel_name = input("Enter the channel name: ")
            insert_channel((channel_id, youtube_id, channel_name, 0))
            print(f"Channel '{channel_name}' added successfully.")

        elif choice == "2":
            channels = fetch_all_channels()
            if channels:
                print("\nChannels:")
                for idx, channel in enumerate(channels, start=1):
                    print(f"{idx}. {channel[2]} (ID: {channel[0]})")
            else:
                print("No channels found.")

        elif choice == "3":
            channels = fetch_all_channels()
            if channels:
                print("\nAvailable Channels:")
                for idx, channel in enumerate(channels, start=1):
                    print(f"{idx}. {channel[2]} (ID: {channel[0]})")
                selected = int(input("Select a channel by number: ")) - 1
                if 0 <= selected < len(channels):
                    set_active_channel(channels[selected][0])
                    print(f"Active channel set to: {channels[selected][2]}.")
                else:
                    print("Invalid selection.")
            else:
                print("No channels available. Please add a channel first.")

        elif choice == "4":
            print("Exiting channel configuration.")
            break

        else:
            print("Invalid choice. Please try again.")

def display_yesterday_top_videos():
    """
    Fetches and displays the top 10 videos from yesterday, ranked by views/hour.
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    videos = fetch_videos_by_date(yesterday)

    if not videos:
        print("No data for yesterday. Please download data first.")
        return

    ranked_videos = []
    for video in videos:
        publication_time = datetime.strptime(f"{video[5]} {video[6]}", "%Y-%m-%d %H:%M")
        elapsed_hours = (datetime.now() - publication_time).total_seconds() / 3600
        if elapsed_hours > 0:
            views_per_hour = video[2] / elapsed_hours
            ranked_videos.append((video[1], views_per_hour))

    ranked_videos.sort(key=lambda x: x[1], reverse=True)
    print("\n🚀 Top 10 Videos from Yesterday by Views/Hour:")
    print()
    for idx, (title, vph) in enumerate(ranked_videos[:10], start=1):
        print(f"{idx}. {title} - {vph:.2f} views/hour")


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📊 Welcome to YouData! Today is {today}.")

    active_channel = fetch_active_channel()
    if active_channel:
        print()
        print(f"🎥 Active Channel: {active_channel[2]}")
    else:
        print("No active channel. Please configure a channel.")

    display_yesterday_top_videos()

    while True:
        print("\n🤖 YouData - Main Menu")
        print()
        print("1. Download Video Data")
        print("2. Consult Top Videos by Date")
        print("3. Generate Excel Report by Date")
        print("4. Change Channel Configuration")
        print("5. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            if active_channel:
                date = input("Enter the date to download data for (YYYY-MM-DD): ")
                fetch_and_store_videos(active_channel[1], date)
            else:
                print("No active channel. Please configure a channel first.")

        elif choice == "2":
            date = input("Enter the date to consult (YYYY-MM-DD): ")
            videos = fetch_videos_by_date(date)
            if videos:
                videos = sorted(videos, key=lambda x: x[2], reverse=True)[:10]  # Sort by views
                print("\nTop 10 Videos:")
                for idx, video in enumerate(videos, start=1):
                    print(f"{idx}. {video[1]} - {video[2]} views")
            else:
                print("No videos found for the specified date.")

        elif choice == "3":
            date = input("Enter the date to generate a report for (YYYY-MM-DD): ")
            generate_report(date)

        elif choice == "4":
            configure_channel()

        elif choice == "5":
            print("Exiting YouData. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")

if __name__ == "__main__":
    main()
