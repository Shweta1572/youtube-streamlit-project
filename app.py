import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from pymongo import MongoClient
import os

# Function to connect to MongoDB
@st.cache_resource
def connect_mongo():
    mongo_host = os.getenv('MONGO_HOST', 'localhost')
    mongo_user = os.getenv('MONGO_USERNAME', '')
    mongo_pass = os.getenv('MONGO_PASSWORD', '')
    if mongo_user and mongo_pass:
        mongo_uri = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:27017/"
    else:
        mongo_uri = f"mongodb://{mongo_host}:27017/"
    
    client = MongoClient(mongo_uri)
    db = client.youtube_data
    return db

# Function to connect to YouTube API
def get_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

# Function to get channel info
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    
    if response['items']:
        data = response['items'][0]
        channel_name = data['snippet']['title']
        subscribers = data['statistics']['subscriberCount']
        total_views = data['statistics']['viewCount']
        total_videos = data['statistics']['videoCount']
        description = data['snippet']['description']
        
        return {
            "Channel Name": channel_name,
            "Subscribers": subscribers,
            "Total Views": total_views,
            "Total Videos": total_videos,
            "Description": description
        }
    else:
        return None

# Function to get video details
def get_videos(youtube, channel_id):
    videos = []
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"  # Fetch latest videos
    )
    
    while request:
        response = request.execute()
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                published_at = item['snippet']['publishedAt']
                
                videos.append({
                    "Video ID": video_id,
                    "Title": title,
                    "Published At": published_at
                })
        request = youtube.search().list_next(request, response)
    
    return pd.DataFrame(videos)

# Streamlit App
st.title("🎥 YouTube Channel Analyzer")

api_key = st.text_input("Enter your YouTube API Key")
channel_id = st.text_input("Enter YouTube Channel ID")

# Set session state to remember if channel info is fetched
if "channel_info_fetched" not in st.session_state:
    st.session_state["channel_info_fetched"] = False

# Button to get Channel Info
if st.button("Get Channel Info"):
    if api_key and channel_id:
        youtube = get_youtube_service(api_key)
        channel_info = get_channel_info(youtube, channel_id)
        
        if channel_info:
            st.subheader(f"Channel: {channel_info['Channel Name']}")
            st.write(f"**Subscribers**: {channel_info['Subscribers']}")
            st.write(f"**Total Views**: {channel_info['Total Views']}")
            st.write(f"**Total Videos**: {channel_info['Total Videos']}")
            st.write(f"**Description**: {channel_info['Description']}")
            
            # Save to MongoDB
            db = connect_mongo()
            db.channels.insert_one(channel_info)
            st.success("Channel info saved to MongoDB!")
            
            # Mark as fetched
            st.session_state["channel_info_fetched"] = True
        else:
            st.error("Channel not found. Please check Channel ID.")

# Button to get all videos only after channel info fetched
if st.session_state["channel_info_fetched"]:
    if st.button("Get All Videos"):
        if api_key and channel_id:
            youtube = get_youtube_service(api_key)
            videos_df = get_videos(youtube, channel_id)
            st.subheader(f"Total Videos Fetched: {len(videos_df)}")
            st.dataframe(videos_df)

            # Save to MongoDB
            db = connect_mongo()
            db.videos.insert_many(videos_df.to_dict('records'))
            st.success("Videos saved to MongoDB!")

            # Also save to CSV (optional)
            videos_df.to_csv(f"{channel_id}_videos.csv", index=False)
            st.success(f"Video data also saved to `{channel_id}_videos.csv`")
