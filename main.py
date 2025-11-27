import json
import os
import datetime
import pytz
import requests

import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# CONFIG
# -----------------------------
VIDEO_IDS = [
        "vVDp1ulBKIk",
        "l2vB4qovRoE"
    ]

def main():
    # -----------------------------
    # Load Firebase credentials
    # -----------------------------
    cred_json = os.environ["FIREBASE_CREDENTIALS"]
    cred_dict = json.loads(cred_json)

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    api_key = os.environ["YOUTUBE_API_KEY"]

    # -----------------------------
    # IST timestamp
    # -----------------------------
    ist = pytz.timezone("Asia/Kolkata")
    now_ist = datetime.datetime.now(ist)
    timestamp = now_ist.strftime("%Y-%m-%d %I:%M %p")

    # -----------------------------
    # Loop through each video
    # -----------------------------
    for video_id in VIDEO_IDS:

        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics",
            "id": video_id,
            "key": api_key
        }

        response = requests.get(url, params=params).json()
        item = response["items"][0]

        title = item["snippet"]["title"]
        stats = item["statistics"]

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))

        # Firestore path:
        # videos/{videoId}/stats/{timestamp}
        doc_ref = (
            db.collection("videos")
              .document(video_id)
              .collection("stats")
              .document(timestamp)
        )

        doc_ref.set({
            "title": title,
            "views": views,
            "likes": likes,
            "comments": comments,
            "timestamp": timestamp
        })

        print(f"Saved stats for {video_id} at: {timestamp}")



if __name__ == "__main__":
    main()
