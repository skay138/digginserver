import requests

def get_youtube_info(req):

    try :
        raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={req}&key=AIzaSyAN5CLX1zBoI5sywWcZPHPPh9EIy-WkICA&part=snippet").json()
        video_data = raw_video_data['items'][0]['snippet']
    except IndexError:
        raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id=528yECWgtVg&key=AIzaSyAN5CLX1zBoI5sywWcZPHPPh9EIy-WkICA&part=snippet").json()
        video_data = raw_video_data['items'][0]['snippet']
    
    title = video_data['title']
    description = video_data['description']
    try :
        thumbnail = video_data['thumbnails']['standard']['url']
    except:
        thumbnail = video_data['thumbnails']['default']['url']
        
    data = {"title" : title,
            "thumb" : thumbnail,
            "desc" : description
    }

    return data

def get_youtube_link(req):
    if "youtube.com/watch?v=" in req:
        youtube_link = req.split('&')[0]
        youtube_link = youtube_link.split('v=')[1]
        
        return youtube_link
    
    elif "youtu.be/" in req:
        return req.split('be/')[1]
    
    else:
        return '528yECWgtVg'