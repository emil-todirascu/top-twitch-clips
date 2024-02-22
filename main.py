import datetime
from download import download_multiple
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

    clip_path = edit_clips(download_multiple(gameID, time, count))

    print(f"Are you sure you want to upload {clip_path}? (y/n)")

    if input() == "y":
        upload(clip_path)
    else:
        print("Exiting...")

def main():
    game = input("Enter game: ")
    if game not in game_to_twitchID:
        print("Invalid game")
        return
    
    hours = int(input("Enter hours: "))
    if hours < 0:
        print("Invalid hours")
        return
    
    count = int(input("Enter count: "))
    if count < 2:
        print("Invalid count")
        return
    
    upload_video(game, hours, count)

main()