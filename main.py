from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta
import sqlite3
from utils import select_time_frame, generate_table
from db_utils import insert_video, delete_channel, fetch_videos_by_date, fetch_all_videos, insert_channel, fetch_all_channels, set_active_channel, fetch_active_channel

def fetch_and_store_videos(youtube_id, date):
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
            channelId=youtube_id,
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
                    video["snippet"]["channelTitle"],
                    youtube_id
                )
                insert_video(video_data)

        print(f"Videos for {date} have been successfully stored in the database.")

    except Exception as e:
        print(f"An error occurred while fetching and storing videos: {e}")
def download_data(youtube_id):
    """
    Handles the downloading of video data for a user-defined time frame.
    """
    print("\nStarting data download process...")
    dates = select_time_frame()  # This should show the selection menu
    if dates:
        for date in dates:
            print(f"Downloading data for {date}...")
            fetch_and_store_videos(youtube_id, date)
        print("Download complete.")
    else:
        print("No valid dates selected. Returning to main menu.")

def generate_report(date):
    """
    Generates an Excel report of the top 10 videos for the given date.
    """
    # Fetch videos from the database
    active_channel = fetch_active_channel()
    if not active_channel:
        print("No active channel. Please configure a channel.")
        return

    youtube_id = active_channel[1]
    videos = fetch_videos_by_date(date, youtube_id)

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
    Manages channel configurations: add, change, delete, or set active channel.
    """
    while True:
        print("\nChannel Configuration Menu")
        print("1. Add New Channel")
        print("2. List All Channels")
        print("3. Set Active Channel")
        print("4. Delete a Channel")
        print("5. Exit")
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
            channels = fetch_all_channels()
            if channels:
                print("\nAvailable Channels:")
                for idx, channel in enumerate(channels, start=1):
                    print(f"{idx}. {channel[2]} (ID: {channel[0]})")
                selected = int(input("Select a channel to delete by number: ")) - 1
                if 0 <= selected < len(channels):
                    channel_id = channels[selected][0]
                    delete_channel(channel_id)
                    print(f"Channel '{channels[selected][2]}' and its associated data have been deleted.")
                else:
                    print("Invalid selection.")
            else:
                print("No channels available to delete.")

        elif choice == "5":
            print("Exiting channel configuration.")
            break

        else:
            print("Invalid choice. Please try again.")

def display_yesterday_top_videos():
    """
    Fetches and displays the top 10 videos from yesterday, ranked by views/hour.
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    active_channel = fetch_active_channel()

    # Ensure there's an active channel
    if not active_channel:
        print("\nNo active channel. Please configure a channel.")
        return

    youtube_id = active_channel[1]  # Fetch active channel's YouTube ID
    videos = fetch_videos_by_date(yesterday, youtube_id)

    # Ensure videos exist for yesterday
    if not videos:
        print("\nNo data for yesterday. Please download data first.")
        return

    ranked_videos = []
    for video in videos:
        # Extract publication date and time
        publication_date = video[5]  # publication_date
        publication_hour = video[6]  # publication_hour
        publication_time = datetime.strptime(f"{publication_date} {publication_hour}", "%Y-%m-%d %H:%M")

        # Calculate elapsed hours since publication
        elapsed_hours = (datetime.now() - publication_time).total_seconds() / 3600
        if elapsed_hours > 0:  # Avoid division by zero
            views_per_hour = video[2] / elapsed_hours  # video[2] is `views`
            ranked_videos.append((video[1], views_per_hour))  # video[1] is `name`

    # Sort videos by views/hour in descending order
    ranked_videos.sort(key=lambda x: x[1], reverse=True)

    # Display the top 10 videos
    print("\n🚀 Top 10 Videos from Yesterday by Views/Hour:")
    print()
    for idx, (title, vph) in enumerate(ranked_videos[:10], start=1):
        print(f"{idx}. {title} - {vph:.2f} views/hour")

def main():

    while True:
            
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"\n📊 Welcome to YouData! Today is {today}.")

        active_channel = fetch_active_channel()
        if active_channel:
            print(f"\n🎥Active Channel: {active_channel[2]} (YouTube ID: {active_channel[1]})")
        else:
            print("\nNo active channel. Please configure a channel.")

        display_yesterday_top_videos()

        print("\n🤖 YouData - Main Menu")
        print("\n1. Download Video Data")
        print("2. Consult Top Videos by Date")
        print("3. Generate Excel Report by Date")
        print("4. Change Channel Configuration")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            if active_channel:
                download_data(active_channel[1])
            else:
                print("No active channel. Please configure a channel first.")

        elif choice == "2":
            dates = select_time_frame()
            if dates:
                all_videos = []
                for date in dates:
                    videos = fetch_videos_by_date(date, active_channel[0])
                    if videos:
                        all_videos.extend(videos)

                if all_videos:
                    generate_table(all_videos, columns=[0, 1, 2], summary=True)
                else:
                    print("No videos found for the selected dates.")
            else:
                print("No valid date selected.")

        elif choice == "3":
            dates = select_time_frame()
            if dates:
                for date in dates:
                    generate_report(date)
            else:
                print("No valid dates selected.")

        elif choice == "4":
            configure_channel()

        elif choice == "5":
            print("Exiting YouData. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")

if __name__ == "__main__":
    main()
