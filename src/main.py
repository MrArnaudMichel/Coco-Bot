from bananabot import Bananabot
from upload_video import *
if __name__ == '__main__':
    upload("uploads/videotest.mp4", {
        "title": "#shorts",
        "description": "This is a test video. #shorts",
        "tags": ["test", "video"],
        "category": 22,
        "status": "private"
    })