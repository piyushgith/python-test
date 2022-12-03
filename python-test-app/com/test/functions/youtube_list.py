import pytube

#where to save
SAVE_PATH = "C:/Users/Piyush/Downloads/Video/" #to_do

#link of the video to be downloaded
link="https://www.youtube.com/watch?v=3R1SWkHuFH4"


yt = pytube.YouTube(link)
stream = yt.streams.get_highest_resolution()
stream.download()