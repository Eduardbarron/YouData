from googleapiclient.discovery import build

API_KEY = "AIzaSyCLLrmj7wz7_HqdfXIsGc1C51Ci0UFq0QQ"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def test_api_connection(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_api_connection("Qtcvtze8k4g")  # Replace with a valid YouTube video ID
