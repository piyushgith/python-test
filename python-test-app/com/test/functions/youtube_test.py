from pytube import YouTube
import shutil
import os
    
# it can be Source Code path    
source_dir = 'C:/Users/Piyush/Downloads/Video/Script'
target_dir = 'C:/Users/Piyush/Downloads/Video/'


def MoveFiles():
    print("Moving file to destination path..............")

    images = [f for f in os.listdir(source_dir) if '.mp4' in f.lower()]

    for image in images:
        shutil.move(os.path.join(source_dir, image), target_dir)
    
    print("File has been transferred successfully!!!!!!!")    


def Download(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")


#Calling methods after running the file
link = input("Enter the YouTube video URL: ")
Download(link)
MoveFiles()