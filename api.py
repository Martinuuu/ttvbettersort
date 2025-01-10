import json
import requests
import os
from dotenv import load_dotenv
import time
import math
import sys
import clips as clippy
from datetime import datetime, timezone
import database as db
load_dotenv()  # take environment variables from .env.

# Initialize appToken with regenerateToken function
appToken = 0
tokenExpire = 0

def getClips(name, dataOnly = False):
    checkToken()
    streamer_id = getStreamerID(name)

    response = requests.get(f"https://api.twitch.tv/helix/clips",
                            headers={
                                "Authorization": f"Bearer {appToken}",
                                "Client-Id": f"{os.getenv('TWITCH_APPID')}"
                            },
                            params={
                                 "broadcaster_id" : streamer_id,
                                 "started_at": getTime(),
                                 #"ended_at" : "2000-01-01T00:00:00+01:00",
                                 "first": 100,
                             })
    
    if dataOnly:
        return response.json()
    data = response.json()["data"]
    clips = []
    for clip in data:
        clips.append(clippy.Clip(clip["title"],clip["embed_url"],clip["thumbnail_url"],clip["created_at"]))
    return clips


def getStreamerID(name):
    global appToken
    chache = db.getIDCache(name)
    if chache is not None:
        return chache
    else:
        checkToken()
        response = requests.get(f"https://api.twitch.tv/helix/users?login={name}",
                                headers={
                                    "Authorization": f"Bearer {appToken}",
                                    "Client-Id": f"{os.getenv('TWITCH_APPID')}"
                                })

        try:
            db.addStreamer(name, response.json()["data"][0]["id"])
            return response.json()["data"][0]["id"]
        except:
            #print(name, file=sys.stderr)
            print("Error while getting streamer id" + json.dumps(response.json()), file=sys.stderr)
            return json.dumps(response.json())


def regenerateToken():
    global appToken
    global tokenExpire
    
    response = requests.post("https://id.twitch.tv/oauth2/token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             params={
                                 "client_id": os.getenv("TWITCH_APPID"),
                                 "client_secret": os.getenv("TWITCH_SECRET"),
                                 "grant_type": "client_credentials"
                             })
    response_json = response.json()
    appToken = response_json["access_token"]
    tokenExpire = response_json["expires_in"] + time.time()
    tokenExpire = math.floor(tokenExpire)

def checkToken():
    if tokenExpire < math.floor(time.time()):
        regenerateToken()

regenerateToken()

def getTime():
    # Get current time in UTC
    current_time_utc = datetime.now(timezone.utc)

    # Convert timezone to string
    timezone_str = current_time_utc.astimezone().isoformat()[-6:]

    # Format current time in RFC3339 format with timezone
    rfc3339_time = current_time_utc.replace(tzinfo=None).isoformat() + timezone_str

    return rfc3339_time


