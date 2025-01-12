from googleapiclient.discovery import build
from db_utils import insert_video, fetch_videos_by_date, fetch_all_videos
from datetime import datetime, timedelta

def fetch_and_store_videos(channel_id, date):
 
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
                    date,
                    video["snippet"].get("description", ""),
                    int(video["statistics"].get("viewCount", 0)),
                    int(video["statistics"].get("likeCount", 0)),
                    int(video["statistics"].get("commentCount", 0)),
                    video["snippet"]["channelTitle"],
                    video["snippet"]["thumbnails"]["default"]["url"]
                )
                insert_video(video_data)

        print(f"Videos for {date} have been successfully stored in the database.")

    except Exception as e:
        print(f"An error occurred while fetching and storing videos: {e}")

def generate_report(channel_id, date):
    """
    Generates an Excel report of the top 10 videos for the given channel and date.
    """
    import pandas as pd

    # Fetch videos from the database
    videos = fetch_videos_by_date(date)

    if videos:
        # Create a DataFrame from the database results
        columns = ["ID", "Title", "Publication Date", "Description", "Views", "Likes", "Comments", "Channel", "Thumbnail"]
        df = pd.DataFrame(videos, columns=columns)
        df = df.sort_values(by="Views", ascending=False).head(10)

        file_name = f"top_videos_{date}.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Report generated: {file_name}")
    else:
        print("No videos found in the database for the specified date.")

def increment_date(date_str):
    """
    Increment the given date string by one day.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    next_date_obj = date_obj + timedelta(days=1)
    return next_date_obj.strftime("%Y-%m-%d")

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📊 Welcome to YouData! 🎥 ")
    print(f"Today is {today}")

    # Default channel ID (replaceable in configurations)
    channel_id = "UCsT4NSardFSUa0bokXXI6Fg"

    # Fetch and display today's top 10 videos
    print("\n🌟 Fetching today's top 10 videos... 🚀\n")
    fetch_and_store_videos(channel_id, today)

    videos = fetch_videos_by_date(today)
    if videos:
        videos = sorted(videos, key=lambda x: x[4], reverse=True)[:10]  # Sort by views
        print("Top 10 Videos Today:")
        print("")
        for idx, video in enumerate(videos, start=1):
            print(f"{idx}. {video[1]} - {video[4]} views ({today})")
    else:
        print("No videos found for today.")

    while True:
        print("\nYouData - Main Menu")
        print("1. Consult Top Videos by Date")
        print("2. Generate Excel Report by Date")
        print("3. Change Channel Configuration")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter the date (YYYY-MM-DD): ")
            fetch_and_store_videos(channel_id, date)

            videos = fetch_videos_by_date(date)
            if videos:
                videos = sorted(videos, key=lambda x: x[4], reverse=True)[:10]  # Sort by views
                print("Top 10 Videos:")
                for idx, video in enumerate(videos, start=1):
                    print(f"{idx}. {video[1]} - {video[4]} views ({date})")
            else:
                print("No videos found for the specified date.")

        elif choice == "2":
            date = input("Enter the date (YYYY-MM-DD): ")
            fetch_and_store_videos(channel_id, date)
            generate_report(channel_id, date)

        elif choice == "3":
            channel_id = configure_channel()

        elif choice == "4":
            print("Exiting YouData. Goodbye!")
            break

        else:
            print("Invalid choice. Please select an option from the menu.")

def configure_channel():
    new_channel_id = input("Enter the new channel ID: ")
    print(f"Channel ID updated to: {new_channel_id}")
    return new_channel_id

if __name__ == "__main__":
    main()
