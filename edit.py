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

    clip_times = get_clip_times(clips, trans.duration)
    final_clip_path = add_data(clip_paths, clip_times)
    
    final_clip = concatenate_videoclips(clips, transition=trans)
    final_clip.write_videofile(final_clip_path, preset="ultrafast")

    for clip in clips:
        clip.close()
    
    final_clip.close()
    trans.close()

    print("Edited clips.")
    return final_clip_path

def get_clip_times(clips, transition_time):
    times = [0]
    output = ["00:00"]
    for i in range(len(clips)):
        time = clips[i].duration + transition_time + times[i]
        times.append(int(time))
        output.append(f"{int(time//60):02d}:{int(time%60):02d}")
    
    return output[:-1]

    
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

def add_data(clip_paths, clip_times):
    with open(clip_paths[0].replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
        file_data = json.load(f)
    game = file_data["game"]
    streamers_list = []
    keywords_list = []
    twitch_credits = "Credits:\n"
    chapters = "Chapters:\n"
    for i, clip_path in enumerate(clip_paths):
        with open(clip_path.replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
            file_data = json.load(f)
        streamers_list.append(file_data["streamer"])
        keywords_list.extend(file_data["keywords"].split(", "))

        if file_data["streamer"] not in twitch_credits:
            twitch_credits += f"https://www.twitch.tv/{file_data['streamer']}\n"
        chapters += f"{clip_times[i]} {file_data["title"]}\n"

    streamers = ", ".join(set(streamers_list))
    keywords = "#" + ", #".join(set(keywords_list))

    description = f"{chapters}\n\n\n{twitch_credits}\n\n\n{keywords}"
    streamer_names = ", ".join(sorted(list(set(streamers_list)),key=lambda x: len(x))[:min(3, len(streamers_list))])
    title = f"🚨Top {game.upper()} Clips🚨{streamer_names} and more...🚨{datetime.datetime.today().date()}🚨"
        
    data_path = f"files/clips/{datetime.datetime.today().date()}/result/Top {game.upper()} Clips.json"

    data = {
        "title": title,
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

# edit_clips(["files/clips/2024-02-21/ hydra and ott complete a usb trade.mp4", "files/clips/2024-02-21/2 to the head.mp4", "files/clips/2024-02-21/jump scare and a death .mp4", "files/clips/2024-02-21/jps pickup gets denied.mp4", "files/clips/2024-02-21/cg vs company.mp4"])