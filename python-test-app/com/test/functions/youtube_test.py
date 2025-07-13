from pytube import YouTube
import shutil
import os
    
# it can be Source Code path    
source_dir = 'C:/Users/Piyush/Downloads/Video/Script'
target_dir = 'C:/Users/Piyush/Downloads/Video/'


#Not needed anymore for downlaod task
#It is super good method to keep
def MoveFiles():
    print("Moving file to destination path..............")

    fileList = [f for f in os.listdir(source_dir) if '.mp4' in f.lower()]

    for video in fileList:
        shutil.move(os.path.join(source_dir, video), target_dir)
    
    print("File has been transferred successfully!!!!!!!")    


def Download(link):
    youtubeObject = YouTube(link)
    try:
        youtubeObject.streams.filter(type='video', progressive=True, file_extension='mp4'). \
            order_by('resolution').desc().first().download(target_dir)
    except:
        print("An error has occurred")
    print("Download is completed successfully")


#Calling methods after running the file
link = input("Enter the YouTube video URL: ")
Download(link)

#Not Needed anymore
#MoveFiles()