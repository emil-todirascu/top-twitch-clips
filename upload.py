
import json
from upload_video import upload_video


def upload(file_path):
    
    with open(file_path.replace(".mp4", ".json"), 'r', encoding="utf-8") as f:
        file_data = json.load(f)
    
    upload_video(file_path, title=file_data["title"], description=file_data["description"], category=file_data["category"], keywords=file_data["keywords"], privacy_status=file_data["privacy_status"])
