import shutil
import os
    
source_dir = 'D:/test1'
target_dir = 'D:/test2'
    
file_names = os.listdir(source_dir)
    
#for file_name in file_names:
#    shutil.move(os.path.join(source_dir, file_name), target_dir)

file_names = [f for f in os.listdir(source_dir) if '.mp4' in f.lower()]

for file_name in file_names:
    shutil.move(os.path.join(source_dir, file_name), target_dir)