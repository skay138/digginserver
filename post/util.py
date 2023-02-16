import requests

key = 'AIzaSyAfOGRGxL7qpWWq9qTSGiLi2XJ5OfxITkI'

def get_youtube_link(req):
    if "youtube.com/watch?v=" in req:
        youtube_link = req.split('&')[0]
        youtube_link = youtube_link.split('v=')[1]

        try :
            raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={youtube_link}&key={key}&part=snippet").json()
            video_data = raw_video_data['items'][0]['snippet']
            title = video_data['title']
            try :
                thumbnail = video_data['thumbnails']['standard']['url']
            except:
                thumbnail = video_data['thumbnails']['default']['url']
            return youtube_link, title, thumbnail
        except IndexError:
            return None, None, None
    
    elif "youtu.be/" in req:
        youtube_link = req.split('be/')[1]
        try :
            raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={youtube_link}&key={key}&part=snippet").json()
            video_data = raw_video_data['items'][0]['snippet']
            title = video_data['title']
            try :
                thumbnail = video_data['thumbnails']['standard']['url']
            except:
                thumbnail = video_data['thumbnails']['default']['url']
            return youtube_link, title, thumbnail
        except IndexError:
            return None, None,  None
    
    else:
        try : 
            raw_video_data = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={req}&key={key}&part=snippet").json()
            video_data = raw_video_data['items'][0]['snippet']
            title = video_data['title']
            try :
                thumbnail = video_data['thumbnails']['standard']['url']
            except:
                thumbnail = video_data['thumbnails']['default']['url']
            return youtube_link, title, thumbnail
        except IndexError:
            return None, None, None