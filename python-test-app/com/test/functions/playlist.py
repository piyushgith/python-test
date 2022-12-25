from pytube import YouTube, Playlist
import random
import time

target_dir = 'D:/YouTube'
#playlist = Playlist('https://www.youtube.com/watch?v=PN7YFKHOR9Y&list=PL7RtZMiaOk8gdRf130w4gFYyhstL-5VRh')
urlList=[]
playListDict={}

def GetPlayListUrls(youTubeLink):
    substring = "&list"
    removeString ="&index"

    if youTubeLink != None and substring in youTubeLink:
        print("PlayList URL Found!")
        link=youTubeLink.split(removeString)
        playlist = Playlist(link[0])

        for video in playlist.videos:
            print('downloading : {} with url : {}'.format(video.title, video.watch_url))
            time.sleep(random.randint(60,100))
            Download(video)
            print('Downloaded Video : {}'.format(video.title))
            #print('"{}":"{}",'.format(video.title, video.watch_url))
    else:
        print("This is single video found!")
        Download(youTubeLink)


def Download(link):
    youtubeObject = YouTube(link)
    try:
        print("Starting download....")
        youtubeObject.streams.filter(type='video', progressive=True, file_extension='mp4'). \
            order_by('resolution').desc().first().download(target_dir)
    except:
        print("An error has occurred")
    print("Download is completed successfully!!!!!!")


#Calling methods after running the file
playListLink = input("Enter the YouTube Playlist URL: ")
GetPlayListUrls(playListLink)

















