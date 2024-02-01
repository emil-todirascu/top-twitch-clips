import datetime
from download import download
from upload import upload
import sys

game_to_twitchID = {
    "gta": "32982",
    "lol": "21779",
    "cs2": "32399",
    "tft": "513143",
    "minecraft": "27471",
    "valorant": "516575",
    "fortnite": "33214",
    "eft": "491931",
    "irl": "509658",
}

def upload_new_video(game, pastHours):

    gameID = game_to_twitchID[game]
    time = (datetime.datetime.today() - datetime.timedelta(hours=pastHours)).isoformat() + "Z"

    clip_path = download(gameID, time)

    upload(clip_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <game> <pastHours>")
        sys.exit(1)

    game = sys.argv[1]
    pastHours = int(sys.argv[2])

    upload_new_video(game, pastHours)

# gta 12