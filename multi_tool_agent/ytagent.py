from googleapiclient.discovery import build
from google.adk.agents import Agent

YOUTUBE_API_KEY = AIzaSyCyOiCrzuer1OL7r2zmyGxoHu22SRoFgkk

def search_youtube_videos(query: str, max_results: int = 5) -> dict:
    """
    Searches for YouTube videos based on the provided query.

    Args:
        query (str): The search query for YouTube.
        max_results (int): Maximum number of results to return (default: 5).

    Returns:
        dict: Contains status and either video results or error message.
    """
    try:
        if not YOUTUBE_API_KEY:
            return {
                "status": "error",
                "error_message": "YouTube API key not configured."
            }

        # Create YouTube API client
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        # Execute search request
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=max_results,
            type='video'
        ).execute()

        # Extract video information
        videos = []
        for item in search_response.get('items', []):
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail = item['snippet']['thumbnails']['medium']['url']
            channel = item['snippet']['channelTitle']
            published_at = item['snippet']['publishedAt']

            videos.append({
                'videoId': video_id,
                'title': title,
                'description': description,
                'thumbnail': thumbnail,
                'channel': channel,
                'publishedAt': published_at,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })

        return {
            "status": "success",
            "videos": videos
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error searching YouTube: {str(e)}"
        }

def generate_video_description(query: str, videos: List[Dict[str, str]]) -> dict:
    """
    Generates a summary description about the search query and found videos.

    Args:
        query (str): The original search query.
        videos (List[Dict[str, str]]): List of found videos.

    Returns:
        dict: Contains status and generated description.
    """
    try:
        if not videos:
            return {
                "status": "error",
                "error_message": f"No videos found for '{query}'."
            }

        channels = set(video['channel'] for video in videos)
        channel_str = ", ".join(list(channels)[:3])
        if len(channels) > 3:
            channel_str += ", and others"

        description = (
            f"I found {len(videos)} videos about '{query}'. "
            f"These include content from {channel_str}. "
            f"The videos cover various aspects of {query}. "
            f"You can click on any video link to watch it on YouTube."
        )

        return {
            "status": "success",
            "description": description
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating description: {str(e)}"
        }

# Create the Google ADK Agent
root_agent = Agent(
    name="youtube_search_agent",
    model="gemini-2.0-flash",  # Use appropriate model from Google ADK
    description=(
        "Agent to search YouTube for videos based on user queries and provide descriptions."
    ),
    instruction=(
        "You are a helpful agent who can search YouTube for videos based on user queries "
        "and provide concise descriptions about the results."
    ),
    tools=[search_youtube_videos, generate_video_description],
)

