import datetime
import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from moviepy.audio import *
from moviepy.video import *

import json
from PIL import Image, ImageDraw, ImageFont

def edit_clips(clip_paths):
    print("Editing clips...")
    
    clips = []
    for clip_path in clip_paths:
        overlay = make_overlay(clip_path)

        clip = VideoFileClip(clip_path)
        clip = add_overlay(clip, overlay)
        clips.append(clip)

    trans = VideoFileClip("files/transitions/white noise.mp4").subclip(0, 0.5)
    trans = trans.volumex(0.1)

    final_clip_path = add_data(clip_paths)
    
    final_clip = concatenate_videoclips(clips, transition=trans)
    final_clip.write_videofile(final_clip_path, preset="ultrafast")

    for clip in clips:
        clip.close()
    
    final_clip.close()
    trans.close()

    print("Edited clips.")
    return final_clip_path

    
def make_overlay(clip_path):
    with open(clip_path.replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
        file_data = json.load(f)
    
    streamer_name = file_data["streamer"]

    img = Image.new('RGBA', (1920, 1080), color = (255,255,255,0))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("files/fonts/Inter/Inter-VariableFont_slnt,wght.ttf", 50)
    twitch_logo = Image.open("files/imgs/TwitchGlitchPurple.png").resize((100, 100))
    img.paste(twitch_logo, (100, 900))

    draw.text((225, 925), streamer_name, font=fnt, stroke_width=3, stroke_fill=(0,0,0), fill=(255,255,255))

    path = clip_path.replace(".mp4", ".png")
    img.save(path)

    return path


def add_overlay(clip, overlay):
    img_clip = ImageClip(overlay).set_duration(5)
    edited_video = CompositeVideoClip([clip, img_clip])
    return edited_video

def add_data(clip_paths):
    with open(clip_paths[0].replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
        file_data = json.load(f)
    game = file_data["game"]
    streamers_list = []
    keywords_list = []
    twitch_credits = "Credits:\n"
    for clip_path in clip_paths:
        with open(clip_path.replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
            file_data = json.load(f)
        streamers_list.append(file_data["streamer"])
        keywords_list.extend(file_data["keywords"].split(", "))
        twitch_credits += f"https://www.twitch.tv/{file_data['streamer']}\n"

    streamers = ", ".join(set(streamers_list))
    keywords = ", ".join(set(keywords_list))
    description = f"Top {game.upper()} Clips {datetime.datetime.today().date()}\n\n\n{twitch_credits}\n\n\n{keywords}"

        
    data_path = f"files/clips/{datetime.datetime.today().date()}/result/Top {game.upper()} Clips.json"

    data = {
        "title": f"Top {game.upper()} Clips {datetime.datetime.today().date()}",
        "description": description,
        "category": "20", # Gaming
        "keywords": keywords,
        "privacy_status": "public",
        "streamer": streamers,
        "game": game
    }

    path = f"files/clips/{datetime.datetime.today().date()}/result/"

    if not os.path.exists(path): os.makedirs(path)
    with open(data_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return data_path[:-5] + ".mp4"


# edit_clips(["files/clips/2024-02-21/jps pickup gets denied.mp4", "files/clips/2024-02-21/psa.mp4"])