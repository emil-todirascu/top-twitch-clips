import datetime
from download import download_single, download_multiple
from upload import upload
from edit import edit_clips

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

def upload_video(game, pastHours, count=1):

    gameID = game_to_twitchID[game]
    time = (datetime.datetime.today() - datetime.timedelta(hours=pastHours)).isoformat() + "Z"

    clip_path = None
    if count > 1:
        clip_paths = download_multiple(gameID, time, count)
        clip_path = edit_clips(clip_paths)
    else:
        clip_path = download_single(gameID, time)

    print("Are you sure you want to upload this video? (y/n)")

    if input() == "y":
        # upload(clip_path)
        print("up")
    else:
        print("Exiting...")

# if __name__ == "__main__":
#     if len(sys.argv) not in [3]:
#         print("Usage: python main.py <game> <pastHours>")
#         sys.exit(1)

#     game = sys.argv[1]
#     pastHours = int(sys.argv[2])

#     upload_new_video(game, pastHours)

# gta 12

game = input("Enter game: ")
hours = int(input("Enter hours: "))
count = int(input("Enter count: "))

upload_video(game, hours, count)
