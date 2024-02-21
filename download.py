import datetime
import json
import os
import requests
import datetime

GENERAL_DESCRIPTION = "\n\n\nFor all inquiries, please email: hello.toptwitchclips@gmail.com"

class TwitchAPI():

    def __init__(self):
        self.headers = None
        self.client_id = "s97o9ivny2kk0kl6j3vfss1ptjmocs"
        self.client_secret = "lglwiqd1zxt3abmg26jo8tnhtrfd78"

    def auth(self):
        print("Authenticating...")
    
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = f'client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials'

        try:
            response = requests.post('https://id.twitch.tv/oauth2/token', headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
            
        bearer = response.json()['access_token']

        self.headers = {
            'Authorization': f'Bearer {bearer}',
            'Client-Id': self.client_id,
        }
        print("Authenticated.\n")

api = TwitchAPI()

def get_top_game_clips(game_id, time):
    print("Retrieving clips...")

    first = 100

    url = f"https://api.twitch.tv/helix/clips?game_id={game_id}&started_at={time}&first={first}"

    headers = api.headers

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve clips.\n")
        return []
    print("Retrieved clips.\n")

    clips = response.json()["data"]
    return clips

def filter_english_clips(clips):
    print("Filtering English clips...")
    
    english_clips = []
    
    for clip in clips:
        if clip["language"] == "en":
            english_clips.append(clip)
    
    print("Filtered English clips.\n")
    
    return english_clips

def download_clip(clip_object, path):
    index = clip_object["thumbnail_url"].find('-preview')
    clip_url = clip_object["thumbnail_url"][:index] + '.mp4'
    r = requests.get(clip_url)

    clip_path = f'{path}{clip_object["title"].replace("/","_")}.mp4'.replace("\\", "").replace("\'", "").replace("\"", "").replace("|", "").replace("?","").lower()

    if r.headers['Content-Type'] == 'binary/octet-stream':
        if not os.path.exists(path): os.makedirs(path)
        with open(clip_path, 'wb') as f:
            f.write(r.content)
    else:
        print(f'Failed to download clip from thumb: {clip_object["thumbnail_url"]}')

    return clip_path

def add_data_clip(clip_object, path):
    data_path = f'{path}{clip_object["title"].replace("/","_")}.json'.replace("\\", "").replace("\'", "").replace("\"", "").replace("|", "").replace("?","").lower()

    hashtags = f'#{twitchID_to_game[clip_object["game_id"]]} #{clip_object["broadcaster_name"]} #twitch #gaming'
    description = f'Credit: https://www.twitch.tv/{clip_object["broadcaster_name"]} {GENERAL_DESCRIPTION} \n\n\n {hashtags}'

    keywords = f'{twitchID_to_game[clip_object["game_id"]]}, {clip_object["broadcaster_name"]}, twitch, gaming, {clip_object["title"]}'


    data = {
        "title": clip_object["title"] + " | " + clip_object["broadcaster_name"] + " | Top Twitch Clips",
        "description": description,
        "category": "20", # Gaming
        "keywords": keywords,
        "privacy_status": "public",
        "streamer": clip_object["broadcaster_name"],
        "game": twitchID_to_game[clip_object["game_id"]],
    }

    if not os.path.exists('files/clips'): os.makedirs('files/clips')
    with open(data_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def download_single(game_id, pastHours):
    api.auth()

    clipObject = filter_english_clips(get_top_game_clips(game_id, pastHours))[0]
    
    path = f"files/clips/{datetime.datetime.today().date()}/"
    
    clip_path = download_clip(clipObject, path)
    add_data_clip(clipObject, path)

    return clip_path

def download_multiple(game_id, pastHours, amount):
    api.auth()

    clips = filter_english_clips(get_top_game_clips(game_id, pastHours))[:amount]
    
    path = f"files/clips/{datetime.datetime.today().date()}/"
    
    clip_paths = []
    print("Downloading clips...")
    for clip in clips:
        clip_path = download_clip(clip, path)
        add_data_clip(clip, path)
        clip_paths.append(clip_path)
    print("Downloaded clips.\n")

    return clip_paths

twitchID_to_game = {
    "32982": "gta",
    "21779": "lol",
    "32399": "cs2",
    "513143": "tft",
    "27471": "minecraft",
    "516575": "valorant",
    "33214": "fortnite",
    "491931": "eft",
    "509658": "irl",
}
