import json
import os
import datetime
import requests

import firebase_admin
from firebase_admin import credentials, firestore

# -----------------------------
# CONFIG
# -----------------------------
VIDEO_ID = "vVDp1ulBKIk"  # <--- change this anytime to track another video


def main():
    # -----------------------------
    # Load Firebase credentials
    # -----------------------------
    cred_json = os.environ["FIREBASE_CREDENTIALS"]
    cred_dict = json.loads(cred_json)

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    # -----------------------------
    # Call YouTube API
    # -----------------------------
    api_key = os.environ["YOUTUBE_API_KEY"]

    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "id": VIDEO_ID,
        "key": api_key
    }

    response = requests.get(url, params=params).json()
    item = response["items"][0]

    title = item["snippet"]["title"]
    stats = item["statistics"]

    views = int(stats.get("viewCount", 0))
    likes = int(stats.get("likeCount", 0))
    comments = int(stats.get("commentCount", 0))

    # -----------------------------
    # Save to Firestore
    # -----------------------------
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M")

    doc_ref = (
        db.collection("videos")
          .document(VIDEO_ID)
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

    print("Saved stats at:", timestamp)


if __name__ == "__main__":
    main()
