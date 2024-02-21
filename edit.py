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

    # final_clip_path = add_data(clip_paths)
    final_clip_path = "files/clips/final.mp4"
    
    final_clip = concatenate_videoclips(clips, transition=trans, method="compose")
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

edit_clips(["files/clips/2024-02-21/cg vs company.mp4", "files/clips/2024-02-21/ooc youre a bi♱ch.mp4"])