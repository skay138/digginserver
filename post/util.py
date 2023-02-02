import requests

def get_youtube_info(req):
    try :
        video_id = req.split('v=')[1]
    except :
        return 

    raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key=AIzaSyAN5CLX1zBoI5sywWcZPHPPh9EIy-WkICA&part=snippet").json()
    video_data = raw_video_data['items'][0]['snippet']
    
    title = video_data['title']
    description = video_data['description']
    thumbnail = video_data['thumbnails']['standard']['url']
    data = {"title" : title,
            "thumb" : thumbnail,
            "desc" : description
    }

    return data

def youtube_link_varify(req):
    if "youtube.com/watch?v=" in req:
        return True
    elif "youtu.be/" in req:
        return True
    else:
        return False